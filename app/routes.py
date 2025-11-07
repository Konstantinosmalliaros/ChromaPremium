from __future__ import annotations

import re
from flask import Blueprint, Request, current_app, flash, redirect, render_template, request, url_for

from .email_utils import EmailConfigurationError, send_contact_email


main = Blueprint("main", __name__)


@main.route("/")
def home() -> str:
    return render_template("home.html")


@main.route("/services")
def services() -> str:
    return render_template("services.html")


@main.route("/process")
def process() -> str:
    return render_template("process.html")


@main.route("/quality")
def quality() -> str:
    return render_template("quality.html")


@main.route("/gallery")
def gallery() -> str:
    return render_template("gallery.html")


@main.route("/contact", methods=["GET", "POST"])
def contact() -> str:
    form_data = (
        _extract_form_data(request)
        if request.method == "POST"
        else {"name": "", "email": "", "phone": "", "message": ""}
    )

    if request.method == "POST":
        errors = _validate_form_data(form_data)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            try:
                send_contact_email(form_data)
            except EmailConfigurationError as exc:
                flash(
                    "Δεν ήταν δυνατή η αποστολή του email. Ελέγξτε τις "
                    "ρυθμίσεις SMTP στον διακομιστή.",
                    "error",
                )
                current_app.logger.warning("Contact email failed: %s", exc)
            except Exception as exc:  # pragma: no cover - log unexpected error
                current_app.logger.exception("Unexpected error sending email: %s", exc)
                flash(
                    "Παρουσιάστηκε απρόσμενο σφάλμα κατά την αποστολή του μηνύματος.",
                    "error",
                )
            else:
                flash("Ευχαριστούμε! Θα επικοινωνήσουμε μαζί σας σύντομα.", "success")
                return redirect(url_for("main.contact"))

    return render_template("contact.html", form_data=form_data)


def _extract_form_data(req: Request) -> dict[str, str]:
    return {
        "name": req.form.get("name", "").strip(),
        "email": req.form.get("email", "").strip(),
        "phone": req.form.get("phone", "").strip(),
        "message": req.form.get("message", "").strip(),
    }


def _validate_form_data(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []

    if not form_data["name"]:
        errors.append("Παρακαλούμε εισάγετε το όνομά σας.")

    if not _is_valid_email(form_data["email"]):
        errors.append("Παρακαλούμε εισάγετε ένα έγκυρο email.")

    if not form_data["message"]:
        errors.append("Παρακαλούμε περιγράψτε τις ανάγκες του έργου.")

    return errors


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_valid_email(value: str) -> bool:
    return bool(EMAIL_REGEX.match(value))

