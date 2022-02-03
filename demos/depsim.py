# This script makes an entailment decision based on dependency similarity.

import sys
import spacy
import pickle
from collections import defaultdict

nlp = spacy.load('nl_core_news_lg')


def convert_to_dict(pair):
    """
    Adds four key-value pairs to a t-h pair: for both
    documents 1) a lowered and tokenised version and 2) its dependencies.

    :return: the t-h list converted to an appended t-h dict
    """

    t_doc = nlp(pair[0])
    h_doc = nlp(pair[1])

    pair_dict = defaultdict(dict)
    pair_dict['t']['t_tokens'] = [token.text.lower() for sent in t_doc.sents for token in sent]
    pair_dict['h']['h_tokens'] = [token.text.lower() for sent in h_doc.sents for token in sent]
    pair_dict['t']['t_deps'] = [(token.lemma_, token.dep_, token.head.lemma_) for token in t_doc]
    pair_dict['h']['h_deps'] = [(token.lemma_, token.dep_, token.head.lemma_) for token in h_doc]

    return pair_dict


def process_deps(pair_dict):
    """
    Processes the appended inference dict by removing relations that lower accuracy.

    :param pair_dict: t-h pair dict as returned by convert_to_dict
    :return: the processed dependencies for both the text and hypothesis
    """

    # Remove insignificant rels
    insignificant = ('ROOT', 'aux:pass', 'aux', 'punct')
    t_deps = [dep_t for dep_t in pair_dict['t']['t_deps'] if dep_t[1] not in insignificant]
    h_deps = [dep_h for dep_h in pair_dict['h']['h_deps'] if dep_h[1] not in insignificant]

    return t_deps, h_deps


"""
6 paths to compare words. Note that a match is positive if a word in the hypothesis is
a substring of the word in the text (e.g. volleybal = bal).

:param dep_t: one of the dependency triplets in the text (tuple)
:param dep_h: one of the dependency triplets in the hypothesis (tuple)
:return: True if it is a match, False otherwise
"""
def linear_full_overlap(dep_t, dep_h):
    """Checks whether both the head and dependent of the triplets match."""
    return (dep_h[0] in dep_t[0]) and (dep_h[2] in dep_t[2])


def linear_head_overlap(dep_t, dep_h):
    """Checks whether the heads of the triplets match."""
    return dep_h[2] in dep_t[2]


def linear_dependent_overlap(dep_t, dep_h):
    """Checks whether the dependents of the triplets match."""
    return dep_h[0] in dep_t[0]


def cross_full_overlap(dep_t, dep_h):
    """Checks whether the dependent and head in the hypthesis triplet respectively
    matches the head and dependent in the text triplet."""
    return (dep_h[2] in dep_t[0]) and (dep_h[0] in dep_t[2])


def cross_partial_overlap_1(dep_t, dep_h):
    """Checks whether the dependent in the text triplet matches the head in the hypthesis triplet."""
    return dep_h[2] in dep_t[0]


def cross_partial_overlap_2(dep_t, dep_h):
    """Checks whether the head in the text triplet matches the dependent in the hypthesis triplet."""
    return dep_h[0] in dep_t[2]


def apply_rule(t_deps, dep_h, rel_rels, overlap_func):
    """
    Checks whether the relations match and the words match according to the specified overlap path.

    :param t_deps: a list of all dependency triples (tuples) in the text
    :parm dep_h: the current (i.e. to be checked) dependency triple (tuple) in the hypothesis
    :param rel_rels: order independent list of two lists containing related relations
                    (e.g. [['nmod'], ['obj', 'nsubj']])
    :param overlap_func: func of the corresponding overlap pattern
    :return: True if a match is found, False otherwise
    """
    # one direction, e.g. H(Y, 'nmod', X) and and T(X, 'obj', Y)
    if dep_h[1] in rel_rels[0]:
        for dep_t in t_deps:
            if dep_t[1] in rel_rels[1] and overlap_func(dep_t, dep_h):
                return True

    # opposite direction, e.g. H(X, 'obj', Y) and and T(Y, 'nmod', X)
    elif dep_h[1] in rel_rels[1]:
        for dep_t in t_deps:
            if dep_t[1] in rel_rels[0] and overlap_func(dep_t, dep_h):
                return True

    else:
        return False


class customUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "depsim"
        return super().find_class(module, name)


def depsim_pred(pair, overlap, return_score=False):
    """
    Makes an entailment decision for a t-h pair based on dependency similarity.

    :param pair: list where [0] is t and [1] is h
    :param overlap: degree of syntactical overlap between t and h
    :param return_score: whether to return the similarity score (bool)
    :return: entailment decision and dependency similarity (if enabled)
    """

    if len(pair[0].split()) > 1 and len(pair[1].split()) > 1:
        decision_params = {'high': {'threshold': 0.37,
                                    'rules_path': '../data/rules/sicknl.p'},
                           'med': {'threshold': 0.32,
                                   'rules_path': '../data/rules/merged.p'},
                           'low': {'threshold': 0.28,
                                   'rules_path': '../data/rules/rte3.p'}}

        with open(decision_params[overlap]['rules_path'], 'rb') as f:
            unpickler = customUnpickler(f)
            rules = unpickler.load()

        score = 0
        pair_dict = convert_to_dict(pair)
        t_deps, h_deps = process_deps(pair_dict)

        # Apply rules
        for dep_h in h_deps:
            # Apply custom rule 4 (negation)
            if ('geen' in pair_dict['t']['t_tokens'] or 'niet' in pair_dict['t']['t_tokens']) and not \
                    ('geen' in pair_dict['h']['h_tokens'] or 'niet' in pair_dict['h']['h_tokens']) or \
                    ('geen' in pair_dict['h']['h_tokens'] or 'niet' in pair_dict['h']['h_tokens']) and not \
                    ('geen' in pair_dict['t']['t_tokens'] or 'niet' in pair_dict['t']['t_tokens']):
                score = 0
                break

            # Apply custom rule 3 (aan het ..)
            if 'aan het' in ' '.join(pair_dict['t']['t_tokens']) or 'aan het' in ' '.join(pair_dict['h']['h_tokens']):
                if apply_rule(t_deps, dep_h, [['nmod'], ['obj']], cross_full_overlap):
                    score += 1
                    continue

            # Apply manual rules
            for rule in rules:
                if apply_rule(t_deps, dep_h, rule[0], rule[1]):
                    score += rule[2]
                    break

        depsim = round(score / (len(h_deps)), 3)

        # Make prediction
        threshold = decision_params[overlap]['threshold']
        if return_score:
            return depsim >= threshold, depsim
        else:
            return depsim >= threshold

    else:
        print('The text and hypothesis must contain at least two tokens.', file=sys.stderr)
