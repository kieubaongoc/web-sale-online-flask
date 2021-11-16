from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from flask_admin import Admin
#from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "\x14\xa2/\x03i\xab\xeb\xc0\x9d\xdc>\r \xd7\xc3\xd6"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:101000@localhost/sale02db?charset=utf8mb4"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

#\db = SQLAlchemy(app=app)

#admin = Admin(app=app, name="Quản lý bán hàng", template_mode="Bootstrap3")

#login = LoginManager(app=app)