from os import environ
from flask import Flask, render_template
app = Flask(__name__)
 
@app.route('/')
def home():
   return render_template(environ['html_name'])

@app.route('/health')
def health():
   return {"status": "ok"}, 200
if __name__ == '__main__':
   app.run()