from typing import List, Tuple
import json
from collections import Counter
import boto3

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    mention_counts = Counter()
    
    # Se inicializa el cliente de S3
    s3 = boto3.client('s3')

    # Ruta al archivo en el bucket de S3
    bucket_name = 'dvalenzuela-latam-challenge'

    # Se obtiene el archivo de S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_path)

    # Itera sobre cada línea del archivo ubicado en S3
    for line in obj['Body'].iter_lines():
        try:
            tweet = json.loads(line)
            
            # Obtiene la lista de usuarios mencionados en el tweet
            mentioned_users = tweet.get('mentionedUsers')
                
            if mentioned_users is None:
                continue
            elif not isinstance(mentioned_users, list):
                continue
            else:
                # Extrae los nombres de usuario de la lista de usuarios mencionados, 
                # solo si son diccionarios y contienen el campo 'username'
                usernames = [user['username'] for user in mentioned_users if isinstance(user, dict) and 'username' in user]
                # Actualiza el contador de menciones con los nombres de usuario extraídos
                mention_counts.update(usernames)
                
        except json.JSONDecodeError:
            print(f"JSON inválido")
        except KeyError as e:
            print(f"KeyError - {str(e)}")
        except Exception as e:
            print(f"Error inesperado - {str(e)}")
    
    # Obtiene los 10 usuarios más mencionados
    top_10_mentions = mention_counts.most_common(10)
    
    return top_10_mentions
