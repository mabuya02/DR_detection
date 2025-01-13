from flask import render_template
from apps.prediction import blueprint
from apps.prediction.models import Prediction
from apps import db
from flask_login import login_required
from apps.patient.models import Patient

@blueprint.route('/panel')
@login_required
def prediction_panel():
    class_avg_confidence = db.session.query(Prediction.predicted_label, db.func.avg(Prediction.confidence_score))\
                                      .group_by(Prediction.predicted_label).all()
    
    class_avg_confidence_scores = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    for label, avg_conf in class_avg_confidence:
        class_avg_confidence_scores[label] = round(avg_conf, 4)

    labels = list(class_avg_confidence_scores.keys())
    avg_confidences = list(class_avg_confidence_scores.values())

    predictions_data = db.session.query(Prediction, Patient).join(Patient).all()

    return render_template('predictions/panel.html', labels=labels, avg_confidences=avg_confidences, predictions_data=predictions_data)
