import serv.iops as iops
import serv.algo as alg
import os


model_file = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
ort_format = "serv/res/traced_bert.onnx"
embed_file = "serv/res/embed_train_v02_rc.pkl"
meta_file = "serv/res/meta_train_v02_rc.pkl"
rawdata_file = "serv/data/prod_rawtext.csv"
cold_file = "serv/data/ch_1april23_2lines.txt"

sim_sys = alg.S2PSimilarity(model_file, ort_format)



def save_data(embed_file, meta_file):
    sim_sys.save_data(embed_file, meta_file)
    return

def load_data(embed_file, meta_file):
    sim_sys.load_data(embed_file, meta_file)              # Load previously embedded data


def insert_cold_data(cold_file, label='prod'):
    for row in iops.lazy_txt_reader(cold_file):
        url = row[0]
        if sim_sys.is_url_indexed(url):                  # Check if in index already
            continue
        status, text = iops.extract_text_from_url(url)   # Extract text from url
        if not status:
            print("Error in extracting text")
            continue
    
        meta_data_value = {'label':label, 'emd_indxs':[]}
        sim_sys.insert_largetext(url, meta_data_value, text) # Load new corpus of data


def update(url, text, date, title, label='prod'):
    meta_data_value = {'label':'prod', 'emd_indxs':[], 'date':date, 'title':title}
    sim_sys.insert_largetext(url, meta_data_value, text) # Load new corpus of data
    return True


def find(test_kwords, k_val=5):
    embd_data = sim_sys.get_embedding(test_kwords)
    test_pred_data, top_k_urls = sim_sys.find_phrase(embd_data, k_val=k_val)
    #print(res['top_sites'], res['top_contexts'])
    return top_k_urls

if __name__ == "__main__":
    # Basic Test Sequence for Semrider
    load_data(embed_file, meta_file)
    insert_cold_data(cold_file, label='prod-test')
    update("http://paulgraham.com/getideas.html", "How to get ideas", label='prod-test')
    find("How to get ideas")
