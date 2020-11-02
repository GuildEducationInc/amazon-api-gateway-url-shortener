import os

import boto3

from url_shortener_handler import UrlShortenerHandler

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
link_table = dynamodb.Table(os.environ["LINK_TABLE_NAME"])

handler = UrlShortenerHandler(link_table=link_table)
