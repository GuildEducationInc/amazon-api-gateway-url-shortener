from url_shortener_handler import UrlShortenerHandler


def test_adds_record_when_none_exists(table):
    url_shortener = UrlShortenerHandler(table)
    event = {"body": {"url": "https://guildeducation.com"}}
    url_shortener(event)
    records = table.scan()

    assert records["Count"] == 1


def test_does_not_add_second_record_when_id_already_exists(table):
    item = {"id": "hUbuf6t", "url": "first"}
    table.put_item(TableName="comms-url-shortener-test", Item=item)

    url_shortener = UrlShortenerHandler(table)
    event = {"body": {"url": "https://guildeducation.com"}}
    url_shortener(event)
    records = table.scan()
    record = records["Items"][0]

    assert records["Count"] == 1
    assert record["url"] == "first"


def test_inserts_the_correct_values(table):
    url_shortener = UrlShortenerHandler(table)
    event = {"body": {"url": "https://guildeducation.com"}}
    url_shortener(event)
    records = table.scan()
    record = records["Items"][0]

    assert record["id"] == "hUbuf6t"
    assert record["url"] == event["body"]["url"]
    assert record["owner"] == "comms@guildeducation.com"


def test_returns_success_response_when_handling_new_record(table):
    url_shortener = UrlShortenerHandler(table)
    event = {"body": {"url": "https://guildeducation.com"}}
    result = url_shortener(event)

    assert result == {"statusCode": 200, "body": "https://guildedu.com/hUbuf6t"}


def test_returns_success_response_when_handling_duplicate_record(table):
    item = {"id": "hUbuf6t"}
    table.put_item(TableName="comms-url-shortener-test", Item=item)

    url_shortener = UrlShortenerHandler(table)
    event = {"body": {"url": "https://guildeducation.com"}}
    result = url_shortener(event)

    assert result == {"statusCode": 200, "body": "https://guildedu.com/hUbuf6t"}
