from aind_metadata_queries.core.wrapped_query import (
    QueryParameter,
    WrappedQuery,
)


class AllRecordsFromSubjectIdQuery(WrappedQuery):
    """A query to retrieve all records associated with a specific subject ID."""

    def __init__(self):
        name = "all_records_from_subject_id"

        query_template = {
            "subject.subject_id": QueryParameter(
                "subject_id", "The ID of the subject", str
            )
        }
        super().__init__(name, query_template, self.post_processing_function)

    def post_processing_function(self, records):
        """Post-process the retrieved records if necessary."""
        # Example post-processing: return just the subject metadata
        return [{"subject": record.get("subject", {})} for record in records]
