from flask import Response, current_app as app
from .parser import Searcher


@app.route('/')
def index():
    try:
        searcher = Searcher()
        searcher.go()
    except Exception as e:
        print(e)
        status_code = Response(status=404)
        return status_code
    else:
        status_code = Response(status=200)
        return status_code


