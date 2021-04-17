import os
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import (Column, DateTime, Float, Integer, MetaData, String,
                        Table, create_engine)

load_dotenv(find_dotenv())

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'), echo=False)

# Create a metadata instance
metadata = MetaData(engine)

# Declare a table
table = Table('mensagem', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('topic_name', String(255), nullable=False),
              Column('topic_value', Float, nullable=False),
              Column('created_at', DateTime, nullable=False)
              )

# Create all tables
metadata.create_all()
for _t in metadata.tables:
    print("Table: ", _t)
