import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def fetch_data_from_sql():
    conn = pyodbc.connect(
        'DRIVER={SQL Server}; \
        SERVER=DARYL; \
        DATABASE=MarketingAnalytics; \
        Trusted_Connection=yes')
    
    query = 'SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM customer_reviews'
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()
    return df

customer_reviews_df = fetch_data_from_sql()

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    return sia.polarity_scores(review)['compound']

customer_reviews_df['value_sentiment']=customer_reviews_df['ReviewText'].apply(calculate_sentiment)
print(customer_reviews_df)

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
            return 'Mixto'

customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['value_sentiment'], row['Rating']), axis=1)

print(customer_reviews_df.head())

customer_reviews_df.to_csv('customer_reviews_sentiment.csv', index=False)

# correlacion=customer_reviews_df['Rating'].corr(customer_reviews_df['value_sentiment'])
# print("Correlación: ", correlacion)

# incongruencias = customer_reviews_df[((customer_reviews_df['value_sentiment'] > 0) & (customer_reviews_df['Rating'] < 3)) | ((customer_reviews_df['value_sentiment'] < 0) & (customer_reviews_df['Rating'] > 3))]
# print("\nIncongruencias:")
# print(incongruencias)
# if __name__ == '__main__':
#     fetch_data_from_sql()
#     calculate_sentiment(customer_reviews_df['ReviewText'])