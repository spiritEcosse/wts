from flask import Blueprint, render_template

case_page = Blueprint('test', __name__, template_folder='templates')


@case_page.route('/<int:id>/')
def case(id):
    from apps.test.models import Case  # noqa
    case = Case.query.get(id)
    return render_template('case.html', case=case)
