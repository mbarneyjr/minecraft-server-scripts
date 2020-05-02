import os
import json
import time
import requests
import subprocess


def render_map(job):
    command = 'make upload'
    os.environ['JOB_ID'] = job.get('createdAt')
    process = subprocess.Popen(command, shell=True)
    process.wait()
    del os.environ['JOB_ID']


def get_job():
    response = requests.get('https://api.map.mc.mbarney.me/jobs')
    jobs = response.json() or {}
    jobs = jobs.get('jobs')
    if jobs:
        return jobs[0]


def complete_job(job):
    requests.put('https://api.map.mc.mbarney.me/jobs/{}'.format(job['createdAt']), json={
        'status': 'COMPLETED',
        'percent': 100,
    })


while True:
    try:
        job = get_job()
        if job:
            render_map(job)
            complete_job(job)
    except Exception as e:
        print(e)
        pass
    time.sleep(5)
