
from flask import Flask, jsonify, request

app = Flask(__name__)

events = [
    {
        "id": 1,
        "title": "Quizaften",
        "date": "2026-11-13",
        "capacity": 3,
        "participants": ["Anna", "Bo"]
    },
    {
        "id": 2,
        "title": "Brætspilsaften",
        "date": "2026-11-20",
        "capacity": 5,
        "participants": ["Peter"]
    },
    {
        "id": 3,
        "title": "Beerpong-turnering",
        "date": "2026-11-27",
        "capacity": 4,
        "participants": []
    }
]


def find_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return event
    return None


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Eventet blev ikke fundet"}), 404

    return jsonify(event), 200


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Ugyldig JSON"}), 400

    title = data.get("title")
    date = data.get("date")
    capacity = data.get("capacity")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Titel mangler"}), 400

    if not isinstance(date, str) or not date.strip():
        return jsonify({"error": "Dato mangler"}), 400

    if type(capacity) is not int or capacity <= 0:
        return jsonify({"error": "Kapacitet skal være et positivt heltal"}), 400

    new_id = max((event["id"] for event in events), default=0) + 1

    new_event = {
        "id": new_id,
        "title": title.strip(),
        "date": date.strip(),
        "capacity": capacity,
        "participants": []
    }

    events.append(new_event)

    return jsonify(new_event), 201


@app.route("/events/<int:event_id>/signups", methods=["POST"])
def signup(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Eventet blev ikke fundet"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Ugyldig JSON"}), 400

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Navn mangler"}), 400

    name = name.strip()

    if name in event["participants"]:
        return jsonify({"error": "Personen er allerede tilmeldt"}), 409

    if len(event["participants"]) >= event["capacity"]:
        return jsonify({"error": "Eventet er fuldt"}), 409

    event["participants"].append(name)

    return jsonify(event), 201


@app.route("/events/<int:event_id>/signups/<name>", methods=["DELETE"])
def delete_signup(event_id, name):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Eventet blev ikke fundet"}), 404

    if name not in event["participants"]:
        return jsonify({"error": "Tilmeldingen blev ikke fundet"}), 404

    event["participants"].remove(name)

    return "", 204


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Eventet blev ikke fundet"}), 404

    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
