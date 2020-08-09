from flask import Flask
from get import get_info
import json 
config = json.loads(open("./important.json").read())
from shindel import ui

app = Flask(__name__)
app.secret_key = config["secretKey"]
app.register_blueprint(get_info)
app.register_blueprint(ui)

if __name__=="__main__":
    app.run()
