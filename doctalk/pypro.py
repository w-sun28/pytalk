from natlog.natlog import natlog,Int
from natlog.db import db

from .params import *
from .talk import Talker


class NatTalker(Talker) :
  def __init__(self,from_file=None,from_text=None,
               natscript=None,
               sk=sum_count,wk=key_count,show=show_pics):
    super().__init__(from_file=from_file,from_text=from_text,
        sk=sk,wk=wk,show=show)
    self.engine=natlog(text=natscript)
    self.engine.db=self.to_nat_db()

  def to_nat_db(self):
    nd=db()
    for svo, occs in self.to_svos().items():
      s, v, o = svo
      for id in sorted(occs) :
        c=(s,v,o,id) # should be Int
        #ppp(c)
        #assert isinstance(id,int)
        nd.add_db_clause(c)
    return nd

  def natrun(self,natgoal):
    for answer in distinct(self.engine.solve(natgoal)):
      print('ANSWER:', answer)
      pass

def distinct(g) :
  seen=set()
  for x in g :
    if not x in seen :
      seen.add(x)
      yield x
      
def nrun() :
  natscript = '''

  tc_search A Rel B Res : tc A Rel B (s (s 0)) _ Res.
  
  tc A Rel C (s N1) N1 Res : ~ A Rel B Id, tc1 B Rel C N1 N2 Id Res.

  tc1 B _Rel B N N Id Id.
  tc1 B Rel C N1 N2 _Id Res : tc B Rel C N1 N2 Res.

  similar A B Id:
    ~ A R B Id,
    ~ T R A Id1,
    ~ T R B Id1.
  '''

  #T=Talker(from_file='examples/geo.txt')
  N=NatTalker(from_file='examples/geo.txt',
              natscript=natscript,
              )
  natgoal1 = 'similar deposit B Id?'
  natgoal2 = 'tc_search permian Rel B Where ?'
  print('GOAL:',natgoal1)
  N.natrun(natgoal1)
  print('')
  print('GOAL:',natgoal2)
  N.natrun(natgoal2)

