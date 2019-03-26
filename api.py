from note_model import DatabaseHandler
from flask import Flask, url_for, request, json, Response, jsonify
from flask_cors import CORS, cross_origin

interactor = DatabaseHandler()
print(interactor.connected())

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ['GET'])
def index():

    note = {
        "Subject" : "New Note",
        "Content" : "Write your content here."
    }

    resp = jsonify(note)
    return resp

@app.route("/api/postNote", methods = ['POST', 'PUT'])
def postNote():

    if request.method == 'POST':

        res = json.dumps(request.json)
        resDict = json.loads(res)
        interactor.insert_one_note(subject = resDict.get("Subject"), note_content = resDict.get("Content"), mode = 'POST', ttl_in_seconds = resDict.get("ttl_in_sec"))
        
        return res

    elif request.method == 'PUT':
        
        res = json.dumps(request.json)
        resDict = json.loads(res)
        interactor.insert_one_note(subject = resDict.get("Subject"), note_content = resDict.get("Content"), mode = 'PUT')
        
        return res

    else:
        return jsonify({"error" : "check method type"})

@app.route("/api/getNote/<noteSubject>", methods = ['GET', 'DELETE'])
def getNote(noteSubject):
    if request.method == 'GET':
        
        note = interactor.get_one_note(noteSubject)
        if note is None:
            return jsonify({"error" : "note not found"})

        note.pop('_id', None)
    
        resp = jsonify(note)
        return resp

    elif request.method == 'DELETE':
        
        note = interactor.delete_one_note(noteSubject)
        if note is not None:
            return jsonify({"error" : note})
        else:
            return jsonify({"operation" : "successful"})

    else:

        return jsonify({"error" : "check method type"})


if __name__ == "__main__":
    app.run()
