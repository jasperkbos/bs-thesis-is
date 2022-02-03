# This script makes an entailment decision based on cosine similarity.

import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn import preprocessing
import spacy

nlp = spacy.load('nl_core_news_lg')


def preprocess(doc):
    """
    Removes punctuation and stopwords and lemmatises words.

    :param doc: document string
    :return: the preprocessed document
    """

    nlp.Defaults.stop_words -= {"geen", "niet"}
    doc = nlp(doc)
    cleaned = []
    for token in doc:
        if not token.is_punct and token.lemma_ not in nlp.Defaults.stop_words:
            cleaned.append(token.lemma_)
    return cleaned


def cosim_pred(pair, overlap, return_score=False):
    """
    Makes an entailment decision for a t-h pair based on cosine similarity.

    :param pair: list where [0] is t and [1] is h
    :param overlap: degree of syntactical overlap between t and h
    :param return_score: whether to return the similarity score (bool)
    :return: entailment decision and cosine similarity (if enabled)
    """

    if len(pair[0].split()) > 1 and len(pair[1].split()) > 1:
        thresholds = {'high': 0.63,
                      'med': 0.56,
                      'low': 0.36}

        t_tokens = preprocess(pair[0])
        h_tokens = preprocess(pair[1])

        # Convert e.g. 'volleybal' in t to 'bal' in t if 'bal' in h
        for h_token in h_tokens:
            for i, t_token in enumerate(t_tokens):
                if h_token != t_token and h_token in t_token:
                    t_tokens[i] = h_token

        # Create BoW
        th_tokens = set(t_tokens + h_tokens)
        t_vector = [t_tokens.count(th_token) for th_token in th_tokens]
        h_vector = [h_tokens.count(th_token) for th_token in th_tokens]
        t_vector = preprocessing.normalize([t_vector], norm='l2')
        h_vector = preprocessing.normalize([h_vector], norm='l2')

        # Calculate cosine similarity
        cosim = round(cosine_similarity(t_vector, h_vector).item(), 3)
        if ('geen' in t_tokens or 'niet' in t_tokens) and not \
                ('geen' in h_tokens or 'niet' in h_tokens) or \
                ('geen' in h_tokens or 'niet' in h_tokens) and not \
                ('geen' in t_tokens or 'niet' in t_tokens):
            cosim = 0

        # Make prediction
        threshold = thresholds[overlap]
        if return_score:
            return cosim >= threshold, cosim
        else:
            return cosim >= threshold

    else:
        print('The text and hypothesis must contain at least two tokens.', file=sys.stderr)
