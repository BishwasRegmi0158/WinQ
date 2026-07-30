import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from connection import get_connection

model = joblib.load("mero_model_pipeline.joblib")

app = FastAPI()


class WineData(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    Id: int


@app.post("/predict")
def predict_quality(data: WineData):

    df = pd.DataFrame([data.dict()])

    df.columns = [
        "fixed acidity",
        "volatile acidity",
        "citric acid",
        "residual sugar",
        "chlorides",
        "free sulfur dioxide",
        "total sulfur dioxide",
        "density",
        "pH",
        "sulphates",
        "alcohol",
        "Id",
    ]

    prediction = model.predict(df)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO wineQ_table (
            fixed_acidity,
            volatile_acidity,
            citric_acid,
            residual_sugar,
            chlorides,
            free_sulfur_dioxide,
            total_sulfur_dioxide,
            density,
            pH,
            sulphates,
            alcohol,
            Id,
            wine_quality
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data.fixed_acidity,
            data.volatile_acidity,
            data.citric_acid,
            data.residual_sugar,
            data.chlorides,
            data.free_sulfur_dioxide,
            data.total_sulfur_dioxide,
            data.density,
            data.pH,
            data.sulphates,
            data.alcohol,
            data.Id,
            int(prediction[0]),
        ),
    )
    conn.commit()
    conn.close()

    return {"predicted_quality": int(prediction[0])}


@app.get("/predictions")
def get_predictions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM wineQ_table")
    rows = cursor.fetchall()

    return {
        "data": [
            {
                "fixed_acidity": row[0],
                "volatile_acidity": row[1],
                "citric_acid": row[2],
                "residual_sugar": row[3],
                "chlorides": row[4],
                "free_sulfur_dioxide": row[5],
                "total_sulfur_dioxide": row[6],
                "density": row[7],
                "pH": row[8],
                "sulphates": row[9],
                "alcohol": row[10],
                "Id": row[11],
                "wine_quality": row[12],
            }
            for row in rows
        ]
    }