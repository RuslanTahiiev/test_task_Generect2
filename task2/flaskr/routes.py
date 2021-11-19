from flask import jsonify, Response, current_app as app
from .parser import Searcher


@app.route('/')
def index():
    """
    get all leads
    :return:
    """
    try:
        searcher = Searcher()
        response = searcher.go()
    except Exception as e:
        print(e)
        status_code = Response(status=404)
        return status_code
    else:
        return jsonify(response)


