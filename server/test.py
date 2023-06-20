import requests
from bs4 import BeautifulSoup
from algo import get_embeddings, top_results, chunk_text
from iops import lazy_csv_reader
from os.path import exists
import pickle as pkl
import numpy as np
#from exceptions import MissingSchema


num_of_results = 1100


def extract_text_from_html(url):
    try:
        response = requests.get(url[0].strip())
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
    except:
        return "Text Not available"
    return text


def convert_multple_urls(urls):
    for url in urls:
        text = extract_text_from_html(url)
        data = {"site": url[0], "text": text}
        requests.post("http://127.0.0.1:5000/update", json=data)


def prep_test_train(train_embeds_file, train_sites_file, test_embeds_file):
    ''' Given train_embeds_file and test_embeds_file
        load them if they are not there, else calculate embedding and store the same
    '''
    train_data_file = "res/hn_url_gt_100.csv"
    test_data_file = "res/100_test_samples.csv"
    train_sites = []

    # Get Train Embeddings, if embedding exists just load it
    if exists(train_embeds_file):
        train_embeds = pkl.load(open(train_embeds_file, "rb"))
        train_sites.extend(pkl.load(open(train_sites_file, "rb")))
    else:
        train_embeds = np.array([])
        for idx, train_row in enumerate(lazy_csv_reader(train_data_file)):
            print("Train IDX: ", idx)
            if idx == 1000:
                break
            train = extract_text_from_html(train_row[0])
            train_sites.append(train_row[0])
            chunks = chunk_text(train)
            for chunk in chunks:
                if train_embeds.size == 0:
                    train_embeds = get_embeddings(chunk)
                else:
                    train_embeds = np.vstack([train_embeds, get_embeddings(chunk)])
                #np.append(train_embeds, get_embeddings(chunk))
                #train_embeds.vstack(get_embeddings(chunk))
        for test_row in lazy_csv_reader(test_data_file):
            test = extract_text_from_html(test_row[0])
            train_sites.append(test_row[0])
            chunks = chunk_text(test)
            for chunk in chunks:
                train_embeds = np.vstack([train_embeds, get_embeddings(chunk)])
                #train_embeds.vstack(get_embeddings(chunk))
        pkl.dump(train_embeds, open(train_embeds_file, "wb"))
        pkl.dump(train_sites, open(train_sites_file, "wb"))
 
    # Get Test Embeddings, if embedding exists just load it
    if exists(test_embeds_file):
        test_embeds = pkl.load(open(test_embeds_file, "rb"))
    else:
        test_embeds = np.array([])
        for idx, test_row in enumerate(lazy_csv_reader(test_data_file)):
            print(idx)
            test = test_row[2]
            test_embed = get_embeddings(test)
            if test_embeds.size == 0:
                test_embeds = test_embed
            else:
                test_embeds = np.vstack([test_embeds, test_embed])
            #np.append(test_embeds, test_embed)
            #test_embeds.append(test_embed)
        pkl.dump(test_embeds, open(test_embeds_file, "wb"))
    return train_embeds, train_sites, test_embeds
        

def run_test():
    train_embeds, train_sites, test_embeds = prep_test_train("res/train_embeds.pkl", "res/train_sites.pkl", "res/test_embeds.pkl")
    test_data_file = "res/100_test_samples.csv"
    test_data = open(test_data_file, "rb")
    sites = test_data.readlines()
    score = 0
    for idx, test in enumerate(test_embeds):
        print("IDX: ", idx)

        #TODO: Fix this
        #results = top_results(test, train_embeds, num_of_results)
        results = top_results(test, num_of_results, embeds_arg=train_embeds, sites_arg= train_sites)
        
        if str(sites[idx + 1]).split(",")[0] in results['top_sites']:
            score += 1
        else:
            print(len(results['top_sites']))
            #print(results['top_sites'])
    print(score/len(test_embeds))
    


if __name__ == '__main__':
    run_test()