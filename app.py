import os
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from connection import get_connection

TABLE_NAME = "wine_table"
MODEL_PATH = "mero_model_pipeline.joblib"
DEFAULT_FRONTEND_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"

model = joblib.load(MODEL_PATH)

app = FastAPI(title="Wine Quality API")


def _get_frontend_origins() -> list[str]:
    raw_origins = os.getenv("FRONTEND_ORIGINS", DEFAULT_FRONTEND_ORIGINS)
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    if not origins:
        return ["*"]
    return origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_frontend_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _init_database() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            fixed_acidity REAL,
            volatile_acidity REAL,
            citric_acid REAL,
            residual_sugar REAL,
            chlorides REAL,
            free_sulfur_dioxide REAL,
            total_sulfur_dioxide REAL,
            density REAL,
            pH REAL,
            sulphates REAL,
            alcohol REAL,
            Id INTEGER,
            wine_quality INTEGER,
            prediction_ID INTEGER PRIMARY KEY AUTOINCREMENT
        )
        """
    )

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event() -> None:
    _init_database()


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


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict_quality(data: WineData):
    _init_database()

    df = pd.DataFrame([data.model_dump()])
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

    prediction = int(model.predict(df)[0])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        INSERT INTO {TABLE_NAME} (
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
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
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
            prediction,
        ),
    )

    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {"predicted_quality": prediction, "prediction_id": prediction_id}


@app.get("/predictions")
def get_predictions():
    _init_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT
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
            wine_quality,
            prediction_ID
        FROM {TABLE_NAME}
        ORDER BY prediction_ID DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()

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
                "prediction_id": row[13],




            }
            for row in rows
        ]
    }