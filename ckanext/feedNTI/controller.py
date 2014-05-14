import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model

import pylons.config as config

import datetime
import webhelpers.feedgenerator
from webhelpers.util import SimplerXMLGenerator

from ckan.common import c,g, response

from feedNTI import FeedNTI

"""
Realiza la consulta a la API para recuperar todos los datasets del catalogo
Retorna la cantidad de datasets y los metadatos de cada uno
"""
def _package_search():

	context = {'model': model, 'session': model.Session,
				'user': c.user or c.author, 'auth_user_obj': c.userobj }
    
	# Ordenar los resultados por fecha de modificacion
	data_dict = {} 
	data_dict['sort'] = 'metadata_modified desc'

	# Realizar la consulta
	query = logic.get_action('package_search')(context, data_dict.copy())
    
	return query['count'], query['results']

# Se encarga de gestionar el proceso para generar el feed.
# Coge los datos del catalogo y se los pasas al NTIAtom1Feed para que genere el feed
class FeedNTIController(base.BaseController):
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
		
		return self.output_feed(datasets,feedData)
    
	def output_feed(self, datasets, feedData={}):
		# Cabeceras del feed, metadatos del catalogo
		feed = _NTIAtom1Feed(
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
			group = ''
			groupA = pkg.get('groups',None)
			if groupA is not None:
				group = groupA[0]['display_name']
				
			# Tag / Etiqueta principal
			tag= ''
			tagA = pkg.get('tags',None)
			if tagA is not None:
				tag = tagA[0]['display_name']
				
			# Idioma / Cobertura Geografica / Cobertura Temporal
			idiomaT = ''
			cobgeo = ''
			cobtemp = ''
			vigencia = ''
			frecupd = ''
			recrel= ''
			norma = ''
			
			extras = pkg.get('extras',None)
			if extras is not None:
				for extra in extras:
					if extra['key'] == 'Idioma':
						idiomaT = extra['value']
					elif extra['key'] == 'Cobertura geográfica':
						cobgeo = extra['value']
					elif extra['key'] == 'Cobertura temporal':
						cobtemp = extra['value']
					elif extra['key'] == 'Vigencia':
						vigencia = extra['value']
					elif extra['key'] == 'Frecuencia Actualización':
						frecupd = extra['value']
					elif extra['key'] == 'Recurso Relacionado':
						recrel = extra['value']
					elif extra['key'] == 'Normativa':
						norma = extra['value']
			
			# Publicador
			publisher = ''
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
					'informacionAdiocional': g.site_url + '/dataset' + pkg.get('name','') + '/resource/' + ckanResource['id']
				}
				
				resources.append(resource)
			
			feed.add_item(
				nombre = pkg.get('title',''),
				sumary = pkg.get('notes',''),
				id = g.site_url + "/dataset/" + pkg.get('name',''),
				category = group,
				keyword = tag,
				published = pkg.get('metadata_created',''),
				updated = pkg.get('metadata_modified',''),
				frecuenciaActualizacion = frecupd,
				idioma = idiomaT, 
				organismoPublicador = publisher, 
				condicionesUso = pkg.get('license_url',''),
				coberturaGeografica = cobgeo, 
				coberturaTemporal = cobtemp,
				vigenciaRecurso = vigencia,
				recursoRelacionado = recrel,
				normativa = norma,
				distribucion = resources)        
							
		response.content_type = feed.mime_type
		return feed.writeString('utf-8')

