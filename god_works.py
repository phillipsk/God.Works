import flask, flask.views
import os
import functools
import requests
import json
import pprint

def parse_rough_draft(json_dict_output):
    books = json_dict_output[u'book']
    result_dict={}
    for i in books:
        book_name_variable = i[u'book_name']
        current_book_value = result_dict.setdefault(book_name_variable, {})
        chapter_variable = i[u'chapter_nr']
        chapter_value = current_book_value.setdefault(chapter_variable, {})
        all_chapter_verses_variable = i[u'chapter']
        for m in all_chapter_verses_variable.keys():
            verse = all_chapter_verses_variable[m]
            chapter_value[m] = verse[u'verse']
        chapter_sorted = []
        for key in sorted(chapter_value, key=int):
            chapter_sorted.append((key, chapter_value[key]))
        current_book_value[chapter_variable] = chapter_sorted
    return result_dict

def compare_number_strings(string1, string2):
    
    return cmp(int(string1), int(string2))

def user_bible(query):
    output = requests.get("http://getbible.net/json?passage={0}".format(query))
    if output.text == "NULL":
        return "no result"
    
    json_dict_output = json.loads(output.text.strip("();"))

    before_for_loop_parse = json_dict_output[u'book'][0][u'chapter'] 

    keys = before_for_loop_parse.keys()
    keys.sort(compare_number_strings)

    stored_list = []

    for k in keys:
        stored_list.append(before_for_loop_parse[k][u'verse'])

    return parse_rough_draft(json_dict_output)

app = flask.Flask(__name__)
app.secret_key = "password"

class Bible(flask.views.MethodView):
    def get(self):
        return flask.render_template('bible.html')
    def post(self):
        result = (flask.request.form['expression'])
        print user_bible(result)
        flask.flash(user_bible(result))
        return flask.redirect(flask.url_for('Bible'))

class hymns(flask.views.MethodView):
    def get(self):
        return flask.render_template('bible.html', endpoint="hymns")
    def post(self):
        result = (flask.request.form['expression'])
        flask.flash(result)
        return flask.render_template("hymns.html")

app.add_url_rule('/',
                 view_func=Bible.as_view('Bible'),
                 methods=["GET", "POST"])

app.add_url_rule('/hymns/',
                 view_func=hymns.as_view('hymns'),
                 methods=['GET', 'POST'])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
"""
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
"""