#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Tuple, Union

from mediahaven.mediahaven import MediaHavenClient

# Records
from mediahaven.resources.records import Records
from mediahaven.resources.field_definitions import FieldDefinitions
from mediahaven.resources.organisations import Organisations


class MediaHaven(MediaHavenClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = Records(self)
        self.field_definitions = FieldDefinitions(self)
        self.organisations = Organisations(self)

class MediaHavenQuery:
    "MediaHaven query object."

    def __init__(self, ):
        self._clauses = []

    def add_clauses(self, query_params: Union[List[Tuple[str, str]], List[str]] , exclude: bool = False, is_and: bool = False):
        """Adds clauses to the query.

        Args:
            query_params: A list of tuples containing the query parameters (field and value), or a string containing free text.
            exclude: If true the clauses will be excluded from the query.
            is_and: If true the clauses will be combined with an AND operator, otherwise with an OR operator.
        """


        self._clauses.append(
            {
                "query_params": query_params,
                "operator": ("-" if exclude else "+"),
                "is_and": is_and
            }
        )

    def generate_query(self) -> str:
        """Generates the query string.

        Returns:
            The query string.
        """

        query = " ".join(
            [
                f'{clause["operator"]}(' + ' '.join(
                    [f'{k_v[0]}:"{k_v[1]}"' for k_v in clause["query_params"]]
                    if isinstance(clause["query_params"][0], Tuple)
                    else [f'{v}' for v in clause["query_params"]]
                ) + ')'
                if not clause["is_and"]
                else " ".join(
                    [f'{clause["operator"]}({k_v[0]}:"{k_v[1]}")' for k_v in clause["query_params"]]
                    if isinstance(clause["query_params"][0], Tuple)
                    else [f'{clause["operator"]}({v})' for v in clause["query_params"]]
                )
                for clause in self._clauses
            ]
        )
        
        return query