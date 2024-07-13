from typing import List, Tuple
import json
from datetime import datetime
from collections import defaultdict
import heapq
from dateutil.parser import parse as parse_date
import boto3

def load_data_generator(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                json_object = json.loads(line)
                yield json_object
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {line}")
                print(f"Error message: {e}")

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_user_count = defaultdict(lambda: defaultdict(int))
    
    # Se inicializa el cliente de S3
    s3 = boto3.client('s3')

    # Ruta al archivo en el bucket de S3
    bucket_name = 'dvalenzuela-latam-challenge'

    # Se obtiene el archivo de S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_path)

    for line in obj['Body'].iter_lines():
        # Primero se decodifican los bytes a un string y se parsean como JSON
        json_data = json.loads(line.decode('utf-8'))
        date = parse_date(json_data['date']).date()
        username = json_data['user']['username']
        date_user_count[date][username] += 1
    
    top_users = []
    for date, user_counts in date_user_count.items():
        # Se ordena por recuento (descendiente) y luego por nombre de usuario (ascendente), cosa de lidiar con empates consistentemente
        sorted_users = sorted(user_counts.items(), key=lambda x: (-x[1], x[0]))
        top_user, top_count = sorted_users[0]
        heapq.heappush(top_users, (-top_count, top_user, date))
    
    # Se guarda sólo el top 10
    top_10 = heapq.nsmallest(10, top_users)
    
    result = [(date, username) for _, username, date in top_10]
    return result