import os
import requests
import json
import logging
import time
JOBCONTROLLER_HOST = os.environ.get('PACKTIVITY_REANA_APIHOST','job-controller.default.svc.cluster.local')
log = logging.getLogger(__name__)

BUFFER_TIME = 0.05

def submit(experiment, image, cmd, cvmfs = False, grid = False):
    time.sleep(BUFFER_TIME) #buffers to not hammer server when this is called in a tight loop

    job_spec = {
        'experiment': experiment,
        'docker-img': image,
        'cmd': cmd,
        'env-vars': {}
    }
    if cvmfs:
        job_spec['cvmfs_mounts'] = ['atlas-condb', 'atlas','sft']
        
    log.info('submitting %s',json.dumps(job_spec, indent = 4, sort_keys = True))

    for submit_try in range(10):
        try:
            response = requests.post(
                'http://{host}/{resource}'.format(
                    host=JOBCONTROLLER_HOST,
                    resource='jobs'
                ),
                json=job_spec,
                headers={'content-type': 'application/json'}
            )
            job_id = str(response.json()['job-id'])
            return job_id
        except requests.exceptions.ConnectionError:
            log.info('caught ConnectionError in submit try: %s.. try again in 10 seconds..',submit_try)
            pass
        time.sleep(10)

def check_status(job_id):
    time.sleep(BUFFER_TIME) #buffers to not hammer server when this is called in a tight loop

    for check_try in range(10):
        try:
            response = requests.get(
                'http://{host}/{resource}/{id}'.format(
                    host=JOBCONTROLLER_HOST,
                    resource='jobs',
                    id=job_id
                ),
                headers = {'cache-control':'no-cache'}
            )
            job_info = response.json()['job']
            return job_info
        except requests.exceptions.ConnectionError:
            log.info('caught ConnectionError in check_status try %s.. try again in 10 seconds',check_try)
            pass
        time.sleep(10)

