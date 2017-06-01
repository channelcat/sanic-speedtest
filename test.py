import sys
import os
import inspect

sys.path.insert(0, '/repository')

from sanic import Sanic
from sanic.response import json

app = Sanic("test")

@app.route("/")
async def test(request):
    return json({"test": True})

if __name__ == '__main__':
    try:
    	app.run(host="127.0.0.1", port=sys.argv[1], log_config=None)
    except:
    	app.run(host="127.0.0.1", port=sys.argv[1])
