from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aind_metadata_queries.core.query_parameter import QueryParameter

_MISSING_PARAMETER = object()


class WrappedQuery:
    """A class that wraps a query template.

    Parameters
    ----------
    name : str
        The name of the query.
    query_template : dict
        The query template containing QueryParameter instances.
    post_processing_function : Callable, optional
        A function to post-process the retrieved records. Default is None.
        Signature: Callable[[list[dict]], list[dict]]
    """

    def __init__(
        self,
        name: str,
        query_template: dict,
        post_processing_function: Callable[[list[dict]], list[dict]] = None,
    ):
        self.name = name
        self.query_template = query_template
        self.post_processing_function = post_processing_function

    def format(self, parameters: dict) -> dict:  # noqa: C901
        """
        Format the query template by replacing QueryParameter instances with actual
        values from ``parameters``.

        Parameter presence
        ------------------
        A parameter is considered "provided" only if its name appears as a key in the
        ``parameters`` mapping when calling this function. Providing a value of ``None``
        counts as providing the parameter and will be passed through unless rejected by
        the QueryParameter's validator.

        Extra parameters
        ----------------
        If ``parameters`` contains keys that are not referenced by any QueryParameter in
        the template, they are ignored.

        Rules
        -----
        - If a QueryParameter name is provided in ``parameters`` keys:
        - Use the provided value.
        - If a QueryParameter name is not provided in ``parameters`` keys:
        - If the QueryParameter is required:
            - Raise ``ValueError``.
        - If the QueryParameter is not required:
            - If the QueryParameter's default is ``None``, omit the key/value pair.
            - If the QueryParameter's default is not ``None``, use the default value.

        Type checking
        -------------
        - If the resolved value is not ``None``, it must be an instance of
        ``QueryParameter.param_type``; otherwise raise ``TypeError``.
        - If the resolved value is ``None``, type checking is skipped (use ``validator``
        to forbid ``None`` if desired).

        Validation
        ----------
        If ``validator`` is provided, it is applied to the resolved value (whether
        provided or default). If it returns False, raise ``ValueError``.

        Parameters
        ----------
        parameters : dict
            Mapping from parameter names (matching ``QueryParameter.name``) to values.

        Returns
        -------
        dict
            The formatted query with parameters replaced by concrete values.

        Raises
        ------
        ValueError
            If a complete required parameter is missing, or if validation fails.
        TypeError
            If a non-``None`` parameter value does not match the expected type.
        """

        # local recursive function to materialize the template
        def _materialize(node: Any) -> Any:
            """
            Recursively materialize the query template node.

            Parameters
            ----------
            node : Any
                The current node in the query template.

            Returns
            -------
            Any
                The materialized node with QueryParameters replaced by actual values.

            Raises
            ------
            ValueError
                If a complete required parameter is missing, or if validation fails.
            TypeError
                If a non-``None`` parameter value does not match the expected type.
            """
            if isinstance(node, QueryParameter):
                # "Provided" means key present, even if value is None
                if node.name in parameters:
                    value = parameters[node.name]
                else:
                    if node.required:
                        raise ValueError(
                            f"Missing required parameter: {node.name}"
                        )

                    # not required: use default if not None; else omit
                    if node.default is None:
                        return _MISSING_PARAMETER
                    value = node.default

                # Type check (including default). Skip when value is None.
                if value is not None and not isinstance(
                    value, node.param_type
                ):
                    raise TypeError(
                        f"Parameter '{node.name}' must be {node.param_type.__name__},"
                        f" got {type(value).__name__}"
                    )

                # Validation check, if applicable (including default and None if provided)
                if node.validator is not None and not node.validator(value):
                    raise ValueError(
                        f"Validation failed for parameter: {node.name}"
                    )

                return value

            if isinstance(node, dict):
                out = {}
                for k, v in node.items():
                    mv = _materialize(v)
                    if mv is _MISSING_PARAMETER:
                        continue
                    out[k] = mv
                if not out:
                    return _MISSING_PARAMETER
                return out

            if isinstance(node, list):
                out = []
                for item in node:
                    mv = _materialize(item)
                    if mv is _MISSING_PARAMETER:
                        continue
                    out.append(mv)
                if not out:
                    return _MISSING_PARAMETER
                return out

            return node

        rendered = _materialize(self.query_template)
        if rendered is _MISSING_PARAMETER:
            rendered = {}
        if not isinstance(rendered, dict):
            raise TypeError("Top-level query_template must be a dict.")
        return rendered
