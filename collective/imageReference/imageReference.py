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
from plone.app.z3cform.widget import DatetimeFieldWidget, RelatedItemsFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow, IDataGridField
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


from collective.object.utils.widgets import AjaxSingleSelectFieldWidget, ExtendedRelatedItemsFieldWidget
from plone.app.contenttypes.interfaces import IImage
from plone.namedfile.field import NamedBlobImage

# # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #
# imageRefrence schema        #
# # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #

class IImageReference(model.Schema):

    priref = schema.TextLine(title=_(u'priref'), required=False)

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

    reproductionData_identification_reproductionType = schema.List(
        title=_(u'Reproduction type'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('reproductionData_identification_reproductionType', AjaxSingleSelectFieldWidget, vocabulary="collective.imageReference.reproductionType")


    reproductionData_identification_copies = schema.TextLine(title=_(u'Copies'), required=False)

    reproductionData_identification_technique = schema.List(
        title=_(u'Technique'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('reproductionData_identification_technique', AjaxSingleSelectFieldWidget, vocabulary="collective.imageReference.technique")

    reproductionData_identification_location = schema.List(
        title=_(u'Location'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('reproductionData_identification_location', AjaxSingleSelectFieldWidget, vocabulary="collective.imageReference.location")

    reproductionData_identification_date = schema.TextLine(title=_(u'Date'), required=False)
    reproductionData_identification_identifierURL = schema.TextLine(title=_(u'Identifier (URL)'), required=False)

    # Descriptive elements of the reproduction
    reproductionData_descriptiveElements_title = ListField(title=_(u'Title'),
        value_type=DictRow(title=_(u'title'), schema=ITitle),
        required=False)
    form.widget(reproductionData_descriptiveElements_title=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductionData_descriptiveElements_title')
    
    reproductionData_descriptiveElements_creator = RelationList(
        title=_(u'Creator'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )

    form.widget('reproductionData_descriptiveElements_creator', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    
    reproductionData_descriptiveElements_subject = schema.List(
        title=_(u'Subject'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('reproductionData_descriptiveElements_subject', AjaxSelectFieldWidget, vocabulary="collective.imageReference.subject")

    reproductionData_descriptiveElements_description = ListField(title=_(u'Description'),
        value_type=DictRow(title=_(u'Description'), schema=IDescription),
        required=False)
    form.widget(reproductionData_descriptiveElements_description=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductionData_descriptiveElements_description')

    reproductionData_descriptiveElements_publisher = RelationList(
        title=_(u'Publisher'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )

    form.widget('reproductionData_descriptiveElements_publisher', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    reproductionData_descriptiveElements_contributor = RelationList(
        title=_(u'Contributor'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )

    form.widget('reproductionData_descriptiveElements_contributor', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    reproductionData_descriptiveElements_source = ListField(title=_(u'Source'),
        value_type=DictRow(title=_(u'Source'), schema=ISource),
        required=False)
    form.widget(reproductionData_descriptiveElements_source=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductionData_descriptiveElements_source')

    reproductionData_descriptiveElements_coverage = schema.List(
        title=_(u'Coverage'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )
    form.widget('reproductionData_descriptiveElements_coverage', AjaxSelectFieldWidget, vocabulary="collective.imageReference.coverage")

    reproductionData_descriptiveElements_rights = ListField(title=_(u'Rights'),
        value_type=DictRow(title=_(u'Rights'), schema=IRights),
        required=False)
    form.widget(reproductionData_descriptiveElements_rights=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductionData_descriptiveElements_rights')

    reproductionData_descriptiveElements_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(reproductionData_descriptiveElements_notes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductionData_descriptiveElements_notes')

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
        fields=['linkedObjects_linkedobjects']
    )

    linkedObjects_linkedobjects = RelationList(
        title=_(u'Object number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            vocabulary='collective.object.relateditems'
        ),
        required=False
    )

    form.widget('linkedObjects_linkedobjects', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


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
            if group.__name__ not in ['settings', 'categorization', 'ownership', 'dates']:
                for widget in group.widgets.values():
                    if IDataGridField.providedBy(widget):
                        widget.auto_append = False
                        widget.allow_reorder = True
                    alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget):
                widget.auto_append = False
                widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)


class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('imageReference_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            if group.__name__ not in ['settings', 'categorization', 'ownership', 'dates']:
                for widget in group.widgets.values():
                    if IDataGridField.providedBy(widget):
                        widget.auto_append = False
                        widget.allow_reorder = True
                    alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    






