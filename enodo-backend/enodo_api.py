from wsgiref.simple_server import make_server

import falcon, sqlite3, json

from falcon import response

con = sqlite3.connect("enodo_challenge.db")
cur = con.cursor()

class Search:
    def on_post(self, req, resp):
        print("Get search")
        query = req.get_media()
        sql_query = "SELECT * FROM properties"
        sql_params = tuple()
        if "query_string" in query.keys():
            sql_query += " WHERE property LIKE ?"
            sql_params = sql_params + ("%" + query["query_string"] + "%",)
        if "selected" in query.keys():
            if "query_string" in query.keys():
                sql_query += " AND selected is ?"
            else:
                sql_query += " WHERE selected is ?"
            sql_params = sql_params + (query["selected"],)
        if "limit" in query.keys():
            sql_query += " LIMIT ?"
            sql_params = sql_params + (query["limit"],)

        print(sql_query)
        print(sql_params)
        resp_body = {'properties': []}
        for row in cur.execute(sql_query, sql_params):
            entry = {'value':row[0], 'property': row[0], 'long': row[1], 'lat': row[2], 'class_desc':row[3], 'selected':row[4]}
            resp_body['properties'].append(entry)
        resp.media = resp_body

class Selected:
    def on_post(self, req, resp):
        print("Update selected")
        query = req.get_media()
        sql_query = "UPDATE properties SET selected = ? WHERE property LIKE ?"
        sql_params = (query['selected'], query['property'])
        print(sql_query, sql_params)
        cur.execute(sql_query, sql_params)
        con.commit()

app = falcon.App(cors_enable=True)

search = Search()
selected = Selected()

app.add_route('/search', search)
app.add_route('/selected', selected)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()