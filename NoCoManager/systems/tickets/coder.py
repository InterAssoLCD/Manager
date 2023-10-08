import base64
from io import BytesIO
import qrcode
import jinja2
from flask import render_template


def render_ticket_html(infos: dict):
    """
    Render html page using jinja
    """
    output_text = render_template(
        "tickets/ticket.jinja2",
        nom=infos["nom"],
        prenom=infos["prenom"],
        anniversaire=infos["anniversaire"],
        uuid=infos["uid"],
        image=_get_base64_str(_generate_qr(infos["uid"])),
    )

    return output_text


def _generate_qr(data: str):
    img = qrcode.make(data)
    return img


def _get_base64_str(image):
    buffered = BytesIO()
    image.save(buffered)
    return base64.b64encode(buffered.getvalue()).decode()
