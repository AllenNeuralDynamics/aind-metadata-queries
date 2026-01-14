from aind_data_access_api.document_db import MetadataDbClient

API_GATEWAY_HOST = "api.allenneuraldynamics.org"
DATABASE = "metadata_index"
COLLECTION = "data_assets"

docdb_api_client = MetadataDbClient(
    host=API_GATEWAY_HOST,
    database=DATABASE,
    collection=COLLECTION,
)

def build_modality_pipeline(subject_id: str, modalities: list[str]) -> list[dict]:
    """
    Build a MongoDB aggregation pipeline to find derived data records
    that have ALL specified modalities for a given subject.
    
    Parameters
    ----------
        subject_id : str
            The subject ID to filter records by.
        modalities : list[str]
            List of modality abbreviations to filter records by.
    
    Returns
    -------
        list[dict]
            MongoDB aggregation pipeline
    """
    if not modalities:
        raise ValueError("At least one modality must be specified")
    
    pipeline = [
        {
            "$match": {
                "subject.subject_id": subject_id,
                "data_description.data_level": "derived",
            }
        },
        {"$unwind": "$data_description.modalities"},
        {"$unwind": "$data_description.source_data"},
        {
            "$match": {
                "data_description.modalities.abbreviation": {"$in": modalities}
            }
        },
        {"$sort": {"data_description.creation_time": -1}},
        {
            "$group": {
                "_id": {
                    "source_data": "$data_description.source_data",
                    "modality": "$data_description.modalities.abbreviation",
                },
                "doc": {"$first": "$$ROOT"},
            }
        },
        {
            "$group": {
                "_id": "$_id.source_data",
                **{
                    modality: {
                        "$max": {
                            "$cond": [
                                {"$eq": ["$_id.modality", modality]},
                                "$doc",
                                None,
                            ]
                        }
                    }
                    for modality in modalities
                },
            }
        },
        {
            "$match": {
                modality: {"$ne": None}
                for modality in modalities
            }
        },
        {
            "$project": {
                "_id": 0,
                "source_data": "$_id",
                **{
                    modality: {
                        "name": f"${modality}.data_description.name",
                        "location": f"${modality}.location",
                    }
                    for modality in modalities
                },
            }
        },
    ]
    
    return pipeline

if __name__ == "__main__":
    subject_id = "123456"
    modalities = ["pophys", "behavior"]
    pipeline = build_modality_pipeline(subject_id, modalities)
    results = docdb_api_client.aggregate_docdb_records(pipeline)