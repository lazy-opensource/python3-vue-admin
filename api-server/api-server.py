from flask import Flask

from app_router import app_router
from com.lzy.project.admin.helper.db_helper import DbHelper

app = Flask(__name__)
app.register_blueprint(app_router, url_prefix='/api/admin')


DbHelper.init_db(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
