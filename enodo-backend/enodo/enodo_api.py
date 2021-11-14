import sqlite3, falcon

class Database:
    def __init__(self,database,check_same_thread=True) -> None:
        self.con = sqlite3.connect(database,check_same_thread=check_same_thread)
        self.cur = self.con.cursor()

class Search:
    def __init__(self, databaseInstance) -> None:
        self.con = databaseInstance.con
        self.cur = databaseInstance.cur

    def on_post(self, req, resp):
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

        resp_body = {'properties': []}
        for row in self.cur.execute(sql_query, sql_params):
            entry = {'value':row[0], 'property': row[0], 'long': row[1], 'lat': row[2], 'class_desc':row[3], 'selected':row[4]}
            resp_body['properties'].append(entry)
        resp.media = resp_body

class Selected:
    def __init__(self, databaseInstance) -> None:
        self.con = databaseInstance.con
        self.cur = databaseInstance.cur

    def on_post(self, req, resp):
        query = req.get_media()
        sql_query = "UPDATE properties SET selected = ? WHERE property LIKE ?"
        if 'selected' in query.keys() and 'property' in query.keys() and query['selected'] is not None and query['property'] is not None:
            sql_params = (query['selected'], query['property'])
            self.cur.execute(sql_query, sql_params)
            self.con.commit()
        else:
            raise falcon.HTTPBadRequest(
                title="Missing paramerter",
                description="Missing one or more required paramerters in request body"
            )