# Se encarga de crear el feed Atom con los datos que se le suministran
class _NTIAtom1Feed(webhelpers.feedgenerator.Atom1Feed):
	feedNTISchema = FeedNTI()
	
	def __init__(self,
				nombre, link, descripcion, id=None, organoPublicador=None, tamanoCatalogo=None, 
				fechaCreacion=None, updated=None, idioma=None, coberturaGeografica=None, 
				category=None, terminosUso=None, **kwargs):
				
		super(_NTIAtom1Feed,self).__init__(title=nombre, link=link, description=descripcion, categories=category, **kwargs)
		
		nti = {
			'id': id, # Nombre de campo y propiedad no definido en la NTI
			'identificador': id,
			'nombre': nombre,
			'descripcion': descripcion,
			'organoPublicador': organoPublicador,
			'tamanoCatalogo': tamanoCatalogo,
			'fechaCreacion': fechaCreacion,
			'fechaActualizacion': updated,
			'updated': updated, # Nombre de campo y propiedad no definido en la NTI
			'idioma': idioma,
			'coberturaGeografica': coberturaGeografica,
			'tematica': category,
			'category': category, # Nombre de campo y propiedad no definido en la NTI
			'paginaWeb': link,
			'terminosUso': terminosUso,
		}
		
		self.feed.update(nti)

	def root_attributes(self):
		attrs = {}
		
		# Anadir  todos los namespaces definidos en el template
		for abrv in self.feedNTISchema.namespaces:
			index = 'xmlns:' + abrv
			attrs[index] = self.feedNTISchema.namespaces[abrv]
		# Se cambia el ns de atom para que sea el base
		attrs['xmlns'] = attrs['xmlns:atom']
		del attrs['xmlns:atom']

		# Anadir idioma al feed
		attrs['xml:lang'] = self.feed['idioma']
		
		# Anadir los schemaLocation
		schemas = ""
		for schema in self.feedNTISchema.schemaLocations:
			schemas = schemas + " " + self.feedNTISchema.schemaLocations[schema] + " " + schema + " "
		attrs['xsi:schemaLocation'] = schemas

		return attrs
		
	def add_root_elements(self, handler):
		# Campos obligatorios (segun el constructor)
		handler.addQuickElement(self.feedNTISchema.feed['nombre'], self.feed['nombre'])
		handler.addQuickElement(self.feedNTISchema.feed['descripcion'], self.feed['descripcion'])
		handler.addQuickElement(self.feedNTISchema.feed['link'], "", {u"rel": u"alternate", u"href": self.feed['link']})
		handler.addQuickElement(self.feedNTISchema.feed['paginaWeb'], self.feed['paginaWeb'])
		
		# Campos opcionales (constructuro =None)
		if self.feed['id'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['id'], self.feed['id'])
		if self.feed['identificador'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['identificador'], self.feed['identificador'])
		if self.feed['organoPublicador'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['organoPublicador'], self.feed['organoPublicador'])
		if self.feed['tamanoCatalogo'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['tamanoCatalogo'], self.feed['tamanoCatalogo'])
		if self.feed['fechaCreacion'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['fechaCreacion'], self.feed['fechaCreacion'])
		if self.feed['fechaActualizacion'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['fechaActualizacion'], self.feed['fechaActualizacion'])
		if self.feed['updated'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['updated'], self.feed['updated'])
		if self.feed['idioma'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['idioma'], self.feed['idioma'])
		if self.feed['coberturaGeografica'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['coberturaGeografica'], self.feed['coberturaGeografica'])
		if self.feed['tematica'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['tematica'], self.feed['tematica'])
		if self.feed['category'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['category'], self.feed['category'])
		if self.feed['terminosUso'] is not None:
			handler.addQuickElement(self.feedNTISchema.feed['terminosUso'], self.feed['terminosUso'])

	def add_distribution(self, link, formato, identificador=None, nombre=None, 
							tamano=None, informacionAdiocional=None):
		ntiDistribution = {
			'identificador': identificador,
			'nombre': nombre,
			'urlAcceso': link,
			'link': link,
			'formato': formato,
			'tamano': tamano,
			'informacionAdiocional': informacionAdiocional
		}
		
		return ntiDistribution
		
	def add_item(self, nombre, sumary, id, category=None,
					keyword=None, published=None, updated=None, frecuenciaActualizacion=None,
					idioma=None, organismoPublicador=None, condicionesUso=None,
					coberturaGeografica=None, coberturaTemporal=None, vigenciaRecurso=None,
					recursoRelacionado=None, normativa=None, distribucion = [], **kwargs):
		
		ntiItem = {
			'id' : id,
			'identificador': id,
			'nombre': nombre,
			'descripcion': sumary,
			'sumary': sumary,
			'tematica': category,
			'category': category,
			'etiqueta': keyword,
			'keyword': keyword,
			'fechaCreacion': published,
			'published': published,
			'fechaActualizacion': updated,
			'updated': updated,
			'frecuenciaActualizacion': frecuenciaActualizacion,
			'idioma': idioma,
			'organismoPublicador': organismoPublicador,
			'condicionesUso': condicionesUso,
			'coberturaGeografica': coberturaGeografica,
			'coberturaTemporal': coberturaTemporal,
			'vigenciaRecurso': vigenciaRecurso,
			'recursoRelacionado': recursoRelacionado,
			'normativa': normativa,
			'distribucion': [],
		}
		
		for dist in distribucion:
			dist_link = ''
			dist_formato= ''
			dist_identificador = ''
			dist_nombre = ''
			dist_tamano= ''
			dist_informacionAdiocional = ''
			if dist['link'] is not None:
				dist_link = dist['link']
			if dist['formato'] is not None:
				dist_formato = dist['formato']
			if dist['identificador'] is not None:
				dist_identificador = dist['identificador']
			if dist['nombre'] is not None:
				dist_nombre = dist['nombre']
			if dist['tamano'] is not None:
				dist_tamano = dist['tamano']
			if dist['informacionAdiocional'] is not None:
				dist_informacionAdiocional = dist['informacionAdiocional']
			newDist = self.add_distribution(link = dist_link,
										formato = dist_formato,
										identificador = dist_identificador,
										nombre = dist_nombre,
										tamano = dist_tamano,
										informacionAdiocional = dist_informacionAdiocional)
			ntiItem['distribucion'].append(newDist)
		
		kwargs.update(ntiItem);	
		
		super(_NTIAtom1Feed, self).add_item(title=nombre,
											link=id,
											description=sumary,
											**kwargs)
	
	def add_item_elements(self, handler, item):
		# Campos obligatorios (segun el constructor)
		handler.addQuickElement(self.feedNTISchema.entry['id'], item['id'])
		handler.addQuickElement(self.feedNTISchema.entry['identificador'], item['identificador'])
		handler.addQuickElement(self.feedNTISchema.entry['nombre'], item['nombre'])
		handler.addQuickElement(self.feedNTISchema.entry['descripcion'], item['descripcion'])
		handler.addQuickElement(self.feedNTISchema.entry['sumary'], item['sumary'])

		# Campos opcionales (constructuro =None)
		if item['tematica'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['tematica'], item['tematica'])
		if item['category'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['category'], item['category'])
		if item['etiqueta'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['etiqueta'], item['etiqueta'])
		if item['keyword'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['keyword'], item['keyword'])
		if item['fechaCreacion'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['fechaCreacion'], item['fechaCreacion'])
		if item['published'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['published'], item['published'])
		if item['fechaActualizacion'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['fechaActualizacion'], item['fechaActualizacion'])
		if item['updated'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['updated'], item['updated'])
		if item['frecuenciaActualizacion'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['frecuenciaActualizacion'], item['frecuenciaActualizacion'])
		if item['idioma'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['idioma'], item['idioma'])
		if item['organismoPublicador'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['organismoPublicador'], item['organismoPublicador'])	
		if item['condicionesUso'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['condicionesUso'], item['condicionesUso'])	
		if item['coberturaGeografica'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['coberturaGeografica'], item['coberturaGeografica'])	
		if item['coberturaTemporal'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['coberturaTemporal'], item['coberturaTemporal'])	
		if item['vigenciaRecurso'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['vigenciaRecurso'], item['vigenciaRecurso'])	
		if item['recursoRelacionado'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['recursoRelacionado'], item['recursoRelacionado'])	
		if item['normativa'] is not None:
			handler.addQuickElement(self.feedNTISchema.entry['normativa'], item['normativa'])	
		if item['distribucion'] is not None:
			for dist in item['distribucion']:
				handler.startElement(self.feedNTISchema.entry['distribucion'],{})
				if dist['identificador'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['identificador'], dist['identificador'])
				if dist['nombre'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['nombre'], dist['nombre'])
				if dist['urlAcceso'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['urlAcceso'], dist['urlAcceso'])
				if dist['link'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['link'], dist['link'])
				if dist['formato'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['formato'], dist['formato'])
				if dist['tamano'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['tamano'], dist['tamano'])
				if dist['informacionAdiocional'] is not None:
					handler.addQuickElement(self.feedNTISchema.distribution['informacionAdiocional'], dist['informacionAdiocional'])
				handler.endElement(self.feedNTISchema.entry['distribucion'])
