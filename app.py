#importing libraries
from flask import Flask, jsonify, render_template, url_for, request
from get_text import get_text
from flask_googlecharts import GoogleCharts, BarChart, MaterialLineChart
from flask_googlecharts.utils import prep_data

#initialization
app = Flask(__name__)
charts = GoogleCharts(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/topics',methods = ['POST','GET'])
def topics():
    if request.method == 'POST':
        result = request.form
    url = result['url']
    #page_text = get_text(url)
    print(url)


    #making google chart
    my_chart = BarChart("my_chart", options={'title': 'My Chart'})

    #data for chart
    chart_data = [["technology",0.85],["maths",0.70],["war",0.6],['education',0.4],['candy',0.1]]

    #adding data to chart
    my_chart.add_column("Topic","Confidence Score")
    my_chart.add_rows(chart_data)

    #registering chart
    charts.register(my_chart)

    #rendering the page
    return render_template('results.html',result = url)


if __name__ == "__main__":

    app.run(debug=True)