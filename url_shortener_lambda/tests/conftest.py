import boto3
import pytest
from moto import mock_dynamodb2


@pytest.fixture(name="table", scope="function")
def fixture_table():
    schema = {
        "TableName": "comms-url-shortener-test",
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "S"},
        ],
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "BillingMode": "PAY_PER_REQUEST",
        "Tags": [{"Key": "Owner:Contact", "Value": "comms:squad-comms"}],
    }

    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
        dynamodb.create_table(**schema)
        table_name = schema["TableName"]
        table = dynamodb.Table(table_name)
        yield table
        table.delete()
