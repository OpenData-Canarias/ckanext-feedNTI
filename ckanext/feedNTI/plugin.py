#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ckan.plugins as plugins
import pylons.config as config

# Clase encargada de realizar el routing en CKAN.
# 
# V1.0:
# - Permite una ruta por defecto que ser� /feeds/datasetNTI.atom'
# - Permite configurar la ruta del feed mediante un parametro de configuraci�n de CKAN (ckan.feedAtomNTI.url)

class RoutingFeedAtomNTI(plugins.SingletonPlugin):

	defaultPath = '/feeds/datasetNTI.atom'
	ckanConfigParam = 'ckan.feedAtomNTI.url'
	
	#Obtiene el path desde el fichero de configuracion
	path = config.get(ckanConfigParam,defaultPath)

	plugins.implements(plugins.IRoutes, inherit=True)
	
	def before_map(self, map):
		map.connect(self.path,
                	controller='ckanext.feedNTI.controller:NTIAtom1FeedController',
			action='getCatalog')
		return map
