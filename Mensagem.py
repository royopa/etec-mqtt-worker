import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from Base import Base


class Mensagem(Base):
    __tablename__ = 'mensagem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_name = Column(String(255), nullable=False)
    topic_value = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, msg):
        self.topic_name = msg.get('topic_name')
        self.topic_value = msg.get('topic_value')
        self.created_at = msg.get('created_at')

    def get_id(self):
        return self.id

    def get_topic_name(self):
        return self.topic_name

    def get_topic_value(self):
        return self.topic_value

    def get_created_at(self):
        return self.created_at

    def __repr__(self):
        return f'{self.id}, {self.topic_name}, {self.topic_value}, {self.created_at}'
