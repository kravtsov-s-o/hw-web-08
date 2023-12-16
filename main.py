from models import Author, Quote
import db_connect
import redis
from redis_lru import RedisLRU

redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)


@cache
def find_by_fullname(name):
    author = Author.objects(fullname__iregex=f'^{name}').first()
    quotes = Quote.objects(author=author.id)

    return quotes


@cache
def find_by_tag(tag):
    quotes = Quote.objects(tags__name__iregex=f'^{tag}')

    return quotes


@cache
def find_by_tags(tags: list):
    quotes = Quote.objects(tags__name__in=tags)

    return quotes


def print_quotes(quotes):
    for q in quotes:
        print(q['quote'])
        print(f"- {q['author']['fullname']}")
        print()


# name: Steve Martin

def main():
    while True:
        message = input('Write command: ')

        if message == 'exit':
            break

        if message.startswith('name:'):
            name = message.split(':')[1].strip()
            quotes_to_show = find_by_fullname(name)

            print_quotes(quotes_to_show)

        if message.startswith('tag:'):
            tag = message.split(':')[1].strip()
            quotes_to_show = find_by_tag(tag)

            print_quotes(quotes_to_show)

        if message.startswith('tags:'):
            tags = message.split(':')[1].strip()
            tags_list = [tag.strip() for tag in tags.split(',')]
            quotes_to_show = find_by_tags(tags_list)

            print_quotes(quotes_to_show)


if __name__ == '__main__':
    main()
