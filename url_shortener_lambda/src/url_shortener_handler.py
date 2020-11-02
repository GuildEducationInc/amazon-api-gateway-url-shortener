from datetime import datetime

import shortuuid
from botocore.exceptions import ClientError


class UrlShortenerHandler:
    def __init__(self, link_table):
        self.link_table = link_table

    def __call__(self, event: dict, context: object) -> dict:
        url = event.get("url")
        shortlink_id = shortuuid.uuid(name=url)[:7]

        try:
            self.link_table.put_item(
                Item={
                    "id": shortlink_id,
                    "owner": "comms@guildeducation.com",
                    "timestamp": str(datetime.now()),
                    "url": url,
                },
                ConditionExpression="attribute_not_exists(id)",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
                return {"statusCode": 400, "body": e.response["Error"]["Code"]}

        return {"statusCode": 200, "body": f"https://guildedu.com/{shortlink_id}"}
