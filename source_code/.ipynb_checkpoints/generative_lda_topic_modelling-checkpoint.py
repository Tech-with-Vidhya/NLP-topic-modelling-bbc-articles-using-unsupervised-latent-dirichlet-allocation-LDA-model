# -*- coding: utf-8 -*-
"""Generative_LDA_Topic_Modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LnP4qXscpKkd0c3prJT24ny7VR5cXYxL

# NLP TOPIC MODELLING OF BBC ARTICLES - USING UNSUPERVISED LATENT DIRICHLET ALLOCATION (LDA) GENERATIVE MODEL

## Importing the Python Pandas Library
"""

import pandas as pd

print("Import Completed")

# Mounting the Google Drive to Import the Data 

from google.colab import drive
drive.mount('/content/drive')

"""## Loading the BBC Articles CSV File Data"""

data = pd.read_csv("/content/drive/MyDrive/~~~VP_Data_Science/DS_Real_Time_Projects/NLP_Topic_Modelling_of_BBC_Articles_using_Unsupervised_Latent Dirichlet Allocation_LDA_Model/data/bbc_articles_2018.csv")

print("Data Import Completed")

"""## Data Exploration"""

# Verifying the shape of the Data

data.shape

# Verifying the First 5 Rows of Data Instances

data.head()

# Verifying the Last 5 Rows of Data Instances

data.tail()

# Displaying the Contents of the First Article

data.iloc[0][0]

"""### As we can see from the above results; there are a total of 309 BBC articles with 2 attributes namely 'articles' containing the article content in the text format and 'lang' that denotes the language of the article.

## Data Cleaning
"""

# Removal of the Blank Articles

data = data.dropna().reset_index(drop=True)

print("Execution Completed")

# Re-verifying the shape of the Data after cleaning the articles with missing information

data.shape

"""### As we can see from the above results; there is only one row of article data with missing information.

## Retaining only the English articles for our modellling purposes
"""

from langdetect import detect
from tqdm import tqdm_notebook

tqdm_notebook().pandas()

print("Execution Completed")

data['lang'] = data.articles.progress_map(detect)

# Verifying the First 5 Rows of Data Instances
data.head()

# Displaying the Count of the Articles Based on the Individual Languages

data.lang.value_counts()

# Keeping Only the English Language Articles

data_english = data.loc[data.lang=='en']

data_english

"""## Tokenisation

### Splitting Each Article in to Sentences
"""

# Importing the Python's Sentence Tokenizer Function

from nltk.tokenize import sent_tokenize

print("Import Completed")

# Importing the nltk library and Downloading the 'punkt' package

import nltk
nltk.download('punkt')

# Tokenising the Articles and Displaying the First 5 Sentences

data_english['sentences'] = data_english.articles.progress_map(sent_tokenize)

# Printing the First 5 Sentences of the List Article
data_english['sentences'].head(1).tolist()[0][:5]

# Viewing the Updated DataFrame after Tokenising the Articles into Sentences

data_english

"""### Splitting Each Sentences in to Individual Words"""

# Importing the Python's Words Tokenizer Function

from nltk.tokenize import word_tokenize

print("Import Completed")

# Tokenising the Sentences and Displaying the Words of the First 5 Sentences

data_english['tokens_sentences'] = data_english['sentences'].progress_map(lambda sentences: [word_tokenize(sentence) for sentence in sentences])

# Printing the Words of the First 5 Sentences
print(data_english['tokens_sentences'].head(1).tolist()[0][:5])

# Viewing the Updated DataFrame after Tokenising the Sentences into Words

data_english

"""## Lemmatizing With POS Tagging"""

# Importing the pos tag function

from nltk import pos_tag

print("Execution Completed")

# Downloading the 'averaged_perceptron_tagger' Package from the nltk Library for POS Tagging

import nltk
nltk.download('averaged_perceptron_tagger')

# Executing the Pos Tagging for all the Articles Words

data_english['POS_tokens'] = data_english['tokens_sentences'].progress_map(lambda tokens_sentences: [pos_tag(tokens) for tokens in tokens_sentences])

# Printing the POS Tagging Mapping Results for the 
print(data_english['POS_tokens'].head(1).tolist()[0][:5])

