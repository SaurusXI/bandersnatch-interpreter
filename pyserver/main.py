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
        self.BSN = 'https://playscenario.dscvit.com/api/bandersnatch/play'
        print('Worker started')

app = App(__name__)


@app.route('/', methods=['POST'])
def start_controller():
    start = time.time()
    content = request.get_json()
    user_input = content['user_input']
    left_option = None
    right_option = None
    must_progress = False

    if 'left_option' in content:
        left_option = content['left_option']
        if left_option == 'all':
            must_progress = True
    if 'right_option' in content:
        right_option = content['right_option']
        if right_option == 'all':
            must_progress = True
    
    if not must_progress:
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
                url = app.BSN,
                headers = {'Authorization': request.headers['Authorization'], 'Content-Type': request.headers['Content-Type']},
                data = f'{{"option": {best_option} }}',
                cookies = request.cookies)
            print(time.time() - star2)
            response = Response(response.text, response.status_code, response.headers.items())

        print(time.time() - start)
        return response

    else:
        best_option = 0
        response = requests.request(
                method = 'POST',
                url = app.BSN,
                headers = {'Authorization': request.headers['Authorization'], 'Content-Type': request.headers['Content-Type']},
                data = f'{{"option": {best_option} }}',
                cookies = request.cookies)
        response = Response(response.text, response.status_code, response.headers.items())

        return response


if __name__ == '__main__':
    nlp = spacy.load('./bandersnatch_nlu')
    evaluator = Evaluator(nlp)
    replier = Replier(nlp)
    BSN = 'https://playscenario.dscvit.com/api/bandersnatch/play'
    app.run(debug=True)
