from flask import Flask, request
import modifyDB as util

app = Flask(__name__)

@app.route("/")
def index():
    return ("Hello World")

@app.route("/addEntry", methods=['POST', 'GET'])
def addEntry():
    entry = ""
    if request.method == 'POST':
        entry = request.form['entry']
        print(entry)
    else:
        entry = request.args.get('entry')
        util.test()
        print(entry)
    return "New Entry!"

if __name__ == '__main__':
    app.run(port="1337", debug=True)