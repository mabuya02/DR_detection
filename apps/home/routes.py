from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.patient.models import Patient
from apps.test.models import  Test
from apps.prediction.models import  Prediction

@blueprint.route('/index')
@login_required
def index():
    num_patients = Patient.query.count()
    num_tests = Test.query.count()
    num_predictions = Prediction.query.count()

    return render_template('home/index.html', segment='index', num_patients=num_patients, num_tests=num_tests,num_predictions=num_predictions)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
