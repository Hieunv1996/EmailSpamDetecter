from flask import Flask, request
from train import train, test, save_model
import re
from data_prep import TextPreprocess
app = Flask(__name__)


def is_vietnam_email(email):
    pats = 'á|à|ả|ã|ạ|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ|ó|ò|ỏ|õ|ọ|ơ|ớ|ờ|ở|ỡ|ợ|ô|ố|ồ|ổ|ỗ|ộ|é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ|ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự|í|ì|ỉ|ĩ|ị|ý|ỳ|ỷ|ỹ|ỵ|đ'
    return re.findall(pats, email)

@app.route('/')
def hello():
    return 'PONG'


model = train('data/prep/train.txt')


@app.route('/train', methods=['POST'])
def train_api():
    train_path = request.form['train_path']
    global model
    model = train(train_path)
    return 'Huấn luyện thành công!'


@app.route('/test', methods=['POST'])
def test_api():
    test_path = request.form['test_path']
    if model is None:
        return 'Bạn chưa huấn luyện mô hình!'
    else:
        return test(model, test_path)


@app.route('/check', methods=['POST'])
def check():
    email = request.form['email']
    if model is None:
        return 'Bạn chưa huấn luyện mô hình!'
    else:
        if is_vietnam_email(email):
            return 'Chương trình chưa hỗ trợ tiếng Việt'
        email = TextPreprocess('data/stopwords.txt').preprocess(email)
        if not email:
            return 'Không có nội dung email để dự đoán'
        rs = model.predict([email])[0]
        if rs == 0:
            return 'Là email SPAM'
        else:
            return 'Không phải email SPAM'

if __name__ == '__main__':
    app.run('0.0.0.0', 1234, debug=True)
