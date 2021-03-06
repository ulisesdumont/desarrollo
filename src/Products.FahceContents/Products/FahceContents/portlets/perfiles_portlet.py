# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from zope.interface import implements

class IPerfilesPortlet(IPortletDataProvider):
    #count = schema.Int(title=_(u'Number of items to display'),description=_(u'How many items to list.'),required=True,default=5)
    pass

class Assignment(base.Assignment):
    implements(IPerfilesPortlet)

    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Enlaces segun perfiles")

from zope.formlib import form
class AddForm(base.NullAddForm):
    #form_fields = form.Fields(IRecentPortlet)
    label = _(u"Agregar portlet de accesos directos")
    description = _(u"This portlet displays recently modified content.")

    def create(self):
        return Assignment()

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('perfiles_portlet.pt')

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

    def dameItems(self):
        area=self.context.getPhysicalPath()[0:2]
        folder_path = '/'.join(area)
        links = self.catalog(path={'query': folder_path, 'depth': 2}, portal_type='Products.FahceContents.acceso')

        res=[]
        if len(links) > 0:
            for link in links:
                url=""
                info_link=self.context.unrestrictedTraverse(link.getPath())
                perfiles=" ".join(info_link.perfiles)
                if hasattr(info_link.enlace,'to_path'):
                    url=info_link.enlace.to_path
                res.append((info_link.title,info_link.Description(),perfiles,url))
        return  res

