# This script makes an entailment decision based on linear SVMs trained on both the
# cosine and dependency similarities on SICK-NL, RTE-3 or their union.

import sys
from joblib import load
from cosim import cosim_pred
from depsim import depsim_pred


def svm_pred(pair, overlap, return_prob=False):
    """
    Makes an entailment decision for a t-h pair based on both cosine and dependency similarity.

    :param pair: list where [0] is t and [1] is h
    :param overlap: degree of syntactical overlap between t and h
    :param return_prob: whether to return the probability score for the predicted label (bool)
    :return: entailment decision and probability score (if enabled)
    """

    if len(pair[0].split()) > 1 and len(pair[1].split()) > 1:
        models = {'high': '../code/models/clf_sicknl.joblib',
                  'med': '../code/models/clf_merged.joblib',
                  'low': '../code/models/clf_rte3.joblib'}
        clf = load(models[overlap])
        cosim = cosim_pred(pair, overlap, return_score=True)[1]
        depsim = depsim_pred(pair, overlap, return_score=True)[1]
        vector = [[cosim, depsim]]

        # Make prediction
        if return_prob:
            if clf.predict(vector)[0] == 1:
                return clf.predict(vector)[0] == 1, round(clf.predict_proba(vector)[0][1], 3)
            else:
                return clf.predict(vector)[0] == 1, round(clf.predict_proba(vector)[0][0], 3)
        else:
            return clf.predict(vector)[0] == 1

    else:
        print('The text and hypothesis must contain at least two tokens.', file=sys.stderr)
