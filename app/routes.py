from __future__ import annotations

import os
import re
from datetime import datetime
from flask import Blueprint, Request, Response, current_app, flash, redirect, render_template, request, send_from_directory, url_for

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
    # Marketplace reviews data from TexnitesOnline
    marketplace_url = "https://www.texnitesonline.gr/controller/profile/show.php?as=homeTech&token=saltyLsalty5127bb2a425f9&tid=1132"
    total_reviews = 25
    review_screenshot = "marketplace-reviews.png"
    
    return render_template(
        "quality.html",
        marketplace_url=marketplace_url,
        total_reviews=total_reviews,
        review_screenshot=review_screenshot
    )


@main.route("/gallery")
def gallery() -> str:
    photos_dir = os.path.join(current_app.static_folder, "images", "photos")
    photos = []
    
    if os.path.exists(photos_dir):
        # Get all image files from the photos directory
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        for filename in sorted(os.listdir(photos_dir)):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                photos.append(filename)
    
    return render_template("gallery.html", photos=photos)


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


@main.route("/robots.txt")
def robots_txt() -> Response:
    """Serve robots.txt file."""
    return send_from_directory(current_app.static_folder, "robots.txt", mimetype="text/plain")


@main.route("/sitemap.xml", methods=["GET"])
def sitemap() -> Response:
    """Generate and serve sitemap.xml for SEO."""
    # Ensure we use the correct base URL (handle both http and https)
    base_url = request.url_root.rstrip("/")
    # If on PythonAnywhere, ensure we use https
    if "pythonanywhere.com" in base_url or "chromapremium.gr" in base_url:
        base_url = base_url.replace("http://", "https://")
    
    # Define all pages with their priorities and change frequencies
    pages = [
        {"url": "", "priority": "1.0", "changefreq": "weekly"},
        {"url": "/services", "priority": "0.9", "changefreq": "monthly"},
        {"url": "/process", "priority": "0.8", "changefreq": "monthly"},
        {"url": "/quality", "priority": "0.8", "changefreq": "monthly"},
        {"url": "/gallery", "priority": "0.7", "changefreq": "weekly"},
        {"url": "/contact", "priority": "0.8", "changefreq": "monthly"},
    ]
    
    # Get last modification date (use current date as fallback)
    lastmod = datetime.now().strftime("%Y-%m-%d")
    
    # Generate XML sitemap
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        sitemap_xml += f'  <url>\n'
        sitemap_xml += f'    <loc>{base_url}{page["url"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{lastmod}</lastmod>\n'
        sitemap_xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += f'  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    return Response(sitemap_xml, mimetype="application/xml")


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

