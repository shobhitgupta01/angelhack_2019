#importing libraries
from flask import Flask, jsonify, render_template, url_for, request
from get_text import get_text
import pandas as pd


#initialization
app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html')


@app.route('/topics',methods = ['POST','GET'])
def topics():
    team_name="do_the_code"
    
    if request.method == 'POST':
        result = request.form
    url = result['url']
    #page_text = get_text(url)
    print(url)

    

    #fetching data from service
    import requests

    request_url = "http://10.2.89.90:5000/topics"

    #payload = 
    headers = {
        'content-type': "application/json",
        }

    payload = str({'url':'{}'.format(url)})

    response = requests.request("POST", request_url, data=payload, headers=headers)

    response = response.text

    strs = response.replace('[','').split('],')
    lists = [map(int, s.replace(']','').split(',')) for s in strs]
    
    df = pd.DataFrame(lists,columns=['topic','score'])

    #data for chart
    #df = pd.DataFrame([['technology',0.85],['maths',0.70],['war',0.6],['education',0.4],['candy',0.1]],columns=["topic","score"])
   
    #rendering the page
    return render_template('results.html',df=df, titles=df.columns.values,team=team_name,url=url)


if __name__ == "__main__":

    app.run(debug=True)