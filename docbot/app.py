import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from docbot import *
# production server
from waitress import serve

# bot, covering content of given text file
bots = {
  "alice": None,
  "bfr"	: None,
  "heaven" : None,
  "relativity" : None,
  "cats"	: None,
  "heli" :None,
  "tesla" :None,
  "const"	: None,
  "hindenburg"	: None,
  "covid"	: None,
  "kafka"	: None,
  "texas"	: None,
  "ec2"	: None,
  "logrank"	: None,
  "toxi"	: None,
  "einstein"	: None,
  "peirce" : None,
  "wasteland"	: None,
  "geo"	: None,
  "red"	: None,
  "wolfram"	: None
}

UPLOAD_FOLDER = '/home/UNT/ws0163/Documents/pytalk/examples'
ALLOWED_EXTENSIONS = {'pdf'}

def activate_bot(name) :
  if not bots[name]:
     bots[name] = Bot("../examples/"+name+".txt")
  return bots[name]

# returns whether the file uploaded has correct filetype
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# the Flask-based Web app
app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    userText = request.args.get('msg')
    if ':' not in userText:
      return 'Expected "document_name : query ?" as input'
    else :
        fname, query = userText.split(':')
        fname=fname.strip()
        query=query.strip()
        try :
          bot=activate_bot(fname)
        except :
          return "Sorry, no such document found."
        if "summary" in query :
          return bot.summary
        if "keywords" in query:
         return bot.keyphrases
        try:
          return bot.ask(userText)
        except:
          return "Sorry, I have no answer to that."

# receives uploaded file
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            bot = Bot("../examples/" + filename)
            botname = filename[:-4]
            bots[botname] = bot
            print(bots)
            return redirect(request.url)
            # return redirect(url_for('uploaded_file',filename=filename))

    return 0

# method used once user is redirected from upload_file()
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
  '''
  starts, on given port, production or
  Flask based development server
  '''
  #app.run() # development only
  serve(app, host="0.0.0.0", port=8080) #production

