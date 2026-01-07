# aind-metadata-queries

[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
![Code Style](https://img.shields.io/badge/code%20style-black-black)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
![Interrogate](https://img.shields.io/badge/interrogate-45.8%25-red)
![Coverage](https://img.shields.io/badge/coverage-71%25-red)
![Python](https://img.shields.io/badge/python->=3.10-blue?logo=python)

## Usage
 - To use this repo: TODO

## Repo Structure
```
aind-metadata-queries/
├── README.md
├── src/
│   └── aind_metadata_queries/
│       ├── __init__.py
│       ├── core/
|           ├── __init__.py
|           ├── query_parameter.py
│           └── wrapped_query.py
│       ├── examples/
│           └── format_query_template.py
│       └── queries/
|           ├── __init__.py
│           └── all_records_from_subject_id.py
├── tests/
│   └── test_core.py
└── scripts/
    └── run_pipeline.py
```

### WrappedQuery
Useful queries are defined as classes that inherit from aind_metadata_queries.core.WrappedQuery. This provides a few key benefits:
 - Parameterization. Parameters can be defined by using aind_metadata_queries.core.QueryParameter, and properly formatted using WrappedQuery.format()
 - Post-processing. Best practices for using the DocDB suggest to use simple noSQL queries, and leave heavy computation for a post-processing step.

### QueryParameter
Queries can define user-provided parameters with aind_metadata_queries.core.QueryParameter. This gives all parameters the following properies:  
 - name (str)
 - description (str)
 - param_type (type object)
 - required (bool)
 - default (Any)
 - validator (Callable)
 
## Level of Support
Please indicate a level of support:
 - [ ] Supported: We are releasing this code to the public as a tool we expect others to use. Issues are welcomed, and we expect to address them promptly; pull requests will be vetted by our staff before inclusion.
 - [X] Occasional updates: We are planning on occasional updating this tool with no fixed schedule. Community involvement is encouraged through both issues and pull requests.
 - [ ] Unsupported: We are not currently supporting this code, but simply releasing it to the community AS IS but are not able to provide any guarantees of support. The community is welcome to submit issues, but you should not expect an active response.

## Release Status
GitHub's tags and Release features can be used to indicate a Release status.

 - Stable: v1.0.0 and above. Ready for production.
 - Beta:  v0.x.x or indicated in the tag. Ready for beta testers and early adopters.
 - Alpha: v0.x.x or indicated in the tag. Still in early development.

## Installation
To use the software, in the root directory, run
```bash
pip install -e .
```

To develop the code, run
```bash
pip install -e . --group dev
```
Note: --group flag is available only in pip versions >=25.1

Alternatively, if using `uv`, run
```bash
uv sync
```
