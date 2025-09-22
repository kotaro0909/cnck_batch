import logging
from logging import config, getLogger, NullHandler, DEBUG

import mariadb
import multipledispatch


class DbMariaTx:
    __username = "root"
    __password = "root"
    __mariadb_host = "localhost"
    __mariadb_port = 3306
    __database = "cryptocurrency"
    __conn = None
    __cursor = None
    _logger = None

    def __init__(self):
        self._logger = getLogger(__name__)
        self._logger.debug("init finished")

    def connect(self) -> None:
        try:
            self.__conn = mariadb.connect(
                user=self.__username,
                password=self.__password,
                host=self.__mariadb_host,
                port=self.__mariadb_port,
                database=self.__database
            )
            self._logger.debug(f'dbinfo [user: {self.__username}, host: {self.__mariadb_host}'
                              f', port: {self.__mariadb_port}, database: {self.__database}]')
            self._logger.debug("connection initialized")
        except mariadb.Error as e:
            print(f"データベースエラーが発生しました: {e}")
            raise e

    def close(self) -> None:
        try:
            if not self.__cursor.check_closed():
                self.__cursor.close()
            self.__conn.close()
            self._logger.debug(f'cursor and connection has closed')
        except mariadb.Error as e:
            self._logger.fatal(f"データベースエラーが発生しました: {e}")
            raise e
        self.__conn = None

    def get_rows(self) -> list:
        try:
            rows = self.__cursor.fetchall()
            # curs = self.__conn.cursor()
            # rows = curs.fetchall()
            # curs.close()
            self._logger.debug(f'got rows [{len(rows)} rows]')
            return rows
        except mariadb.Error as e:
            self._logger.fatal(f"データベースエラーが発生しました: {e}")
            self.close()
            raise e

    def commit(self) -> None:
        try:
            self.__conn.commit()
            self._logger.debug(f'committed')
        except mariadb.Error as e:
            self._logger.fatal(f"データベースエラーが発生しました: {e}")
            self.close()
            raise e

    def rollback(self) -> None:
        try:
            self.__conn.rollback()
            self._logger.debug(f'rollback done')
        except mariadb.Error as e:
            self._logger.fatal(f"データベースエラーが発生しました: {e}")
            self.close()
            raise e

    @multipledispatch.dispatch()
    def execute(self, sql: str) -> None:
        self.__execute(sql, None)

    @multipledispatch.dispatch()
    def execute(self, sql: str, params: tuple) -> None:
        self.__execute(sql, params)

    def __execute(self, sql: str, params: tuple) -> None:
        try:
            self.__cursor = self.__conn.cursor()
        except mariadb.Error as e:
            self._logger.fatal(f"データベースエラーが発生しました: {e}")
            raise e

        try:
            if params is None:
                self.__cursor.execute(sql)
            else:
                self.__cursor.execute(sql, params)
            self._logger.debug(f'execute done [sql: {sql} / params: {params}]')
        except mariadb.Error as e:
            self._logger.fatal(f"データベースエラーが発生しました: {e}")
            self.__conn.rollback()
            self.close()
            raise e


def test():
    logger = getLogger(__name__)
    sql = ""

    logger.info("0 事前準備 - start")
    db = DbMariaTx()
    db.connect()
    db.execute("delete from test")
    db.commit()
    db.close()
    logger.info("0 事前準備 - end")

    logger.info("1-1 1件追加 ID=1 - start")
    db.connect()
    db.execute("insert into test(id, text) values (1, 'Hello')")
    db.commit()
    db.close()
    logger.info("1-1 1件追加 ID=1 - end")

    logger.info("1-2 1件追加 ID=2 - start")
    db.connect()
    db.execute("insert into test(id, text) values (?, ?)", (2, "Bye"))
    db.commit()
    db.close()
    logger.info("1-2 1件追加 ID=2 - end")

    logger.info("2 1件追加 トランザクション内でSELECT - start")
    db.connect()
    db.execute("insert into test(id, text) values (?, ?)", (3, "Morning"))
    db.execute("select * from test")
    rows = db.get_rows()
    logger.info(rows)
    db.rollback()
    db.close()
    logger.info("2 1件追加 トランザクション内でSELECT - end")

    logger.info("3 同一トランザクション内で複数SQL実行 - start")
    db.connect()
    db.execute("insert into test(id, text) values (4, 'Afternoon')")
    db.execute("insert into test(id, text) values (5, 'Evening')")
    db.commit()
    db.close()
    logger.info("3 同一トランザクション内で複数SQL実行 - end")

    logger.info("4 同一トランザクション内でSELECT→DELETE→SELECT - start")
    logger.info("4-1 最初のSELECT - start")
    db.connect()
    db.execute("select * from test")
    rows = db.get_rows()
    logger.info(rows)
    logger.info("4-1 最初のSELECT - end")

    logger.info("4-2 SELECT後EDLETE - start")
    db.execute("delete from test where id in (1, 4, 5)")
    logger.info(rows)
    logger.info("4-2 SELECT後EDLETE - end")

    logger.info("4-3 DELETE後に再度SELECT - start")
    db.execute("select * from test")
    rows = db.get_rows()
    logger.info(rows)
    db.close()
    logger.info("4-3 DELETE後に再度SELECT - end")
    logger.info("4-3 Rollbackせずに接続を閉じるo - end")

    logger.info("4-4 別コネクションでSELECT - start")
    db.connect()
    db.execute("select * from test")
    rows = db.get_rows()
    db.close()
    logger.info(rows)
    logger.info("4-4 別コネクションでSELECT - end")

    logger.info("4 同一トランザクション内でSELECT→DELETE→SELECT - end")
