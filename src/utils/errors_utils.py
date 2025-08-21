class InvaliDuckDbQuery(Exception):
    """For invalid queries in DuckDb"""
    pass


class ConnectionFailedDuckDb(Exception):
    from duckdb import IOException
    """For failed connection to DuckDb"""
    pass


class InvalidTableDuckDb(Exception):
    from duckdb import CatalogException
    """For problem to find table name"""
    pass
