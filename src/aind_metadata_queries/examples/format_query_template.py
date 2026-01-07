"""Example of formatting a query template with parameters."""

# Import the necessary query from the registry, or the entire registry
from aind_metadata_queries.queries import QUERIES_REGISTRY

# Main function to demonstrate formatting
def run():
    # Retrieve the query template from the registry
    wrapped_query = QUERIES_REGISTRY["all_records_from_subject_id"]

    # Define parameters to format the query template (name must match QueryParameter names)
    my_parameters_dict = {"subject_id": "123456"}
    formatted_nosql_query = wrapped_query.format(my_parameters)

    print("Final query", formatted_nosql_query)

    # HERE use aind-data-access-api to query metadata DocDB.
    records = [] # response will be a list of dicts
    processed_records = wrapped_query.post_processing_function(records)

    # HERE use processed records


if __name__ == "__main__":
    run()
