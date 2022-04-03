# NER and topic-modeling methods for strategic decision-making in Urban Air Mobility
## Capstone Project
Repository for all capstone project-related code.

## Table of contents
1. [NER](#ner)
2. [Topic-modeling](#topic-models)
3. [Visualizations](#visualizations)

## NER <a name="ner"></a>
All NER-related work is in the `ner` folder. There, you can test the fine-tuned SpaCy NER component by opening `trained_nlp_examples.ipynb`.

To check visualizations and compare SpaCy's pretrained pipeline to the custom NER component, open `ner-data-analysis.ipynb`. 

The `save_data.py` file takes two different datasets in Python files, `valid_data.py` and `annotated_data.py` as validation and training sets, respectively. The file saves both datasets to disk as `.spacy` data files. 

Within the `models` directory, the custom `ner` and `tok2vec` pipeline components are saved within `output`. The aforementioned Jupyter notebooks load those models to use the components.

To setup the `config.cfg` file for training the SpaCy components and run the training cycle using the training and validation datasets saved on disk, run the `train_save_model.sh` script.

## Topic-modeling <a name="topic-models"></a>
All topic-modeling-related work is inside the `topic-modeling` folder. Visualizations are found within the Jupyter notebooks themselves, and saved within the `vis` subdirectory inside the topic-modeling folder.

As suggested by the names of the notebooks, different libraries are used in each. `gensim-models.ipynb` uses the Gensim library, which has the broadest functionality dedicated to topic-modeling of the packages used, since it is dedicated to the task. `topic-modeling-LDA.ipynb` implements LDA using scikit-learn.

## Visualizations <a name="visualizations"></a>
Visualizations in the form of .html and .png files can be found in the `vis` subdirectories within each tasks folders. 