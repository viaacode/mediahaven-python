import pytest
from unittest.mock import patch

from mediahaven import MediaHavenQuery

class TestQuery:
    @pytest.fixture()
    def query(self):
        return MediaHavenQuery()

    def test_include_or(self, query: MediaHavenQuery):
        # Arrange
        query_params = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params)

        #Act 
        query_string = query.generate_query()

        #Assert
        assert query_string == '+(dc_title:"title1" dc_title:"title2")'

    def test_include_and(self, query: MediaHavenQuery):
        # Arrange
        query_params = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params, is_and=True)

        #Act 
        query_string = query.generate_query()

        #Assert
        assert query_string == '+(dc_title:"title1") +(dc_title:"title2")'

    def test_exclude_or(self, query: MediaHavenQuery):
        # Arrange
        query_params = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params, exclude=True)

        #Act 
        query_string = query.generate_query()

        #Assert
        assert query_string == '-(dc_title:"title1" dc_title:"title2")'

    def test_exclude_and(self, query: MediaHavenQuery):
        # Arrange
        query_params = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params, exclude=True, is_and=True)

        #Act 
        query_string = query.generate_query()

        #Assert
        assert query_string == '-(dc_title:"title1") -(dc_title:"title2")'

    def test_include_and_exclude_or(self, query: MediaHavenQuery):
        # Arrange
        query_params_1 = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params_1, is_and=True)

        query_params_2 = [
            ("dc_description", "description1"),
            ("dc_description", "description2"),
        ]
        query.add_clauses(query_params_2, exclude=True)

        #Act
        query_string = query.generate_query()

        #Assert
        assert query_string == '+(dc_title:"title1") +(dc_title:"title2") -(dc_description:"description1" dc_description:"description2")'

    def test_include_or_exclude_and(self, query: MediaHavenQuery):
        # Arrange
        query_params_1 = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params_1)

        query_params_2 = [
            ("dc_description", "description1"),
            ("dc_description", "description2"),
        ]
        query.add_clauses(query_params_2, exclude=True, is_and=True)

        #Act
        query_string = query.generate_query()

        #Assert
        assert query_string == '+(dc_title:"title1" dc_title:"title2") -(dc_description:"description1") -(dc_description:"description2")'

    def test_include_and_exclude_and(self, query: MediaHavenQuery):
        # Arrange
        query_params_1 = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params_1, is_and=True)

        query_params_2 = [
            ("dc_description", "description1"),
            ("dc_description", "description2"),
        ]
        query.add_clauses(query_params_2, exclude=True, is_and=True)

        #Act
        query_string = query.generate_query()

        #Assert
        assert query_string == '+(dc_title:"title1") +(dc_title:"title2") -(dc_description:"description1") -(dc_description:"description2")'

    def test_include_or_exclude_or(self, query: MediaHavenQuery):
        # Arrange
        query_params_1 = [
            ("dc_title", "title1"),
            ("dc_title", "title2"),
        ]
        query.add_clauses(query_params_1)

        query_params_2 = [
            ("dc_description", "description1"),
            ("dc_description", "description2"),
        ]
        query.add_clauses(query_params_2, exclude=True)

        #Act
        query_string = query.generate_query()

        #Assert
        assert query_string == '+(dc_title:"title1" dc_title:"title2") -(dc_description:"description1" dc_description:"description2")'
