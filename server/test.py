import requests
from bs4 import BeautifulSoup
import json


urls = ["http://paulgraham.com/getideas.html", "http://paulgraham.com/users.html", "http://paulgraham.com/fn.html", "http://paulgraham.com/newideas.html", "http://paulgraham.com/ace.html", "https://patrickcollison.com/advice", "https://patrickcollison.com/fast", "https://patrickcollison.com/culture", "https://patrickcollison.com/svhistory", "https://patrickcollison.com/questions", "https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/", "https://lilianweng.github.io/posts/2023-01-10-inference-optimization/", "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/", "https://lilianweng.github.io/posts/2021-07-11-diffusion-models/", "https://lilianweng.github.io/posts/2020-08-06-nas/", "https://huyenchip.com/2023/05/02/rlhf.html", "https://huyenchip.com/2023/04/11/llm-engineering.html", "https://huyenchip.com/2022/12/27/books-for-every-engineer.html", "https://huyenchip.com/2021/09/07/a-friendly-introduction-to-machine-learning-compilers-and-optimizers.html", "https://huyenchip.com/2021/02/27/why-not-join-a-startup.html", "https://www.jasoncolavito.com/the-case-of-the-false-quotes.html","https://www.techspot.com/news/99102-european-union-votes-bring-back-replaceable-phone-batteries.html","https://www.theguardian.com/us-news/2023/jun/16/louisiana-drivers-license-hack-cyber-attack","https://susam.net/blog/control-escape-meta-tricks.html","https://www.bbc.com/future/article/20230613-onkalo-has-finland-found-the-answer-to-spent-nuclear-fuel-waste-by-burying-it","https://www.bitsaboutmoney.com/archive/requiem-for-a-bank-loan/","https://e360.yale.edu/digest/groundwater-depletion-earths-axis","https://www.earth.com/news/breakthrough-surges-of-cosmic-radiation-from-space-directly-linked-to-earthquakes/","https://www.ksat.com/news/local/2023/06/15/gov-greg-abbott-signs-new-law-mandating-armed-security-at-all-texas-schools/","http://www.jdawiseman.com/books/pricing-money/Pricing_Money_JDAWiseman.html", "https://www.cricbuzz.com/cricket-news/125321/bowlers-the-shining-lights-of-south-africas-gritty-win","https://www.cricbuzz.com/cricket-news/125112/sa20-a-glimmer-of-light-amid-south-africas-gloom","https://www.cricbuzz.com/cricket-news/125029/when-disciplined-saurashtra-defied-the-odds","https://www.cricbuzz.com/cricket-news/124987/sarfaraz-khan-and-musheer-khan-living-their-fathers-dream","https://www.cricbuzz.com/cricket-news/124901/the-insatiable-appetite-of-yashasvi-jaiswal-for-runs","https://www.cricbuzz.com/cricket-news/124427/how-mumbai-solved-the-elusive-trophy-puzzle","https://www.cricbuzz.com/cricket-news/124426/selection-interference-remains-afghanistans-achilles-heel","https://www.cricbuzz.com/cricket-news/124380/liton-shines-bright-in-bangladeshs-spirited-fight-against-india","https://www.cricbuzz.com/cricket-news/123966/areas-of-concern-for-bangladesh-despite-confidence-boosting-win","https://www.cricbuzz.com/cricket-news/123564/can-shakib-al-hasan-change-bangladeshs-t20i-fortune"]
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
num_of_results = 3


def extract_text_from_html(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text


def convert_multple_urls(urls):
    for url in urls:
        text = extract_text_from_html(url)
        data = {"site": url, "text": text}
        requests.post("http://127.0.0.1:5000/update", json=data)


if __name__ == '__main__':
    #convert_multple_urls(urls)
    score = 0
    for test in tests:
        data = {"question": test, "number_of_results": str(num_of_results)}
        res = requests.post("http://127.0.0.1:5000/search", json=data)
        result = json.loads(res.text)
        if tests[test] in result['top_sites']:
            score += 1
        else:
            print(test, result['top_sites'])
    print(score/len(tests))
