## PYTHON AUDIO SERVER

### Python/Flask/MongoDB

### `python3 -m venv venv`

### `. venv/bin/activate`

### `pip3 install -r requirements.txt`

### `export FLASK_APP=app.py`
### `export FLASK_ENV=development`

### `flask run`


### APIs:

## Create API (POST):
### `http://localhost:5000/api/db_populate`
Example:
`{
    "audio_id": 4,
    "title_of_audiobook": "A Promised Land",
    "duration": 10500,
    "audio_type": "audiobook",
    "author": "Barack Obama",
    "narrator": "Barack Obama"
}
`

## Get APIs(GET):

All Audio files in the database:
### `http://localhost:5000/api/audio`

Get specific files based on ID/File type:
### `http://localhost:5000/api/audio/<audio_id>`
OR
### `http://localhost:5000/api/<audio_type>/<audio_id>`

## UPDATE APIs(PUT):

Update a specific record in the database:
### `http://localhost:5000/api/<audio_type>/<audio_id>`
OR
### `http://localhost:5000/api/audio/<audio_id>`

Example: 
`
{
    "title_of_audiobook": "My Life in Red and White",
    "author": "Arsène Wenger",
    "narrator": "Arsène Wenger",
    "duration": 2100
}
`
## DELETE APIs(DELETE):
Delete a specific record in the database:
### `http://localhost:5000/api/<audio_type>/<audio_id>`
OR
### `http://localhost:5000/api/audio/<audio_id>`