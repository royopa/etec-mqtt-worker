import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Mensagem import Mensagem


def on_connect(client, userdata, flags, rc):
    print("Cliente mqtt conectado com código de retorno {0}".format(rc))
    topic_01 = "cli-mlk-002-pub/temperature"
    topic_02 = "cli-mlk-002-pub/humidity"
    client.subscribe(topic_01)
    client.subscribe(topic_02)


def on_subscribe(client, userdata, mid, granted_qos):
    print("  Subscribed on topics")


def on_message(client, userdata, msg):
    #print("  Mensagem recebida")
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    topic = msg.topic

    # formata um dicionário, ara salvar no banco de dados
    item_msg = {
        'created_at': datetime.now(),
        'topic_name': topic,
        'topic_value': float(m_decode)
    }

    print('  ', item_msg)
    insert(item_msg)


def insert(item_msg):
    #print("  Mensagem será inserida na base de dados")
    mensagem = Mensagem(item_msg)

    # create session
    Session = sessionmaker()
    SQLALCHEMY_DATABASE_URI = 'postgresql://sviatuearxzboo:d8d975ade500b9435f8a2a9a7f4a3120cebee4131a76330c36df07b38582d3fd@ec2-52-7-115-250.compute-1.amazonaws.com:5432/d2ga1lst1t68n3'
    SQLALCHEMY_DATABASE_URI = 'postgresql://cbukkihhcpcspc:4932d8a498252be38837c547a2df964e4a60cfbcff6e10d345d6d423a8cee5d2@ec2-23-21-229-200.compute-1.amazonaws.com:5432/d7tpop55rlpik5'
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    Session.configure(bind=engine)
    session = Session()
    session.add(mensagem)
    session.commit()
    session.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.insert = insert


# conecta ao mqtt
host = "mqtt.eclipseprojects.io"
client.connect(host, 1883, 60)

# fica num loop infinito escutando a mensagem
client.loop_forever()
