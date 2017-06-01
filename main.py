from sanic import Sanic, response
from sanic.exceptions import InvalidUsage
import git

RUNNING = False

app = Sanic('sanic-tester')

app.static('/', 'index.html')

@app.get('/test/<commit:[A-Za-z0-9]+>')
async def test(request, commit):
	global RUNNING
	if RUNNING:
		raise InvalidUsage('Please wait for the current test to finish')
	try:
		RUNNING = True
		run_data = await git.test_commit(commit)
	finally:
		RUNNING = False

	return response.json(run_data)

app.run(host='0.0.0.0', port=80, debug=False)