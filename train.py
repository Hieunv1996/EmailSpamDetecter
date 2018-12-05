# -*- coding: utf8 -*-
"""
Train and save model
"""
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib


def load_data(path):
    X = []
    y = []
    for line in open(path, encoding='utf8').readlines():
        y.append(int(line[0]))
        X.append(line[2:])
    return X, y


def save_model(model, path):
    try:
        joblib.dump(model, path)
        print('Lưu model thành công!')
    except:
        print('Lưu model không thành công!')


def train(train_path):
    X_train, y_train = load_data(train_path)
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', DecisionTreeClassifier(max_features=2000))])
    text_clf = text_clf.fit(X_train, y_train)
    return text_clf


def test(model, test_file):
    if model is None:
        raise ValueError('Model is None. Call train method')
    X, y = load_data(test_file)
    y_pred = model.predict(X)
    print(confusion_matrix(y, y_pred))
    print(classification_report(y, y_pred))
    return classification_report(y, y_pred)


if __name__ == '__main__':
    cls = train('data/prep/train.txt')
    save_model(cls, 'model/model.pkl')
    test(cls, 'data/prep/test.txt')
