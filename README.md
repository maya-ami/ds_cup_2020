## 1st place solution for a [data science championship 2020](https://online.innoagency.ru/datascience/)
Case by University 20.35: building a machine learning model to predict personality traits based on textual data.

Ideas and results are presented in the [slides](https://github.com/maya-ami/project2035/blob/master/%D0%9F%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F.pdf)

Demo of a created NLP service (predicts a personality archetype and recommend relevant courses) - [nlp_serivce/demo.mp4](https://github.com/maya-ami/project2035/blob/master/nlp_service/demo.mp4)


## Solution step-by-step:

- [1 Prepare Data.ipynb](https://github.com/maya-ami/project2035/blob/master/1_Prepare_Data.ipynb)

- [2 Additional Data.ipynb](https://github.com/maya-ami/project2035/blob/master/2_Additional_Data.ipynb)

- [3 Feature Generation.ipynb](https://github.com/maya-ami/project2035/blob/master/3_Feature_Generation.ipynb)

- [4 Analysing N Grams.ipynb](https://github.com/maya-ami/project2035/blob/master/4_Analysing_N_Grams.ipynb)

- [5 Correlations.ipynb](https://github.com/maya-ami/project2035/blob/master/5_Correlations.ipynb)

- Classification model to predict a personality archetype based on texts - [6 Model Classifier.ipynb](https://github.com/maya-ami/project2035/blob/master/6_Model_Classifier.ipynb)

- Regression model to predict the level of students' key motives - [7 Model Regressor.ipynb](https://github.com/maya-ami/project2035/blob/master/7_Model_Regressor.ipynb)

- Feature generation with topic modeling.[Topic Modleing.ipynb](https://github.com/maya-ami/project2035/blob/master/Topic_Modeling.ipynb)

NB: copy dataset from `data` to your working directory or change the paths in the notebooks.
NB: Tested on OS Windows only.

## MLaaS: NLP service

A service predicting a student's archetype and recommending relevant online courses (warning: recommendations are hard-coded! to do: create a proper recommender system for each achetype)

![](nlp_service/schema.PNG)

### Run

```
cd nlp_service
pip install -r requirements.txt
python app.py
```

The prototype is available at http://127.0.0.1:5000/


## Misc

`data` contains intermediate datasets generated at each step (aggreatations, features retrieved from texts, etc).
