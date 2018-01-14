from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Web ui for push notification"

if __name__ == '__main__':
    app.run(debug=True)