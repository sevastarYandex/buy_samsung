from flask import Flask, request, jsonify
import logging
from random import shuffle

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
                "У меня техника apple.",
                "Айфон хочу!",
                "Я смотрю Вилсакома.",
                "Я больше по яблокам.",
                "ЭЭЭ ЭЭЭ это же Самсунг!!!"
            ]
        }
        res['response']['text'] = 'Привет! Купи Самсунг!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        res['response']['text'] = 'Самсунг можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return
    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи Самсунг!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][2:]
    sessionStorage[user_id] = session
    shuffle(sessionStorage[user_id])
    if len(suggests) < 2:
        suggests.append({
            "title": "Айфоны оверпрайс! Купи уже Самсунг!",
            "url": "https://market.yandex.ru/search?text=Самсунг",
            "hide": True
        })
    return suggests


if __name__ == '__main__':
    app.run()
