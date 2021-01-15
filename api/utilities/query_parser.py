""" Module for parsing url queries """

from re import sub

class QueryParser():

    """Parses queries from the frontend"""

    # Queries excluded from parsing
    excluded_keys = ['include', 'limit', 'page', 'deleted', 'sort', 'order']

    @classmethod
    def to_snake_case(cls, string):
        """Converst a string in PascalCase or camelCase to snake_case."""
        return sub(r'(.)([A-Z])', r'\1_\2', string).lower()


    @classmethod
    def validate_column_exists(cls, model, name):
        """
        Checks if `name` exists on `model` as a column

        Parameters:
            model (BaseModel): the model a filter is being generated for
            name (str): the key of the url query
        """
        if name not in model.__table__.columns:
            cls.raises('invalid_query_non_existent_column', name,
                       model.__name__)
        return getattr(model, name, None)
