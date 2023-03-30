import bottle
import redis
import json
import sys

sys.path.append('../shared')
from shared.jobs_list import JobsList


class Ui:
    def __init__(self, redis_host='redis', redis_port=6379):
        self.cache = redis.Redis(host=redis_host, port=redis_port)

    def get_data(self):
        return None

    def get_jobs(self):
        job_list = JobsList()
        if self.cache.exists('jobs-list'):
            job_list = JobsList.create(self.cache.get('jobs-list'))
        return job_list.sorted_jobs()


ui = Ui()
app = bottle.default_app()


@app.route(path="/", method="GET")
def main_route():
    data = ui.get_data()
    bottle.response.content_type = 'text/html; charset=UTF8'
    return bottle.template('main', data=data)


@app.route(path="/jobs", method="GET")
def jobs():
    jobs = ui.get_jobs()
    bottle.response.content_type = 'application/json'
    return json.dumps({'jobs': jobs})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, reloader=True)
