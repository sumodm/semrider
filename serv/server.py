import signal
import atexit
from flask import Flask, request, jsonify
from flask_cors import CORS
import serv.algo2 as alg


app = Flask(__name__)
CORS(app)
alg.load_data()

def dump_files(*args):
    alg.save_data()
    exit()


@app.route('/update', methods=['POST'])
def update():
    received_text = request.json.get('text')
    site = request.json.get('site')
    print(f'Received Data: {received_text}')
    print(f'Received site: {site}')
    if alg.update(received_text, site):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})


@app.route('/search', methods=['POST'])
def search():
    question = request.json.get('question')
    number_of_results = int(request.json.get('number_of_results'))
    results = alg.find(question)
    return jsonify(results)


signal.signal(signal.SIGINT, dump_files)


if __name__ == '__main__':
    app.run(debug=True)
