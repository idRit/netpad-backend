from pymongo import MongoClient
import uuid
import pprint
import datetime


class DatabaseHandler:
    
    def __init__(self):
        self.client = MongoClient("mongodb+srv://red:blxgre369@cluster0-oaiys.mongodb.net/test?retryWrites=true")
        self.notes_db = self.client.notes
        self.notes_collection = self.notes_db.notes


    def insert_one_note(self, subject = None, note_content = None):

        if subject is None:
            subject = 'Empty' + str(uuid.uuid4())

        if note_content is None:
            note_content = 'Empty'

        subject = "#" + subject
        
        note = {
            "Subject" : subject,
            "Content" : note_content
        }


        self.notes_collection.update_one({"Subject" : subject}, {"$set" : note}, upsert = True )

        print('inserted/updated!')


    def get_one_note(self, note_subject = None):
        
        if note_subject is None:
            return None

        note = self.notes_collection.find_one({"Subject" : '#'+note_subject})

        pprint.pprint(note)

        return note

    def delete_one_note(self, note_subject = None):

        if note_subject is None:
            return "no such note"

        self.notes_collection.delete_one({"Subject" : note_subject})

        print("deleted")

    def connected(self):
        return "connected!"


def test():
    a = DatabaseHandler()
    print(a.connected())
    a.insert_one_note("this is subject", "this is content")
    notex = a.get_one_note("this is subject")
    print(type(notex))
    a.delete_one_note("#this is subject")

#test()