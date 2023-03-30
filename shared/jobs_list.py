import json
import datetime

class JobsList:

    def __init__(self):
        self.jobs = {}

    @classmethod
    def create(cls, jobs_json_encoded: str):
        obj = cls()
        obj.jobs = json.loads(jobs_json_encoded)
        return obj

    def contains(self, job):
        return job in self.jobs
    
    def add(self, job):
        self.jobs[job] = str(datetime.datetime.now())

    def sorted_jobs(self):
        return dict(sorted(self.jobs.items(), key=lambda item: item[1]))

    def to_json(self):
        return json.dumps(self.jobs)
