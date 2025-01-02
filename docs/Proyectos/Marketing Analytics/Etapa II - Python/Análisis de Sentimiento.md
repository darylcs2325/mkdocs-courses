Una gran manera de poder analizar las opiniones de los clientes hacía el servicio entregado. Mediante un análisis de las reseñas en los productos o comentarios en las redes sociales, se obtiene una medida que nos indica si es positivo o negativo la opinión del cliente o usuario.

## Bibliotecas ha utilizar

* `nltk`: Librería para usar modelos pre entrenados de NLP para el análisis de sentimientos.
* `pandas`: Librería para poder manejar, mediante dataframes, los datos importados de la base de datos.
* `pyodbc`: Es un controlador ODBC (Open Database Connectivity) para Python, permitiendo ejecutar consultas SQL.

```py linenums="1" hl_lines="9-28 30-54 58-64"
import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon') #(1)!
sia = SentimentIntensityAnalyzer() #(2)!

def fetch_data_from_sql():
    conn = pyodbc.connect(
        'DRIVER={SQL Server}; \
        SERVER=DARYL; \
        DATABASE=MarketingAnalytics; \
        Trusted_Connection=yes')
    
    query = '''
        SELECT 
            ReviewID,
            CustomerID, 
            ProductID, 
            ReviewDate, 
            Rating, 
            ReviewText 
        FROM customer_reviews''' 
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()
    return df #(3)!

def calculate_sentiment(review):
    return sia.polarity_scores(review)['compound'] #(4)!

def categorize_sentiment(value, rating):
    if value > 0.05:
        if rating >= 4:
            return 'Positivo'
        elif rating == 3:
            return 'Positivo mixto'
        else:
            return 'Negativo mixto'
    elif value < -0.05:
        if rating <= 2:
            return 'Negativo'
        elif rating == 3:
            return 'Negativo mixto'
        else:
            return 'Positivo mixto'
    else:
        if rating >=4:
            return 'Positivo'
        elif rating <= 2:
            return 'Negativo'
        else:
            return 'Mixto' #(5)!
        


customer_reviews_df = (
    fetch_data_from_sql()
    .assign(value_sentiment=lambda df: df['ReviewText'].apply(calculate_sentiment))
    .assign(SentimentCategory=lambda df: df.apply(
        lambda row: categorize_sentiment(row['value_sentiment'], row['Rating']),
        axis=1))
) #(6)!

print(customer_reviews_df.head())

customer_reviews_df.to_csv("customer_reviews_sentiment.csv", index=False) #(7)!

```

1. Descargar el léxico Vader ya entrenado, donde las palabras están asociadas a una puntuación que indica su polaridad emocional (positiva, negativa o neutral) incluyendo su intensidad.
2. Se instancia la clase.
3. Función para acceder a la base de datos de SQL Server, mediante el `query` se obtiene todos los registros para las columnas solicitadas.
4. Función para obtener las puntuaciones de las reseñas (`#!py {'neg': x, 'neu': y, 'pos': z, 'compound': result}`), nos interesa el valor de `compound`, ya que es el valor final de los comentarios.
5. Reglas para categorizar los valores que se obtiene del análisis de sentimiento (`#! 'Negativo', 'Negativo mixto', 'Mixto', 'Positivo mixto', 'Positivo'`)
6. Mediante la función `assign()` podemos aplicar múltiples pasos en un solo bloque.
    * Se inicializa la conexión con la base de datos y se guarda los datos en el dataframe `customer_reviews_df`
    * Se crea la columna `value_sentiment`, es la aplicación de la función `#!py calculate_sentiment()` a la columna `ReviewText`
    * Se crea la columna `SentimentCategory` y se le aplica a la función `#!py categorize_sentiment()` a cada fila (`axis=1`).
7. Se genera un csv para almacenar los valores creados.