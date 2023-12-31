from unittest.mock import patch
from scrapping_pages import lambda_handler


@patch('urllib.request.urlopen')
@patch('boto3.client')
def test_lambda_handler(mock_s3_client, mock_urlopen):
    mock_urlopen.return_value.read.return_value = b'Simulated HTML Content'
    mock_s3_client.return_value.put_object.return_value = {}
    result = lambda_handler(None, None)
    assert result['statusCode'] == 200
    assert mock_urlopen.call_count == 2
    assert result['body'] == 'Contenido HTML guardado en S3 exitosamente'
