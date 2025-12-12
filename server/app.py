#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/events')
def get_events():
    Events = Event.query.all()
    events_list = [ 
        {'id': event.id, 
         'name': event.name, 
         'location': event.location} for event in Events ]
    return jsonify(events_list), 200



@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter(Event.id == id).first()
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    sessions_list = [ 
        {'id': session.id, 
        'title': session.title, 
        'start_time': session.start_time
        } 
        for session in event.sessions ]
    return jsonify(sessions_list), 200


@app.route('/speakers')
def get_speakers():
    Speakers = Speaker.query.all()
    speakers_list = [ {'id': speaker.id, 'name': speaker.name} for speaker in Speakers ]
    return jsonify(speakers_list), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter(Speaker.id == id).first()
    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404
    speaker_data = {
        'id': speaker.id,
        'name': speaker.name,
        'bio_text': speaker.bio.bio_text if speaker.bio else f"No bio available"
    }
    return jsonify(speaker_data), 200


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter(Session.id == id).first()
    if session is None:
        return jsonify({"error": "Session not found"}), 404
    speakers_list = [ 
        {'id': speaker.id, 
         'name': speaker.name,
         'bio_text': speaker.bio.bio_text if speaker.bio else f"No bio available"
         } for speaker in session.speakers ]
    return jsonify(speakers_list), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)