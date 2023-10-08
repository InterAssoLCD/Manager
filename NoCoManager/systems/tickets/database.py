import psycopg2
from uuid import uuid4
from systems import Connection, IdentiteSession


class TicketSession(Connection):
    def __init__(self, session_uid):
        Connection.__init__(self)
        self.session_uid = session_uid

    def get_ticket(self, ticket_uuid: str) -> tuple[str, str, str, str, int]:
        self.execute(
            "select t.uid, i.nom, i.prenom, i.dob as anniversaire, t.used from ticket as t join identite as i on i.uid = t.identite_uid where t.uid=%s and t.session_uid = %s",
            str(ticket_uuid),
            str(self.session_uid),
        )
        ticket = self.fetch()
        self.close()
        if not ticket:
            return None
        return ticket

    def create_ticket(self, email: str, nom: str, prenom: str, *args) -> str:
        ids = IdentiteSession()
        identite = ids.get_identite(champs=[email, nom, prenom])
        uid: uuid4 = uuid4()
        if not identite:
            champs = [email, nom, prenom] + list(args)
            identite_uid = ids.create_identite(*champs)
            identite = ids.get_identite(uid=identite_uid)

        self.execute(
            "insert into ticket (uid, session_uid, identite_uid) values (%s,%s,%s)",
            str(uid),
            str(self.session_uid),
            str(identite["uid"]),
        )
        self.commit()
        self.close()

        return str(uid)

    def delete_ticket(self, ticket_uuid: str):
        self.execute("delete from ticket where uid=%s", str(ticket_uuid))
        self.commit()
        self.close()

    def use_ticket(self, ticket_uuid: str):
        self.execute("update ticket set used='1' where uid=%s", str(ticket_uuid))
        self.commit()
        self.close()

    def get_all(self, with_join: bool = True):
        sqlfrom = (
            "from ticket"
            if not with_join
            else "t.uid, i.nom, i.prenom, i.dob as anniversaire, t.used from ticket as t join identite as i on i.uid = t.identite_uid"
        )
        self.execute(f"select * {sqlfrom} where session_uid = %s", self.session_uid)
        values = self.fetch(False)
        self.close()
        return values
