import unittest


class WrappedQueryTest(unittest.TestCase):
    """Test cases for WrappedQuery class."""

    def test_parameter_none_handling(self):
        """Test that parameters with None values are handled correctly."""
        from aind_metadata_queries.core.query_parameter import QueryParameter
        from aind_metadata_queries.core.wrapped_query import WrappedQuery

        query_template = {
            "subject.subject_id": QueryParameter(
                name="subject_id",
                description="The subject ID of interest",
                param_type=str,
                required=False,
                default=None,
            ),
        }

        wrapped_query = WrappedQuery(
            name="foo query", query_template=query_template
        )

        # Test with parameter not provided
        parameters = {}
        formatted_query = wrapped_query.format(parameters)
        expected_query = {}  # Criterion should be omitted
        self.assertEqual(formatted_query, expected_query)

        # Test with parameter 'subject_id' set to None
        parameters = {"subject_id": None}
        formatted_query = wrapped_query.format(parameters)
        expected_query = {
            "subject.subject_id": None
        }  # Criterion should check for None
        self.assertEqual(formatted_query, expected_query)

        # Test with parameter 'subject_id' set to a valid string
        parameters = {"subject_id": "bar"}
        formatted_query = wrapped_query.format(parameters)
        expected_query = {"subject.subject_id": "bar"}
        self.assertEqual(formatted_query, expected_query)


if __name__ == "__main__":
    unittest.main()
