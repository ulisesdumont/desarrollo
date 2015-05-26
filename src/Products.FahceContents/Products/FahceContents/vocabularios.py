# -*- coding: utf-8 -*-
from five import grok
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite
from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from Acquisition import aq_parent
_ = MessageFactory('plone')
class NoticiasVocab(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return self.generaVocab()

    def generaVocab(self):
        terms = []
        site = getSite()


        wcat  = getToolByName(site, 'portal_catalog', None)

        cata=wcat(object_provides="Products.ATContentTypes.interfaces.news.IATNewsItem",sort_on="effective",review_state="published")[:20]

        for brain in cata:
            
            barinToken=brain.UID
            
            terms.append(SimpleTerm(
                    token=barinToken,
                    value=brain.getURL(),
                    title=brain.Title)
                )

        return SimpleVocabulary(terms)

NoticiasVocabFactory = NoticiasVocab()
