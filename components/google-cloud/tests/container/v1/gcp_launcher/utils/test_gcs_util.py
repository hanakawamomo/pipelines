# Copyright 2021 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import storage
from google_cloud_pipeline_components.container.v1.gcp_launcher.utils import gcs_util

import unittest
from unittest import mock


class GcsUtilTests(unittest.TestCase):

  def setUp(self):
    super(GcsUtilTests, self).setUp()
    self._project = 'test_project'
    self._location = 'test_region'
    self._test_bucket_name = 'test_bucket_name'
    self._test_blob_path = 'test_blob_path'
    self._gcs_temp_path = f'gs://{self._test_bucket_name}/{self._test_blob_path}'

  def test_parse_blob_path_returns_bucket_name_and_blob_name(self):
    result = gcs_util.parse_blob_path(self._gcs_temp_path)
    self.assertEqual(result, (self._test_bucket_name, self._test_blob_path))

  def test_parse_blob_path_raises_value_error_for_invalid_path(self):
    with self.assertRaises(ValueError):
      gcs_util.parse_blob_path('not_gs://test_invalid_path')

  @mock.patch.object(storage, 'Client', autospec=True)
  def test_read_text_from_gcs(self, mock_client):
    mock_storage_client = mock.Mock()
    mock_client.return_value = mock_storage_client
    mock_bucket = mock.Mock()
    mock_storage_client.get_bucket.return_value = mock_bucket
    mock_blob = mock.Mock()
    mock_bucket.blob.return_value = mock_blob

    gcs_util.read_text_from_gcs(self._gcs_temp_path)

    mock_storage_client.get_bucket.assert_called_once_with(
        self._test_bucket_name)
    mock_bucket.blob.assert_called_once_with(self._test_blob_path)
    mock_blob.download_as_text.assert_called_once()
