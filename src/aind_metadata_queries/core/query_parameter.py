from typing import Any, Callable


class QueryParameter:
    """A class representing a query parameter.

    Parameters
    ----------
    name : str
        The name of the parameter.
    description : str
        A brief description of the parameter.
    param_type : type
        The expected type of the parameter value.
    required : bool, optional
        Whether a user-specified value for the parameter is required. Default is True.
    default : Any, optional
        The default value of the parameter if not provided. Unused if 'required' is True.
        Passing 'None' indicates no default value, and the query criteria containing this
        QueryParameter will be omitted if no user-specified value is provided. Default is None.
    validator : Callable[[Any], bool], optional
        A function to validate the parameter. It should take a value of the parameter and
        return True if valid, False otherwise. Default is None.

    """

    def __init__(
        self,
        name: str,
        description: str,
        param_type: type,
        required: bool = True,
        default: Any = None,
        validator: Callable[[Any], bool] = None,
    ):
        self.name = name
        self.description = description
        self.param_type = param_type
        self.required = required
        self.default = default
        self.validator = validator
