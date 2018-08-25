import http
import uuid

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

import settings
from utils import get_youtube_id, TEXT

app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    party = db.Column(db.String(50))
    url = db.Column(db.String(50))

    def is_valid(self):
        return self.url is not None

    def __init__(self, user: str, party: str, url: str):
        self.user = user
        self.party = party
        self.url = get_youtube_id(url)


class SongSchema(Schema):
    id = fields.Int(dump_only=True)
    # user = fields.Str()
    # party = fields.Str()
    url = fields.Str()


song_schema = SongSchema()


@app.route('/api/songs', methods=['GET', ])
def songs():
    party: str = request.args.get('party')
    last: int = request.args.get('last', 0)
    limit: int = request.args.get('limit', settings.QUERY_LIMIT)

    if not party:
        return jsonify({
            'party': TEXT.ERROR.REQUIRED,
        }), http.HTTPStatus.BAD_REQUEST

    result: list = Song.query.add_columns('id', 'url').filter(Song.party == party, Song.id > last).limit(limit)

    return jsonify(song_schema.dump(result, many=True)[0])


@app.route('/api/add-song', methods=['POST', ])
def add_song():
    data: dict = request.get_json()

    user: str = data.get('user')
    party: str = data.get('party')
    url: str = data.get('url')

    if not user or not party or not url:
        return jsonify({
            'message': TEXT.ERROR.GENERAL,
            'user': TEXT.ERROR.REQUIRED,
            'party': TEXT.ERROR.REQUIRED,
            'url': TEXT.ERROR.REQUIRED,
        }), http.HTTPStatus.BAD_REQUEST

    song: Song = Song(user, party, url)

    if not song.is_valid():
        return jsonify({
            'message': TEXT.ERROR.YOUTUBE,
            'url': TEXT.ERROR.INVALID
        }), http.HTTPStatus.BAD_REQUEST

    db.session.add(song)
    db.session.commit()

    return jsonify(song_schema.dump(song)[0]), http.HTTPStatus.CREATED


@app.route('/api/delete-song', methods=['DELETE', ])
def delete_song():
    data: dict = request.get_json()

    id_: int = data.get('id')
    user: str = data.get('user')

    if not id_ or not user:
        return jsonify({
            'id': TEXT.ERROR.REQUIRED,
            'user': TEXT.ERROR.REQUIRED,
        }), http.HTTPStatus.BAD_REQUEST

    song: Song = Song.query.filter_by(id=id_, user=user)

    if not song.scalar():
        return jsonify({'message': TEXT.ERROR.SONG}), http.HTTPStatus.NOT_FOUND

    song.delete()
    db.session.commit()

    return jsonify({'message': 'Song deleted.'}), http.HTTPStatus.ACCEPTED


@app.route('/api/generate', methods=['GET', ])
def generate():
    return jsonify({
        'party': uuid.uuid4(),
        'user': uuid.uuid4(),
    })


@app.route('/api')
def api():
    return jsonify(TEXT.API)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
