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

class IMenu(model.Schema):
    """
    Una carpeta de menú
    """
    
    form.mode(title='hidden')
    title = schema.TextLine(
           title=_(u"Título"),
           default=_(u"Menú"),
           required=False,
    )

class Menu(Container):
    grok.implements(IMenu)
    #Add your class methods and properties here
    pass

class View(grok.View):
    """ sample view class """
    grok.context(IMenu)
    grok.require('zope2.View')
    grok.name('view')
    
    def dame_enlaces(self):
        res=[]
        items = self.context.getFolderContents()
        for item in items:         
            enlace=self.context.unrestrictedTraverse(item.getPath())
            #if elem.id != self.context.id:
                #fullname="%s %s" %(miObjPosta.nombre,miObjPosta.apellido)
            #url='/'.join(enlace.to_object.enlace.getPhysicalPath())
            res.append((item.Title,item.getPath(),enlace))
        return res
 
