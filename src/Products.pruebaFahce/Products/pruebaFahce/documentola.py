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

from Products.pruebaFahce import MessageFactory as _

from Products.Five.browser import BrowserView
import random
from five import grok


from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@grok.provider(IContextSourceBinder)
def personas_relacionadas(context):
    """
    Populate vocabulary with values from portal_catalog.

    @param context: z3c.form.Form context object (in our case site root)

    @return: SimpleVocabulary containing all areas as terms.
    """

    from Products.CMFCore.utils import getToolByName
    catalog = getToolByName(context, 'portal_catalog')
    result = catalog(portal_type='Products.FahceContents.persona')
    terminos = []
    for brain in result:
        persona = context.unrestrictedTraverse(brain.getPath())   
        termino=SimpleTerm(value=persona.id, token=persona.apellido+' '+persona.nombre, title=persona.apellido+' '+persona.nombre)
        terminos.append(termino)
    return SimpleVocabulary(terminos)



# Interface class; used to define content-type schema.

class IDocumentola(model.Schema):
    """
    Un documento loco
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/documentola.xml to define the content type.

    details = RichText(
            title=_(u"Campo texto"),
            description=_(u"Texto con formato"),
            required=False,
        )

    #persona = schema.Choice(
            #title=_(u"Persona"),
            #description=_(u"Elija el nivel"),
            #source = personas_relacionadas
        #)


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Documentola(Item):
    implements(IDocumentola)
    #Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# documentola_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(BrowserView):
    """ sample view class """
    #grok.context(IDocumentola)
    #grok.require('zope2.View')
    def __init__(self, context, request):
        """ Initialize context and request as view multi adaption parameters.

        Note that the BrowserView constructor does this for you.
        This step here is just to show how view receives its context and
        request parameter. You do not need to write __init__() for your
        views.
        """
        self.context = context
        self.request = request

    # grok.name('view')
    # Add view methods here
    def dameUnTituloLoco(self):
        #import pdb
        #pdb.set_trace()
        titulos=["Mauricio es un groso", "Parente esta de fiesta", "Archuby hace asado","Peron en bicicleta"]
        return titulos[int(random.uniform(1,len(titulos)-1))]


