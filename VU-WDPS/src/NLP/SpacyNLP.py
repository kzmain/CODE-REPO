from array import ArrayType

import spacy
import validators

# from abc import ABC

from pyspark.sql.functions import udf, col, size, explode
from pyspark.sql.types import StringType, ArrayType
from pyspark.sql import DataFrame

from System import Columns as Col
from Tools.Writer import Writer


class SpacyNLP:
    nlp = spacy.load("en_core_web_sm")

    INTERESTED_LABELS = [
        'ORG',
        'PERSON',
        'GPE',
        'PRODUCT'
    ]

    TOKEN_POS = "pos"
    TOKEN_TAG = "tag"
    TOKEN_DEP = "dep"

    # Calculate special characters (non-alphabet) to alphabet ratio
    @staticmethod
    def __special_ratio(text: str):
        m = 0
        n = len(text)
        has_alpha = False
        for i in range(n):
            c = text[i]
            if c == ' ' or c == '.': continue
            if c.isnumeric(): continue
            if c.isalpha():
                has_alpha = True
                continue

            m += 1
        return has_alpha, m / n  # Return if text has alphabetical text and ratio as tuple

    @staticmethod
    def __get_token_dict(nlp):

        token_dict = {}
        for token in nlp:
            token_dict[str(token)] = {SpacyNLP.TOKEN_POS: token.pos_,
                                      SpacyNLP.TOKEN_TAG: token.tag_,
                                      SpacyNLP.TOKEN_DEP: token.dep_}
        return token_dict

    @staticmethod
    def __confirm_filter(ent):
        ent = str(ent)
        has_alpha, ratio = SpacyNLP.__special_ratio(ent)
        if has_alpha \
                and (ent[0].isalpha() or ent[0].isnumeric()) \
                and not validators.domain(ent.lower()) \
                and "  " not in ent \
                and ratio < 0.1:
            return True
        else:
            return False

    @staticmethod
    def __pack_entity(ent, token_dict, sentence=None):
        ent = str(ent)
        pos_list = []
        tag_list = []
        dep_list = []
        for token in ent.split(" "):
            try:
                pos_list.append(token_dict[token][SpacyNLP.TOKEN_POS])
                tag_list.append(token_dict[token][SpacyNLP.TOKEN_TAG])
                dep_list.append(token_dict[token][SpacyNLP.TOKEN_DEP])
            except KeyError:
                pass
        if sentence is not None:
            return [[sentence], pos_list, tag_list, dep_list]
        else:
            return [ent, pos_list, tag_list, dep_list]

    @staticmethod
    def __generate_entities(key, payload):
        print("SpacyNLP: %s" % key)
        entries = []
        ent_set = set()
        nlp = SpacyNLP.nlp(payload)
        token_dict = SpacyNLP.__get_token_dict(nlp)

        for ent in nlp.ents:
            if ent.label_ in SpacyNLP.INTERESTED_LABELS and SpacyNLP.__confirm_filter(ent) and str(ent) not in ent_set:
                entries.append(SpacyNLP.__pack_entity(ent, token_dict))
                ent_set.add(str(ent))
        return entries

    @staticmethod
    def process_linker_trident(target_entity, sentences):
        entries = []
        for sentence in sentences:
            nlp = SpacyNLP.nlp(sentence)
            token_dict = SpacyNLP.__get_token_dict(nlp)
            entries.append(SpacyNLP.__pack_entity(target_entity, token_dict, sentence))
        return entries

    @staticmethod
    def extract(text_df: DataFrame, out_file=""):
        sum_cols = udf(SpacyNLP.__generate_entities, ArrayType(ArrayType(StringType())))
        text_df = text_df.withColumn(Col.NLP_NLP, sum_cols(Col.WARC_ID, Col.WARC_CONTENT))
        text_df = text_df.withColumn(Col.NLP_SIZE, size(col(Col.NLP_NLP)))
        text_df = text_df.filter(col(Col.NLP_SIZE) >= 1)
        text_df = text_df.withColumn(Col.NLP_NLP, explode(Col.NLP_NLP))
        text_df = text_df.withColumn(Col.NLP_MENTION, col(Col.NLP_NLP).getItem(0)) \
            .withColumn(Col.NLP_POS, col(Col.NLP_NLP).getItem(1)) \
            .withColumn(Col.NLP_TAG, col(Col.NLP_NLP).getItem(2)) \
            .withColumn(Col.NLP_DEP, col(Col.NLP_NLP).getItem(3))
        text_df = text_df.drop(col(Col.NLP_NLP))
        text_df = text_df.drop(col(Col.NLP_SIZE))

        # NOTE: Readded this to check F score without new Linker implementation (otherwise no duplicate filtering occured)
        # text_df = text_df.dropDuplicates([Col.WARC_ID, Col.NLP_MENTION])

        if out_file != "":
            Writer.csv_writer(out_file, text_df)
        return text_df
