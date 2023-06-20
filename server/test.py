import requests
from bs4 import BeautifulSoup
from algo import get_embeddings, top_results
from server.iops import lazy_csv_reader
from os.path import exists
import pickle as pkl

num_of_results = 5


def extract_text_from_html(url):
    response = requests.get(url[0])
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text


def convert_multple_urls(urls):
    for url in urls:
        text = extract_text_from_html(url)
        data = {"site": url[0], "text": text}
        requests.post("http://127.0.0.1:5000/update", json=data)


def prep_test_train(train_embeds_file, test_embeds_file):
    ''' Given train_embeds_file and test_embeds_file
        load them if they are not there, else calculate embedding and store the same
    '''
    train_data_file = "res/train.csv"
    test_data_file = "res/test.csv"

    # Get Train Embeddings, if embedding exists just load it
    if exists(train_embeds_file):
        train_embeds = pkl.load(open(train_embeds_file))
    else:
        for train_row in lazy_csv_reader(train_data_file):
            train = extract_text_from_html(train_row[0])
            train_embed = get_embedding(train)
            train_embeds.append(train_embed)
        for test_row in lazy_csv_reader(test_data_file):
            test = extract_text_from_html(test_row[0])
            train_embed = get_embedding(test)
            train_embeds.append(train_embed)
        pkl.dump(train_embeds, open(train_embeds_file, "wb"))
 
    # Get Test Embeddings, if embedding exists just load it
    if exists(test_embeds_file):
        test_embeds = pkl.load(open(test_embeds_file))
    else:
        for test_row in lazy_csv_reader(test_data_file):
            test = test_row[2]
            test_embed = get_embeddings(test)
            test_embeds.append(test_embed)
        pkl.dump(test_embeds, open(test_embeds_file, "wb"))
   return train_embeds, test_embeds
        
    

def run_test():
    train_embeds, test_embeds = prep_test_train("res/train_embeds.pkl", "res/test_embeds.pkl")
    score = 0
    for idx, test in enumerate(test_embeds):
        print("IDX: ", idx)

        #TODO: Fix this
        results = top_results(question_embed, num_of_results, embeds_arg=train_embeds)
        
        if tests[test] in results['top_sites']:
            score += 1
        else:
            print(test, results['top_sites'])
    print(score/len(tests))
    


if __name__ == '__main__':