# Defining the Lemmatization Rules


# Inspired from the Internet Source - https://stackoverflow.com/a/15590384

from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

print("Execution Completed")

# Downloading the 'wordnet' Package from the nltk Library

import nltk
nltk.download('wordnet')

# Lemmatizing Each Word with its POS Tag, in Each Sentence

data_english['tokens_sentences_lemmatized'] = data_english['POS_tokens'].progress_map(
    lambda list_tokens_POS: [
        [
            lemmatizer.lemmatize(el[0], get_wordnet_pos(el[1])) 
            if get_wordnet_pos(el[1]) != '' else el[0] for el in tokens_POS
        ] 
        for tokens_POS in list_tokens_POS
    ]
)

print("Execution Completed")

# Viewing the Updated DataFrame after Lemmatization

data_english

# Viewing the Lemmatized Data for the First 5 Sentences

data_english['tokens_sentences_lemmatized'].head(1).tolist()[0][:5]

"""## Re-grouping of the Tokens and Removal of the Stop Words"""

# Downloading the Stop Words Package from the nltk library

import nltk
nltk.download('stopwords')

print("Execution Completed")

from nltk.corpus import stopwords

stopwords_verbs = ['say', 'get', 'go', 'know', 'may', 'need', 'like', 'make', 'see', 'want', 'come', 'take', 'use', 'would', 'can']
stopwords_other = ['one', 'mr', 'bbc', 'image', 'getty', 'de', 'en', 'caption', 'also', 'copyright', 'something']

my_stopwords = stopwords.words('english') + stopwords_verbs + stopwords_other

print(my_stopwords)

# Flattening The List of Sentences of Tokens into a List of Tokens

from itertools import chain

data_english['tokens'] = data_english['tokens_sentences_lemmatized'].map(lambda sentences: list(chain.from_iterable(sentences)))
data_english['tokens'] = data_english['tokens'].map(lambda tokens: [token.lower() for token in tokens if token.isalpha() 
                                                    and token.lower() not in my_stopwords and len(token)>1])

print("Execution Completed")

# Viewing the Updated DataFrame after Flattening

data_english

# Displaying the Tokens Column of the DataFrame after Flattening

data_english['tokens'].head(1).tolist()[0][:30]

"""## Unsupervised Latent Dirichlet Allocation (LDA) Generative Statistical Model

## LDA - Data Preparartion

### Preparing Bi-Grams and Tri-Grams
"""

from gensim.models import Phrases

print("Import Completed")

tokens = data_english['tokens'].tolist()
bigram_model = Phrases(tokens)
trigram_model = Phrases(bigram_model[tokens], min_count=1)
tokens = list(trigram_model[bigram_model[tokens]])

tokens

"""### Preparing Objects for the LDA Gensim Implementation"""

from gensim import corpora

print("Execution Completed")

dictionary_LDA = corpora.Dictionary(tokens)
dictionary_LDA.filter_extremes(no_below=3)
corpus = [dictionary_LDA.doc2bow(tok) for tok in tokens]

corpus

"""## Execution of the LDA Model"""

from gensim import models
import numpy as np

print("Import Completed")

# Commented out IPython magic to ensure Python compatibility.
np.random.seed(123456)
num_topics = 20
# %time lda_model = models.LdaModel(corpus, num_topics=num_topics, \
                                  id2word=dictionary_LDA, \
                                  passes=4, alpha=[0.01]*num_topics, \
                                  eta=[0.01]*len(dictionary_LDA.keys()))

print("Execution Completed")

"""## Exploration of the LDA Model Results

### Review of the Topics
"""

for i,topic in lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=20):
    print(str(i)+": "+ topic)
    print()

print("Execution Completed")

"""### Allocation of the Topics to the Documents"""

print(data_english.articles.loc[0][:500])

lda_model[corpus[0]]

"""## Prediction of the Topics on the Unseen Documents/Articles"""

