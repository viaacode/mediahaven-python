import json
import pytest
import responses

from mediahaven.mediahaven import MediaHavenException
from mediahaven.resources.records import Records


class TestRecords:
    @pytest.fixture(scope="class")
    def records(self, mh_client):
        return Records(mh_client)

    @responses.activate
    def test_get(self, records):
        media_id = "1"
        resp_json = {
            "internal": {
                "RecordId": media_id,
            }
        }
        url = f"{records.mh_client.base_url_path}{records._construct_path(media_id)}"
        responses.add(
            responses.GET,
            url,
            json=resp_json,
            status=200,
        )

        resp = records.get(media_id)

        assert json.loads(resp.raw_response) == resp_json
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].response.json() == resp_json
        assert responses.calls[0].response.status_code == 200

    @responses.activate
    def test_get_404(self, records):
        media_id = "1"
        resp_json = {"error": "not found"}
        url = f"{records.mh_client.base_url_path}{records._construct_path(media_id)}"
        responses.add(
            responses.GET,
            url,
            json=resp_json,
            status=404,
        )

        with pytest.raises(MediaHavenException) as mhe:
            records.get(media_id)
        assert mhe.value.status_code == 404
        assert mhe.value.args[0] == resp_json

    @responses.activate
    def test_search(self, records):
        media_id = "1"
        resp_json = {
            "NrOfResults": 1,
            "Results": [
                {
                    "internal": {
                        "RecordId": media_id,
                    }
                }
            ],
            "StartIndex": 0,
            "TotalNrOfResults": 1,
        }
        query = f'(MediaObjectId:"{media_id}")'
        encoded_query = records.mh_client._encode_query_params(q=query)
        url = f"{records.mh_client.base_url_path}{records._construct_path()}?{encoded_query}"

        responses.add(
            responses.GET,
            url,
            json=resp_json,
            status=200,
        )

        resp = records.search(q=query)

        assert json.loads(resp.raw_response) == resp_json
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].response.json() == resp_json
        assert responses.calls[0].response.status_code == 200

    @responses.activate
    def test_count(self, records):
        result_count = "1"
        resp_headers = {"Result-Count": result_count}
        query = '(MediaObjectId:"1")'
        encoded_query = records.mh_client._encode_query_params(q=query)
        url = f"{records.mh_client.base_url_path}{records._construct_path()}?{encoded_query}"
        responses.add(
            responses.HEAD,
            url,
            headers=resp_headers,
            status=200,
        )

        resp = records.count(query)
        assert resp == 1
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].response.headers["Result-Count"] == result_count
        assert responses.calls[0].response.status_code == 200

    @responses.activate
    def test_delete(self, records):
        media_id = "1"
        url = f"{records.mh_client.base_url_path}{records._construct_path(media_id)}"
        responses.add(
            responses.DELETE,
            url,
            status=204,
        )

        resp = records.delete(media_id)

        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].response.status_code == 204

    @responses.activate
    def test_update_json(self, records):
        media_id = "1"
        url = f"{records.mh_client.base_url_path}{records._construct_path(media_id)}"

        payload = {"description": "New description"}

        responses.add(
            responses.POST,
            url,
            status=204,
        )

        resp = records.update(media_id, json=payload)

        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body.decode("utf8") == json.dumps(payload)
        assert responses.calls[0].response.status_code == 204

    @responses.activate
    def test_update_xml(self, records):
        media_id = "1"
        url = f"{records.mh_client.base_url_path}{records._construct_path(media_id)}"

        payload = "<description>New description</description>"

        responses.add(
            responses.POST,
            url,
            status=204,
        )

        resp = records.update(media_id, xml=payload)

        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.headers["Content-Type"] == "application/xml"
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == payload
        assert responses.calls[0].response.status_code == 204

    @responses.activate
    def test_update_form_data(self, records):
        media_id = "1"
        url = f"{records.mh_client.base_url_path}{records._construct_path(media_id)}"

        payload = {"description": "New description"}

        responses.add(
            responses.POST,
            url,
            status=204,
        )

        resp = records.update(media_id, **payload)

        assert resp is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert (
            "multipart/form-data" in responses.calls[0].request.headers["Content-Type"]
        )
        assert responses.calls[0].request.url == url
        assert "New description" in str(responses.calls[0].request.body)
        assert responses.calls[0].response.status_code == 204
