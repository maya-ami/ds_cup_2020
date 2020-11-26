from subprocess import PIPE, Popen
from flask import Flask, request, redirect, render_template
from ml import predict, recommend_course

app=Flask(__name__)


@app.route('/',methods=['GET','POST'])
def start():
    return render_template('start.html')

@app.route('/predict_type',methods=['GET','POST'])
def predict_type():
    if request.method == 'POST':
        text = request.form['message']
        if len(text):
            types = predict(text)
            courses = recommend_course(types)
    return render_template('predict.html', types=types, courses=courses)

@app.errorhandler(500)
def internalServerError(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def internalServerError(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
