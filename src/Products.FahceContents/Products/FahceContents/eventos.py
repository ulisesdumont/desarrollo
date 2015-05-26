# -*- coding: utf-8 -*-
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from Products.ATContentTypes.lib import constraintypes
from zope.container.interfaces import INameChooser
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component.hooks import getSite
import logging
from AccessControl.interfaces import IRoleManager

import transaction
carpetasAreaDict=[
    {"id":"noticias","titulo":"Noticias","tipo":"Folder","constraint":["News Item"],"descri":""},
    {"id":"eventos","titulo":"Eventos","tipo":"Folder","constraint":["Event"],"descri":""},
    {"id":"descargables","titulo":"Descargables","tipo":"Folder","constraint":["File"],"descri":""},
    {"id":"imagenes","titulo":"Imagenes","tipo":"Folder","constraint":["Image"],"descri":"Carpeta de imagenes"},
    {"id":"menu","titulo":"Menu","tipo":"Products.FahceContents.menu","constraint":[],"descri":""},
    {"id":"cargos","titulo":"Cargos","tipo":"Folder","constraint":["Products.FahceContents.cargo"],"descri":""},
]
carpetasSuperAreaDict=carpetasAreaDict+[
    {"id":"areas","titulo":"Areas","tipo":"Folder","constraint":["Products.FahceContents.area"],"descri":""},
]
def onCreateSuperArea(objeto,event):
    workflowTool = getToolByName(objeto, "portal_workflow")
    #flag=0

    for carpeta in carpetasSuperAreaDict:
        newId=carpeta["id"]

        if not hasattr(objeto,newId):
            oid=objeto.invokeFactory(carpeta["tipo"], id=newId)
            transaction.savepoint(optimistic=True)
            new_obj = objeto[oid]
            new_obj.setTitle(carpeta["titulo"])
            new_obj.setDescription(carpeta["descri"])

            #
            # Habilita el filtrado de tipos de contenidos
            #
            if len(carpeta["constraint"])>0:
                new_obj.setConstrainTypesMode(constraintypes.ENABLED)
                # Types for which we perform Unauthorized check
                new_obj.setLocallyAllowedTypes(carpeta["constraint"])
                # Add new... menu  listing
                new_obj.setImmediatelyAddableTypes(carpeta["constraint"])

            try:
                workflowTool.doActionFor(new_obj, "publish")
                #logger.info("Estado cambiado!")
            except WorkflowException:
                # a workflow exception is risen if the state transition is not available
                # (the sampleProperty content is in a workflow state which
                # does not have a "submit" transition)
                logger.info("Could not publish:" + str(new_obj.getId()) + " already published?")
                pass
            new_obj.reindexObject()
            #flag=flag+1
        else:
            print "la carpeta estaba creada"

def onCreateArea(objeto,event):
    #workflowTool = getToolByName(objeto, "portal_workflow")

    for carpeta in carpetasAreaDict:
        newId=carpeta["id"]
        #import pdb
        #pdb.set_trace()
        if hasattr(objeto,newId):
            if len(objeto.getPhysicalPath())>len(getattr(objeto,newId).getPhysicalPath()):
                
                creaCarpeta(carpeta,objeto,newId)
            else:
                print "ya estola"
        else:
             creaCarpeta(carpeta,objeto,newId)
                
def creaCarpeta(carpeta,objeto,newId):    
    workflowTool = getToolByName(objeto, "portal_workflow")
    #flag=0

    oid=objeto.invokeFactory(carpeta["tipo"], id=newId)
    transaction.savepoint(optimistic=True)
    new_obj = objeto[oid]
    new_obj.setTitle(carpeta["titulo"])
    new_obj.setDescription(carpeta["descri"])

    #
    # Habilita el filtrado de tipos de contenidos
    #
    if len(carpeta["constraint"])>0:
        new_obj.setConstrainTypesMode(constraintypes.ENABLED)
        # Types for which we perform Unauthorized check
        new_obj.setLocallyAllowedTypes(carpeta["constraint"])
        # Add new... menu  listing
        new_obj.setImmediatelyAddableTypes(carpeta["constraint"])

    try:
        workflowTool.doActionFor(new_obj, "publish")
        #logger.info("Estado cambiado!")
    except WorkflowException:
        # a workflow exception is risen if the state transition is not available
        # (the sampleProperty content is in a workflow state which
        # does not have a "submit" transition)
        logger.info("Could not publish:" + str(new_obj.getId()) + " already published?")
        pass
    new_obj.reindexObject()
    #flag=flag+1
    
