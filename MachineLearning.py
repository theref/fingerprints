import random
import itertools
import numpy as np
import axelrod as axl
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def create_models_for_sample(sample_df):
    """Create Logistic Regression and SVC models for a sample of strategies

    sample_df - a dataframe only for the specific strategies to train model on
    """
    sample_df.drop(['Name_A', 'Name_B'], axis=1, inplace=True)
    sample_equivalent = sample_df['Equivalent']
    sample_df.drop('Equivalent', axis=1, inplace=True)
    log_model = LogisticRegression()
    svc_model = svm.SVC()
    log_model.fit(X=sample_df, y=sample_equivalent)
    svc_model.fit(X=sample_df, y=sample_equivalent)
    return [log_model, svc_model]


def split_dataframe(strategies, original_df):
    """A function that splits a dataframe into two

    strategies - the strategies to split the data frame by
    original_df - the data frame to split
    """
    try:
        strategies = [s.name for s in strategies]
    except:
        strategies = strategies
    samples_df = original_df[original_df['Name_A'].isin(strategies) & original_df['Name_B'].isin(strategies)]
    scoring_df = original_df[~original_df['Name_A'].isin(strategies) | ~original_df['Name_B'].isin(strategies)]
    return samples_df.copy(), scoring_df.copy()


def compute_scores_for_models(models, data):
    """A function for scoring a list of models against some data

    models - a list of models that have been trained
    data - the data to score the models against
    """
    equivalent = data['Equivalent']
    data.drop(['Name_A', 'Name_B', 'Equivalent'], axis=1, inplace=True)
    model_scores = [model.score(X=data, y=equivalent) for model in models]
    model_predictions = [model.predict(X=data) for model in models]
    model_conf_matrix = [confusion_matrix(equivalent, model_pred)  for model_pred in model_predictions]
    model_conf_matrices = [model_cm.astype('float') / sum(sum(model_cm)) for model_cm in model_conf_matrix]
    return model_scores, model_conf_matrices


def score_for_size(size, large_df, strategies):
    """A function to get a score for a sample size

    size - number of strategies to use in sample
    large_df - dataframe to take the samples from
    """
    sample_strategies = random.sample(strategies, size)
    samples_df, scoring_df = split_dataframe(sample_strategies, large_df)
    models = create_models_for_sample(samples_df)
    model_scores, model_conf_matrices = compute_scores_for_models(models, scoring_df)
    return model_scores, model_conf_matrices, models


def compute_sample_scores(sample_size, num, dataframe, strategies):
    """A function to get a number of scores for a sample size

    sample_size - number of strategies to use in sample
    num - number of different samples to score
    dataframe - the dataframe to sample from
    strategies - the strategies to sample from
    """
    sample_scores = []
    for _ in range(num):
        try:
            sample_score, sample_conf_matrix, models = score_for_size(sample_size, dataframe, strategies)
            sample_scores.append(sample_score)
        except:
            pass

    return [0] if not sample_scores else sample_scores


def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues):
    """A function that plots the confusion matrix.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    cmj = cm.astype('float') / sum(sum(cm))

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, "{0} ~ {1:.3f}%".format(cm[i, j], cmj[i, j]),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

