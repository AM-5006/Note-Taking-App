class Config:
    SECRET_KEY = '5hj3h421jkj123nv43'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    MONGO_URI = 'mongodb+srv://admin:123@cluster0.3lxbjcp.mongodb.net/test'