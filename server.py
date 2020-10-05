from flask_cors import CORS
from flask import Flask, request, jsonify
from google.cloud.automl_v1beta1 import PredictionServiceClient
import firebase_admin
from firebase_admin import firestore, credentials

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

"""get_prediction returns the highest prediction result from AutoML
in the form of a tuple: (sentiment name, prediction score)
"""

firebase_admin.initialize_app(credential=credentials.Certificate("./firebase.service.json"))
db = firestore.client()

def get_prediction(phrase):
  # Create the client from the AutoML service account
  client = PredictionServiceClient.from_service_account_file("./hackutd-1550944892104-1ba910d00c8f.json")
  path = client.model_path("hackutd-1550944892104", "us-central1", "TCN6183341381162616853")

  # Retrieve the prediction data
  payload = {"text_snippet": {"content": phrase, "mime_type": "text/plain"}}
  request = client.predict(path, payload)

  # Extract the highest prediction result
  result = request.payload[0]
  data = (result.display_name, result.classification.score)

  return data

""" [POST] /sentiments
Passes the given phrase to AutoML to generate
a sentiment value, then stores the result in
Cloud Firestore linked to the given user
"""

@app.route("/sentiments", methods=["POST"])
def add_sentiment():
  # Retrieve the necessary data from the request
  phrase = request.json.get("phrase", "")  # The user's inputted phrase
  user = request.json.get("user", "")      # The user's ID

  response = get_prediction(phrase)
  data = {
    "name": response[0],
    "score": response[1],
  }

  # Store in Firebase
  db.collection("sentiments").add(data)

	return jsonify({
		"name": response[0],
		"score": response[1],
	})

# Run the flask app
if __name__ == "__main__":
  app.run(debug=True)
