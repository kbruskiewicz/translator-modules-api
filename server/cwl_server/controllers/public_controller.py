import connexion
import six
from cwl_server.controllers.controller_impl import handle_run_workflow

from cwl_server.models.full_task_payload import FullTaskPayload  # noqa: E501
from cwl_server.models.workflow_results import WorkflowResults  # noqa: E501
from cwl_server import util


def run_workflow_by_payload(full_task_payload=None):  # noqa: E501
    """runs a workflow and returns its results (TODO or delays them?) based off a (TODO given sequence of) workflow names and their (TODO scatterable) inputs

    The request here requires /full specification/, meaning that the user posts both a workflow to execute and all of the input that&#39;s needed. # noqa: E501

    :param full_task_payload: 
    :type full_task_payload: dict | bytes

    :rtype: WorkflowResults
    """
    if connexion.request.is_json:
        full_task_payload = FullTaskPayload.from_dict(connexion.request.get_json())  # noqa: E501
    return handle_run_workflow(full_task_payload)
