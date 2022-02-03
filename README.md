# _Recognising Textual Entailment for Dutch using Dependency Analysis_
This repository is part of my bachelor’s thesis, which concludes my Bachelor’s degree programme in [Information Science](https://www.rug.nl/bachelors/information-science/) at the University of Groningen. 

It provides details on the [`data`](https://github.com/jasperkbos/bs-thesis-is/tree/main/data) preprocessing and includes the [`code`](https://github.com/jasperkbos/bs-thesis-is/tree/main/code) used for developing or training and evaluating the cosine-based, dependency-based and hybrid systems. Additionally, it offers interactive [`demos`](https://github.com/jasperkbos/bs-thesis-is/tree/main/demos). 

Further details are presented in the respective directories.

# Installation
To replicate the systems or run the demos, please follow the steps below.

## 1. Clone this repository
```
git clone https://github.com/jasperkbos/bs-thesis-is
```
## 2. Install dependencies
The systems support Python 3.7 or later. To install all required dependencies, simply run:
```
cd bs-thesis-is
pip3 install -r requirements.txt
```

## 3. Download spaCy’s trained pipeline

To download the Dutch trained pipeline package, simply run:
```
python3 -m spacy download nl_core_news_lg
```
