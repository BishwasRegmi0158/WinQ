from connection import get_connection

conn = get_connection() 

cursor = conn.cursor()

cursor.execute('''

CREATE TABLE IF NOT EXISTS wine_table (
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

''')

conn.commit()
conn.close()