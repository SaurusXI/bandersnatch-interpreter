from flask import Flask
from flask import request, Response
from flask import jsonify
from replier import Replier
from scorer import Evaluator
import spacy
import requests
import time

class App(Flask):
    def __init__(self, name):
        super(App, self).__init__(name)
        nlp = spacy.load('./bandersnatch_nlu')
        self.evaluator = Evaluator(nlp)
        self.replier = Replier(nlp)
        self.BACKEND = 'https://playscenario.dscvit.com/api/bandersnatch/play'
        print('Worker started')

app = App(__name__)


@app.route('/', methods=['POST'])
def start_controller():
    start = time.time()
    print('c')
    content = request.get_json()
    user_input = content['user_input']
    left_option = None
    right_option = None

    if 'left_option' in content:
        left_option = content['left_option']
    if 'right_option' in content:
        right_option = content['right_option']
    
    valid_input, best_option, left_score, right_score = app.evaluator.check_options(user_input, left_option, right_option)
    print(time.time() - start)
    if not valid_input:
        reply = app.replier.reply(user_input, left_score, right_score, left_option, right_option)
        response = {"data": {"content": reply}}
        response = jsonify(response)

    else:
        star2 = time.time()
        response = requests.request(
            method = 'POST',
            url = app.BACKEND,
            headers = {'Authorization': request.headers['Authorization'], 'Content-Type': request.headers['Content-Type']},
            data = f'{{"option": {best_option} }}',
            cookies = request.cookies)
        print(time.time() - star2)
        response = Response(response.text, response.status_code, response.headers.items())

    print(time.time() - start)
    return response


if __name__ == '__main__':
    nlp = spacy.load('./bandersnatch_nlu')
    evaluator = Evaluator(nlp)
    replier = Replier(nlp)
    BACKEND = 'https://playscenario.dscvit.com/api/bandersnatch/play'
    print ('asdfasdf')
    app.run(debug=True)
