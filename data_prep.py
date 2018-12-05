import re
from sklearn.model_selection import train_test_split
import os

RAW_DATA = [
    "data/raw/ham",
    "data/raw/spam"
]

PREP_DATA = [
    "data/prep/train.txt",
    "data/prep/test.txt"
]

EMAIL = re.compile(r"([\w0-9_\.-]+)(@)([\d\w\.-]+)(\.)([\w\.]{2,6})")
URL = re.compile(r"https?:\/\/(?!.*:\/\/)\S+")
PHONE = re.compile(r"(09|01[2|6|8|9])+([0-9]{8})\b")
MENTION = re.compile(r"@.+?:")

RE_HTML_TAG = re.compile(r'<[^>]+>')
RE_CLEAR_1 = re.compile("[^a-zA-Z]")
RE_CLEAR_2 = re.compile("__+")
RE_CLEAR_3 = re.compile("\s+")


def read_stop_word(stopwordfile):
    stopwords = set()
    for stopword in open(stopwordfile, encoding='utf8').readlines():
        stopwords.add(stopword.strip().lower())
    return stopwords


class TextPreprocess:
    def __init__(self, stopword):
        if isinstance(stopword, set):
            self.stopword = stopword
        else:
            self.stopword = read_stop_word(stopword)

    def replace_common_token(self, txt):
        txt = re.sub(EMAIL, '<email>', txt)
        txt = re.sub(URL, '<url>', txt)
        txt = re.sub(MENTION, '<user>', txt)
        txt = re.sub(RE_HTML_TAG, ' ', txt)
        return txt

    def remove_emoji(self, txt):
        txt = re.sub(':v', '', txt)
        txt = re.sub(':D', '', txt)
        txt = re.sub(':3', '', txt)
        txt = re.sub(':\(', '', txt)
        txt = re.sub(':\)', '', txt)
        return txt

    def remove_stopword(self, txt):
        words = []
        for word in txt.split():
            if word not in self.stopword:
                words.append(word)
        return ' '.join(words)

    def preprocess(self, txt):
        txt = txt.lower()
        txt = self.replace_common_token(txt)
        txt = re.sub('&.{3,4};', '', txt)
        txt = self.remove_emoji(txt)
        txt = re.sub(RE_CLEAR_1, ' ', txt)
        txt = re.sub(RE_CLEAR_2, ' ', txt)
        txt = re.sub(RE_CLEAR_3, ' ', txt)
        txt = self.remove_stopword(txt)
        return txt.strip()


def file_processing(path, tp):
    X = []
    y = []
    email = open(path, encoding='utf8').read()
    email = tp.preprocess(email)
    if email:
        X.append(email)
    y.extend([0 if 'spam' in path else 1] * len(X))
    return X, y


def save_sklearn_format(X_data, y_data, output_file):
    with open(output_file, 'w', encoding='utf8') as fp:
        for x, y in zip(X_data, y_data):
            fp.write(str(y) + "#" + x + '\n')


if __name__ == '__main__':
    tp = TextPreprocess('data/stopwords.txt')
    Xs = []
    ys = []
    for path in RAW_DATA:
        for file in os.listdir(path):
            X, y = file_processing(os.path.join(path, file), tp)
            Xs.extend(X)
            ys.extend(y)

    X_train, X_test, y_train, y_test = train_test_split(Xs, ys, test_size=0.2)
    save_sklearn_format(X_train, y_train, PREP_DATA[0])
    save_sklearn_format(X_test, y_test, PREP_DATA[1])
