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

from plone.namedfile import field
from DateTime import DateTime

from plone.formwidget.autocomplete import AutocompleteFieldWidget, AutocompleteMultiFieldWidget
from Products.FahceContents.persona import IPersona
from Products.CMFCore.utils import getToolByName

# Interface class; used to define content-type schema.

class ICurso(model.Schema):
    """
    Un curso de posgrado
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.
 
    #form.mode(title='hidden')
    title = schema.TextLine(
           title=_(u"Título"),
           default=_(u"Curso"),
           required=False,
    )

    form.widget(docentes=AutocompleteMultiFieldWidget)
    docentes = schema.List(title=_(u"Docentes"),
            value_type=RelationChoice(
                    source=ObjPathSourceBinder(object_provides=IPersona.__identifier__),
                    required=False)
    )    
    programa=field.NamedFile(title=u"Programa")
    
    inscripcionini=schema.Datetime(
        title=_(u"Inicio de inscripción"),
        required=True,
    )
    inscripcionfin=schema.Datetime(
        title=_(u"Cierre de inscripción"),
        required=True,
    )

    inscriptos=schema.Text(
        title=_(u"Inscriptos"),required=False
    )

    email = schema.TextLine(title=_(u"Email del responsable"), default=u"mesterellas@fahce.unlp.edu.ar")

class Curso(Item):
    implements(ICurso)
    #Add your class methods and properties here
    def guardainscripto(self,inscripto):
        self.inscriptos=inscripto
    pass

#crea el título del objeto y su id a partir del nombre y apellido 
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.normalizer import idnormalizer


from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog


class View(grok.View):
    """ sample view class """
    grok.context(ICurso)
    grok.require('zope2.View')
    grok.name('view')

    def formvisible(self):
        hoy = DateTime()
        inicio=DateTime(self.context.inscripcionini)
        fin=DateTime(self.context.inscripcionfin)
        if (inicio < hoy) and (hoy < fin):
            return True
        else:
            return False
    
    def damedatos(self):
        datos=[]
        docentes=self.context.docentes
        res[]
        for docente in docentes:
            datos_docente=(docente.nombre, docente.apellido, docente.Path()
        import pdb
        pdb.set_trace()
        datos=[self.context.title,docentes]
        return datos