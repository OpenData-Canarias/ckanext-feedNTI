import ckan.plugins as plugins
import pylons.config as config

#La clase se encarga de crear la ruta en la que escuchar las peticiones del feed.
class RoutingFeed(plugins.SingletonPlugin):

	defaultPath = '/feeds/datasetNTI.atom'
	ckanConfigParam = 'ckan.feedNTI.url'
	#Obtiene el path desde el fichero de configuracion
	path = config.get(ckanConfigParam,defaultPath)
    
	plugins.implements(plugins.IRoutes, inherit=True)
	
	def before_map(self, map):
	

        	map.connect(self.path,
                	controller='ckanext.feedNTI.controller:FeedNTIController',
			action='getCatalog')
		return map
