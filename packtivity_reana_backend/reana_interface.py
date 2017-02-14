import os
import requests
import json
import logging

JOBCONTROLLER_HOST = os.environ.get('PACKTIVITY_REANA_APIHOST','job-controller.default.svc.cluster.local')
log = logging.getLogger(__name__)

def submit(experiment, image, cmd, cvmfs = False, grid = False):
    job_spec = {
        'experiment': experiment,
        'docker-img': image,
        'cmd': cmd,
        'env-vars': {}
    }
    if cvmfs:
        job_spec['cvmfs_mounts'] = ['atlas-condb', 'atlas','sft'],
        

    log.info('submitting %s',json.dumps(job_spec, indent = 4, sort_keys = True))

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

def check_status(job_id):
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
