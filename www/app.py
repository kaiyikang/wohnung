from flask import Flask,request,render_template,jsonify
import os,sys
o_path = os.getcwd()
sys.path.append(o_path)
from Modules.begin_time import dump_latest

app = Flask(__name__)

# https://www.datasciencelearner.com/python-ajax-json-request-form-flask/


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dump_date_dist',methods= ['POST'])
def process():
    print(r"/process")
    # Receive from front-end
    latest_json = dump_latest()
    return latest_json



if __name__ == '__main__':
    app.run(debug=True)