export interface WineData {
  fixed_acidity: number;
  volatile_acidity: number;
  citric_acid: number;
  residual_sugar: number;
  chlorides: number;
  free_sulfur_dioxide: number;
  total_sulfur_dioxide: number;
  density: number;
  pH: number;
  sulphates: number;
  alcohol: number;
  Id: number;
}

export interface PredictionResponse {
  predicted_quality: number;
  prediction_id: number;
}

export interface PredictionRecord extends WineData {
  wine_quality: number;
  prediction_id: number;
}

export interface PredictionsResponse {
  data: PredictionRecord[];
}
