from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


url = 'sqlite:///competask.db'
if not database_exists(url):
    create_database(url)
engine = create_engine(url, echo=True)
