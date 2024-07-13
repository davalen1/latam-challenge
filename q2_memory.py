import json
from typing import List, Tuple
from collections import Counter
import emoji
from memory_profiler import profile
import boto3

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counts = Counter()
    
    # Se inicializa el cliente de S3
    s3 = boto3.client('s3')

    # Ruta al archivo en el bucket de S3
    bucket_name = 'dvalenzuela-latam-challenge'

    # Se obtiene el archivo de S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_path)

    # Se lee contenido del archivo
    for line in obj['Body'].iter_lines():
            try:
                tweet = json.loads(line)
                content = tweet.get('content', '')
                
                # Se extraen los emoji del contenido
                emojis = [char for char in content if char in emoji.EMOJI_DATA]
                
                # Se actualiza la cuenta de emoji
                emoji_counts.update(emojis)
                
            except json.JSONDecodeError:
                continue  # Se saltan las líneas JSON inválidas
    
    # Se toma el top 10 de emoji
    top_10_emojis = emoji_counts.most_common(10)
    
    return top_10_emojis