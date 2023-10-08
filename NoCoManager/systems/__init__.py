import psycopg2
from psycopg2.extras import DictCursor
from uuid import uuid4


class Connection:
    def __init__(self):
        self.connector, self.cursor = None, None

    def init(self):
        connect = psycopg2.connect(
            dbname="pi",
            user="pi",
            password="pi",
            host="localhost",
        )
        cur = connect.cursor(cursor_factory=DictCursor)
        with open("./systems/schematic.sql", "r", encoding="UTF-8") as sql:
            cur.execute(sql.read())
        return connect, cur

    def close(self):
        self.connect()
        self.connector.close()

    def execute(self, sql: str, *args):
        self.connect()
        return self.cursor.execute(sql, args)

    def fetch(self, one: bool = True):
        value = self.cursor.fetchone() if one else self.cursor.fetchall()
        if not value:
            return None

        return dict(value) if one else list(map(dict, value))

    def commit(self):
        self.connect()
        self.connector.commit()

    def connect(self):
        if self.cursor == None or self.cursor.closed:
            self.connector, self.cursor = self.init()


class IdentiteSession(Connection):
    def __init__(self):
        Connection.__init__(self)

    def get_identite(self, uid: str = None, champs: list = None) -> dict:
        identite: tuple = None
        if uid:
            self.execute("select * from identite as i where uid = %s", str(uid))

            identite = self.fetch()
        else:
            self.execute(
                "select * from identite as i where email = %s and nom = %s and prenom = %s ;",
                *champs,
            )

            identite = self.fetch()

        self.close()
        if not identite:
            return None
        return identite

    def create_identite(self, *args) -> uuid4:
        uid = uuid4()
        cols = ["uid", "email", "nom", "prenom", "dob", "telephone", "adresse"]
        arguments = [str(uid)] + list(args)
        print("arguments: ", arguments)
        needed_cols = ",".join(cols[: len(arguments)])
        values = ",".join(["%s" for i in range(len(arguments))])

        sql = f"insert into identite ({needed_cols}) values ({values});"
        self.execute(sql, *arguments)
        self.commit()
        self.close()
        return uid

    def get_all(self):
        self.execute("select * from identite")
        values = self.fetch(False)
        self.close()
        return values


class SessionSession(Connection):
    def __init__(self):
        Connection.__init__(self)

    def get_all(self):
        self.execute("select * from session")
        values = self.fetch(False)
        self.close()
        return values

    def get_session(self, uid: str = None, title: str = None) -> dict:
        session: dict = None
        if uid:
            self.execute("select * from session where uid = %s", str(uid))

            session = self.fetch()
        else:
            self.execute(
                "select * from session where title = %s ;",
                title,
            )

            session = self.fetch()

        self.close()
        if not session:
            return None
        return session

    def create_session(self, title: str) -> uuid4:
        uid: uuid4 = uuid4()

        sql: str = f"insert into session (uid, title, valid) values (%s, %s, 't');"

        self.execute(sql, str(uid), title)
        self.commit()

        self.close
        return uid
