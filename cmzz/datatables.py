from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import IntegerIdCol, LinkCol, Col, LinkToMapCol, IdCol
from clld.db.models.common import Parameter
from cmzz import models
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.sentence import Sentences
from clld.web.datatables.value import Values


def includeme(config):
    """register custom datatables"""


class Words(Parameters):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'id', sTitle='ID'),
            LinkCol(self, 'name'),
            Col(self, 'middle_chinese', sTitle='Middle Chinese'),
            Col(self, 'gloss', sTitle="Gloss"),
            Col(self, "occurrences", sTitle="Occurrences"),
            ]

class Examples(Values):
    def col_defs(self):
        return [
                IntegerIdCol(self, "id", sTitle="ID"),
                Col(self, "word", sTitle="Word Form"),
                Col(self, "middle_chinese", sTitle="Middle Chinese"),
                Col(self, "old_chinese", sTitle="Old Chinese"),
                Col(self, "image", sTitle="Original Characters"),
                Col(self, "phrase", sTitle="Phrase ID"),
                ]


class Phrases(Sentences):
    def col_defs(self):
        return [
                IntegerIdCol(self, "id", sTitle = "ID"),
                Col(self, "name", sTitle="Sentence"),
                Col(self, "description", sTitle="Glosses"),
                Col(self, "middle_chinese", sTitle="Middle Chinese"),
                Col(self, "old_chinese", sTitle="Old Chinese"),
                Col(self, "images", sTitle="Original"),
                ]


def includeme(config):
    config.register_datatable('parameters', Words)
    config.register_datatable('values', Examples)
    config.register_datatable('sentences', Phrases)

