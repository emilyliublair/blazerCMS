from flask import Flask
from get import get_info

app = Flask(__name__)
app.register_blueprint(get_info)

if __name__=="__main__":
    app.run()
