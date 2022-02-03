
# Running the demos
These demos are able to make an entailment precision given any text-hypothesis (*t-h*) pair. All three explored methods are represented.

## Cosine-based demo
> `cosim_pred(pair, overlap, return_score=False)`

| Parameter | Value |
|--|--|
|pair| ***list of shape ['*t*', '*h*']*** <br /> Input data (*t-h* pair).|
|overlap| ***{'high', 'med', 'low'}*** <br /> Specifies the level of syntactical overlap between *t* and *h*.<br /><br /><ul><li>'high': high overlap; use the threshold developed on SICK-NL</li><li>'med': medium overlap; use the threshold developed on SICK-NL ∪ RTE-3</li><li>'low': low overlap; use the threshold developed on RTE-3</li></ul>
|return_score| ***bool, default=False***<br />Whether to include the cosine similarity in the output. |

### Example

    >>> from cosim import cosim_pred
	>>> t_h = ['De man tekent.', 'Een meisje tekent een man.']
	>>> cosim_pred(t_h, overlap='high', return_score=True)
	(True, 0.816)


## Dependency-based demo
> `depsim_pred(pair, overlap, return_score=False)`

| Parameter | Value |
|--|--|
|pair| ***list of shape ['*t*', '*h*']*** <br /> Input data (*t-h* pair).|
|overlap| ***{'high', 'med', 'low'}*** <br /> Specifies the level of syntactical overlap between *t* and *h*.<br /><br /><ul><li>'high': high overlap; use the threshold and rules developed on SICK-NL</li><li>'med': medium overlap; use the threshold and rules developed on SICK-NL ∪ RTE-3</li><li>'low': low overlap; use the threshold and rules developed on RTE-3</li></ul>
|return_score| ***bool, default=False***<br />Whether to include the dependency similarity in the output. |

### Example

    >>> from depsim import depsim_pred
	>>> t_h = ['De man tekent.', 'Een meisje tekent een man.']
	>>> depsim_pred(t_h, overlap='high', return_score=True)
	(False, 0.0)


## SVM-based demo
> `svm_pred(pair, overlap, return_prob=False)`

| Parameter | Value |
|--|--|
|pair| ***list of shape ['*t*', '*h*']*** <br /> Input data (*t-h* pair).|
|overlap| ***{'high', 'med', 'low'}*** <br /> Specifies the level of syntactical overlap between *t* and *h*.<br /><br /><ul><li>'high': high overlap; use the classifier trained on similarity scores of SICK-NL pairs</li><li>'med': medium overlap; use the classifier trained on similarity scores of both SICK-NL and RTE-3 pairs </li><li>'low': low overlap; use the classifier trained on similarity scores of RTE-3 pairs</li></ul>
|return_prob| ***bool, default=False***<br />Whether to include the probability estimate for the entailment decision in the output. |

### Example

	>>> from svm import svm_pred
	>>> t_h = ['De man tekent.', 'Een meisje tekent een man.']
	>>> svm_pred(t_h, overlap='high', return_prob=True)
	(False, 0.581)
