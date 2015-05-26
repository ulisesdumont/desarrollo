# -*- coding: utf-8 -*-
from plone.supermodel import model
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.autoform import directives as form

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implements
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.app.textfield import RichText

from Products.FahceContents import MessageFactory as _

from Products.Five.browser import BrowserView
import random
from five import grok

from Products.FahceContents.cargo import ICargo

from zope.component import createObject


# Interface class; used to define content-type schema.

class ISuperArea(model.Schema):
    """
    Una Super Area
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.

    form.fieldset('contacto',
           label=u"Contacto",
           fields=['telefono', 'edificio', 'oficina', 'email']
    )

    telefono = schema.TextLine(
           title=_(u"Teléfono"),
           description=_(u"Ingrese el número de interno"),
    )

    edificio = schema.Choice(
            title=_(u"Edificio"),
            description=_(u"Seleccione el edificio"),
            values=(
                u'A',
                u'B',
                u'C',)
    )

    oficina = schema.TextLine(
             title=_(u"Oficina"),
    )
    
    email = schema.TextLine(
             title=_(u"E-mail"),
    )
    
class SuperArea(Container):
    grok.implements(ISuperArea)
    #Add your class methods and properties here
    pass

class View(grok.View):
    """ sample view class """
    grok.context(ISuperArea)
    grok.require('zope2.View')
    grok.name('view')
    
    def dame_noticias(self):
        noticias=self.context.noticias.getFolderContents()
        resultado=[]
        for noticia in noticias:
            resultado.append((noticia.Title,noticia.Description,noticia.getPath()))
        return resultado

    def dame_eventos(self):
        eventos=self.context.eventos.getFolderContents()
        resultado=[]
        for evento in eventos:
            resultado.append((evento.Title,evento.Description,evento.getPath()))
        return resultado


