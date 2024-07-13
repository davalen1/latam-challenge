from typing import List, Tuple
import pandas as pd
from collections import Counter
import emoji

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Se lee el archivo JSON a DataFrame
    df = pd.read_json(file_path, lines=True)
    
    # Se combina todo el texto en un solo string
    all_text = ' '.join(df['content'].astype(str))
    
    # Se extraen los emoji del texto
    emojis = [char for char in all_text if char in emoji.EMOJI_DATA]
    
    # Se cuentan los emoji
    emoji_counts = Counter(emojis)
    
    # Se extrae el top 10
    top_10_emojis = emoji_counts.most_common(10)
    
    return top_10_emojis