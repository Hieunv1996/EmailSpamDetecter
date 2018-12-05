import pickle
from sklearn.metrics import classification_report, confusion_matrix
import traceback
from sklearn.externals import joblib


def load_data(path):
    X = []
    y = []
    for line in open(path, encoding='utf8').readlines():
        y.append(int(line[0]))
        X.append(line[2:])
    return X, y


def load_model(path):
    try:
        model = joblib.load(path)
        print('Load model thành công!')
        return model
    except:
        traceback.print_exc()
        exit(-1)


class Guess(object):
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def detect(self, test_data):
        """
        Get label for each data item in list test_data
        :param test_data: list
        :return: list
        """
        if isinstance(test_data, str):
            test_data = [test_data]
        return self.model.predict(test_data)

    def evaluate(self, test_file):
        X, y = load_data(test_file)
        y_pred = self.model.predict(X)
        return classification_report(y, y_pred)


if __name__ == '__main__':
    g = Guess('model/model.pkl')
    print(g.detect('please subcrice me'))
