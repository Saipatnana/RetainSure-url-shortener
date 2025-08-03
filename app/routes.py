from flask import Blueprint, request, jsonify, redirect, abort, url_for
from app.utils import generate_short_code, is_valid_url
from app.models import insert_url_mapping, get_url, increment_clicks, get_stats, check_url_already_exist

routes = Blueprint("routes", __name__)

@routes.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400

    original_url = data["url"]
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400


    existing_code = check_url_already_exist(original_url)
    if existing_code:
        return jsonify({
            "short_code": existing_code,
            "short_url": url_for("routes.redirect_short_url", short_code=existing_code, _external=True)
        }), 201
        
    short_code = generate_short_code()
    while get_url(short_code):
        short_code = generate_short_code()

    insert_url_mapping(short_code, original_url)

    return jsonify({
        "short_code": short_code,
        "short_url": url_for("routes.redirect_short_url", short_code=short_code, _external=True)
    }), 201

@routes.route("/<short_code>")
def redirect_short_url(short_code):
    record = get_url(short_code)
    if not record:
        abort(404)

    increment_clicks(short_code)
    return redirect(record["original_url"])

@routes.route("/api/stats/<short_code>")
def stats(short_code):
    record = get_stats(short_code)
    if not record:
        abort(404)

    return jsonify({
        "url": record["original_url"],
        "clicks": record["clicks"],
        "created_at": record["created_at"] + "Z"
    })
