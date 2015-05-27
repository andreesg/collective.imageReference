#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapts
#from plone.formwidget.contenttree import ObjPathSourceBinder

from .utils.source import ObjPathSourceBinder

#
# plone.app.widgets dependencies
#
from plone.app.widgets.dx import DatetimeFieldWidget, RelatedItemsFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container, Item
from plone.dexterity.browser import add, edit

# # # # # # # # # # # # # # # # # #
# !ImageRefrence specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.imageReference import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

from plone.app.contenttypes.interfaces import IImage
from plone.namedfile.field import NamedBlobImage

# # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #
# imageRefrence schema        #
# # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #

class IImageReference(model.Schema):
    #
    # Reproduction Data
    #
    model.fieldset('reproduction_data', label=_(u'Reproduction data'), 
        fields=['reproductionData_identification_reproductionReference', 'reproductionData_identification_format',
                'reproductionData_identification_reproductionType', 'reproductionData_identification_copies',
                'reproductionData_identification_technique', 'reproductionData_identification_location',
                'reproductionData_identification_date', 'reproductionData_identification_identifierURL',
                'reproductionData_descriptiveElements_title', 'reproductionData_descriptiveElements_creator',
                'reproductionData_descriptiveElements_subject', 'reproductionData_descriptiveElements_description',
                'reproductionData_descriptiveElements_publisher', 'reproductionData_descriptiveElements_contributor',
                'reproductionData_descriptiveElements_source', 'reproductionData_descriptiveElements_coverage',
                'reproductionData_descriptiveElements_rights', 'reproductionData_descriptiveElements_notes']
    )

    # identification
    reproductionData_identification_reproductionReference = schema.TextLine(title=_(u'Reproduction reference'), required=False)
    reproductionData_identification_format = schema.TextLine(title=_(u'Format'), required=False)
    reproductionData_identification_reproductionType = schema.TextLine(title=_(u'Reproduction type'), required=False)
    reproductionData_identification_copies = schema.TextLine(title=_(u'Copies'), required=False)
    reproductionData_identification_technique = schema.TextLine(title=_(u'Technique'), required=False)
    reproductionData_identification_location = schema.TextLine(title=_(u'Location'), required=False)
    reproductionData_identification_date = schema.TextLine(title=_(u'Date'), required=False)
    reproductionData_identification_identifierURL = schema.TextLine(title=_(u'Identifier (URL)'), required=False)

    # Descriptive elements of the reproduction
    reproductionData_descriptiveElements_title = schema.TextLine(title=_(u'Title'), required=False)
    reproductionData_descriptiveElements_creator = schema.TextLine(title=_(u'Creator'), required=False)
    reproductionData_descriptiveElements_subject = schema.TextLine(title=_(u'Subject'), required=False)
    reproductionData_descriptiveElements_description = schema.TextLine(title=_(u'Description'), required=False)
    reproductionData_descriptiveElements_publisher = schema.TextLine(title=_(u'Publisher'), required=False)
    reproductionData_descriptiveElements_contributor = schema.TextLine(title=_(u'Contributor'), required=False)
    reproductionData_descriptiveElements_source = schema.TextLine(title=_(u'Source'), required=False)
    reproductionData_descriptiveElements_coverage = schema.TextLine(title=_(u'Coverage'), required=False)
    reproductionData_descriptiveElements_rights = schema.TextLine(title=_(u'Rights'), required=False)
    reproductionData_descriptiveElements_notes = schema.TextLine(title=_(u'Notes'), required=False)

    #
    # Documentation
    #
    model.fieldset('documentation', label=_(u'Documentation'), 
        fields=['documentation_documentation']
    )

    documentation_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentationDocumentation),
        required=False)
    form.widget(documentation_documentation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('documentation_documentation')

    #
    # Linked objects
    #
    model.fieldset('linked_objects', label=_(u'Linked Objects'), 
        fields=['linkedObjects_linkedObjects']
    )

    """linkedObjects_relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder()
        ),
        required=False
    )"""

    linkedObjects_linkedObjects = ListField(title=_(u'Linked Objects'),
        value_type=DictRow(title=_(u'Linked Objects'), schema=ILinkedObjects),
        required=False)
    form.widget(linkedObjects_linkedObjects=DataGridFieldFactory)
    dexteritytextindexer.searchable('linkedObjects_linkedObjects')


alsoProvides(IImageReference, IFormFieldProvider)


# # # # # # # # # # # # # # # # #
# imageRefrence declaration     #
# # # # # # # # # # # # # # # # #

class ImageReference(Item):
    implements(IImageReference)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context


class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('imageReference_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if widget.__name__ in ['IImageReference.linkedObjects_linkedObjects', 'IImageReference.documentation_documentation']:
                    widget.auto_append = False
                    widget.allow_reorder = True

                if 'IImageReference' in widget.__name__:
                    alsoProvides(widget, IFormWidget)


class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('imageReference_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if widget.__name__ in ['IImageReference.linkedObjects_linkedObjects', 'IImageReference.documentation_documentation']:
                    widget.auto_append = False
                    widget.allow_reorder = True

                if 'IImageReference' in widget.__name__:
                    alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    






