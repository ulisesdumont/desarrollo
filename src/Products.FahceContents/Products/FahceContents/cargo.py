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

from plone.formwidget.contenttree import ObjPathSourceBinder, ContentTreeFieldWidget, PathSourceBinder

from plone.app.textfield import RichText

from Products.FahceContents import MessageFactory as _

from Products.Five.browser import BrowserView
import random
from five import grok

from plone.formwidget.autocomplete import AutocompleteFieldWidget, AutocompleteMultiFieldWidget


from Products.FahceContents.persona import IPersona
from plone.autoform import directives
from plone.directives import dexterity, form
from Products.FahceContents.adapter import KeywordSourceBinder
from plone.formwidget.contenttree import ContentTreeFieldWidget

#función para definir donde buscar cargos


#@grok.provider(IContextSourceBinder)
#def personas_disponibles(context):

    #path = '/Plone/personal'
    #query = { "portal_type" : ("Products.FahceContents.persona"),
              #"path": {'query' :path } 
             #}
  
    #return ObjPathSourceBinder(navigation_tree_query = query).__call__(context) 

# Interface class; used to define content-type schema.

class ICargo(form.Schema):
    """
    Añadir un cargo
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.

    title = schema.TextLine(
           title=_(u"Nombre del cargo"),
    )

    tipo = schema.Choice(
            title=_(u"Tipo"),
            description=_(u"Elija el tipo"),
            values=(
                u'Docente',
                u'No Docente',
                u'Gestion',
                u'Otro',)
    )

 
    form.widget(persona=AutocompleteFieldWidget)
    #directives.widget('persona', AutocompleteFieldWidget)
    persona = RelationChoice(
             title=_(u"Persona"),
             source=ObjPathSourceBinder(object_provides=IPersona.__identifier__),
             #source=personas_disponibles,
             required=True,
    )
    
    #form.widget(model=ContentTreeFieldWidget)
    #model = schema.Choice(
            #title=_('label_model', default='Model'),
            #source=ObjPathSourceBinder(object_provides=IPersona.__identifier__),
    #)
    
    #form.widget(tipos=AutocompleteMultiFieldWidget)
    #directives.widget('persona', AutocompleteFieldWidget)
    #tipos = RelationList(
             #title=_(u"Tipos"),
             #value_type=RelationChoice(
                #source=ObjPathSourceBinder(object_provides=IPersona.__identifier__),),
             #source=personas_disponibles,
             #unique=True,
             #required=True,
    #)
    
class Cargo(Item):
    implements(ICargo)
    #Add your class methods and properties here
    pass

class View(grok.View):
    """ sample view class """
    grok.context(ICargo)
    grok.require('zope2.View')
    grok.name('view')


