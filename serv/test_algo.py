import numpy as np
import serv.iops as iops
import serv.algo2 as alg


def test_algo():
    # C1: Case of Testing, Init
    model_file = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
    ort_format = "serv/res/traced_bert.onnx"
    embed_file = "serv/res/embed_train_v02_rc.pkl"
    meta_file = "serv/res/meta_train_v02_rc.pkl"
    confsbl_file = "serv/data/confsbl_hn_url_gt_100.csv"
    eval_file = "serv/data/eval_100_samples.csv"
    rawdata_file = "serv/data/rawtext.csv"
    sim_evltr = alg.S2PSimilarity(model_file, ort_format)
    DO_ADD_TRAIN = False
    DO_ADD_TEST = False
    DO_EVAL = True

    # C1: Insert/Load Training data (both confusable content and eval content)
    sim_evltr.load_data(embed_file, meta_file)                 # Load previously embedded data

    # C1: Insert/Load Training data (add new data)
    if DO_ADD_TRAIN:
        for idx,row in enumerate(iops.lazy_csv_reader(confsbl_file)):
            if idx == 1000:
                break
            url = row[0]                                           # Url
            if sim_evltr.is_url_indexed(url):
                print("NotProcess Test Doc", idx,": ", url)
                continue
            print("Processing Train Doc", idx,": ", url)
            meta_data_value =  {'label':'train', 'emd_indxs':[]}
            status, text = iops.extract_text_from_url(url)
            if not status: 
                print("Error in extracting text")
                continue
            sim_evltr.insert_largetext(url, meta_data_value, text) # Load new corpus of data
            iops.csv_writer(rawdata_file, url + " , " + repr(text) + "\n")

            if idx % 100 == 0:                                     # Save data after every 1000
                sim_evltr.save_data(embed_file, meta_file)

        sim_evltr.save_data(embed_file, meta_file)

    # C1: Insert/Load Test data
    if DO_ADD_TEST:
        for idx, row in enumerate(iops.lazy_csv_reader(eval_file)):
            url = row[0]
            topic = row[1]
            kwords = row[2]
            if sim_evltr.is_url_indexed(url):
                print("NotProcess Test Doc", idx,": ", url)
                continue
            print("Processing Test Doc", idx,": ", url)
            meta_data_value = {'label':'test', 'kwords':kwords, 'topic':topic, 'emd_indxs':[]}
            status, text = iops.extract_text_from_url(url)
            if not status:
                print("Error in extracting text")
                continue
            sim_evltr.insert_largetext(url, meta_data_value, text)

        sim_evltr.save_data(embed_file, meta_file)

    ### C1: For a set of phrases or their embedding, find similarity and get metrics
    if DO_EVAL:
        embd_dim = 768
        test_embed_data = np.empty((0, embd_dim))
        test_meta_data = []
        total_correct = 0
        total = 0
        for idx, row in enumerate(iops.lazy_csv_reader(eval_file)):
            test_url = row[0]
            test_topic = row[1]
            test_kwords = row[2]
            embd_data = sim_evltr.get_embedding(test_kwords)
            test_embed_data = np.vstack([test_embed_data, embd_data])
            test_pred_data, top_k_urls = sim_evltr.find_phrase(embd_data, k_val=5)
            test_meta_data.extend([test_url, test_topic, test_kwords, test_pred_data])
            
            if test_url in [u for u,t in top_k_urls]:
                total_correct += 1
            total += 1

        print(100*total_correct/total)


if __name__ == "__main__":
    test_algo()
