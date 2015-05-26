# -*- coding: utf-8 -*-
#formulario de inscripción a cursos de posgrado
from five import grok
from plone.supermodel import model
from plone.directives import form
from zope import schema
from z3c.form import button, field
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import Interface
from Products.FahceContents import MessageFactory as _
from Products.CMFCore.utils import getToolByName

class IInscripcion(model.Schema):

    nombre = schema.TextLine(title=_(u"Nombre"))
    apellido = schema.TextLine(title=_(u"Apellido"))
    dni = schema.TextLine(title=_(u"Documento"))
    email = schema.TextLine(title=_(u"E-mail"))
    responsable = schema.TextLine(title=_(u"E-mail"))
    uid =  schema.TextLine(title=_(u"E-mail"))
    
class Inscripcion(form.SchemaForm):
    grok.name('forminscripcion')    
    grok.require('zope2.View')
    grok.context(Interface)

    schema = IInscripcion
    ignoreContext = True

    label = _(u"Inscripción")

    def update(self):
        self.request.set('disable_border', True)
        super(Inscripcion, self).update()
        #guardo en una variable el acceso al widget del campo     
        micampo=self.widgets["responsable"]
        #oculto el campo para que exista en el formulario, pero que el usuario no lo vea.
        micampo.mode="hidden"
        
        micampouid=self.widgets["uid"]
        if self.request.form.has_key("uid"):
           micampouid.value=self.request.form["uid"]
        #oculto el campo para que exista en el formulario, pero que el usuario no lo vea.
        micampouid.mode="hidden"
        
        if self.request.form.has_key("emailresponsable"):
           micampo.value=self.request.form["emailresponsable"]
            
    def getContent(self):
        data={}
        data['nombre'] = u"nombre"
        data['apellido'] = u"apellido"
        data['dni'] = u"dni"
        data['email'] = u"email"
        data['responsable'] = u"responsable"
        data['uid'] = u"uid"


    @button.buttonAndHandler(_(u'Enviar'))
    def handleOk(self, action):
        data, errors = self.extractData()
        #Envia correo
        #self.context.MailHost.send(subject="Inscripción", messageText=data["nombre"], mto=data["responsable"], mfrom=data["email"])
        #llama a la función de almacenar inscriptos en el objeto curso
        cat=getToolByName(self.context,'portal_catalog')
        cat(UID=data['uid'])
        brain=cat(UID=data['uid'])
        brain[0].getObject().guardainscripto(data['nombre'])
        #redirecciona a la url del curso
        url = self.context.absolute_url()
        self.request.response.redirect(url)
        
        if errors:
            self.status = self.formErrorsMessage
            return

       
    #@button.buttonAndHandler(_(u"Cancelar"))
    #def handleCancel(self, action):
        #return