test_document = '''Eric Tucker, a 35-year-old co-founder of a marketing company in Austin, Tex., had just about 40 Twitter followers. But his recent tweet about paid protesters being bused to demonstrations against President-elect Donald J. Trump fueled a nationwide conspiracy theory ??? one that Mr. Trump joined in promoting. 
Mr. Tucker's post was shared at least 16,000 times on Twitter and more than 350,000 times on Facebook. The problem is that Mr. Tucker got it wrong. There were no such buses packed with paid protesters.
But that didn't matter.
While some fake news is produced purposefully by teenagers in the Balkans or entrepreneurs in the United States seeking to make money from advertising, false information can also arise from misinformed social media posts by regular people that are seized on and spread through a hyperpartisan blogosphere.
Here, The New York Times deconstructs how Mr. Tucker???s now-deleted declaration on Twitter the night after the election turned into a fake-news phenomenon. It is an example of how, in an ever-connected world where speed often takes precedence over truth, an observation by a private citizen can quickly become a talking point, even as it is being proved false.'''

tokens = word_tokenize(test_document)
topics = lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=20)
pd.DataFrame([(el[0], round(el[1],2), topics[el[0]][1]) for el in lda_model[dictionary_LDA.doc2bow(tokens)]], columns=['topic #', 'weight', 'words in topic'])

"""## Advanced Exploration of the LDA Model Results

## Allocation of the Topics in all the Documents/Articles
"""

topics = [lda_model[corpus[i]] for i in range(len(data_english))]

topics

# Custom Function to Allocate Topics to all the Documents/Articles

def topics_document_to_dataframe(topics_document, num_topics):
    res = pd.DataFrame(columns=range(num_topics))
    for topic_weight in topics_document:
        res.loc[0, topic_weight[0]] = topic_weight[1]
    return res

topics_document_to_dataframe([(9, 0.03853655432967504), (15, 0.09130117862212643), (18, 0.8692868808484044)], 20)

# Similar to the TF-IDF Approach; Creating a Matrix of Topic Weighting, with Documents/Articles as Rows and Topics as Columns

document_topic = \
pd.concat([topics_document_to_dataframe(topics_document, num_topics=num_topics) for topics_document in topics]) \
  .reset_index(drop=True).fillna(0)

print("Execution Completed")

# Viewing the First 5 Instances of the Document Topics

document_topic.head()

# Sorting and Displaying the List of 20 Documents/Articles that belong to the Topic 8

document_topic.sort_values(8, ascending=False)[8].head(20)

# Sorting and Displaying the List of 20 Documents/Articles that belong to the Topic 15

document_topic.sort_values(15, ascending=False)[15].head(20)

# Displaying the 100th Document/Article to Show the First 1000 Words

print(data_english.articles.loc[99][:1000])

"""## Visualising the Distribution of the Topics in all the Documents/Articles"""

# Commented out IPython magic to ensure Python compatibility.
# Heat Map

# %matplotlib inline
import seaborn as sns
sns.set(rc={'figure.figsize':(10,20)})
sns.heatmap(document_topic.loc[document_topic.idxmax(axis=1).sort_values().index])

# Bar Chart

sns.set(rc={'figure.figsize':(10,5)})
document_topic.idxmax(axis=1).value_counts().plot.bar(color='lightblue')

"""## Visualising the Topics

### Reference: https://cran.r-project.org/web/packages/LDAvis/vignettes/details.pdf

### Here is a Short Legend to Explain the Visualisation:
> ### Size of The Bubble: Proportional to the Proportions of the Topics across the N Total Tokens in the Corpus
> ### Red Bars: Estimated Number of Times a Given Term was Generated by a Given Topic
> ### Blue Bars: Overall Fequency of Each Term in the Corpus
> ### Relevance of the Words is Computed with a Parameter Lambda
> ### Lambda Optimal Value is ~0.6 
(https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf)
"""

# Commented out IPython magic to ensure Python compatibility.
'''

# Visualisation the Topics as per the Above Details

# %matplotlib inline
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

pyLDAvis.enable_notebook()

# Feeding the LDA Model into pyLDAvis Instance

vis_data = gensimvis.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary_LDA)
#vis_data = gensimvis.prepare(lda_model, corpus, dictionary_LDA)

pyLDAvis.show(vis_data)

#vis_data

print("Execution Completed")

'''