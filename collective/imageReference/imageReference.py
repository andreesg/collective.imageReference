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

    model.fieldset('image_references', label=_(u'Image reference'), 
        fields=['imageReference', 'productionDate', 'imageFormat', 'referenceNumber', 'creator', 'location',
                'notes', 'reproductionType']
    )

    imageReference = schema.TextLine(title=_(u'Image reference'), required=False)
    productionDate = schema.TextLine(title=_(u'Production date'), required=False)
    imageFormat = schema.TextLine(title=_(u'Format'), required=False)
    referenceNumber = schema.TextLine(title=_(u'Reference number'), required=False)
    creator = schema.TextLine(title=_(u'Creator'), required=False)
    location = schema.TextLine(title=_(u'Location'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
    reproductionType = schema.TextLine(title=_(u'Reproduction type'), required=False)


alsoProvides(IImageReference, IFormFieldProvider)


# # # # # # # # # # # # # # # # #
# imageRefrence declaration     #
# # # # # # # # # # # # # # # # #

class ImageReference(Item):
    implements(IImageReference)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context






