import connexion
import six

from openapi_server.models.full_task_payload import FullTaskPayload  # noqa: E501
from openapi_server.models.workflow_results import WorkflowResults  # noqa: E501
from openapi_server import util

import os
import subprocess
import api_utils
import json

def run_workflow_by_payload(full_task_payload=None):  # noqa: E501
    """runs a workflow and returns its results (TODO or delays them?) based off a (TODO given sequence of) workflow names and their (TODO scatterable) inputs

    The request here requires /full specification/, meaning that the user posts both a workflow to execute and all of the input that&#39;s needed. # noqa: E501

    :param full_task_payload: 
    :type full_task_payload: dict | bytes

    :rtype: WorkflowResults
    """
    if connexion.request.is_json:
        full_task_payload = FullTaskPayload.from_dict(connexion.request.get_json())  # noqa: E501

    name = full_task_payload.workflow_name
    input_name = full_task_payload.input_mappings

    workflow = os.path.abspath(api_utils.locate_workflows(name)[0])
    implementation = os.path.abspath(api_utils.locate_implementation(name)[0])
    inputs = os.path.abspath(api_utils.locate_inputs(input_name)[0])
    attachments = ",".join([implementation, workflow, inputs])
    wes_client_process_request = "wes-client --host={} --proto={} --attachments={} --run {} {}" \
        .format(api_utils.service["host"], api_utils.service["proto"], attachments, workflow, inputs)

    result = subprocess.check_output(wes_client_process_request, shell=True)
    result_json = json.loads(result)
    result_dict = dict(result_json)

    return dict(result_json), 200
