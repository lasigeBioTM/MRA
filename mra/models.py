from mra import db, app
from sqlalchemy.sql import func

from unbabel.api import UnbabelApi
from pybioportal.Bioportal import Bioportal

from util import process_bioportal_annotations


class Report(db.Model):
    __tablename__ = 'reports'

    report_id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.UnicodeText)
    original_language = db.Column(db.UnicodeText)
    translated_text = db.Column(db.UnicodeText)
    category = db.Column(db.UnicodeText)
    radlex_annotations = db.Column(db.UnicodeText)
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

    @classmethod
    def get_last_n_reports(cls, n):
        """Get the last n reports added to the database"""
        return cls.query.order_by(cls.creation_date.desc()).limit(10)

    @classmethod
    def add_report(cls, original_text, original_language, category):
        new_report = cls(
            original_text=original_text,
            original_language=original_language,
            category=category
        )
        db.session.add(new_report)
        db.session.commit()

        return new_report

    @classmethod
    def translate_report(cls, report_id):

        report = cls.query.get(report_id)

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

    @classmethod
    def annotate_report(cls, report_id):

        report = cls.query.get(report_id)

        bioportal_api = Bioportal(app.config['BIOPORTAL_API_KEY'])
        annotations = bioportal_api.annotator(
            report.translated_text,
            ontologies='RADLEX'
        )

        processed_annotations = process_bioportal_annotations(annotations,
                                                              bioportal_api)

        annotations_str = str(processed_annotations)

        report.radlex_annotations = annotations_str

        db.session.commit()
