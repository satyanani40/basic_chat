from mongoengine.document import Document
from mongoengine.fields import StringField,ReferenceField,BooleanField, DateTimeField

class users(Document):
    username = StringField(required=True, max_length=200,unique=True)

class chatrooms(Document):
    user1 = StringField(required=True, max_length=200)
    user2 = StringField(required=True, max_length=200)
    chat_room_name = StringField(required=True, max_length=200,unique=True)


class messages(Document):
    user1 = StringField(required=True)
    user2 = StringField(required=True)
    message = StringField()
    transfered_data = BooleanField(default=False)
    seen =  BooleanField(default=False)
    created = DateTimeField()

