import json
from types import SimpleNamespace
from typing import List

from mediahaven.resources.base_resource import (
    MediaHavenPageObjectJSON,
    MediaHavenSingleObjectJSON,
)


class MediaHavenSingleObjectJSONMock(MediaHavenSingleObjectJSON):
    def __init__(self, data: dict):
        self._single_result: SimpleNamespace = json.loads(
            json.dumps(data), object_hook=lambda d: SimpleNamespace(**d)
        )


class MediaHavenPageObjectJSONMock(MediaHavenPageObjectJSON):
    def __init__(
        self,
        results: List[dict],
        nr_of_results: int = 1,
        start_index: int = 0,
        total_nr_of_results: int = 1,
    ):
        paged_dict = {
            "NrOfResults": nr_of_results,
            "StartIndex": start_index,
            "TotalNrOfResults": total_nr_of_results,
            "Results": results,
        }
        self._page_result: SimpleNamespace = json.loads(
            json.dumps(paged_dict), object_hook=lambda d: SimpleNamespace(**d)
        )

        self._total_nr_of_results = total_nr_of_results
        self._nr_of_results = nr_of_results
        self._start_index = start_index

        self._has_more = self.total_nr_of_results > (
            self.nr_of_results + self.start_index
        )
