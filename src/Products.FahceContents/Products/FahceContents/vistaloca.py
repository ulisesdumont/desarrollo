from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
class VistaLoca(grok.View):
    """View for showing content related to a particular DAM code
    """
    grok.context(INavigationRoot)
    grok.name('vistaloca')
    grok.require('zope2.View')

    def update(self):
       # Hide the editable-object border
       self.request.set('disable_border', True)      

