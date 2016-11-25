from flask import request, render_template

from util import split_span
from mra import app
from models import *


@app.route('/', methods=['GET'])
def index_page():
    reports = Report.get_last_n_reports(10)
    return render_template('index.html', reports=reports)


@app.route('/report/<int:report_id>', methods=['GET'])
def report_page(report_id):
    report = Report.query.get(report_id)

    original_text = report.original_text.split('\n')

    if report.translated_text is not None:
        translated_text = report.translated_text.split('\n')
    else:
        translated_text = None

    if report.radlex_annotations is not None:
        split_translated_text = split_span(report.translated_text)
        annotations = report.radlex_annotations
    else:
        split_translated_text = None
        annotations = None

    return render_template(
        'report.html',
        original_text=original_text,
        translated_text=translated_text,
        split_translated_text=split_translated_text,
        annotations=annotations,
    )


@app.route('/add_report', methods=['POST'])
def add_report_endpoint():
    original_text = request.files['file'].read()
    original_language = request.form['orig_language']
    category = request.form['category']

    report = Report.add_report(original_text, original_language, category)
    Report.translate_report(report.report_id)

    last_reports = Report.get_last_n_reports(10)
    return render_template('index.html', reports=last_reports)


@app.route('/translate_report_callback/<int:report_id>', methods=['POST'])
def translate_report_callback(report_id):
    translated_text = request.form['translated_text']

    report = Report.query.get(report_id)
    report.translated_text = translated_text
    Report.annotate_report(report_id)

    db.session.commit()

    return '', 200
