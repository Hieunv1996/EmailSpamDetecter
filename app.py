from flask import Flask, request
from train import train, test, save_model

app = Flask(__name__)


@app.route('/')
def hello():
    return 'PONG'


model = None


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
        rs = model.predict([email])[0]
        if rs == 0:
            return 'Là email SPAM'
        else:
            return 'Không phải email SPAM'


app.run('0.0.0.0', 1234, debug=True)
