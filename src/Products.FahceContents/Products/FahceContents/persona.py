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
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.app.textfield import RichText

from Products.FahceContents import MessageFactory as _

from Products.Five.browser import BrowserView
import random
from five import grok

# Interface class; used to define content-type schema.

class IPersona(model.Schema):
    """
    Una persona loca
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.
 
    form.mode(title='hidden')
    title = schema.TextLine(
           title=_(u"Título"),
           default=_(u"Persona"),
           required=False,
    )

    nombre = schema.TextLine(
           title=_(u"Nombre"),
    )

    apellido = schema.TextLine(
           title=_(u"Apellido"),
    )

    id_conicet = schema.TextLine(
             title=_(u"Id en CONICET"),
             required= False,
    )

 
class Persona(Item):
    implements(IPersona)
    #Add your class methods and properties here
    pass

#crea el título del objeto y su id a partir del nombre y apellido 
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.normalizer import idnormalizer

def rename(persona,event):
    parent = persona.aq_parent
    titulo=persona.apellido+' '+persona.nombre
    persona.setTitle(titulo)
    persona.reindexObject()
    id_nueva=idnormalizer.normalize(titulo)
    parent.manage_renameObject(persona.getId(), str(id_nueva)) 

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog


class View(grok.View):
    """ sample view class """
    grok.context(IPersona)
    grok.require('zope2.View')
    grok.name('view')
   
    def dameReferencia(self):
        return self.back_references(self.context,"persona")

    def back_references(self,source_object, attribute_name):
        """ Return back references from source object on specified attribute_name """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        for rel in catalog.findRelations(
                                dict(to_id=intids.getId(aq_inner(source_object)),
                                     from_attribute=attribute_name)
                                ):
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result

    def dame_carpeta(self):
        from Acquisition import aq_parent
        padre = aq_parent(self.context) 
        contenidos = padre.getFolderContents()
        res=[]
        for elem in contenidos:
            
            miObjPosta=self.context.unrestrictedTraverse(elem.getPath())


            if elem.id != self.context.id:
                fullname="%s %s" %(miObjPosta.nombre,miObjPosta.apellido)
                res.append((fullname,elem.getPath()))
        return res

