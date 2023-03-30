import redis
import socket
import json
import uuid
import os
import logging
import requests
import time
import random
import sys
from typing import Optional
from incubator import incubate

sys.path.append('../shared')
from shared.jobs_list import JobsList

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

MIN_LENGTH = os.environ.get('MIN_LENGTH', 10)
MAX_LENGTH = os.environ.get('MAX_LENGTH', 40)
NUM_CHILDREN = os.environ.get('NUM_CHILDREN', 3)

class Bioreactor:
    def __init__(self):
        self.cache = self.create_redis_connection()
        self.host = self.get_hostname()
        self.job = None
        self.iteration = 0
        self.target = None
        self.current = None
        self.ready = False

    @staticmethod
    def create_redis_connection():
        r = redis.Redis(host='redis', port=6379, db=0)
        return r

    @staticmethod
    def get_hostname():
        """
        This function returns the hostname of the machine.
        :return: The hostname of the machine.
        """
        return socket.gethostname()

    def run(self):
        self.load_current_job()

        while True:
            if not self.ready:
                self.initialize_job()

            coef = 0.0
            while True:
                candidates = incubate(self.current, self.target, NUM_CHILDREN)
                logger.info('Incubated: ' + json.dumps(candidates))
                self.iteration += 1
                if candidates['best'] < coef:
                    logger.info(f'Discarded generation. Iteration: {self.iteration}.')
                    continue
    
                coef = candidates['best']    
                self.current = candidates['mapping'][coef]
                logger.info(f'Current: "{self.current}", iteration: {self.iteration}.')
                self.save_job()
    
                if self.current == self.target:
                    logger.info(f'Completed in {self.iteration} iterations.')
                    self.clean_up()
                    break
                
    def load_current_job(self) -> bool:
        """
        This function reads the current job from the cache and sets the job, iteration, target, and current variables.
        :return: True if the job exists in the cache, False otherwise.
        """
        jobkey = self.host + '-job'
        if not self.cache.exists(jobkey):
            return False
        job_id = self.cache.get(jobkey)
        logger.info('Loaded current job ' + jobkey + ': ' + job_id)
        
        if not self.cache.exists('JOB:' + job_id):
            logger.info('Job ID ' + job_id + ' not found')
            return False
        
        key_value = self.cache.get('JOB:' + job_id)
        job = json.loads(key_value)
        self.job = job['id']
        self.iteration = job['iteration']
        self.target = job['target']
        self.current = job['current']

    def initialize_job(self) -> None:
        """
        This function initializes a new job and sets the job, iteration, target, and current variables.
        """
        self.job = str(uuid.uuid4())
        self.iteration = 0
        self.target = self.fetch_target(MIN_LENGTH, MAX_LENGTH)
        self.current = 'a' * len(self.target)
        jobkey = self.host + '-job'
        self.cache.set(jobkey, self.job)
        logger.info(f'Generated new job {jobkey}, ID: {self.job}, target: "{self.target}"')
        self.save_job()
        self.register()
        self.ready = True

    def save_job(self) -> None:
        job = {
            'id': self.job,
            'iteration': self.iteration,
            'target': self.target,
            'current': self.current
        }
        self.cache.set('JOB:' + self.job, json.dumps(job))

    def register(self) -> None:
        """
        This function registers the job by adding it to the job list.
        """
        time.sleep(random.randint(1, 1000) / 1000)
        while self.cache.exists('job-list-lock'):
            time.sleep(random.randint(1, 1000) / 1000)
            logger.info(f'[{self.host}] waiting for lock.')
        self.cache.set('job-list-lock', 'Lock', ex=5)
        logger.info(f'[{self.host}] acquired lock.')
        job_list = JobsList()
        if self.cache.exists('jobs-list'):
            job_list = JobsList.create(self.cache.get('jobs-list'))
        if not job_list.contains(self.job):
            job_list.add(self.job)
            logger.info(f'[{self.host}] job {self.job} added to job list.')
            self.cache.set('jobs-list', job_list.to_json())

    def clean_up(self) -> None:
        self.job = None
        self.iteration = 0
        self.target = None
        self.current = None
        self.ready = False
            
    def fetch_target(self, min_length: int, max_length: int) -> Optional[str]:
        """
        This function fetches a target string from a remote endpoint using GET method and returns it.
        :param min_length: The minimum length of the target string.
        :param max_length: The maximum length of the target string.
        :return: The target string.
        """
        url = f"http://generator:8080/get-sentence?min_length={min_length}&max_length={max_length}"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            logger.info("Acquired new target: \"" + data['sentence'] + "\" from host: " + data["host"])
            return data['sentence'] 
        else:
            logger.error(f"Failed to fetch target from {url}. Status code: {response.status_code}")
            return None


if __name__ == "__main__":
    sg = Bioreactor()
    sg.run()
