import http.client
import json
import os
import time
import urllib.parse
import uuid
from itertools import chain

import pandas as pd
import pyspark
import requests
import spacy
import textdistance
from pyspark.sql.functions import udf, lit, min, col
from pyspark.sql.types import StringType, ArrayType, BooleanType

from NLP.SpacyNLP import SpacyNLP
from System import Columns as Cols, Location
from Tools import Reader, Renamer
from Tools.Writer import Writer


class Linker:
    THRESHOLD_SCORE = 3
    THRESHOLD_SCORE_H = 0.65

    freebase_columns = [Cols.LINKER_ENTITY, Cols.LINKER_SCORE,
                        Cols.LINKER_H_SCORE, Cols.LINKER_LABEL, Cols.LINKER_FB_ID]
    trident_columns = [Cols.LINKER_FB_ID, Cols.LINKER_TRI]

    FB_TEMP = "/freebase_temp_"
    FB = "/FB_"
    TRI = "/TRI_"

    NO_FREEBASE_LIST = []

    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def __tokenize(a):
        for word in Linker.nlp(a):
            yield word.text

    @staticmethod
    def __sorensen_dice(a, b):
        return textdistance.sorensen_dice(Linker.__tokenize(a), Linker.__tokenize(b))

    @staticmethod
    def process_spacy(target_entity, sentence_list):
        return SpacyNLP.process_linker_trident(target_entity, sentence_list)

    @staticmethod
    def have_trident(sen_list):
        if len(sen_list) > 0:
            return True
        else:
            return False

    @staticmethod
    def trident_flag(entity_has_trident, word_has_trident):
        if word_has_trident is None:
            return True
        elif entity_has_trident == True and word_has_trident == True:
            return True
        else:
            return False

    @staticmethod
    def sparql(trident_domain, in_id):
        fb_id = in_id.replace("/m/", "m.")
        print("[SYSTEM]: Retrieve %s from trident" % (fb_id))

        query = "select distinct ?abstract where {  \
          ?s <http://www.w3.org/2002/07/owl#sameAs> <http://rdf.freebase.com/ns/%s> .  \
          ?s <http://www.w3.org/2002/07/owl#sameAs> ?o . \
          ?o <http://dbpedia.org/ontology/abstract> ?abstract . \
        }" % fb_id

        conn = http.client.HTTPConnection(trident_domain.split(':')[0], int(trident_domain.split(':')[1]))
        headers = {'User-Agent': 'python-requests/2.21.0',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept': '*/*',
                   'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        params = urllib.parse.urlencode({'print': True, 'query': query})
        conn.request("POST", "/sparql", params, headers=headers)
        while True:
            try:
                response = conn.getresponse()
                break
            except (ConnectionResetError, http.client.ResponseNotReady):
                time.sleep(0.01)
        abstract = ""
        if response:
            try:
                results = json.loads(response.read())
                for result in results["results"]["bindings"]:
                    if "\"@en\"" in result["abstract"]["value"]:
                        abstract += result["abstract"]["value"]
                        # abstract = result["abstract"]["value"].encode().decode('unicode_escape')
                        # doc = Linker.nlp(abstract)
                        # sents = [sent.string.strip() for sent in doc.sents]
                        # sents = [sent for sent in sents if fb_entity in sent]
                        # sentences += sents

            except Exception as e:
                print(e)
                raise e
        df = pd.DataFrame([[in_id, abstract]], columns=Linker.trident_columns)
        df.to_parquet(Location.FREEBASE_PATH_PAR + Linker.TRI + str(uuid.uuid4()) + ".parquet")
        return abstract

    @staticmethod
    def query_freebase(elastic_domain, query):
        conn = http.client.HTTPConnection(elastic_domain.split(':')[0], int(elastic_domain.split(':')[1]))
        conn.request('GET', '/freebase/label/_search?%s' % urllib.parse.urlencode({'q': query, 'size': 1000}))
        response = conn.getresponse()

        results = []
        if response.status == 200:
            response = json.loads(response.read())
            for hit in response.get('hits', {}).get('hits', []):
                freebase_label = hit.get('_source', {}).get('label')
                freebase_id = hit.get('_source', {}).get('resource')
                freebase_score = hit.get('_score', 0)

                if freebase_score < Linker.THRESHOLD_SCORE: continue
                dice_score = Linker.__sorensen_dice(query, freebase_label)
                # if dice_score > Linker.THRESHOLD_SCORE_H: continue
                # trident_abstract = Linker.sparql(trident_domain, freebase_label, freebase_id.replace("/m/", "m."))
                results.append([query, freebase_score, dice_score, freebase_label, freebase_id])
            if len(results) > 0:
                results.sort(key=lambda x: (x[2], -x[1]))
                df = pd.DataFrame(results, columns=Linker.freebase_columns)
                if not os.path.exists(Location.FREEBASE_PATH_PAR):
                    os.mkdir(Location.FREEBASE_PATH_PAR)
                df.to_parquet(Location.FREEBASE_PATH_PAR + Linker.FB_TEMP + str(uuid.uuid4()) + ".parquet")
                # results = list(map(lambda x: x[4], results[0:min(len(results), Linker.SELECT_COUNT)]))
            else:
                if query not in Linker.NO_FREEBASE_LIST:
                    Writer.write_list(Location.FREEBASE_PATH_EMP_TXT, [query], "a+")
        elif response.status == 400:
            if query not in Linker.NO_FREEBASE_LIST:
                Writer.write_list(Location.FREEBASE_PATH_EMP_TXT, [query], "a+")
        return results

    @staticmethod
    def link(es_domain, tri_domain, spark, nlp_df, out_file=""):

        # Get distinction mentions list from nlp
        mention_list = nlp_df.select(Cols.NLP_MENTION).distinct().toPandas()[Cols.NLP_MENTION]
        mention_list = list(mention_list)
        # mention_list = list(set(Reader.read_txt_to_list("listfile.txt")))

        # Get distinction entities list from stored freebase related info
        try:
            os.makedirs(Location.FREEBASE_PATH_PAR, exist_ok=True)
            freebase_df = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.FB + "*.parquet")
            freebase_list = freebase_df.select(Cols.LINKER_ENTITY).distinct().toPandas()[Cols.LINKER_ENTITY]
            freebase_list = list(set(freebase_list))
        except pyspark.sql.utils.AnalysisException:
            freebase_list = []
        # Get mentions those does not have entities in freebase
        no_entity_list = Reader.read_txt_to_list(Location.FREEBASE_PATH_EMP_TXT)
        Linker.NO_FREEBASE_LIST = no_entity_list
        # Get target list
        target_list = [item for item in mention_list if item not in freebase_list]
        target_list = [item for item in target_list if item not in no_entity_list]

        print("[System]: %s distinct mentions from user." % len(mention_list))
        print("[System]: %s distinct entities from stored parquet." % (len(freebase_list) + len(no_entity_list)))
        print("[System]: %s distinct not processed entities from user." % len(target_list))
        # Get things from elastic search

        # Get temp cache not processed in trident list
        try:
            df1 = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.FB + "*.parquet")
            ser_1 = df1.select(Cols.LINKER_ENTITY).distinct().toPandas()[Cols.LINKER_ENTITY]
        except pyspark.sql.utils.AnalysisException:
            ser_1 = pd.Series([])
        try:
            df2 = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.FB_TEMP + "*.parquet")
            ser_2 = df2.select(Cols.LINKER_ENTITY).distinct().toPandas()[Cols.LINKER_ENTITY]
        except pyspark.sql.utils.AnalysisException:
            ser_2 = pd.Series([])

        tp_list = list(set(chain(ser_1, ser_2)))
        fb_list = [item for item in target_list if item not in tp_list]
        if len(fb_list) > 0:
            # Start to get things from elastic search
            es_df = spark.createDataFrame(fb_list, "string").toDF(Cols.NLP_MENTION)
            get_es = udf(Linker.query_freebase, ArrayType(StringType()))
            es_df = es_df.withColumn(Cols.LINKER_ENTITY, get_es(lit(es_domain), Cols.NLP_MENTION))
            es_df.collect()

        # Get things from trident
        try:
            df1 = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.TRI + "*.parquet")
            list_1 = list(df1.select(Cols.LINKER_FB_ID).toPandas()[Cols.LINKER_FB_ID])
        except pyspark.sql.utils.AnalysisException:
            list_1 = []
        try:
            fb_df = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.FB_TEMP + "*.parquet")
            list_2 = list(fb_df.select(Cols.LINKER_FB_ID).distinct().toPandas()[Cols.LINKER_FB_ID])
            tri_list = [item for item in list_2 if item not in list_1]

            tri_df = spark.createDataFrame(tri_list, "string").toDF(Cols.LINKER_FB_ID)
            get_tri = udf(Linker.sparql, StringType())
            tri_df = tri_df.withColumn(Cols.LINKER_TRI, get_tri(lit(tri_domain), Cols.LINKER_FB_ID))
            # fb_df = fb_df.join(fb_id_df, Cols.LINKER_FB_ID, how='left_outer')
            tri_df.collect()
            Renamer.rename_file_at_location(Location.FREEBASE_PATH_PAR, Linker.FB_TEMP, Linker.FB, "*.parquet")
            # print()
            # fb_df = fb_df.withColumn(Cols.LINKER_TRI, get_tri(lit(tri_domain), Cols.LINKER_LABEL, Cols.LINKER_FB_ID))
            # get_is_emtpy = udf(Linker.have_trident, BooleanType())
            # has_df = fb_df.withColumn(Cols.LINKER_MENTION_HAS_TRI, get_is_emtpy(Cols.LINKER_TRI))
            # entity_has_df = has_df.select([col(Cols.LINKER_FB_ID), col(Cols.LINKER_MENTION_HAS_TRI)])
            # fb_df = fb_df.join(entity_has_df, Cols.LINKER_FB_ID, how='left_outer')
            #
            # mention_has_df = has_df.filter(col(Cols.LINKER_MENTION_HAS_TRI)) \
            #     .dropDuplicates([Cols.LINKER_ENTITY]) \
            #     .select([col(Cols.LINKER_ENTITY), col(Cols.LINKER_MENTION_HAS_TRI).alias(Cols.LINKER_HAS_TRI)])
            # fb_df = fb_df.join(mention_has_df, Cols.LINKER_ENTITY, how='left_outer')
            #
            # get_spacy = udf(Linker.process_spacy, ArrayType(ArrayType(StringType())))
            # spacy_df = fb_df.withColumn(Cols.LINKER_TRI, get_spacy(Cols.LINKER_LABEL, Cols.LINKER_TRI))
            #
            # spacy_df.toPandas().to_parquet(Location.FREEBASE_PATH_PAR + "/spacy_" + str(uuid.uuid4()) + ".parquet")
        except pyspark.sql.utils.AnalysisException:
            pass

        fb_df = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.FB + "*.parquet")
        tri_df = spark.read.parquet(Location.FREEBASE_PATH_PAR + Linker.TRI + "*.parquet")
        fb_df = fb_df.join(tri_df, Cols.LINKER_FB_ID, how="full")
        nlp_df = nlp_df.join(fb_df, nlp_df.mention == fb_df.entites, how="full")

        ##+--------------------+--------------------+--------------------+-----------------+--------------+----------+----------------+--------+---------+------------------+---------------+----------+
        # |                 key|                host|             payload|           labels|           pos|       tag|             dep| entites|    score|      hamming_core|          label|     fb_id|
        # +--------------------+--------------------+--------------------+-----------------+--------------+----------+----------------+--------+---------+------------------+---------------+----------+
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac| 7.022306|               0.0|       FLIP4MAC| /m/0bf90p|
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac|6.8787365|               0.0|       flip4Mac| /m/0bf90p|
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac|6.8787365|               0.0|       Flip4mac| /m/0bf90p|
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac|6.7670817|               0.0|       Flip4mac| /m/0bf90p|
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac|6.8787365|0.6666666666666666|   Flip4Mac WMV| /m/0bf90p|
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac|6.7670817|0.6666666666666666|   Flip4Mac WMV| /m/0bf90p|
        # |clueweb12-0000tw-...|centralalbertatv.net|MAC users may nee...|         Flip4Mac|       [PROPN]|     [NNP]|          [oprd]|Flip4Mac| 7.022306|               1.0|       Flip4Mac| /m/0bf90p|
        # Filter by word cosine
        nlp_df = nlp_df.filter(nlp_df.entites.isNotNull())
        score_df = nlp_df.groupBy(col(Cols.NLP_MENTION).alias("n_mention")) \
            .agg(min(Cols.LINKER_H_SCORE).alias("h_max"))
        nlp_df = nlp_df.join(score_df, (nlp_df.mention == score_df.n_mention), how='full')
        nlp_df = nlp_df.withColumn("h_checker", col("hamming_core") == col("h_max"))
        nlp_df = nlp_df.filter(col("h_checker"))
        # Filter by if have trident
        entity_have_tri = udf(Linker.have_trident, BooleanType())
        nlp_df = nlp_df.withColumn(Cols.LINKER_ENTITY_HAS_TRI, entity_have_tri(Cols.LINKER_TRI))

        word_has_df = nlp_df.filter(col(Cols.LINKER_ENTITY_HAS_TRI)) \
            .dropDuplicates([Cols.LINKER_ENTITY]) \
            .select([col(Cols.LINKER_ENTITY), col(Cols.LINKER_ENTITY_HAS_TRI).alias(Cols.LINKER_WORD_HAS_TRI)])
        nlp_df = nlp_df.join(word_has_df, Cols.LINKER_ENTITY, how='left_outer')
        sign_flag = udf(Linker.trident_flag, BooleanType())
        nlp_df = nlp_df.withColumn(Cols.LINKER_TRI_FILTER, sign_flag(Cols.LINKER_ENTITY_HAS_TRI, Cols.LINKER_WORD_HAS_TRI))
        nlp_df = nlp_df.filter(col(Cols.LINKER_TRI_FILTER))

        # print()

        score_df = nlp_df.groupBy(col(Cols.NLP_MENTION).alias("x_mention")) \
            .agg(min(Cols.LINKER_SCORE).alias("s_max"))
        nlp_df = nlp_df.join(score_df, (nlp_df.mention == score_df.x_mention), how='full')
        nlp_df = nlp_df.withColumn("s_checker", col("score") == col("s_max"))
        nlp_df = nlp_df.filter(col("s_checker"))
        nlp_df.show(10000)
        nlp_df = nlp_df.select([col(Cols.WARC_ID),
                                col(Cols.NLP_MENTION),
                                col(Cols.LINKER_FB_ID).alias(Cols.FREEBASE_ID)])
        nlp_df = nlp_df.dropDuplicates([Cols.WARC_ID, Cols.NLP_MENTION])

        return nlp_df

# Linker.sparql("localhost:9090", "Amsterdam", "m.0k3p")
# Linker.query("localhost:9200","Amsterdam")
