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


# Interface class; used to define content-type schema.

class IPortada(model.Schema):
    """
    Una noticia que se mostrará en la página de inicio
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.

    #form.widget(enlace=AutocompleteFieldWidget)
    title = schema.TextLine(title=_(u"titulo"),default=_(u"Portada"))
    noticias=schema.List(
        title=_(u"Noticias destacadas"),
        value_type=schema.Choice(source="vocabularios.Noticias",),
    )


class Portada(Item):
    implements(IPortada)
    #Add your class methods and properties here
    pass


from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

class View(grok.View):
    """ sample view class """
    grok.context(IPortada)
    grok.require('zope2.View')
    grok.name('view')
    
    def dame_noticias(self):
        noticias=self.context.noticias
        resultado=[]
        for noticia in noticias:
            tmp=noticia.split('/')[4:]
            area_titulo=self.context.unrestrictedTraverse(tmp[0]).title
            noti=self.context.unrestrictedTraverse(tmp)
            resultado.append((noti.title,noti.Description(),noti.absolute_url(),area_titulo))
        return resultado

    
