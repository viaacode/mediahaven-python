import json
from unittest.mock import patch

import pytest
import responses
from oauthlib.oauth2.rfc6749.errors import (
    TokenExpiredError,
)
from requests import RequestException
from urllib.parse import urljoin

from mediahaven.mediahaven import (
    AcceptFormat,
    ContentType,
    MediaHavenClient,
    MediaHavenException,
)


class TestMediahaven:
    @responses.activate
    def test_get(self, mh_client: MediaHavenClient):
        # Arrange
        record_id = "1"
        resp_json = {
            "internal": {
                "RecordId": record_id,
            }
        }
        resource_path = f"get_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        responses.get(
            url,
            json=resp_json,
            status=200,
        )

        # Act
        resp = mh_client._get(resource_path, AcceptFormat.JSON)

        # Assert
        assert len(responses.calls) == 1
        assert resp.json() == resp_json
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.headers["Accept"] == AcceptFormat.JSON.value
        assert (
            responses.calls[0].response.headers["Content-Type"]
            == AcceptFormat.JSON.value
        )
        assert responses.calls[0].response.json() == resp_json
        assert responses.calls[0].response.status_code == 200

    @responses.activate
    def test_get_404(self, mh_client):
        # Arrange
        record_id = "1"
        resp_json = {"error": "not found"}
        resource_path = f"get_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)
        responses.get(
            url,
            json=resp_json,
            status=404,
        )

        # Act
        with pytest.raises(MediaHavenException) as mhe:
            mh_client._get(resource_path, AcceptFormat.JSON)

        # Assert
        assert len(responses.calls) == 1
        assert responses.calls[0].response.status_code == 404
        assert mhe.value.status_code == 404
        assert mhe.value.args[0] == resp_json

    @responses.activate
    def test_head(self, mh_client):
        # Arrange
        record_id = "1"
        result_count = "1"
        resp_headers = {"Result-Count": result_count}
        query = f'(MediaObjectId:"{record_id}")'
        encoded_query = mh_client._encode_query_params(q=query)
        resource_path = "head_resource"
        url = f"{urljoin(mh_client.mh_api_url, resource_path)}?{encoded_query}"
        responses.head(
            url,
            headers=resp_headers,
            status=200,
        )

        resp = mh_client._head(resource_path, q=query)
        assert resp == 1
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].response.headers["Result-Count"] == result_count
        assert responses.calls[0].response.status_code == 200

    @responses.activate
    def test_head_400(self, mh_client):
        # Arrange
        record_id = "1"
        query = f'(MediaObjectId:"{record_id}")'
        encoded_query = mh_client._encode_query_params(q=query)
        resource_path = "head_resource/"
        url = f"{urljoin(mh_client.mh_api_url, resource_path)}?{encoded_query}"
        responses.head(
            url,
            status=400,
        )

        # Act
        with pytest.raises(MediaHavenException) as mhe:
            mh_client._head(resource_path, q=query)

        # Assert
        assert len(responses.calls) == 1
        assert responses.calls[0].response.status_code == 400
        assert mhe.value.status_code == 400

    @responses.activate
    @pytest.mark.parametrize("status,result", [(204, True), (200, False)])
    def test_delete(self, mh_client, status, result):
        # Arrange
        record_id = "1"
        resource_path = f"delete_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)
        responses.delete(
            url,
            status=status,
        )

        # Act
        resp = mh_client._delete(resource_path, Reason="reason", EventType="subtype")

        # Assert
        assert resp is result
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body.decode("utf8")
            == '{"Reason": "reason", "EventType": "subtype"}'
        )
        assert responses.calls[0].response.status_code == status

    @responses.activate
    def test_delete_404(self, mh_client):
        # Arrange
        record_id = "1"
        resource_path = f"delete_resource/{record_id}"
        resp_json = {"error": "not found"}
        url = urljoin(mh_client.mh_api_url, resource_path)
        responses.delete(
            url,
            json=resp_json,
            status=404,
        )

        # Act
        with pytest.raises(MediaHavenException) as mhe:
            mh_client._delete(resource_path, Reason="reason", EventType="subtype")

        # Assert
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body.decode("utf8")
            == '{"Reason": "reason", "EventType": "subtype"}'
        )
        assert responses.calls[0].response.status_code == 404
        assert mhe.value.status_code == 404
        assert mhe.value.args[0] == resp_json

    @responses.activate
    @pytest.mark.parametrize(
        "status",
        [
            200,
            201,
            202,
            203,
            205,
            206,
        ],
    )
    def test_post_json(self, mh_client, status):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = {"description": "New description"}
        response = {"recordId": 1}

        responses.post(url, status=status, body=json.dumps(response))

        # Act
        resp = mh_client._post(resource_path, json=payload)

        # Assert
        assert resp == response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body.decode("utf8") == json.dumps(payload)
        assert responses.calls[0].response.status_code == status

    @responses.activate
    def test_post_json_empty_response_body(self, mh_client):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = {"description": "New description"}

        responses.post(url, status=204)

        # Act
        resp = mh_client._post(resource_path, json=payload)

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body.decode("utf8") == json.dumps(payload)
        assert responses.calls[0].response.status_code == 204

    @responses.activate
    @pytest.mark.parametrize(
        "status",
        [
            200,
            201,
            202,
            203,
            205,
            206,
        ],
    )
    def test_post_xml(self, mh_client, status):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = "<description>New description</description>"
        response = {"recordId": 1}

        responses.post(
            url,
            status=status,
            body=json.dumps(response),
        )

        # Act
        resp = mh_client._post(resource_path, xml=payload)

        # Assert
        assert resp == response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.headers["Content-Type"] == "application/xml"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == payload
        assert responses.calls[0].response.status_code == status

    @responses.activate
    def test_post_xml_empty_response_body(self, mh_client):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = "<description>New description</description>"

        responses.post(
            url,
            status=204,
        )

        # Act
        resp = mh_client._post(resource_path, xml=payload)

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.headers["Content-Type"] == "application/xml"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == payload
        assert responses.calls[0].response.status_code == 204

    @responses.activate
    @pytest.mark.parametrize(
        "status",
        [
            200,
            201,
            202,
            203,
            205,
            206,
        ],
    )
    def test_post_form_data(self, mh_client, status):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = {"description": "New description"}
        response = {"recordId": 1}

        responses.post(url, status=status, body=json.dumps(response))

        # Act
        resp = mh_client._post(
            resource_path,
            files={"metadata": ("metadata", "<metadata/>", ContentType.XML.value)},
            **payload,
        )

        # Assert
        assert resp == response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert (
            "multipart/form-data" in responses.calls[0].request.headers["Content-Type"]
        )
        assert responses.calls[0].request.url == url
        assert "New description" in str(responses.calls[0].request.body)
        assert responses.calls[0].response.status_code == status

    @responses.activate
    def test_post_form_data_empty_response_body(self, mh_client):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = {"description": "New description"}

        responses.post(url, status=204)

        # Act
        resp = mh_client._post(
            resource_path,
            files={"metadata": ("metadata", "<metadata/>", ContentType.XML.value)},
            **payload,
        )

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert (
            "multipart/form-data" in responses.calls[0].request.headers["Content-Type"]
        )
        assert responses.calls[0].request.url == url
        assert "New description" in str(responses.calls[0].request.body)
        assert responses.calls[0].response.status_code == 204

    @responses.activate
    def test_post_value_error(self, mh_client):
        # Arrange
        record_id = "1"
        resource_path = f"post_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload_json = {"description": "New description"}
        payload_xml = "<description>New description</description>"
        payload_form = {"description": "New description"}
        responses.post(
            url,
            status=204,
        )

        # Act
        with pytest.raises(ValueError) as ve:
            mh_client._post(
                resource_path, json=payload_json, xml=payload_xml, **payload_form
            )

        # Assert
        assert (
            ve.value.args[0]
            == "Only one payload value is allowed (json, xml or form_data)"
        )

    @responses.activate
    @pytest.mark.parametrize(
        "status",
        [
            204,
            200,
        ],
    )
    def test_put_json(self, mh_client, status):
        # Arrange
        record_id = "1"
        resource_path = f"put_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = {"description": "New description"}

        responses.put(
            url,
            status=status,
        )

        # Act
        resp = mh_client._put(resource_path, json=payload)

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PUT"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body.decode("utf8") == json.dumps(payload)
        assert responses.calls[0].response.status_code == status

    @responses.activate
    @pytest.mark.parametrize(
        "status",
        [
            204,
            200,
        ],
    )
    def test_put_xml(self, mh_client, status):
        # Arrange
        record_id = "1"
        resource_path = f"put_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload = "<description>New description</description>"

        responses.put(
            url,
            status=status,
        )

        # Act
        resp = mh_client._put(resource_path, xml=payload)

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "PUT"
        assert responses.calls[0].request.headers["Content-Type"] == "application/xml"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == payload
        assert responses.calls[0].response.status_code == status

    @responses.activate
    def test_put_value_error(self, mh_client):
        # Arrange
        record_id = "1"
        resource_path = f"put_resource/{record_id}"
        url = urljoin(mh_client.mh_api_url, resource_path)

        payload_json = {"description": "New description"}
        payload_xml = "<description>New description</description>"

        responses.put(
            url,
            status=204,
        )

        # Act
        with pytest.raises(ValueError) as ve:
            mh_client._put(resource_path, json=payload_json, xml=payload_xml)

        # Assert
        assert ve.value.args[0] == "Only one payload value is allowed (json or xml)"

    @patch(
        "requests.sessions.Session.request",
        side_effect=(TokenExpiredError("Token expired"), {"internal": {"test"}}),
    )
    def test_execute_request_token_expired(self, session_mock, mh_client):
        # Act
        resp = mh_client._execute_request()

        # Assert
        assert session_mock.call_count == 2
        assert resp == {"internal": {"test"}}

    @patch("requests.sessions.Session.request", side_effect=RequestException)
    def test_execute_request_exception(self, session_mock, mh_client):
        # Act and Assert
        with pytest.raises(RequestException):
            mh_client._execute_request()
