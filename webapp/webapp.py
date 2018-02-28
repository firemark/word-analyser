from flask import Flask, render_template, request, make_response

import uuid
import pickle

app = Flask(__name__)

with open('urls') as fp:
    urls = [line.strip() for line in fp]
sessions = {}  #  cookieid: list of words
with open('ml.pickle') as fp:
    classifier = pickle.load(fp)
with open('favorite-words') as fp:
    favorite_words = [line.strip() for line in fp]


def _get_session_id():
    sid = request.cookies.get('sid')
    if sid is None:
        sid = uuid.uuid4().hex
    return sid


def _get_label_by_sid(sid):
    data = sessions.get(sid, [])
    document = ' '.join(data)
    labels = classifier.predict([document])
    return labels[0]


def _set_data(sid, new_data):
    data = sessions.get(sid, [])
    data = data + new_data
    sessions[sid] = data[-50:]


def _show_site(sid, label=None, page=None):
    try:
        words = favorite_words[label]
    except IndexError:
        words = ''
    resp = make_response(
        render_template(
            'main.html',
            label=label, page=page,
            words=words, urls=urls,
        )
    )
    resp.set_cookie('sid', sid)
    return resp


@app.route("/")
def index():
    sid = _get_session_id()
    label = _get_label_by_sid(sid)
    return _show_site(sid, label=label)


@app.route("/<page>")
def subpage(page):
    sid = _get_session_id()
    _set_data(sid, page.split('-'))
    label = _get_label_by_sid(sid)

    return _show_site(sid, label=label, page=page)

