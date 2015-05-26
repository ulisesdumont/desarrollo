# -*- coding: utf-8 -*-
from plone.supermodel import model
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implements
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder, PathSourceBinder

from plone.app.textfield import RichText

from Products.FahceContents import MessageFactory as _

from Products.Five.browser import BrowserView
import random
from five import grok

from plone.autoform import directives
from plone.directives import dexterity, form
from plone.formwidget.autocomplete import AutocompleteFieldWidget, AutocompleteMultiFieldWidget
from plone.formwidget.contenttree import ContentTreeFieldWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget

@grok.provider(IContextSourceBinder)
def objetos_disponibles(context):

    #path = '/'.join(context.getTmp_folder().getPhysicalPath())
    path = '/'.join(context.getPhysicalPath()[0:3])
    #path = '/'
    query = {"path": {'query' :path }}
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context) 


# Interface class; used to define content-type schema.

class IAcceso(model.Schema):
    """
    Un acceso directo
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.

    form.widget(perfiles=CheckBoxFieldWidget)
    enlace = RelationChoice(
          title=_(u"Enlace"),
          source=ObjPathSourceBinder(),
          required=False,
    )
    perfiles = schema.List(
            title=_(u"Perfiles"),
            #description=_(u"Elija el tipo"),
            value_type=schema.Choice(values=(
                u'Alumno',
                u'Docente',
                u'No-docente',
                u'Extranjero',
                u'Investigador',)),
            required=True,
    )

class Acceso(Item):
    implements(IAcceso)
    #Add your class methods and properties here
    pass


from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

class View(grok.View):
    """ sample view class """
    grok.context(IAcceso)
    grok.require('zope2.View')
    grok.name('view')

    def dameItem(self):
        res=[]
        #perfiles=[]
        #info_item=self.context.unrestrictedTraverse(self.getPath())
        #.enlace.to_path
        url="#"
        perfiles=self.context.perfiles
        if hasattr(self.context.enlace,'to_path'):
            url=self.context.enlace.to_path
        res.append((self.context.title,self.context.Description(),perfiles,url))
        return res

