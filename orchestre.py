import flask
from flask import Flask,jsonify,json
from flask import request
import json
import requests
import hashlib


#lancer le module Flask    l'execution de l'api
app = flask.Flask(__name__)

#affichage des details des messages d erreur
app.config["DEBUG"] = True

#decrire l'acces a partir de root/messahesKafka limit   a la fonction POST depuis le WEB
@app.route('/orchestrator', methods=['POST'])


def post_orchestrator():

#recuperation des metadonn  es et payload re  us de la requ  te appelante
 payload = request.data
 contentType = request.headers.get('Content-Type')
 source = request.headers.get('User-Agent')
 topicNameDiscMessage = "topicDiscMessage"
 topicNamePending = "topicATraiter"
 topicNameCo2Extracted = "topicCO2Extracted"
 print("origin = ", source)

# allowed format for incoming payload
 importables = ['application/json', 'text/plain', 'image/jpeg']

#envoi le contenu du forum vers producer
 if "discourse" in source and contentType in importables:
  topicName = topicNameDiscMessage
  headers = {"HTTP_HOST": "MyVeryOwnHost", "topicName": topicName, "contentType": contentType }
  url = 'http://prodsvc.co2forumm.svc.cluster.local:5001/messageBroker'
  postObject = requests.post(url = url, data = payload, headers = headers)
#  print("payload, topic et contentType venu de consumer : ", payload, topicName, contentType)
  return("Message from forum sent to producer to kafka topic xxx ")

#topic venant de consumer
 elif "topicDiscMessage" in source:
  #1- poster vers CO2 extracted
  payload = request.data
#  payload = payload.decode("utf-8")
  print("payload decode : ", payload)
  #header    passer pour co2 extrated qui n' attend pas de topic name !
  headers = {"HTTP_HOST": "postMessageToExtractValue" }
  urlCO2Ext = 'http://co2xdsvc.co2forumm.svc.cluster.local:5004/CO2extracted'
  CO2ExtObject = requests.post(url = urlCO2Ext, data = payload, headers = headers)
  CO2 = str(CO2ExtObject.text)
  print(CO2)
  #return("block 2 ok")
  #2- poster vers producer et pour post sur kafka>topicCO2Extracted
  headers = {"HTTP_HOST": "MyVeryOwnHost", "topicName": topicNameCo2Extracted, "contentType": 'text/plain' }
  urlProduc = 'http://prodsvc.co2forumm.svc.cluster.local:5001/messageBroker'
  COProd = requests.post(url = urlProduc, data = CO2, headers = headers)
  print("valeur traitee de CO2 envoyee de orchestre vers producer : ", CO2)
  return("CO2")

 elif "topicCO2Kafka" in source:
  payload = request.data
  print("payload de consumer2 ", payload)
##  headers = {"HTTP_HOST": "postMessageToExtractValue" }
##  urlCO2Json = 'http://vmkafka3.uksouth.cloudapp.azure.com:5005/CO2Json2Blockchain'
##  CO2Json4Blockchain = requests.post(url = urlCO2Json, data = payload, headers = headers)
##  CO2 = CO2Json4Blockchain.text
##  print("j'ai recupere CO2 pour blockchain", CO2)
##  return("Valeur de CO2 a envoyer pour blockchain: ", CO2)

 else:
  print("C parti vers l'etoile noire")
  return("boucle interrompue entre Producer et Kafka alors, Bye!")

if __name__ == '__main__':
 app.run(debug=False,port=5000, host='0.0.0.0')
