import json

import pytest
import responses
from urllib.parse import urljoin

from mediahaven.mediahaven import AcceptFormat, MediaHavenClient, MediaHavenException


class TestMediahaven:
    @responses.activate
    def test_get(self, mh_client: MediaHavenClient):
        # Arrange
        media_id = "1"
        resp_json = {
            "internal": {
                "RecordId": media_id,
            }
        }
        resource_path = f"get_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        responses.add(
            responses.GET,
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
        media_id = "1"
        resp_json = {"error": "not found"}
        resource_path = f"get_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)
        responses.add(
            responses.GET,
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
        media_id = "1"
        result_count = "1"
        resp_headers = {"Result-Count": result_count}
        query = f'(MediaObjectId:"{media_id}")'
        encoded_query = mh_client._encode_query_params(q=query)
        resource_path = "head_resource"
        url = f"{urljoin(mh_client.base_url_path, resource_path)}?{encoded_query}"
        responses.add(
            responses.HEAD,
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
        media_id = "1"
        query = f'(MediaObjectId:"{media_id}")'
        encoded_query = mh_client._encode_query_params(q=query)
        resource_path = "head_resource/"
        url = f"{urljoin(mh_client.base_url_path, resource_path)}?{encoded_query}"
        responses.add(
            responses.HEAD,
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
        media_id = "1"
        resource_path = f"delete_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)
        responses.add(
            responses.DELETE,
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
        media_id = "1"
        resource_path = f"delete_resource/{media_id}"
        resp_json = {"error": "not found"}
        url = urljoin(mh_client.base_url_path, resource_path)
        responses.add(
            responses.DELETE,
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
            204,
            200,
        ],
    )
    def test_post_json(self, mh_client, status):
        # Arrange
        media_id = "1"
        resource_path = f"post_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload = {"description": "New description"}

        responses.add(
            responses.POST,
            url,
            status=status,
        )

        # Act
        resp = mh_client._post(resource_path, json=payload)

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
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
    def test_post_xml(self, mh_client, status):
        # Arrange
        media_id = "1"
        resource_path = f"post_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload = "<description>New description</description>"

        responses.add(
            responses.POST,
            url,
            status=status,
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
        assert responses.calls[0].response.status_code == status

    @responses.activate
    @pytest.mark.parametrize(
        "status",
        [
            204,
            200,
        ],
    )
    def test_post_form_data(self, mh_client, status):
        # Arrange
        media_id = "1"
        resource_path = f"post_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload = {"description": "New description"}

        responses.add(
            responses.POST,
            url,
            status=status,
        )

        # Act
        resp = mh_client._post(resource_path, **payload)

        # Assert
        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert (
            "multipart/form-data" in responses.calls[0].request.headers["Content-Type"]
        )
        assert responses.calls[0].request.url == url
        assert "New description" in str(responses.calls[0].request.body)
        assert responses.calls[0].response.status_code == status

    def test_post_value_error(self, mh_client):
        # Arrange
        media_id = "1"
        resource_path = f"post_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload_json = {"description": "New description"}
        payload_xml = "<description>New description</description>"
        payload_form = {"description": "New description"}
        responses.add(
            responses.POST,
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
        media_id = "1"
        resource_path = f"put_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload = {"description": "New description"}

        responses.add(
            responses.PUT,
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
        media_id = "1"
        resource_path = f"put_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload = "<description>New description</description>"

        responses.add(
            responses.PUT,
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

    def test_put_value_error(self, mh_client):
        # Arrange
        media_id = "1"
        resource_path = f"put_resource/{media_id}"
        url = urljoin(mh_client.base_url_path, resource_path)

        payload_json = {"description": "New description"}
        payload_xml = "<description>New description</description>"

        responses.add(
            responses.PUT,
            url,
            status=204,
        )

        # Act
        with pytest.raises(ValueError) as ve:
            mh_client._put(resource_path, json=payload_json, xml=payload_xml)

        # Assert
        assert ve.value.args[0] == "Only one payload value is allowed (json or xml)"
