# hackumass16
```
mkvirtualenv --python=$(which python3) hackum
pip install -r requirements.txt
daphne -b 127.0.0.1 -p 9000 hackum.asgi:channel_layer
./manage.py runworker
```
