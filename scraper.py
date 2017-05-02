import bs4
import re
import requests
from nltk.tokenize import word_tokenize
from functools import reduce

base_path = "http://praag.co.za/?p="
start_from = 43625

flatten = lambda l: [] if l == [] else reduce(lambda a, b: a + b, l)

# generate a list of responses
art2res = lambda art: requests.request("GET", base_path + str(art))
responses = lambda x: [art2res(start_from - i) for i in range(x)]

# extract paragraphs from response
f0 = lambda res: res.text
f1 = lambda string: re.sub(r"\n", "", string)
f2 = lambda string: bs4.BeautifulSoup(string, "lxml")
f3 = lambda da_soup: da_soup.find("div", attrs={"class": "entry-content"})
f4 = lambda da_soup: da_soup.find_all("p") if da_soup is not None else []
res2ps = lambda res: f4(f3(f2(f1(f0(res)))))

# extract words from paragraph
p2words = lambda p: word_tokenize(p.text)

# extract list of words from response
res2words = lambda res: flatten([p2words(p) for p in res2ps(res)])

# count and sort number of elements in a list
ws0 = lambda l: {x: l.count(x) for x in set(l)}
# TODO flatten2 [dict] -> dict to reduce memory usage
ws1 = lambda d: sorted(d.items(), key=lambda x: x[1], reverse=True)
words2sorted = lambda words: ws1(ws0(words))

# returns list of sorted words from list from list of responses
reses2sorted = lambda l: words2sorted(flatten(map(res2words, l)))

if __name__ == '__main__':
    raw = responses(15)
    with open("results.txt", "w", encoding="utf-8") as myfile:
        myfile.write(
            str(words2sorted(flatten(
                map(p2words, flatten(
                    map(res2ps, [i for i in raw if i.status_code == 200])))))))
