# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.full_task_payload import FullTaskPayload  # noqa: E501
from openapi_server.models.workflow_results import WorkflowResults  # noqa: E501
from openapi_server.test import BaseTestCase



class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_run_workflow_by_payload(self):
        """Test case for run_workflow_by_payload

        runs a workflow and returns its results (TODO or delays them?) based off a (TODO given sequence of) workflow names and their (TODO scatterable) inputs
        """
        full_task_payload = {
          "workflow_name" : "workflow_name",
          "input_mappings" : "input_mappings"
        }
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/run/workflow/',
            method='POST',
            headers=headers,
            data=json.dumps(full_task_payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
