import json
import boto3
from bs4 import BeautifulSoup
import csv
import datetime

def lambda_handler(event, context):
    try:
        # Obtener información sobre el archivo cargado desde el evento
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        
        # Obtener fecha y hora actual para el nombre del archivo CSV
        now = datetime.datetime.now()
        csv_filename = now.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        
        # Descargar contenido del archivo desde S3
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        html_content = response['Body'].read().decode('utf-8')
        
        # Procesar contenido HTML con Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extraer información de las noticias (esto debe adaptarse según la estructura HTML)
        news_data = []
        for news_item in soup.find_all('div', class_='news'):
            category = news_item.find('span', class_='category').text
            title = news_item.find('h2', class_='title').text
            link = news_item.find('a')['href']
            news_data.append({'category': category, 'title': title, 'link': link})
        
        # Escribir los datos en un archivo CSV
        csv_content = 'category,title,link\n'
        for news in news_data:
            csv_content += f'"{news["category"]}", "{news["title"]}", "{news["link"]}"\n'
        
        # Subir el archivo CSV a S3
        s3_key = f'headlines/final/periodico=xxx/year={now.year}/month={now.month}/{csv_filename}'
        s3_client.put_object(Body=csv_content, Bucket=bucket_name, Key=s3_key, ContentType='text/csv')
        
        return {
            'statusCode': 200,
            'body': json.dumps('Datos procesados y guardados en CSV exitosamente')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
