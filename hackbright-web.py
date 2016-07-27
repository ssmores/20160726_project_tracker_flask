from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def display_homepage():
    """Shows homepage with options to add or search for a student."""

    return render_template("index.html")


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'sdevelops')
    title_grade = hackbright.get_grades_by_github(github)

    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html", 
                           first=first, 
                           last=last, 
                           github=github, 
                           title_grade=title_grade)

    return html


@app.route("/project/<project_title>")
def display_project_details(project_title):
    """Display title, description, and max grade of project"""

    title, description, max_grade = hackbright.get_project_by_title(project_title)

    return render_template("project_info.html", 
                           title=title,
                           description=description,
                           max_grade=max_grade)


@app.route("/student-add")
def student_add():
    """Add new student."""

    return render_template("new_student.html")


@app.route("/confirmation", methods=['POST'])
def display_confirmation():
    """Display confirmation message."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_confirmation.html", 
        first=first_name, last=last_name, github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)


