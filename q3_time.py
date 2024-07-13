from typing import List, Tuple
import pandas as pd
from collections import Counter

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # # Se lee el archivo JSON a DataFrame
    df = pd.read_json(file_path, lines=True)
    
    # Se extraen todos los usuarios mencionados
    all_mentions = []
    for mentions in df['mentionedUsers'].dropna():
        all_mentions.extend([user['username'] for user in mentions])
    
    # Se cuentan las menciones
    mention_counts = Counter(all_mentions)
    
    # Se obtiene el top 10 de usuarios mencionados
    top_10_mentions = mention_counts.most_common(10)
    
    return top_10_mentions