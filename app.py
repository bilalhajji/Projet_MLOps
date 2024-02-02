import joblib
import uvicorn
from fastapi import FastAPI, Query
from prometheus_client import Counter, make_asgi_app
import pandas as pd
import numpy as np

spam_counter = Counter("spam_counter", "Counter for spam")
not_spam_counter = Counter("not_spam_counter", "Counter for not spam")

app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.post("/spam-prediction/")
def predict_spam(message: str = Query(..., alias="message")) -> dict:
    try:
        # Load the trained model for prediction
        trained_model = joblib.load("fichier.joblib")

        # Assuming the model expects a string input, no need to convert
        prediction = trained_model.predict([message])
        predicted_class = prediction[0]
        spam = predicted_class == 1

        # Increment the counter based on the prediction
        if spam:
            spam_counter.inc()
        else:
            not_spam_counter.inc()

        return {"spam": spam}
    except Exception as e:
        # Log the detailed error message
        app.logger.error(f"An error occurred: {str(e)}")
        # Return an informative response
        return {"error": "Internal Server Error"}

if __name__ == "__main__":
    # Enable logging for debugging
    import logging
    logging.basicConfig(level=logging.DEBUG)

    uvicorn.run(app, host="0.0.0.0", port=8000)
