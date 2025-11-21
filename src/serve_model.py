"""
Flask API of the SMS Spam detection model.
"""
import os
import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd

from text_preprocessing import prepare, _extract_message_len, _text_process

app = Flask(__name__)
swagger = Swagger(app)

# F10 Implementation
MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

print(f"Loading model from: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)   # we load this once at start up


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether an SMS is Spam.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                sms:
                    type: string
                    example: This is an example of an SMS.
    responses:
      200:
        description: "The result of the classification: 'spam' or 'ham'."
    """
    input_data = request.get_json()
    sms = input_data.get('sms')

    processed_sms = prepare(sms)
    prediction = model.predict(processed_sms)[0]

    res = {
        "result": prediction,
        "classifier": "decision tree",
        "sms": sms
    }
    print(res)
    return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
