# -*- coding: utf-8 -*-
__author__ = 'Paul'
from zope.schema.interfaces import IContextSourceBinder
from z3c.formwidget.query.interfaces import IQuerySource
from zope.interface import Interface, implements
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm
#from Products.bpContents.categoriasVocab import CategoriasVocab
vocab=SimpleVocabulary([SimpleTerm(
                        token="Juan",
                        value="Juan",
                        title="Juan"),
						SimpleTerm(
                        token="Pedro",
                        value="Pedro",
                        title="Pedro"),
						SimpleTerm(
                        token="Pedro1",
                        value="Pedro1",
                        title="Pedro1")])

class KeywordSource(object):
    implements(IQuerySource)


    def __init__(self, context):
        self.context = context
        self.catalog = getToolByName(context, 'portal_catalog')
        self.keywords =vocab
        self.vocab = self.keywords
        self.flag=0

    def __contains__(self, term):
        return self.vocab.__contains__(term)

    def __iter__(self):
        return self.vocab.__iter__()

    def __len__(self):
        return self.vocab.__len__()

    def getTerm(self, value):
        try:
            valor=self.vocab.getTerm(value)
        except LookupError:
            print "Error buscando el termino"
            self.flag+=1
            strT=str(self.flag)

            return SimpleTerm(
                token=strT,
                value=strT+':'+strT,
                title=strT)



        return valor

    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)

    def search(self, query_string):
        qA = query_string.lower()

        filtra= []

        for kw in self.keywords:

            if kw!="":
                ttt=kw.value.decode("utf-8")

                if qA in ttt.lower():
                    filtra.append(self.getTerm(ttt))

        return filtra

class KeywordSourceBinder(object):
    implements(IContextSourceBinder)

    def __call__(self, context):
        return KeywordSource(context)
