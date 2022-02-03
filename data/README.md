


# Directory overview
The developed systems are based on two corpora: [SICK-NL](https://github.com/gijswijnholds/sick_nl) (Wijnholds and Moortgat, 2021) and RTE-3 (Giampiccolo et al.,  2007) translated to Dutch as part of the [Parallel Meaning Bank](https://pmb.let.rug.nl/) (Abzianidze et al., 2017).

    data        
    ├── rte3
    │   ├── rte3.txt 
    │   ├── preprocess.ipynb
    │   # Output of preprocess.ipynb:
    │   ├── dev.p
    │   ├── train.p
    │   └── test.p
    ├── rules  # As developed by dep_sys.ipynb
    │   ├── merged.p 
    │   ├── rte3.p
    │   └── sicknl.p
    └── sicknl
        ├── sicknl.tsv
        ├── preprocess.ipynb
        # Output of preprocess.ipynb:
        ├── dev.p
        ├── train.p
        └── test.p

# References
Lasha Abzianidze, Johannes Bjerva, Kilian Evang, Hessel Haagsma, Rik van Noord, Pierre  Ludmann,  Duc-Duy  Nguyen,  and  Johan  Bos.  2017.  [The  Parallel  Meaning  Bank:  Towards  a  multilingual  corpus  of  translations  annotated  with  compositional meaning representations](https://aclanthology.org/E17-2039). In *Proceedings of the  15th Conference of the European  Chapter of the Association for Computational Linguistics: Volume  2, Short Papers*, pages  242–247, Valencia, Spain. Association for Computational Linguistics.

Danilo Giampiccolo, Bernardo Magnini, Ido Dagan, and Bill Dolan. 2007. [The third PASCAL recognizing textual entailment challenge](https://aclanthology.org/W07-1401). In *Proceedings of the 18 bibliography 19 ACL-PASCAL Workshop on Textual Entailment and Paraphrasing*, pages 1–9, Prague, Czech Republic. Association for Computational Linguistics.

Gijs Wijnholds and Michael Moortgat. 2021. [SICK-NL: A dataset for Dutch natural language inference](https://doi.org/10.18653/v1/2021.eacl-main.126). In *Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume*, pages 1474–1479. Association for Computational Linguistics.
