import requests
from bs4 import BeautifulSoup
import json


urls = [ ["http://paulgraham.com/getideas.html", 'startup-blog'], 
         ["http://paulgraham.com/users.html", 'startup-blog'], 
         ["http://paulgraham.com/fn.html", 'startup-blog'], 
         ["http://paulgraham.com/newideas.html", 'startup-blog'], 
         ["http://paulgraham.com/ace.html", 'startup-blog'], 
         ["https://patrickcollison.com/advice", 'startup-blog'], 
         ["https://patrickcollison.com/fast", 'startup-blog'], 
         ["https://patrickcollison.com/culture", 'startup-blog'], 
         ["https://patrickcollison.com/svhistory", 'startup-blog'],
         ["https://patrickcollison.com/questions", 'startup-blog'],
         ["https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/", 'llm-blog'],
         ["https://lilianweng.github.io/posts/2023-01-10-inference-optimization/", 'llm-blog'],
         ["https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/", 'llm-blog'],
         ["https://lilianweng.github.io/posts/2021-07-11-diffusion-models/", 'llm-blog'],
         ["https://lilianweng.github.io/posts/2020-08-06-nas/", 'llm-blog'],
         ["https://huyenchip.com/2023/05/02/rlhf.html", 'llm-blog'],
         ["https://huyenchip.com/2023/04/11/llm-engineering.html", 'llm-blog'],
         ["https://huyenchip.com/2022/12/27/books-for-every-engineer.html", 'llm-blog'],
         ["https://huyenchip.com/2021/09/07/a-friendly-introduction-to-machine-learning-compilers-and-optimizers.html", 'llm-blog'],
         ["https://huyenchip.com/2021/02/27/why-not-join-a-startup.html", 'llm-blog'],
         ["https://www.jasoncolavito.com/the-case-of-the-false-quotes.html",'news'],
         ["https://www.techspot.com/news/99102-european-union-votes-bring-back-replaceable-phone-batteries.html",'news'],
         ["https://www.theguardian.com/us-news/2023/jun/16/louisiana-drivers-license-hack-cyber-attack",'news'],
         ["https://susam.net/blog/control-escape-meta-tricks.html",'news'],
         ["https://www.bbc.com/future/article/20230613-onkalo-has-finland-found-the-answer-to-spent-nuclear-fuel-waste-by-burying-it",'news'],
         ["https://www.bitsaboutmoney.com/archive/requiem-for-a-bank-loan/",'news'],
         ["https://e360.yale.edu/digest/groundwater-depletion-earths-axis",'news'],
         ["https://www.earth.com/news/breakthrough-surges-of-cosmic-radiation-from-space-directly-linked-to-earthquakes/",'news'],
         ["https://www.ksat.com/news/local/2023/06/15/gov-greg-abbott-signs-new-law-mandating-armed-security-at-all-texas-schools/",'news'],
         ["http://www.jdawiseman.com/books/pricing-money/Pricing_Money_JDAWiseman.html",'news'],
         ["https://www.cricbuzz.com/cricket-news/125321/bowlers-the-shining-lights-of-south-africas-gritty-win", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/125112/sa20-a-glimmer-of-light-amid-south-africas-gloom", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/125029/when-disciplined-saurashtra-defied-the-odds", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/124987/sarfaraz-khan-and-musheer-khan-living-their-fathers-dream", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/124901/the-insatiable-appetite-of-yashasvi-jaiswal-for-runs", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/124427/how-mumbai-solved-the-elusive-trophy-puzzle", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/124426/selection-interference-remains-afghanistans-achilles-heel", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/124380/liton-shines-bright-in-bangladeshs-spirited-fight-against-india", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/123966/areas-of-concern-for-bangladesh-despite-confidence-boosting-win", 'cricket'],
         ["https://www.cricbuzz.com/cricket-news/123564/can-shakib-al-hasan-change-bangladeshs-t20i-fortune", 'cricket']
       ]

tests = {"who did bangladesh defeat": "https://www.cricbuzz.com/cricket-news/123966/areas-of-concern-for-bangladesh-despite-confidence-boosting-win",
         "best batsman in rajasthan royals": "https://www.cricbuzz.com/cricket-news/124901/the-insatiable-appetite-of-yashasvi-jaiswal-for-runs",
         "Brothers in Ranji Trophy": "https://www.cricbuzz.com/cricket-news/124987/sarfaraz-khan-and-musheer-khan-living-their-fathers-dream",
         "How much SA20 earn this year": "https://www.cricbuzz.com/cricket-news/125112/sa20-a-glimmer-of-light-amid-south-africas-gloom",
         "Rashid Khan captain?": "https://www.cricbuzz.com/cricket-news/124426/selection-interference-remains-afghanistans-achilles-heel",
         "Explosions in Mahabharata": "https://www.jasoncolavito.com/the-case-of-the-false-quotes.html",
         "How to choose maturity of bonds": "http://www.jdawiseman.com/books/pricing-money/Pricing_Money_JDAWiseman.html",
         "dark matter responsible for earthquakes?": "https://www.earth.com/news/breakthrough-surges-of-cosmic-radiation-from-space-directly-linked-to-earthquakes/",
         "benefits of nuclear energy": "https://www.bbc.com/future/article/20230613-onkalo-has-finland-found-the-answer-to-spent-nuclear-fuel-waste-by-burying-it",
         "Apple has to comply with EU": "https://www.techspot.com/news/99102-european-union-votes-bring-back-replaceable-phone-batteries.html",
         "what is rotary position embedding": "https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/",
         "Chain-of-Thought prompting": "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
         "Quantization-Aware Training": "https://lilianweng.github.io/posts/2023-01-10-inference-optimization/",
         "Constitutional AI from Anthropic": "https://huyenchip.com/2023/05/02/rlhf.html",
         "Impact of LLMs on SEO": "https://huyenchip.com/2023/04/11/llm-engineering.html",
         "Taking control of YC interviews": "http://paulgraham.com/ace.html",
         "Are nerds independant-minded?": "http://paulgraham.com/fn.html",
         "where good ideas come from": "http://paulgraham.com/getideas.html",
         "is computing a pop culture": "https://patrickcollison.com/svhistory",
         "How fast can ambitious projects get built": "https://patrickcollison.com/fast"
        }

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


if __name__ == '__main__':
    #convert_multple_urls(urls)
    score = 0
    for idx, test in enumerate(tests):
        print("IDX: ", idx)
        data = {"question": test, "number_of_results": str(num_of_results)}
        res = requests.post("http://127.0.0.1:5000/search", json=data)
        try:
            result = json.loads(res.text)
        except ValueError as e:
            print("IDX: ", idx, " Error parsing result json")
            continue
        if tests[test] in result['top_sites']:
            score += 1
        else:
            print(test, result['top_sites'])
    print(score/len(tests))
