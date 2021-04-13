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

        assert resp == resp_json
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].response.json() == resp_json

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
