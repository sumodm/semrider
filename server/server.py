import nltk
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer
import onnxruntime
import numpy as np
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import atexit


chunk_size = 200

def load_files():
    try:
        embeds = pickle.load(open("embeds.pkl", "rb"))
        embeds = np.array(embeds).reshape(len(embeds), -1)
    except FileNotFoundError:
        embeds = np.array([])
    try:
        sites = pickle.load(open("sites.pkl", "rb"))
    except FileNotFoundError:
        sites = []
    try:
        texts = pickle.load(open("texts.pkl", "rb"))
    except FileNotFoundError:
        texts = []
    return embeds, sites, texts


model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
session = onnxruntime.InferenceSession("res/traced_bert.onnx")
nltk.download('punkt')
app = Flask(__name__)
CORS(app)
embeds, sites, texts = load_files()


def get_embeddings(text):
    embedded_text = tokenizer(text, padding="max_length", truncation=True)
    ort_inputs = {"input_ids": np.array(embedded_text["input_ids"]).reshape(1,-1),
                  "attention_mask" : np.array(embedded_text["attention_mask"]).reshape(1,-1)}
    ort_outputs = session.run(None, ort_inputs)
    return ort_outputs[0]


@atexit.register
def dump_files():
    pickle.dump(embeds, open("embeds.pkl", "wb"))
    pickle.dump(sites, open("sites.pkl", "wb"))
    pickle.dump(texts, open("texts.pkl", "wb"))


@app.route('/update', methods=['POST'])
def update():
    global embeds, sites, texts
    received_text = request.json.get('text')
    site = request.json.get('site')
    print(f'Received Data: {received_text}')
    print(f'Received site: {site}')
    #embeds, sites, texts = load_files()
    sentences = sent_tokenize(received_text)
    idx = 0
    text = ""
    for sentence in sentences:
        idx = idx + len(tokenizer.tokenize(sentence))
        text += sentence
        if idx >= chunk_size:
            sites.append(site)
            texts.append(text)
            if embeds.size == 0:
                embeds = get_embeddings(text)
            else:
                embeds = np.vstack([embeds, get_embeddings(text)])
            text = ""
            idx = 0
    else:
        sites.append(site)
        texts.append(text)
        if embeds.size == 0:
            embeds = get_embeddings(text)
        else:
            embeds = np.vstack([embeds, get_embeddings(text)])
    return jsonify({'success': True})


@app.route('/search', methods=['POST'])
def search():
    global embeds, sites, texts
    #embeds, sites, texts = load_files()
    question = request.json.get('question')
    number_of_results = int(request.json.get('number_of_results'))
    question_embed = get_embeddings(question)
    similarities = embeds.dot(question_embed.T)
    top_indices = np.argsort(similarities.flatten())[-(number_of_results * 10):][::-1]
    urls_picked = set()
    top_context = []
    top_sites = []
    for i in top_indices:
        if len(top_context) >= number_of_results:
            break
        if sites[i] not in urls_picked:
            urls_picked.add(sites[i])
            top_context.append(texts[i])
            top_sites.append(sites[i])
    return jsonify({'top_sites': top_sites, 'top_context': top_context})


if __name__ == '__main__':
    app.run(debug=True)
