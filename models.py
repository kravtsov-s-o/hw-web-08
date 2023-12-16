from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField, \
    ReferenceField, DateField


class Author(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()
    created_at = DateTimeField(default=datetime.now())


class Tag(EmbeddedDocument):
    name = StringField()


class Quote(Document):
    quote = StringField()
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author)
    created_at = DateTimeField(de=datetime.now())
