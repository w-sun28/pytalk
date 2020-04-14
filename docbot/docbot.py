from doctalk.api import *
import json

def api_test() :
  '''
  to be used on the server side to expose this as a web or Alexa service
  '''
  params=new_params(from_json='{"top_sum":3,"top_keys":6,"top_answers":3}')
  jsonish='''["
    The cat sits on the mat. 
    The mat sits on the floor.
    The floor sits on planet Earth.
    The Earth does not sit.
    The Earth just wanders.
  "]
  '''
  from_json=jsonish.replace('\n',' ')

  talker=new_talker(from_json=from_json,params=params)
  wss=json.loads(get_summary(talker))
  ks=json.loads(get_keywords(talker))

  print('SUMMARY')
  for ws in wss:
    print(" ".join(ws))

  print('KEYPHRASES')
  for k in ks:
    print(k)
  
  print('QA')
  quest='Where is the cat?'
  print(answer_question(talker,quest))
    
class Bot :
  def __init__(self,textfile) :
    params=new_params(from_json=
      '{"top_sum":4,"top_keys":7,"top_answers":3,"prioritize_compounds":10}')
    self.talker=new_talker(from_file=textfile,params=params)
    wss=json.loads(self.talker.summary_sentences())
    ks=json.loads(self.talker.keyphrases())
    sentences=[" ".join(ws) for ws in wss]    
    self.summary=" ".join(sentences)
    self.keyphrases=", ".join(ks)
    
  def ask(self,question) :
    q=json.dumps(question)
    
    a= answer_question(self.talker,q)
    wss= json.loads(a)
    sentences=[" ".join(ws) for ws in wss]    
    answer=" ".join(sentences)
    return answer
    
def bot_test() :
    bot = Bot('examples/const.txt')
    print(bot.summary)
    print(bot.keyphrases)
    r=bot.ask('How can the President be removed from office?')
    wss=json.loads(r)
    for ws in wss :
      print(' '.join(ws))
      print('')
