from flask import Flask
from flask_pymongo import PyMongo
from database.database import init_app as init_mongo
from apps.User.views import user_routes
from apps.Notes.views import notes_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    init_mongo(app)
    
    app.register_blueprint(user_routes)
    app.register_blueprint(notes_routes)
    
    return app

app = create_app()
# if __name__ == "__main__":
#     app = create_app()
#     app.run()

