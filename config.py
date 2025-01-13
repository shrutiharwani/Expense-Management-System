import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:shru6@localhost:5432/cookie_db'

    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_TRACK_MODIFICATIONS = False