from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from constants import password
import datetime

app = Flask(__name__)

database_name = "test"

DB_URI = "mongodb+srv://test:{}@cluster0.iiyzw.mongodb.net/{}?retryWrites=true&w=majority".format(
    password, database_name)

app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


class Audio(db.DynamicDocument):
    audio_id = db.IntField(unique=True, required=True)
    duration = db.IntField(required=True)
    uploaded_time = db.DateTimeField(
        default=datetime.datetime.now, required=True)
    audio_type = db.StringField(
        choices=['song', 'podcast', 'audiobook'], required=True)
    meta = {'collection': 'audio', 'allow_inheritance': True}

    # def to_json(self):
    #     # converts the document to json
    #     return {
    #         "audio_id": self.audio_id,
    #         "duration": self.duration,
    #         "uploaded_time": self.uploaded_time,
    #         "audio_type": self.audio_type
    #     }


class Podcast(Audio):
    name_of_podcast = db.StringField(max_length=100, required=True)
    host = db.StringField(max_length=100, required=True)
    participants = db.ListField(db.StringField(max_length=100), default=[""]) 


class Audiobook(Audio):
    title_of_audiobook = db.StringField(max_length=100, required=True)
    author = db.StringField(max_length=100, required=True)
    narrator = db.StringField(max_length=100, required=True)

class Song(Audio):
    name_of_song = db.StringField(max_length=100, required=True)



# Create
@app.route("/api/db_populate", methods=["POST"])
def db_populate():
    try:
        content = request.json
        audio = Audio(audio_id=content['audio_id'], duration=content['duration'],
                  uploaded_time=datetime.datetime.now(), audio_type=content['audio_type'])
        if audio.audio_type == "podcast":
            audio = Podcast(audio_id=content['audio_id'], name_of_podcast=content['name_of_podcast'], duration=abs(content['duration']), uploaded_time=datetime.datetime.now(
            ), audio_type=content['audio_type'], host=content['host'], participants=request.json.get('participants'))
            audio.save()
        elif audio.audio_type == "audiobook":
            audio = Audiobook(audio_id=content['audio_id'], title_of_audiobook=content['title_of_audiobook'], duration=abs(content['duration']), uploaded_time=datetime.datetime.now(
            ), audio_type=content['audio_type'], author=content['author'], narrator=content['narrator'])
            audio.save()
        elif audio.audio_type == "song":
            audio = Song(audio_id=content['audio_id'], name_of_song=content['name_of_song'], duration=abs(content['duration']),
                  uploaded_time=datetime.datetime.now(), audio_type=content['audio_type'])
            audio.save()
        else:
            resp = make_response("Any error", 500)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        resp = make_response("Action is successful", 200)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        resp = make_response("The request is invalid", 400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


# Retrieve all audio files from the database
@app.route("/api/audio", methods=["GET"])
def api_audios():
    all_audio = []
    try:
        for audio in Audio.objects:
            all_audio.append(audio)
        resp = make_response(jsonify(all_audio), 200)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        resp = make_response("The request is invalid", 400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

# Working with specific ID
@app.route("/api/audio/<audio_id>", methods=["GET", "PUT", "DELETE"])
def api_all_audio(audio_id):
    if request.method == "GET":
        audio_obj = Audio.objects(audio_id=audio_id).first()
        if audio_obj:
            resp = make_response(jsonify(audio_obj.to_json()), 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = make_response("The request is invalid", 400)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == "PUT":
        try:
            content = request.json
            audio_obj = Audio.objects(audio_id=audio_id).first()
            if audio_type == "podcast":
                audio_obj.update(name_of_podcast=content['name_of_podcast'], duration=abs(content['duration']), uploaded_time=datetime.datetime.now(
            ), host=content['host'], participants=request.json.get('participants'))
            elif audio_type == "audiobook":
                audio_obj.update(title_of_audiobook=content['title_of_audiobook'], duration=abs(content['duration']), uploaded_time=datetime.datetime.now(
            ), author=content['author'], narrator=content['narrator'])
            elif audio_type == "song":
                audio_obj.update(name_of_song=content['name_of_song'], duration=abs(content['duration']),
                  uploaded_time=datetime.datetime.now())
            else:
                resp = make_response("Any error", 500)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
            resp = make_response("Action is successful", 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except:
            resp = make_response("The request is invalid", 400)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == "DELETE":
        try:
            audio_obj = Audio.objects(audio_id=audio_id).first()
            audio_obj.delete()
            resp = make_response("Action is successful", 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except:
            resp = make_response("The request is invalid", 400)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


# Working with Audio-type & specific ID
@app.route("/api/<audio_type>/<audio_id>", methods=["GET", "PUT", "DELETE"])
def api_each_audio(audio_type, audio_id):
    if request.method == "GET":
        audio_obj = Audio.objects(audio_type=audio_type, audio_id=audio_id).first()
        if audio_obj:
            resp = make_response(jsonify(audio_obj), 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = make_response("The request is invalid", 400)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == "PUT":
        try:
            content = request.json
            audio_obj = Audio.objects(audio_type=audio_type, audio_id=audio_id).first()
            if audio_type == "podcast":
                audio_obj.update(name_of_podcast=content['name_of_podcast'], duration=abs(content['duration']), uploaded_time=datetime.datetime.now(
            ), host=content['host'], participants=request.json.get('participants'))
            elif audio_type == "audiobook":
                audio_obj.update(title_of_audiobook=content['title_of_audiobook'], duration=abs(content['duration']), uploaded_time=datetime.datetime.now(
            ), author=content['author'], narrator=content['narrator'])
            elif audio_type == "song":
                audio_obj.update(name_of_song=content['name_of_song'], duration=abs(content['duration']),
                  uploaded_time=datetime.datetime.now())
            else:
                resp = make_response("Any error", 500)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
            resp = make_response("Action is successful", 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except:
            resp = make_response("The request is invalid", 400)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == "DELETE":
        try:
            audio_obj = Audio.objects(audio_type=audio_type, audio_id=audio_id).first()
            audio_obj.delete()
            resp = make_response("Action is successful", 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except:
            resp = make_response("The request is invalid", 400)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == "__main__":
    app.run()
