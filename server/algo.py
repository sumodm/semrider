from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
import nltk
import pickle
from nltk.tokenize import sent_tokenize


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


nltk.download('punkt')
model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
session = ort.InferenceSession("res/traced_bert.onnx")
embeds, sites, texts = load_files()


def get_embeddings(text):
    embedded_text = tokenizer(text, padding="max_length", truncation=True)
    ort_inputs = {"input_ids": np.array(embedded_text["input_ids"]).reshape(1, -1),
                  "attention_mask": np.array(embedded_text["attention_mask"]).reshape(1, -1)}
    ort_outputs = session.run(None, ort_inputs)
    return ort_outputs[0]


def chunk_text(text, chunk_size=200):
    sentences = sent_tokenize(text)
    idx = 0
    chunk = ""
    chunks = []
    for sentence in sentences:
        idx = idx + len(tokenizer.tokenize(sentence))
        chunk += sentence
        if idx >= chunk_size:
            chunks.append(chunk)
            chunk = ""
            idx = 0
    else:
        if len(chunk) == 0:
            return chunks
        chunks.append(chunk)
    return chunks


def insert_embeddings(text, site):
    global embeds, sites, texts
    chunks = chunk_text(text)
    sites.extend(len(chunks) * [site])
    texts.extend(chunks)
    for chunk in chunks:
        if embeds.size == 0:
            embeds = get_embeddings(chunk)
        else:
            embeds = np.vstack([embeds, get_embeddings(text)])
    return True


def top_results(query_embedding, num_of_results=5, embeds_arg=None, sites_arg=None, texts_arg=None):
    if embeds_arg is None and sites_arg is None and texts_arg is None:
        global embeds, sites, texts
    else:
        embeds = embeds_arg
        sites = sites_arg
        texts = texts_arg
    scores = embeds.dot(query_embedding.T)
    top_idx = np.argsort(scores.flatten())[-(num_of_results * 10):][::-1]
    urls_picked = set()
    top_context = []
    top_sites = []
    for i in top_idx:
        if len(top_context) >= num_of_results:
            break
        if sites[i] not in urls_picked:
            urls_picked.add(sites[i])
            top_context.append(texts[i])
            top_sites.append(sites[i])
    return {'top_sites': top_sites, 'top_context': top_context}


def dump_data():
    pickle.dump(embeds, open("embeds.pkl", "wb"))
    pickle.dump(sites, open("sites.pkl", "wb"))
    pickle.dump(texts, open("texts.pkl", "wb"))
