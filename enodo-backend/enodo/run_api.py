from wsgiref.simple_server import make_server
import falcon
import enodo_api

database = enodo_api.Database("enodo_challenge.db")
search = enodo_api.Search(database)
selected = enodo_api.Selected(database)

app = falcon.App(cors_enable=True)
app.add_route('/search', search)
app.add_route('/selected', selected)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()