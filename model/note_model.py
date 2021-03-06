from pymongo import MongoClient
import uuid
import pprint
import datetime


class DatabaseHandler:
    
    def __init__(self):
        self.client = MongoClient("connection string")
        self.notes_db = self.client.notes
        self.notes_collection = self.notes_db.notes


    def insert_one_note(self, subject = None, note_content = None):

        if subject is None:
            subject = 'Empty' + str(uuid.uuid4())

        if note_content is None:
            note_content = 'Empty'

        note = {
            "Subject" : subject,
            "Content" : note_content
        }


        self.notes_collection.update_one({"Subject" : subject}, {"$set" : note}, upsert = True )

        print('inserted/updated!')


    def get_one_note(self, note_subject = None):
        
        if note_subject is None:
            return None

        note = self.notes_collection.find_one({"Subject" : note_subject})

        pprint.pprint(note)

        return note

    def delete_one_note(self, note_subject = None):

        if note_subject is None:
            return "no such note"

        cnt = self.notes_collection.count_documents({})

        self.notes_collection.delete_one({"Subject" : note_subject})

        if cnt == self.notes_collection.count_documents({}) :
            return False
        else :
            return True

    def connected(self):
        return "connected!"


def test():
    a = DatabaseHandler()
    print(a.connected())
    a.insert_one_note("this is subject", "this is content")
    notex = a.get_one_note("this is subject")
    print(type(notex))
    print(a.delete_one_note("this is s"))
    print(a.delete_one_note("this is subject"))

#test()