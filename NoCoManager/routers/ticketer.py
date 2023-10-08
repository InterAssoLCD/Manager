from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
    abort,
)
from routers import SERVICES, isEnabled
from datetime import date

from json import dumps


def get_default_session_id():
    from systems import SessionSession

    ss = SessionSession()
    session_ = ss.get_all()
    session_uid: str = None
    if len(session_) < 1:
        session_uid = str(ss.create_session("default"))
    else:
        session_uid = str(session_[-1]["uid"])

    session["session_uid"] = session_uid


ticket_router = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket_router.route("/")
@isEnabled(SERVICES["ticketer"]["enabled"])
def index():
    return render_template("tickets/app.jinja2")


@ticket_router.route("/api/get/<ticket_uuid>")
@isEnabled(SERVICES["ticketer"]["enabled"])
def get_ticket(ticket_uuid: str):
    from systems.tickets import TicketSession

    ts = TicketSession(session.get("session_uid", get_default_session_id()))
    ticket = ts.get_ticket(ticket_uuid)
    if ticket:
        if ticket["used"] != 1:
            ts.use_ticket(ticket_uuid)
        ticket["anniversaire"] = ticket["anniversaire"].isoformat()
    ts.close()
    return dumps(ticket)


@ticket_router.route("/api/create", methods=["POST"])
@isEnabled(SERVICES["ticketer"]["enabled"])
def create_ticket():
    from systems.tickets import TicketSession, render_ticket_html

    data: dict = request.get_json()

    if not all(e for e in ["email", "nom", "prenom"] if e in data.keys()):
        abort(404, "Mauvais format de données")
    try:
        date.fromisoformat(data["anniversaire"])
    except ValueError:
        abort(404, "Anniversaire : format invalide (doit être iso YYYY-MM-DD)")

    ts = TicketSession(session.get("session_uid", get_default_session_id()))

    ticket_uuid = ts.create_ticket(data["email"], data["nom"], data["prenom"])
    ticket = ts.get_ticket(ticket_uuid)
    with open(f"gen/tickets/{ticket_uuid}.html", "w", encoding="utf-8") as file:
        file.write(render_ticket_html(ticket))

    ts.close()
    return dumps({"code": 200})
