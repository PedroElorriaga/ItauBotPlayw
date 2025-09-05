import duckdb
from typing import List, Literal
from src.utils.errors_utils import InvaliDuckDbQuery, InvalidTableDuckDb


class DuckConnection:
    def __init__(self, url: str):
        self.__connection = duckdb.connect(url)

    def __create_progress_table(self):
        self.__connection.execute("""
            CREATE TABLE IF NOT EXISTS progress (
            idx INTEGER PRIMARY KEY,
            name TEXT,
            cnpj TEXT,
            conta TEXT,                      
            status TEXT -- 'pending', 'done', 'error
        )
        """)

    def insert_companies_if_not_exists(self, companies: List[str]):
        for company in companies:
            self.__connection.execute("""
                INSERT OR IGNORE INTO progress VALUES (?, ?, ?, ?, 'pending')
            """, [company['index'], company['name'], company['cnpj'], company['number']])

    def search_all_companies(self):
        try:
            pendente_status_company = self.__connection.execute("""
                SELECT name, cnpj, conta, status FROM progress ORDER BY idx
            """).fetchall()
        except InvalidTableDuckDb.CatalogException:
            self.__create_progress_table()
            return self.search_all_companies()

        return pendente_status_company

    def update_company_status(self, account: dict, status: Literal['done', 'error']):
        if status == 'done':
            self.__connection.execute("""
                UPDATE progress SET status = 'done' WHERE cnpj = ? AND conta = ?
            """, [account['cnpj'], account['number']])
        elif status == 'error':
            self.__connection.execute("""
                UPDATE progress SET status = 'error' WHERE cnpj = ? AND conta = ?
            """, [account['cnpj'], account['number']])
        else:
            raise InvaliDuckDbQuery(
                'Invalid status argument - this query only accept (done or error) argument')

    def drop_progress_table(self):
        self.__connection.execute("""
            DROP TABLE progress
        """)
