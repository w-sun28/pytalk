from flask import Flask, render_template, request

from docbot import *
# production server
from waitress import serve

# bot, covering content of given text file
bot = Bot('../examples/covid.txt')

# the Flask-based Web app
app = Flask(__name__,static_url_path='/static')

@app.route("/")
def home():
    '''
    defines loaction of html template
    '''
    return render_template("home.html")

# method used by queries
@app.route("/get")
def get_bot_response():
    '''
    passes user text from client form to bot
    gets back answer and returns it to client
    '''
    global bot
    userText = request.args.get('msg')
    if "open " in userText:
      text=userText.replace('.','')
      text = userText.replace('?', '')
      ws=text.split(' ')
      fname=ws[1]
      try :
        bot=Bot("../examples/"+fname+".txt")
        answers=["This document is about: "+bot.keyphrases+" . "
                "Starting with a short summary: "+bot.summary
               ]
        return " ".join(answers)
      except :
        return "Sorry, no such document!"
    elif userText =='summary?':
      return bot.summary
    elif userText =='keywords?':
      return bot.keyphrases
    else :
      try :
        return bot.ask(userText)
      except:
        return "Sorry, I have no answer to that."

if __name__ == "__main__":
  '''
  starts, on given port, production or
  Flask based development server
  '''
  #app.run() # development only
  serve(app, host="0.0.0.0", port=8080) #production

