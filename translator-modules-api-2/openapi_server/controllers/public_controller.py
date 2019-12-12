import connexion
import six

from openapi_server.models.full_task_payload import FullTaskPayload  # noqa: E501
from openapi_server.models.workflow_results import WorkflowResults  # noqa: E501
from openapi_server import util

from pathlib import Path
import os
import subprocess

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
    inputs = full_task_payload.input_mappings

    workflow = os.path.abspath(api_utils.locate_workflows("disease_associated_genes")[0])
    implementation = os.path.abspath(api_utils.locate_implementation("disease_associated_genes")[0])
    input = os.path.abspath(api_utils.inputs_dir+"disease.yaml")
    attachments = ",".join([implementation, workflow, input])
    wes_client_process_request = 'wes-client --host={} --proto={} --attachments="{}" --run {} {}'\
        .format(api_utils.service["host"], api_utils.service["proto"], attachments, workflow, input)

    result = subprocess.check_output(wes_client_process_request, shell=True)

    return result, 200
