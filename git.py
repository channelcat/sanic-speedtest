from subprocess import check_output, run, Popen, PIPE
from threading import Thread
from asyncio import sleep
import re
import logging

def runner(func, shared_output, args, kwargs):
	try:
		output = func(*args, **kwargs)
		shared_output.append(True)
		shared_output.append(output)
	except Exception as e:
		shared_output.append(False)
		shared_output.append(e)

async def async_thread(func, *args, **kwargs):
	shared_output = []
	thread = Thread(target=runner, args=[func, shared_output, args, kwargs])
	thread.start()

	while thread.is_alive():
		await sleep(0.01)

	success, output = shared_output
	if success:
		return output
	else:
		raise output


async def test_commit(commit):
    logging.warning(f"Test {commit}")
    await async_thread(run, f"git checkout {commit}", shell=True, cwd='/repository')
    logging.warning(" - Starting server")
    server = Popen("python3 test.py 8064", shell=True, cwd='/code')
    await sleep(2)

    runs = []
    for n in range(3):
        logging.warning("  - Running test {}".format(n+1))

        raw_output = await async_thread(check_output, 'wrk -t 1 -c 100 -d 8s http://127.0.0.1:8064/', shell=True)
        output = raw_output.decode()
        totals = re.search(r'(\d+) requests in ([0-9.]+)s', output)
        requests = int(totals.group(1))
        seconds = float(totals.group(2))
        requests_per_second = requests / seconds

        logging.warning(f"   - Req/sec: {requests_per_second}")

        runs.append(requests_per_second)

    fastest_run = max(*runs)
    logging.warning(f' - Best Run - {fastest_run} req/s')

    server.terminate()
    await async_thread(run, "pkill -f -9 test", shell=True)

    return {
    	"runs": runs,
    	"requests_per_second": fastest_run
    }