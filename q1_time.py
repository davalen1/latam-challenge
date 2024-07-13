from typing import List, Tuple
from datetime import datetime
import pandas as pd

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Se lee el archivo JSON a DataFrame
    df = pd.read_json(file_path, lines=True)

    # Se procesa la información para obtener los datos de interés a partir de los datos como están organizados en el archivo JSON
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['username'] = df['user'].apply(lambda x: x['username'])
    
    # Se agrupa por fecha y nombre de usuario, contando los tweets
    grouped = df.groupby(['date', 'username']).size().reset_index(name='tweet_count')
    
    # Se ordena por recuento de tweets (descendiente) y nombre de usuario (ascendente) de manera de lidiar con los empates
    grouped = grouped.sort_values(['tweet_count', 'username'], ascending=[False, True])
    
    # Sólo se registra la primera entrada para cada fecha
    top_by_date = grouped.groupby('date').first().reset_index()
    
    # Se ordena de nuevo para obtener el top 10 overall
    top_10 = top_by_date.sort_values('tweet_count', ascending=False).head(10)
    
    result = [(row['date'], row['username']) for _, row in top_10.iterrows()]
    return result
