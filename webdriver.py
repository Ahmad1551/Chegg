from flask import Flask
from threading import Thread
from flask.templating import render_template

app = Flask(__name__, template_folder='template')
@app.route('/test')
def test():
	return render_template("new911.html")

@app.route('/')

def home():
  return 'M GOOD'

def run():
    app.run(host="0.0.0.0", port=0000)

def keep_alive():
    Corona_borealis = Thread(target=run)
    Corona_borealis.start()