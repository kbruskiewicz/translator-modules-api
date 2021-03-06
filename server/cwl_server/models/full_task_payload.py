# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from cwl_server.models.base_model_ import Model
from cwl_server import util


class FullTaskPayload(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, workflow_name=None, input_mappings=None):  # noqa: E501
        """FullTaskPayload - a model defined in OpenAPI

        :param workflow_name: The workflow_name of this FullTaskPayload.  # noqa: E501
        :type workflow_name: str
        :param input_mappings: The input_mappings of this FullTaskPayload.  # noqa: E501
        :type input_mappings: str
        """
        self.openapi_types = {
            'workflow_name': str,
            'input_mappings': str
        }

        self.attribute_map = {
            'workflow_name': 'workflow_name',
            'input_mappings': 'input_mappings'
        }

        self._workflow_name = workflow_name
        self._input_mappings = input_mappings

    @classmethod
    def from_dict(cls, dikt) -> 'FullTaskPayload':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FullTaskPayload of this FullTaskPayload.  # noqa: E501
        :rtype: FullTaskPayload
        """
        return util.deserialize_model(dikt, cls)

    @property
    def workflow_name(self):
        """Gets the workflow_name of this FullTaskPayload.

        A symbol corresponding to the workflow specification and module script  # noqa: E501

        :return: The workflow_name of this FullTaskPayload.
        :rtype: str
        """
        return self._workflow_name

    @workflow_name.setter
    def workflow_name(self, workflow_name):
        """Sets the workflow_name of this FullTaskPayload.

        A symbol corresponding to the workflow specification and module script  # noqa: E501

        :param workflow_name: The workflow_name of this FullTaskPayload.
        :type workflow_name: str
        """
        if workflow_name is None:
            raise ValueError("Invalid value for `workflow_name`, must not be `None`")  # noqa: E501

        self._workflow_name = workflow_name

    @property
    def input_mappings(self):
        """Gets the input_mappings of this FullTaskPayload.


        :return: The input_mappings of this FullTaskPayload.
        :rtype: str
        """
        return self._input_mappings

    @input_mappings.setter
    def input_mappings(self, input_mappings):
        """Sets the input_mappings of this FullTaskPayload.


        :param input_mappings: The input_mappings of this FullTaskPayload.
        :type input_mappings: str
        """
        if input_mappings is None:
            raise ValueError("Invalid value for `input_mappings`, must not be `None`")  # noqa: E501

        self._input_mappings = input_mappings
