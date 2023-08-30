from processing_data import lambda_handler
from bs4 import BeautifulSoup
from unittest.mock import Mock, patch

def test_lambda_handler():
    # Mock para el objeto response de S3
    mock_response = Mock()
    mock_response.read.return_value = b'Contenido HTML simulado'
    mock_s3_client = Mock()
    mock_s3_client.get_object.return_value = {'Body': mock_response}

    # Mock para BeautifulSoup
    mock_soup = Mock(spec=BeautifulSoup)

    # Patch para boto3.client('s3') y BeautifulSoup
    with patch('boto3.client', return_value=mock_s3_client), \
         patch('bs4.BeautifulSoup', return_value=mock_soup):
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'buckethugoa'},
                        'object': {'key': 'index.html'}
                    }
                }
            ]
        }
        result = lambda_handler(event, None)

    assert result['statusCode'] == 200
    assert result['body'] == '"Datos procesados y guardados en CSV exitosamente"'

    mock_s3_client.assert_called_once_with('s3')
    mock_s3_client.return_value.get_object.assert_called_once_with(
        Bucket='buckethugoa', 
        Key='index.html')
    mock_soup.assert_called_once_with(
        b'Contenido HTML simulado',
        'html.parser')
    # Agrega más aserciones según sea necesario para verificar otras partes de la función
