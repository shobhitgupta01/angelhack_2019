from flask import Flask, jsonify, render_template, url_for, request
from get_text import get_text
from flask_googlecharts import GoogleCharts, BarChart, MaterialLineChart
from flask_googlecharts.utils import prep_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/topics',methods = ['POST','GET'])
def topics():
    if request.method == 'POST':
        result = request.form
    url = result['url']
    page_text = get_text(url)
    print(page_text)
    return render_template('results.html',result = page_text)


if __name__ == "__main__":

    app.run(debug=True)