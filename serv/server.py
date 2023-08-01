import signal
import atexit
from flask import Flask, request, jsonify
from flask_cors import CORS
import serv.semrider as sm
import os

embed_file = "serv/res/embed_prod_v02_rc.pkl"
meta_file = "serv/res/meta_prod_v02_rc.pkl"

# Clean up 
clean_up = True
if clean_up:
    if os.path.exists(embed_file):
        os.remove(embed_file)

    if os.path.exists(meta_file):
        os.remove(meta_file)

app = Flask(__name__)
CORS(app)

sm.load_data(embed_file, meta_file)

def dump_files(*args):
    # breakpoint()
    sm.save_data(embed_file, meta_file)
    exit()


@app.route('/update', methods=['POST'])
def update():
    received_text = request.json.get('text')
    site = request.json.get('site')
    date = request.json.get('date')
    title = request.json.get('title')

    print(f'Received Data: {received_text}')
    print(f'Received site: {site}')
    print(f'Received Title: {title}')
    print(f'Received Date: {date}')

    if sm.update(site, received_text, date, title):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})


@app.route('/search', methods=['POST'])
def search():
    question = request.json.get('question')
    number_of_results = int(request.json.get('number_of_results'))
    results = sm.find(question, number_of_results)
    results = {'top_sites': [u for u,t in results], 'top_context': [t for u,t in results]}
    return jsonify(results)


signal.signal(signal.SIGINT, dump_files)


if __name__ == '__main__':
    app.run(debug=True)
