from scrapping_pages import lambda_handler
from unittest.mock import Mock, patch

def test_lambda_handler():
    # Mock para la respuesta HTTP
    mock_response = Mock()
    mock_response.read.return_value = b'Contenido de prueba'
    mock_urlopen = Mock(return_value=mock_response)

    # Mock para boto3.client('s3')
    mock_s3_client = Mock()

    # Patch para urllib.request.urlopen y boto3.client
    with patch('urllib.request.urlopen', mock_urlopen), \
         patch('boto3.client', return_value=mock_s3_client):
            event = {}  # Puedes proporcionar un evento adecuado si es necesario
            result = lambda_handler(event, None)

    assert result['statusCode'] == 200
    assert result['body'] == '"Hello from Lambda!"'

    mock_urlopen.assert_called_once_with('https://www.eltiempo.com/')
    mock_s3_client.assert_called_once_with('s3')
    mock_s3_client.return_value.put_object.assert_called_once_with(
        Body=b'Contenido de prueba', 
        Bucket='buckethugoa', 
        Key='index.html', 
        ContentType='text/html'
    )
