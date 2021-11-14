from unittest.case import TestCase
from wsgiref.simple_server import make_server
from enodo import enodo_api
import falcon, threading, requests, json

class TestAPI(TestCase):
    def test_selected(self):
        try:
            print("Test selected")
            database = enodo_api.Database("enodo_test.db",False)
            search = enodo_api.Search(database)
            selected = enodo_api.Selected(database)
            app = falcon.App(cors_enable=True)
            app.add_route('/search', search)
            app.add_route('/selected', selected)
            httpd = make_server('', 8000, app)
            print('Serving on port 8000...')
            thread = threading.Thread(target=httpd.serve_forever)
            thread.start()
            url = "http://localhost:8000/selected"
            payload = json.dumps({
            "property": "1418 W FLOURNOY ST, CHICAGO, IL",
            "selected": 1
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            url = "http://localhost:8000/search"
            payload = json.dumps({
            "query_string": "1418 W FLOURNOY ST, CHICAGO, IL"
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            returned = json.loads(response.text)
            expected = {
                "properties": [
                    {
                        "value": "1418 W FLOURNOY ST, CHICAGO, IL",
                        "property": "1418 W FLOURNOY ST, CHICAGO, IL",
                        "long":"-87.6625441",
                        "lat":"41.8735290999999",
                        "class_desc":"Two to Six Apartments, Over 62 Years",
                        "selected":1
                    }
                ]
            }
            self.assertDictEqual(returned, expected)
            httpd.shutdown()
            thread.join()
        except BaseException as error:
            print("Test selected failed")
            print("Error: {}".format(error))
            return
        print("Test selected passed")


    def test_search(self):
        try:
            print("Test search")
            database = enodo_api.Database("enodo_test.db",False)
            search = enodo_api.Search(database)
            selected = enodo_api.Selected(database)
            app = falcon.App(cors_enable=True)
            app.add_route('/search', search)
            app.add_route('/selected', selected)
            httpd = make_server('', 8001, app)
            print('Serving on port 8001...')
            thread = threading.Thread(target=httpd.serve_forever)
            thread.start()
            url = "http://localhost:8001/search"
            payload = json.dumps({
            "query_string": "210 N JUSTINE ST, CHICAGO, IL"
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            returned = json.loads(response.text)
            expected = {
                "properties": [
                    {
                        "value": "210 N JUSTINE ST, CHICAGO, IL",
                        "property": "210 N JUSTINE ST, CHICAGO, IL",
                        "long":"-87.6656354999999",
                        "lat":"41.8857718",
                        "class_desc":"Two to Six Apartments, Over 62 Years",
                        "selected":0
                    }
                ]
            }
            self.assertDictEqual(returned, expected)
            httpd.shutdown()
            thread.join()
        except BaseException as error:
            print("Test search failed")
            print("Error: {}".format(error))
            return
        print("Test search passed")

        

if __name__ == '__main__':
    TestAPI().test_selected()
    TestAPI().test_search()