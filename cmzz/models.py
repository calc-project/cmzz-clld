from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common

#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------

@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    glottocode = Column(Unicode)


@implementer(interfaces.IParameter)
class Words(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    name = Column(Unicode)
    middle_chinese = Column(Unicode)
    old_chinese = Column(Unicode)
    gloss = Column(Unicode)
    occurrences = Column(Integer)
    sentences = Column(Unicode)
    images = Column(Unicode)


@implementer(interfaces.ISentence)
class Phrase(CustomModelMixin, common.Sentence):
    pk = Column(Integer, ForeignKey('sentence.pk'), primary_key=True)
    sentence = Column(Unicode)
    gloss = Column(Unicode)
    translation = Column(Unicode)
    middle_chinese = Column(Unicode)
    old_chinese = Column(Unicode)
    images = Column(Unicode)


@implementer(interfaces.IValue)
class Examples(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    word = Column(Unicode)
    gloss = Column(Unicode)
    middle_chinese = Column(Unicode)
    old_chinese = Column(Unicode)
    image = Column(Unicode)
    phrase = Column(Unicode)

