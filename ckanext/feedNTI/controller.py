import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model

import pylons.config as config

import datetime
import webhelpers.feedgenerator
from webhelpers.util import SimplerXMLGenerator

from ckan.common import c,g, response

from ckanext.feedNTI.NTIAtom1FeedTemplate import NTIAtom1FeedTemplate
from ckanext.feedNTI.NTIAtom1Feed import NTIAtom1Feed

# Se encarga de gestionar todo el proceso para generar el feed.
# Desde recoger los datos, crear la estructura del feed hasta devolver
# la respuesta en formatao Atom. 

#Realiza la consulta a la API paa recuperar todos los datasets del catalogo
#Retorna la cantidad de datasets y los metadatos de cada uno
def _package_search():

	context = {'model': model, 'session': model.Session,
				'user': c.user or c.author, 'auth_user_obj': c.userobj }
	
	# Ordenar los resultados por fecha de modificacion
	data_dict = {} 
	data_dict['sort'] = 'metadata_modified desc'
	data_dict['rows'] = '50'	# Se limitan los resultados a 50, ojo con esto

	# Realizar la consulta
	query = logic.get_action('package_search')(context, data_dict.copy())
	
	return query['count'], query['results']

# Se encarga de gestionar el proceso para generar el feed.
# Coge los datos del catalogo y se los pasa al NTIAtom1Feed para que genere el feed
#
# El controllador esd el que entiende como funciona ckan, debe mandarle al NTI1Atom1Feed
# los campos bien formateados.
class NTIAtom1FeedController(base.BaseController):
	# Metodo principal
	# Genera el feed completo del catalogo
	def getCatalog(self):
		item_count, datasets = _package_search()
		
		# Rellenar los campos del feed (metadatos del catalogo)
		feedData = {
			'id': g.site_url,
			'nombre': g.site_title,
			'descripcion': g.site_description,
			'organoPublicador': config.get('ckan.feedNTI.publicador',''),
			'tamanoCatalogo': str(item_count),
			'fechaCreacion': config.get('ckan.feedNTI.fechaCreacion',''),
			'updated': webhelpers.feedgenerator.rfc3339_date(datetime.datetime.now()).decode('utf-8'),
			'idioma': config.get('ckan.locale_default',''),
			'coberturaGeografia': config.get('ckan.feedNTI.coberturaGeografica',''),
			'category': config.get('ckan.feedNTI.tematica',''),
			'link': g.site_url,
			'terminosUso': config.get('ckan.feedNTI.terminosUso','')
		}
		
		# Genera el feed
		return self.output_feed(datasets,feedData)

	# Se encarga de general la respuesta para el feed.
	def output_feed(self, datasets, feedData={}):
		# Cabeceras del feed, metadatos del catalogo
		feed = NTIAtom1Feed(
					nombre=feedData['nombre'],
					link=feedData['link'],
					descripcion=feedData['descripcion'],
					id=feedData['id'],
					organoPublicador=feedData['organoPublicador'],
					tamanoCatalogo=feedData['tamanoCatalogo'], 
					fechaCreacion=feedData['fechaCreacion'],
					updated=feedData['updated'],
					idioma=feedData['idioma'],
					coberturaGeografica=feedData['coberturaGeografia'], 
					category=feedData['category'],
					terminosUso=feedData['terminosUso'])

		# metadatos de los datasets
		for pkg in datasets:
			# Categoria / Grupo principal
			# Solo se obtiene la primera cateogria (grupo)
			group = None
			groupArray = pkg.get('groups',None)
			if (groupArray is not None)	and (len(groupArray) > 0):
				group = groupArray[0]['display_name']
				
			# Tag / Etiqueta principal
			# Solo se muestra la primera etiqueta
			tag= None
			tagArray = pkg.get('tags',None)
			if (tagArray is not None) and (len(tagArray) > 0):
				tag = tagArray[0]['display_name']
				
			# Idioma / Cobertura Geografica / Cobertura Temporal / ...
			# Son campos definidos como extras en CKAN
			idiomaT = None
			cobgeo = None
			cobTempComienzo = None
			cobTempFinal = None
			vigencia = None
			frecupd = None
			recrel= None
			norma = None
			
			extras = pkg.get('extras',None)
			if extras is not None:
				for extra in extras:
					if extra['key'] == 'Idioma':
						idiomaT = extra['value']
					elif extra['key'] == 'Cobertura Geográfica':
						cobgeo = extra['value']
					elif extra['key'] == 'Cobertura Temporal':
						cobTempComienzo = extra['value']
						cobTempFinal = extra['value']
					elif extra['key'] == 'Vigencia':
						vigencia = extra['value']
					elif extra['key'] == 'Frecuencia Actualización':
						frecupd = extra['value']
					elif extra['key'] == 'Recurso Relacionado':
						recrel = extra['value']
					elif extra['key'] == 'Normativa':
						norma = extra['value']
			
			# Organismo Publicador
			publisher = None
			org = pkg.get('organization',None)
			if org is not None:
				publisher = org['title']
			
			# Recursos
			resources = []
			ckanResources = pkg.get('resources',None)
			for ckanResource in ckanResources:
				resource = {
					'link': ckanResource['url'],
					'formato': ckanResource['mimetype'],
					'identificador': ckanResource['id'],
					'nombre': ckanResource['name'],
					'tamano': ckanResource['size'],
					# CKAN no implementa el metadato para información adicional, se genera la url para el recurso en ckan o se deja vacio
					'informacionAdicional': None,
					#'informacionAdicional': g.site_url + '/dataset' + pkg.get('name','') + '/resource/' + ckanResource['id']
				}
				
				resources.append(resource)
			
			feed.add_item(
				nombre = pkg.get('title',None),
				summary = pkg.get('notes',None),
				id = g.site_url + "/dataset/" + pkg.get('name',None),
				category = group,
				keyword = tag,
				published = pkg.get('metadata_created',None),
				updated = pkg.get('metadata_modified',None),
				frecuenciaActualizacion = frecupd,
				idioma = idiomaT, 
				organismoPublicador = publisher, 
				condicionesUso = pkg.get('license_url',None),
				coberturaGeografica = cobgeo, 
				coberturaTemporalComienzo= cobTempComienzo,
				coberturaTemporalFinal = cobTempFinal,
				vigenciaRecurso = vigencia,
				recursoRelacionado = recrel,
				normativa = norma,
				distribucion = resources)        
							
		response.content_type = feed.mime_type
		return feed.writeString('utf-8')


