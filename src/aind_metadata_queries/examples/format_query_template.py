"""Example of formatting a query template with parameters."""

# Import the necessary query from the registry, or the entire registry
from aind_metadata_queries.queries import QUERIES_REGISTRY


# Function to pretty-print a dictionary
def pretty_print_dict(d):
    import json

    print(json.dumps(d, indent=2))


# Main function to demonstrate formatting
def run():
    # Retrieve the query template from the registry
    query_template = QUERIES_REGISTRY["all_records_from_subject_id"]

    # Define parameters to format the query template (name must match QueryParameter names)
    my_parameters = {"subject_id": "my_subject_123"}
    formatted = query_template.format(my_parameters)

    # pretty print dict with 2 spaces indent
    pretty_print_dict(formatted)


if __name__ == "__main__":
    run()
