# create a word cloud using bib file
from tools.bib_wordcloud import generate_word_cloud, filter_papers

generate_word_cloud(bib_file_path='MyCollection.bib',
                    ignore_words=[
                        'NLP'
                    ],
                    save_as='industry_wordcloud.svg'
                    )

# method to filter paper based on the words either in title or abstract
filter_papers(bib_file_path='MyCollection.bib',
              have_words=[
                  ' enemies | assassination | tactic ',
              ]
              )
