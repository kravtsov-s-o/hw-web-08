import json
from models import Author, Tag, Quote
import db_connect
from datetime import datetime


def parse_json(filename=''):
    with open(filename, 'r') as file:
        json_data = file.read()

    parse_data = json.loads(json_data)
    return parse_data


def insert_authors(data):
    for item in data:
        Author(
            fullname=item['fullname'],
            born_date=datetime.strptime(item['born_date'], "%B %d, %Y"),
            born_location=item['born_location'],
            description=item['description']
        ).save()


def insert_quotes(data):
    for item in data:
        tags = []
        for tag in item['tags']:
            tags.append(Tag(name=tag))

        author = Author.objects(fullname__exact=item['author']).first()

        Quote(
            tags=tags,
            author=author.id,
            quote=item['quote'],
        ).save()


authors_json = 'authors.json'
quotes_json = 'quotes.json'

parse_authors = parse_json(authors_json)
parse_quotes = parse_json(quotes_json)

insert_authors(parse_authors)
insert_quotes(parse_quotes)
