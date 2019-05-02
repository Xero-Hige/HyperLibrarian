from flask import Flask, jsonify, request

from analytics import RedisAnalytics
from query_cache import RedisCache

app = Flask(__name__)

CACHE = RedisCache()
ANALYTICS = RedisAnalytics()

# Analytics Tags

TAG_EXERCISE = "exercises"
TAG_TAG = "tags"
TAG_ATTEMPTED = "attempted"


@app.route("/file/<string:exercise>/<string:filename>", methods=["GET"])
def get_single_file(exercise, filename):
    key = f"file::{exercise}::{filename}"
    cached = CACHE.get(key)

    if not cached:
        data = {"file": filename, "folder": exercise}
        CACHE.set(key, data)
        data["cached"] = False
    else:
        data = cached
        data["cached"] = True

    return jsonify(data)


@app.route("/statement/<string:exercise_name>", methods=["GET"])
def get_exercise_statemen(exercise_name):
    key = f"statement::{exercise_name}"

    cached = CACHE.get(key)

    if not cached:
        data = {"exercise": exercise_name, "statement_file": "Programame esto wacho", "tags": ["Programa", "Wacho"]}
        CACHE.set(key, data)
        data["cached"] = False
    else:
        data = cached
        data["cached"] = True

    ANALYTICS.count(exercise_name, data_class=TAG_EXERCISE)
    for tag in data["tags"]:
        ANALYTICS.count(tag, TAG_TAG)

    return jsonify(data)


@app.route("/tests/<string:exercise_name>", methods=["GET"])
def get_exercise_tests(exercise_name):
    key = f"tests::{exercise_name}"

    cached = CACHE.get(key)

    if not cached:
        data = {"exercise": exercise_name,
                "tests_inputs": [{"filename": "input_01", "content": "blablabla(en binario)"}],
                "tests_outputs": [{"filename": "input_01", "content": "blablabla(en binario)"}]}

        CACHE.set(key, data)
        data["cached"] = False
    else:
        data = cached
        data["cached"] = True

    ANALYTICS.count(exercise_name, TAG_ATTEMPTED)
    ANALYTICS.touch(exercise_name, TAG_ATTEMPTED)

    return jsonify(data)


@app.route("/exercise/<string:exercise_name>", methods=["GET"])
def get_full_exercise(exercise_name):
    key = f"exercise::{exercise_name}"

    cached = CACHE.get(key)

    if not cached:
        data = {"exercise": exercise_name,
                "statement_file": "Programame esto wacho",
                "tests_inputs": [{"filename": "input_01", "content": "blablabla(en binario)"}],
                "tests_outputs": [{"filename": "input_01", "content": "blablabla(en binario)"}],
                "tags": ["Programa", "Wacho"]}

        CACHE.set(key, data)
        data["cached"] = False
    else:
        data = cached
        data["cached"] = True

    ANALYTICS.count(exercise_name, data_class=TAG_EXERCISE)
    for tag in data["tags"]:
        ANALYTICS.count(tag, TAG_TAG)

    return jsonify(data)


@app.route("/stats/top/<string:data_type>")
def get_tops(data_type):
    results = request.args.get('results', 5)
    return jsonify(ANALYTICS.get_top_n(data_type, results))


@app.route("/stats/latest/<string:data_type>")
def get_latest(data_type):
    results = request.args.get('results', 5)
    return jsonify(ANALYTICS.get_latest(data_type, results))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
