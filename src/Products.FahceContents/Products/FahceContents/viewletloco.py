from five import grok
from zope.component import getMultiAdapter
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IBelowContentTitle
from zExceptions import Forbidden
from plone.app.layout.viewlets.interfaces import IPortalHeader, IPortalTop
from zope.interface import Interface 
from plone.app.layout.navigation.interfaces import INavigationRoot

class ViewletLoco(grok.Viewlet):
    grok.context(INavigationRoot)
    grok.view(IViewView)
    grok.viewletmanager(IPortalTop)
    grok.name('viewletloco')
    grok.require('zope2.View')
    
    def dame_info(self):
        context = self.context.aq_inner
        return self.dame_enlaces()

    def dame_enlaces(self):
        res=[]
        items = self.context.portal_catalog.searchResults({'portal_type': 'Products.FahceContents.super_area'})
        for item in items:         
            enlace=self.context.unrestrictedTraverse(item.getPath())
            #if elem.id != self.context.id:
                #fullname="%s %s" %(miObjPosta.nombre,miObjPosta.apellido)
            #url='/'.join(enlace.to_object.enlace.getPhysicalPath())
            res.append((item.Title,item.getURL(),enlace))
        return res
