from flask import Flask, request
app = Flask(__name__)

@app.route('/hello',methods=['POST'])
def hello_world():
    print(request.__dict__)
    data = request.get_json(force=True)
    print(data["foo"])
    return 'Hello World'


if __name__ == '__main__':
   app.run()