# Directory overview
This directory contains the three Jupyter Notebooks used for developing or training the different systems.

    code        
    ├── models                  # The 3 SVMs as trained in hybrid_sys.ipynb
    │   ├── clf_merged.joblib
    │   ├── clf_rte3.joblib
    │   └── clf_sicknl.joblib
    ├── cos_sys.ipynb	    # Cosine-based systems
    ├── dep_sys.ipynb	    # Dependency-based systems
    └── hybrid_sys.ipynb	    # Hybrid systems

They rely on preprocessed [`data`](https://github.com/jasperkbos/bs-thesis-is/tree/main/data).
