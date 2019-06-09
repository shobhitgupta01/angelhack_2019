# AngelHack 2019
## Quero Challenge
__@team_name__    : do_the_code <br>
__@team_members__ : 
* Nimish Bajaj
* Shobhit Gupta

This repository contains a web application which can be used for Topic Modelling on any article and return top 5 topics detected from the article

## System Requirements
Please have the following setup ready before running the notebook :
* python 3.6.x
* Flask   ==  0.12.2
* pandas  ==  0.22.0
* pytextrank  ==  1.1.0
* sklearn ==  0.21.2
* spacy   ==  2.1.4
* urllib  ==  1.25.3
* jupyter notebook for running notebooks

## Steps for Execution
1. Complete the system setup
2. Run the web service which fetches the topics by running the following command:
```bash
python3 pytextrank_notebook-word2vec.py
```
3. Run the app service which you will be using
```bash
python3 app.py
```
4. Your app can be accessed on the url __http://\<HOST-IP>\:2019__

## Single Document Topic Modelling Approach

![Process Flow](https://github.com/shobhitgupta01/angelhack_2019/blob/master/flow_diagram.png)

