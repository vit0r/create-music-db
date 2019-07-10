import requests
import discogs_client
import time
from os import environ
from uuid import uuid4
from bs4 import BeautifulSoup
from database import db_session
from models import Artista, Musica

htms = ['art.htm', 'art2.htm', 'art3.htm', 'art4.htm', 'art5.htm']
data = list(map(lambda h: requests.get('http://www.acclaimedmusic.net/061024/1948-09{}'.format(h)), htms))
artist_names = []
for r in data:
    if r.status_code:
        soup = BeautifulSoup(r.text, 'html.parser')
        tags_a = list(map(lambda c: c.contents[0], soup.find_all('a')))[13:]
        for i, c in enumerate(tags_a):
            tags_a = tags_a[i:20]
            if tags_a:
                artist_names = artist_names + tags_a

d = discogs_client.Client('my_music_gets', user_token=environ.get('DISCOGS_USER_TOKEN'))
for query in artist_names:
    try:
        artists_data = list(d.search(q=query, type='artist'))
        for artist in artists_data:
            artist_model = {'Id': str(uuid4()), 'Nome': artist.name}
            artist_model_db = Artista(artist_model)
            db_session.add(artist_model_db)
            print(artist_model)
            for release in artist.releases:
                music_models = list(map(lambda t: {'Id': str(uuid4()), 'ArtistaId': artist_model.get('Id'), 'Nome': t.title}, release.tracklist))
                for m in music_models:
                    music_model_db = Musica(m)
                    db_session.add(music_model_db)
                    print('Music -> %s' %(m))
                    db_session.commit()
                    time.sleep(1)
    except ValueError as ex:
        db_session.rollback()
        print(ex)
    finally:
        db_session.close()
