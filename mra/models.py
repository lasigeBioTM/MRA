from mra import db, app, celery
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT

from unbabel.api import UnbabelApi
from pybioportal.Bioportal import Bioportal

from util import process_bioportal_annotations


class Report(db.Model):
    __tablename__ = 'reports'

    report_id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(LONGTEXT)
    original_language = db.Column(TEXT)
    translated_text = db.Column(LONGTEXT)
    category = db.Column(TEXT)
    radlex_annotations = db.Column(LONGTEXT)
    creation_date = db.Column(
        db.DateTime(timezone=True),
        default=func.utc_timestamp()
    )

    def __init__(self, original_text, original_language, category):
        self.original_text = original_text
        self.original_language = original_language
        self.category = category

    def __repr__(self):
        return '<report_id {}>'.format(self.report_id)

    @staticmethod
    def get_last_n_reports(n):
        """Get the last n reports added to the database"""
        return Report.query.order_by(Report.creation_date.desc()).limit(10)

    @staticmethod
    def add_report(original_text, original_language, category):
        new_report = Report(
            original_text=original_text,
            original_language=original_language,
            category=category
        )
        db.session.add(new_report)
        db.session.commit()

        return new_report

    @staticmethod
    @celery.task()
    def translate_report(report_id):

        report = Report.query.get(report_id)

        api = UnbabelApi(
            username=app.config['UNBABEL_USERNAME'],
            api_key=app.config['UNBABEL_API_KEY'],
            sandbox=True
        )

        callback_url = '{}/translate_report_callback/{}'.format(
            app.config['ROOT_URL'],
            report_id
        )

        api.post_translations(
            text=report.original_text,
            source_language=report.original_language,
            target_language='en',
            callback_url=callback_url
        )

    @staticmethod
    @celery.task()
    def annotate_report(report_id):

        report = Report.query.get(report_id)

        if report.original_language == 'en':
            text_to_annotate = report.original_text
        else:
            text_to_annotate = report.translated_text

        bioportal_api = Bioportal(app.config['BIOPORTAL_API_KEY'])
        annotations = bioportal_api.annotator(
            text_to_annotate,
            ontologies='RADLEX'
        )

        processed_annotations = process_bioportal_annotations(annotations,
                                                              bioportal_api)

        annotations_str = unicode(str(processed_annotations))

        report.radlex_annotations = annotations_str

        db.session.commit()
