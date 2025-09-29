from duckdb import DuckDBPyConnection
from src.services.system_messages import SystemMessages
import duckdb


class DuckConnection:
    def __init__(self, url: str):
        self.__connection_url = url
        self.__connection = None

    def connect(self) -> DuckDBPyConnection:
        try:
            from src.utils.errors_utils import ConnectionFailedDuckDb
            duckdb_connection = duckdb.connect(self.__connection_url)
            self.__connection = duckdb_connection
            SystemMessages().success('Feito conexão com a base de dados...')

            return duckdb_connection
        except ConnectionFailedDuckDb.IOException:
            SystemMessages().error(
                'Ocorreu algum erro ao tentar se conectar com a base de dados :(')
            raise ConnectionFailedDuckDb(
                'Failed to connect in DuckDB engine')

    def get_connection(self) -> DuckDBPyConnection:
        return self.__connection
