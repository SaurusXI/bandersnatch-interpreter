from flask import Flask
from flask import request
from flask import jsonify
from replier import Replier
from scorer import Evaluator
from sklearn.metrics.pairwise import cosine_similarity
from bert_serving.client import BertClient
import requests
import argparse
import nltk

app = Flask(__name__)


@app.route('/', methods=['POST'])
def start_controller():
    content = request.get_json()
    user_input = content['user_input']
    left_option = None
    right_option = None


    if 'left_option' in content:
        left_option = content['left_option']
    if 'right_option' in content:
        right_option = content['right_option']
    
    valid_input, best_option, best_score = evaluator.check_options(user_input, left_option, right_option)
    if not valid_input:
        reply = replier.reply(user_input, best_score)
        response = {"data": {"content": reply}}
        response = jsonify(response)

    else:
        request_body = {"option": best_option}
        response = requests.post(args.backend, request_body, headers = request.headers)

    return response


"""
Return reply for user input
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backend', type=str, default='https://playscenario.dscvit.com/api/bandersnatch/play', dest='backend', help='URL for bandersnatch backend')
    args = parser.parse_args()

    nltk.download('all')
    client = BertClient(ip = 'model')

    evaluator = Evaluator(client, cosine_similarity)
    replier = Replier()
    app.run(host = '0.0.0.0', port = 80, debug=True)