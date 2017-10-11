from flask import Flask, render_template, request
from api import *

app = Flask(__name__)

lst = load('data.json')

key_list = selected_keys_list

@app.route("/")
def home():
    search_list = search(lst, sort_by='end_date', sort_order='desc')
    selected_search_list = mini_list(search_list, key_list)
    last_project = selected_search_list[0]
    return render_template("home.html",
                           last_project=last_project,
                           key_list=key_list)

@app.route("/projects", methods=["POST", "GET"])
def projects():
    project_list = search(lst)
    selected_list = mini_list(project_list, key_list)
    techniques = get_techniques(lst)
    if request.method == "POST":
        input_sort_by = request.form['sort_by']
        input_sort_order = request.form['sort_order']
        input_techniques = request.form.getlist('techniques')
        input_search = request.form['search']
        input_search_fields = request.form.getlist('search_fields')
        search_list = search(lst,
                            input_sort_by,
                            input_sort_order,
                            input_techniques,
                            input_search,
                            input_search_fields)
        selected_search_list = mini_list(search_list, key_list)

        return render_template("projects.html",
                               key_list=key_list,
                               techniques=techniques,
                               selected_search_list=selected_search_list,
                               input_search=input_search)
    
    return render_template("projects.html",
                           lst=lst,
                           selected_list=selected_list,
                           key_list=key_list,
                           techniques=techniques)

@app.route("/skills")
def skills():
    techniques = get_techniques(lst)
    technique_stats = get_technique_stats(lst)
    return render_template("skills.html",
                           techniques=techniques,
                           technique_stats=technique_stats)

@app.route("/projects/<int:id>")
def show_project(id):
    full_key_list = list(lst[id -1].keys())
    project = search(lst, search=id, search_fields=['project_id'])
    return render_template("project.html",
                           project=project,
                           full_key_list=full_key_list)


if __name__ == "__main__":
    app.run(debug=True)

