#!/usr/bin/env python3
import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Mensagem import Mensagem

load_dotenv()  # take environment variables from .env.

# cria lógica para salvar em base de dados apenas quando existe alteração
topic_01_last_value = -99.99
topic_02_last_value = -99.99


def on_connect(client, userdata, flags, rc):
    print("Cliente mqtt conectado com código de retorno {0}".format(rc))
    topic_01 = "cli-mlk-002-pub/temperature"
    topic_02 = "cli-mlk-002-pub/humidity"
    client.subscribe(topic_01)
    client.subscribe(topic_02)


def on_subscribe(client, userdata, mid, granted_qos):
    print("  Subscribed on topics")


def on_message(client, userdata, msg):
    global topic_01_last_value
    global topic_02_last_value

    # pega a mensagem do tópico e faz o decode em utf-8
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    topic = msg.topic

    # formata um dicionário, para salvar no banco de dados
    m_value = float(m_decode)
    item_msg = {
        'created_at': datetime.now(),
        'topic_name': topic,
        'topic_value': m_value
    }

    print('  ', item_msg)

    # se não houve alteração na temperatura, não faz nada
    if topic == "cli-mlk-002-pub/temperature":
        print(
            'Lendo tópico temperatura',
            topic_01_last_value,
            m_value,
            'Inserir na base de dados?',
            topic_01_last_value != m_value
        )
        if topic_01_last_value != m_value:
            topic_01_last_value = m_value
            # insere a informação na tabela do banco de dados
            insert(item_msg)
            return

    # se não houve alteração na umidade, não faz nada
    if topic == "cli-mlk-002-pub/humidity":
        print(
            'Lendo tópico umidade',
            topic_02_last_value,
            m_value,
            'Inserir na base de dados?',
            topic_02_last_value != m_value
        )
        if topic_02_last_value != m_value:
            topic_02_last_value = m_value
            # insere a informação na tabela do banco de dados
            insert(item_msg)
            return


def insert(item_msg):
    mensagem = Mensagem(item_msg)
    # create session
    Session = sessionmaker()
    engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'), echo=False)
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
client.connect(os.getenv('MQTT_HOST'), 1883, 60)

# fica num loop infinito escutando a mensagem
client.loop_forever()
