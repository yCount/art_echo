# art_echo

A website demo of a social media for artists applied in Django framework. It bring the concept of branching of git into aspiration to echo a creative Art environment.

## Dependencies

django 2.2.28
pillow 10.2.0

## Setup The Project

git clone https://github.com/yCount/art_echo.git && cd art_echo
python manage.py migrate
python manage.py makemigrations
python populate_db.py
python manage.py createsuperuser # optional

## Run the project

python manage.py runserver
Paste http://127.0.0.1:8000/artecho/ URL into your browser