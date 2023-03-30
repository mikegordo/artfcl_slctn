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
    
    def job_info(self, job_id):
        key_value = 'JOB:' + job_id
        if not self.cache.exists(key_value):
            return None
        
        job = json.loads(self.cache.get(key_value))
        job['iterations_per_letter'] = job['iteration'] / len(job['target'])
        job['discarded_per_letter'] = job['discarded'] / len(job['target'])
        job['percent_discarded'] = job['discarded'] / job['iteration'] * 100

        return job


ui = Ui()
app = bottle.default_app()


# Static Routes
@app.get("/static/<filename>")
def css(filename):
    return bottle.static_file(filename, root="/app/main/static")


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


@app.route(path="/job", method="GET")
def job_info():
    job_id = bottle.request.query.job
    job = ui.job_info(job_id)
    bottle.response.content_type = 'application/json'
    return json.dumps({'job': job, 'job_id': job_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, reloader=True)
