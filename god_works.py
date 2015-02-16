import flask, flask.views
import os
import functools
import requests
import json
import pprint
import re
from jinja2 import evalcontextfilter, Markup, escape
from hymns import *


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



####


### reference on different .py file ??

#hymns.hymn001

def hymn001():
    content = """
    This is a text with many
    new lines, then we can write long texts 
    here
    """
    

    return content


app = flask.Flask(__name__)
app.secret_key = "password"

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(value))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


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

        message = None

        if result == "hymn001":
            message = hymn001()
        elif result == "xyz":
            message = surr()

        flask.flash(message)
        return flask.render_template("hymns.html")

app.add_url_rule('/',
                 view_func=Bible.as_view('Bible'),
                 methods=["GET", "POST"])

app.add_url_rule('/hymns/',
                 view_func=hymns.as_view('hymns'),
                 methods=['GET', 'POST'])



if __name__ == "__main__":
    app.debug = True
    app.run()
"""
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
"""
