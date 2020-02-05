# How to use Spacy

Run:
`python -m spacy download en_core_web_sm`

# How to use Stanford:

Run:
`java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation'" -port 9000 -timeout 30000`

Requirements: 
* https://stanfordnlp.github.io/CoreNLP/download.html
* Java 1.8