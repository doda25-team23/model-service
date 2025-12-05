"""
Flask API of the SMS Spam detection model.
"""
import os
import joblib
import time
from flask import Flask, jsonify, request, Response
from flasgger import Swagger
import pandas as pd

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

import pandas as pd

from text_preprocessing import prepare, _extract_message_len, _text_process

app = Flask(__name__)
swagger = Swagger(app)

# Prometheus metrics
PREDICTIONS_TOTAL = Counter(
    "app_predictions_total",
    "Total number of prediction requests",
    ["source", "status"],
)

PREDICTION_LATENCY = Histogram(
    "app_prediction_latency_seconds",
    "Prediction latency in seconds",
    ["source"],
    buckets=[0.1, 0.3, 0.5, 1.0, 2.0, 5.0],
)

ACTIVE_USERS = Gauge(
    "app_active_users",
    "Approximate number of active users",
    ["page"],
)

# F10 Implementation
MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

print(f"Loading model from: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)   # we load this once at start up

@app.route("/metrics")
def metrics():
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

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
    start = time.time()
    ACTIVE_USERS.labels(page="api").inc()
    try:
        # existing code: get sms from request
        body = request.get_json()
        sms = body.get("sms") if body else ""

        processed_sms = prepare(sms)
        prediction = model.predict(processed_sms)[0]

        res = {
            "result": prediction,
            "classifier": "decision tree",
            "sms": sms
        }

        # update metrics
        duration = time.time() - start
        PREDICTIONS_TOTAL.labels(source="backend", status="success").inc()
        PREDICTION_LATENCY.labels(source="backend").observe(duration)

        print(res)
        return jsonify(res)
    except Exception as e:
        duration = time.time() - start
        PREDICTIONS_TOTAL.labels(source="backend", status="error").inc()
        PREDICTION_LATENCY.labels(source="backend").observe(duration)
        # your error handling:
        return jsonify({"error": str(e)}), 500
    finally:
        ACTIVE_USERS.labels(page="api").dec()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
