import flask
from flask import Flask,jsonify,json
from flask import request
import json
import requests


#lancer le module Flask à l'execution de l'api
app = flask.Flask(__name__)

#pas d'affichage des details des messages d erreur
app.config["DEBUG"] = False

#decrire l'acces a partir de root/messagesKafka limité a la fonction POST depuis le WEB
@app.route('/CO2extracted', methods=['POST'])
def extract_CO2value():
 bootstrap_servers = 'kafka-service.co2forumm.svc.cluster.local:9092'

#valeurs recuperees de orchestre
 payload = request.data
# payload = payload.decode("utf-8")
 jdata = json.loads(payload)
# discId = jdata["post"]["id"]
# discUser = jdata["post"]["username"]
# discDate = jdata["post"]["updated_at"]

#extraction de CO2 du payload
 try:
     mySbMsg = str(payload)
     mySbMsg = mySbMsg.upper()
     mySbMsg = mySbMsg.replace(" ", "")
     posEq = mySbMsg.index("DIOX")
     posCO2 = mySbMsg.index("CO2")
     lengthEcoCO2 = posCO2-posEq
     ecoCO2Str = mySbMsg[posEq+6:posCO2-1]
     CO2 = ecoCO2Str
#     valeurs = {
 #              "discourse_id" : discId,
  #             "discourse_username" : discUser,
 #              "discourse_heure" : discDate,
  #             "valeurs_CO2" : CO2
#               }
#     valeurs = json.dumps(valeurs)
 #    print(valeurs)
     try:
         type(CO2) is int
         print(CO2)
         return(CO2), 200
     except:
         CO2 = "666"
         print(CO2)
         return(CO2), 406
 except:
     print("payload mal formaté")
     return("bad CO2 value")     # payload), "406"

if __name__ == '__main__':


 app.run(debug=False, port=5004, host='0.0.0.0')
