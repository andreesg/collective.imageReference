#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.imageReference import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget
from collective.object.utils.source import ObjPathSourceBinder

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

from plone.directives import dexterity, form

#priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
#insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass


# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #

## Documentation
class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    title = RelationList(
        title=_(u'Title'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder()
        ),
        required=False
    )
    form.widget('title', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    #author = schema.TextLine(title=_(u'Author'), required=False)
    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    #shelfMark = schema.TextLine(title=_(u'Shelf mark'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    
## Management details
class IManagementDetails(Interface):
    name = schema.TextLine(title=_(u'Name'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    time = schema.TextLine(title=_(u'Time'), required=False)
    dataset = schema.TextLine(title=_(u'Dataset'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

## Linked Objects
class ILinkedObjects(Interface):
    objectNumber = schema.TextLine(title=_(u'Object number'), required=False)
    creator = schema.TextLine(title=_(u'Creator'), required=False)
    objectName = schema.TextLine(title=_(u'Object name'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)

class ITitle(Interface):
    title = schema.TextLine(title=_(u'Title'), required=False)

class IDescription(Interface):
    description = schema.TextLine(title=_(u'Description'), required=False)

class ISource(Interface):
    source = schema.TextLine(title=_(u'Source'), required=False)

class IRights(Interface):
    rights = schema.TextLine(title=_(u'Rights'), required=False)

class INotes(Interface):
    notes = schema.Text(title=_(u'Notes'), required=False)

