"""
This file contains code to generate the word cloud from bibtex file.
"""
import json
import re

from matplotlib import pyplot as plt
from wordcloud import STOPWORDS, WordCloud

from bib_helper.common import read_bib_file


def read_bib_abstract(file_path: str):
    """
    Method to read the bibtex file and return a list of abstracts
    :param file_path:
    :return:
    """
    abstracts = []
    bib_db = read_bib_file(file_path)
    for each in bib_db.entries:
        abstract = each.get('abstract', None)
        if abstract:
            abstracts.append(each['abstract'])
    return abstracts


def filter_papers(bib_file_path, have_words=[]):
    """
    Method to find papers with words in abstract
    :param bib_file_path:
    :param have_words:
    :return:
    """
    results = []
    bib_db = read_bib_file(file_path=bib_file_path)
    for each in bib_db.entries:
        found_all_words = True
        abstract = each.get('abstract', '')
        abstract += ' ' + each['title']
        abstract = abstract.lower()
        for w in have_words:
            if not re.search(w, abstract):
                found_all_words = False
                break
        if found_all_words:
            results.append(each)
    print(f"found : {len(results)}")
    titles = []
    keys = []
    for each in results:
        titles.append(each['title'][1:-1])
        keys.append(each['ID'])
        print(keys[-1], ' - ', titles[-1])
    keys_count = len(keys)
    if keys_count != len(set(keys)):
        raise ValueError(f"Duplicate entries All keys {len(keys)}, Actual {len(set(keys))}")

    print(f'All keys :')
    for i in range(0, keys_count + 1, 10):
        print(' or '.join(keys[i:i + 10]))
    print('Found ', len(set(keys)))

    download_data = {}
    for each in keys:
        f_name = each + '.pdf'

        doi = bib_db.entries_dict[each].get('doi', None)
        if doi is None:
            doi = bib_db.entries_dict[each].get('url', None)
        if doi is None:
            print(f'Unable to find doi or url for ID {each}')
        else:
            download_data[f_name] = doi
    print(json.dumps(download_data))


def generate_word_cloud(bib_file_path: str, ignore_words: list, save_as):
    """
    Method to generate word cloud of the abstracts from bib file
    :param bib_file_path: path to bib file
    :param ignore_words: ignore list of words
    :return:
    """
    print('save_as')
    if ignore_words is None:
        ignore_words = []

    data = ' '.join(read_bib_abstract(file_path=bib_file_path))
    data = ''.join([i if ord(i) < 128 else '' for i in data])
    # Create stop word list:
    stopwords = set(STOPWORDS)
    stopwords.update(ignore_words)
    stopwords = set(stopwords)

    # Generate a word cloud image
    word_cloud = WordCloud(font_path="C:\\Windows\\Fonts\\Verdana.ttf", max_font_size=100,
        stopwords=stopwords, background_color=None, mode="RGBA", max_words=200,
                           height=400, width=1000).generate(data)
    for k, v in word_cloud.words_.items():
        print(f"{k},{v}")
    with open(save_as, 'w') as f:
        f.write(word_cloud.to_svg(embed_font=True))

    plt.axis("off")
    fig = plt.gcf() #get current figure
    fig.set_size_inches(8, 4)
    plt.tight_layout()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.show()

