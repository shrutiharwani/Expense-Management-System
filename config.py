import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/yourdb_db'

    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
