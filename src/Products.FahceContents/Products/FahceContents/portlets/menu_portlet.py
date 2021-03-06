# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from zope.interface import implements

class IMenuPortlet(IPortletDataProvider):
    #count = schema.Int(title=_(u'Number of items to display'),description=_(u'How many items to list.'),required=True,default=5)
    pass

class Assignment(base.Assignment):
    implements(IMenuPortlet)

    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Menú del area")

from zope.formlib import form
class AddForm(base.NullAddForm):
    #form_fields = form.Fields(IRecentPortlet)
    label = _(u"Agregar carpeta de menú")
    description = _(u"This portlet displays recently modified content.")

    def create(self):
        return Assignment()

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('menu_portlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous
        self.portal_url = portal_state.portal_url()  # the URL of the portal object

        # a list of portal types considered "end user" types
        self.typesToShow = portal_state.friendly_types()

        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        #return not self.anonymous and len(self._data())
        return True

    #def dame_info(self):
        #"""Devuelve la info del area"""
        #lugar=self.context        
        #area=lugar.unrestrictedTraverse(lugar.getPhysicalPath()[2])
        #dato=  {'telefono': area.telefono, 'edificio': area.edificio, 'oficina': area.oficina, 'email': area.email, 'cargos':self.dameCargos()}
        #return dato

    def dameItems(self):
        #items_lugar=self.context.menu
        #import pdb
        #pdb.set_trace()
        #carpeta=items_lugar.unrestrictedTraverse(items_lugar.getPhysicalPath()[3])
        area=self.context.getPhysicalPath()[0:3]
        folder_path = '/'.join(area)+'/menu'
        items = self.catalog(path={'query': folder_path, 'depth': 2}, portal_type=('Products.FahceContents.menu_item'), sort_on='getObjPositionInParent')
        #cargos = self.catalog()
        res=[]
        if len(items) > 0:
            for item in items:
                info_item=self.context.unrestrictedTraverse(item.getPath())
                url="#"
                if hasattr(info_item.enlace,'to_path'):
                    url=info_item.enlace.to_path
                    
                res.append((item.Title,info_item.indent,url))
        return res

