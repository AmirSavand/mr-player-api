import http
import uuid

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

import settings
from utils import get_youtube_id

app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    party = db.Column(db.String(50))
    url = db.Column(db.String(50))

    def __init__(self, user: str, party: str, url: str):
        self.user = user
        self.party = party
        self.url = url


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
            'party': 'This field is required.',
        }), http.HTTPStatus.BAD_REQUEST

    result = Song.query.add_columns('id', 'url').filter(Song.party == party, Song.id > last).limit(limit)

    return jsonify(song_schema.dump(result, many=True)[0])


@app.route('/api/add-song', methods=['POST', ])
def add_song():
    data: dict = request.get_json()

    user: str = data.get('user')
    party: str = data.get('party')
    url: str = data.get('url')

    if not user or not party or not url:
        return jsonify({
            'user': 'This field is required.',
            'party': 'This field is required.',
            'url': 'This field is required.',
        }), http.HTTPStatus.BAD_REQUEST

    url = get_youtube_id(url)

    song: Song = Song(user, party, url)
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
            'id': 'This field is required.',
            'user': 'This field is required.',
        }), http.HTTPStatus.BAD_REQUEST

    song: Song = Song.query.filter_by(id=id_, user=user)

    if not song.scalar():
        return jsonify({'error': 'Song does not exist.'}), http.HTTPStatus.NOT_FOUND

    song.delete()
    db.session.commit()

    return jsonify({'success': 'Song deleted.'}), http.HTTPStatus.ACCEPTED


@app.route('/api/generate', methods=['GET', ])
def generate():
    return jsonify({
        'party': uuid.uuid4(),
        'user': uuid.uuid4(),
    })


@app.route('/api')
def api():
    return jsonify('You are far away from home...')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
