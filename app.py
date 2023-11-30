from flask import Flask, render_template, redirect, url_for, session, request, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from database.database import init_app as init_mongo
from apps.User.views import user_routes
from apps.Notes.views import notes_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.DevelopmentConfig')
    init_mongo(app)
    
    app.register_blueprint(user_routes)
    app.register_blueprint(notes_routes)

    @app.route('/loginpage')
    def login_page():
        message = request.args.get('message', default=None)
        return render_template('login.html', message=message)
    
    @app.route('/')
    def index():
        user_logged_in = session.get('user_logged_in', False)
        user_details = session.get('user_details', {})
        user_token = session.get('token', None)
        return render_template('index.html', user_logged_in=user_logged_in, user_details=user_details, user_token=user_token)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))
    
    return app


app = create_app()
# if __name__ == "__main__":
#     app = create_app()
#     app.run()

