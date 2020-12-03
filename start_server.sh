#java -mx8g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

java -mx12g -cp "../stanford-corenlp-full-2020-04-20/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,depparse,natlog,openie \
-status_port 9000 -port 9000 -timeout 120000 -quiet
