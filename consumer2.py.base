from kafka import KafkaConsumer
import requests
import flask
from flask import Flask,jsonify,json


consumer=KafkaConsumer(
    'topicCO2Extracted',
    bootstrap_servers=['kafka-service.co2forumm.svc.cluster.local:9092'],
    group_id='grouptest',
#    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=False

)
#lancer le module Flask    l'execution de l'api
app = flask.Flask(__name__)
#pas d'affichage des details des messages d erreur
app.config["DEBUG"] = False
#decrire l'acces a partir de root/messahesKafka limit   a la fonction POST depuis le WEB
@app.route('/Consumer2',  methods=['POST'])


def consume_messages():
    consumer.commit()
    while True:
        message_batch = consumer.poll()
        for msg in consumer:
            CO2 = msg.value
            print(CO2)
            headers = {"HTTP_HOST": "MyVeryOwnHost", "User-Agent": "topicCO2Kafka" }
            urlConsum = 'http://orchsvc.co2forumm.svc.cluster.local:5000/orchestrator'
            payCO2 = requests.post(url = urlConsum, data = CO2, headers = headers)

if __name__ == '__main__':
    consume_messages()
app.run(debug=False, port=5004, host='0.0.0.0')
