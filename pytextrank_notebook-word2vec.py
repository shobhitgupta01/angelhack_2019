import ast
from cmd_pytextrank import pytextrank
import sys
import spacy
from sklearn import cluster
from sklearn import metrics
import pandas as pd
from scipy.spatial import distance
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity
from urllib.request import urlopen
import json

nlp = spacy.load('en_core_web_md')
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask import abort

app = Flask(__name__)

# Read the file containing the braud categories of news topics ~ 400 topics
news_topics = pd.read_csv("list_of_topics_filtered.csv")
print("No of topics considered {}".format(len(news_topics)))
news_topics_list = news_topics.topics
vectors = np.array(list(map(lambda x: nlp(x).vector, news_topics_list)))
text_file_path = './test_data/sample.json'


# Default route to check if the service is up
@app.route('/')
def index():
    return "I am up! I am up!"


# Function which returns the key terms in a document
def get_key_terms(text_doc):
    path_stage1 = "o1.json"
    with open(path_stage1, 'w') as f:
        for graf in pytextrank.parse_doc(pytextrank.json_iter(text_doc)):
            f.write("%s\n" % pytextrank.pretty_print(graf._asdict()))

    graph, ranks = pytextrank.text_rank(path_stage1)
    # pytextrank.render_ranks(graph, ranks)

    result = []
    count = 0;
    count_end = int(len(ranks)*0.2)
    for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
        count += 1
        # if count>count_end and count>40: break
        result.append(ast.literal_eval(pytextrank.pretty_print(rl))[:2])

    return result


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


# Extract text data from the provided URL
def get_text_data(url):
    html = urlopen(url).read()

    from readability.readability import Document
    from bs4 import BeautifulSoup

    readable_article = Document(html).summary()
    readable_title = Document(html).title()
    soup = BeautifulSoup(readable_article)
    url_dict = {}
    url_dict['id'] = 1
    url_dict['text'] = soup.text

    with open(text_file_path, 'w') as json_file:
        json.dump(url_dict, json_file)


@app.route('/topics', methods=['POST'])
def get_topics():
    if not request.json or not 'url' in request.json:
        abort(400)

    get_text_data(request.json['url'])
    key_terms = get_key_terms(text_file_path)

    word_vectors = list(map(lambda x: nlp(x[0]).vector, key_terms))
    NUM_CLUSTERS = 5
    kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS, n_jobs=1, n_init=10, max_iter=300,
                            random_state=0)
    kmeans.fit(word_vectors)

    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    result = {}

    for x in centroids:
        cosine_values = list(cosine_similarity(x.reshape(1, -1), vectors)[0])
        tmp = max(cosine_values)
        correlated_word = news_topics_list[cosine_values.index(tmp)]
        while correlated_word in result:
            cosine_values[cosine_values.index(tmp)] = -1
            tmp = max(cosine_values)
            correlated_word = news_topics_list[cosine_values.index(tmp)]

        result[correlated_word] = tmp
    #     result.append([news_topics_list[cosine_values.index(max(cosine_values))], max(cosine_values)])

    # return collections.OrderedDict(result)
    return jsonify(sorted(result.items(), key=lambda kv: -kv[1]))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# print(get_topics("https://www.dawn.com/news/1486778"))
#https://www.who.int/denguecontrol/disease/en/
