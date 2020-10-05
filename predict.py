import sys
import json
import os
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from google.protobuf.json_format import MessageToJson
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./ServiceAccountKey.json" )
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'text_snippet': {'content': content, 'mime_type': 'text/plain' }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

if __name__ == '__main__':
  #get sentence from database
  content = "not feeling good today"
  project_id = 'hackutd-1550944892104'
  model_id = 'TCN6183341381162616853'

  result = get_prediction(content, project_id,  model_id)
  print(result)

  jsonStr = MessageToJson(result)
  jsonObj = json.loads(jsonStr)
  
  phrase = content
  emotion_arr = []
  confidence_arr = []

  for i in range(0,3):
    emotion = jsonObj['payload'][i]['displayName']
    print('classification---------',emotion)
    confidence = jsonObj['payload'][i]['classification']['score']
    print('confidence',confidence)
    emotion_arr.append(emotion)
    confidence_arr.append(confidence)
    print('\n')
  
  my_dict_positive = {
    "enjoy_the_moment": 1,
    "achievement": 1,
    "leisure": 1,
    "bonding": 1,
    "nature": 1,
    "exercise": 1,
    "affection": 1,
    "positive": 1,
  }

  my_dict_negative = {
    "hate":2,
    "offensive":2
  }                    

  count = 0
  #get data from database here
  
#  if emotion in my_dict_positive:
#      count = 1
#  elif emotion in my_dict_negative:
#      count = 0
#
#  doc_ref = db.collection(u'users').document(u'i')
#  doc_ref.set({
#              u'emotion':count,
#              u'probability':confidence_arr
#            })

#send count to database and have a count for each journal entry per week








