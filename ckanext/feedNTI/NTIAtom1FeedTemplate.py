# Clase que contiene la informacion de los metadatos
# Intenta representar la ficha completa de metadatos y su traduccion a los vocabularios
#
#
# V1.0
# - Solo esta adaptada para la federacion segun la plantilla de datos.gob.es
# - Ademas de los metadatos NTI hay algunos especificados por el federador de datos.gob.es

class NTIAtom1FeedTemplate:
	# nameSpaces del template
	namespaces = {
		'atom'	: 'http://www.w3.org/2005/Atom',
		'xml'	: 'http://www.w3.org/XML/1998/namespace',
		'fed'	: 'http://datos.gob.es/federador/ns',
		'time'	: 'http://www.w3.org/2006/time',
		'dct'	: 'http://purl.org/dc/terms/',
		'dc'	: 'http://purl.org/dc/elements/1.1/',
		'foaf'	: 'http://xmlns.com/foaf/0.1/',
		'xsi'	: 'http://www.w3.org/2001/XMLSchema-instance',
		#'dcat'	: 'http://www.w3.org/ns/dcat#'
	}
	
	# schemaLocations del template
	schemaLocations = {
		'atom.xsd'											: 'http://www.w3.org/2005/Atom',
		'http://dublincore.org/schemas/xmls/qdc/dcterms.xsd': 'http://purl.org/dc/terms/',
		'federador.xsd'										: 'http://datos.gob.es/federador/ns'
	}
	
	# metadatos del feed general (catalogo)
	feed = {
		'id': 'id', # Nombre de campo y propiedad no definido en la NTI
		#'identificador': 'dct:identifier', # Campo NTI no usado en la plantilla
		'nombre': 'title',
		'descripcion': 'dct:description',
		'organoPublicador': 'dct:publisher',
		'tamanoCatalogo': 'dct:extent',
		'fechaCreacion': 'dct:issued',
		#'fechaActualizacion': 'dct:modified', # Campo NTI no usado en la plantilla
		'updated': 'updated', # Nombre de campo y propiedad no definido en la NTI
		'idioma': 'dc:language',
		'coberturaGeografica': 'dct:spatial',
		#'tematica': 'dcat:themeTaxonomy', # Campo NTI no usado en la plantilla
		'category': 'category', # Nombre de campo y propiedad no definido en la NTI
		#'paginaWeb': 'foaf:homepage',# Campo NTI no usado en la plantilla
		'link': 'link', # Nombre de campo y propiedad no definido en la NTI
		'terminosUso': 'dct:license',
		#'documento': 'dcat:dataset', # Campo NTI no usado en la plantilla
		'entry': 'entry' # Nombre de campo y propiedad no definido en la NTI
	}
	
	# metadatos del item/entry (dataset)
	entry = {
		'id': 'id', # Nombre de campo y propiedad no definido en la NTI
		#'identificador': 'dct:identifier', # Campo NTI no usado en la plantilla
		'nombre': 'title',
		#'descripcion': 'dct:description', # Campo NTI no usado en la plantilla
		'summary': 'summary', # Nombre de campo y propiedad no definido en la NTI
		#'tematica': 'dcat:theme', # Campo NTI no usado en la plantilla
		'category': 'category', # Nombre de campo y propiedad no definido en la NTI
		#'etiqueta': 'dcat:keyword', # Campo NTI no usado en la plantilla
		'keyword': 'fed:keyword', # Nombre de campo y propiedad no definido en la NTI
		'fechaCreacion': 'dct:issued',
		'published': 'published', # Nombre de campo y propiedad no definido en la NTI
		#'fechaActualizacion': 'dct:modified', # Campo NTI no usado en la plantilla
		'updated': 'updated', # Nombre de campo y propiedad no definido en la NTI
		'frecuenciaActualizacion': 'dct:accrualPeriodicity',
		'idioma': 'dc:language',
		'organismoPublicador': 'dct:publisher',
		'condicionesUso': 'dct:license',
		'coberturaGeografica': 'dct:spatial',
		'coberturaTemporal': { 'etiqueta': 'dct:temporal',
								'intervalo': {
									'etiqueta': 'time:Interval',
									'comienzo': 'time:hasBeginning',
									'final': 'time:hasEnd',
									'instante': 'time:Instant',
									'datetime': 'time:inXSDDateTime'
								}
							},
		'vigenciaRecurso': 'dct:valid',
		'recursoRelacionado': 'dct:references',
		'normativa': 'dct:conformsTo',
		#'distribucion': 'dcat:distribution', # Campo NTI no usado en la plantilla
		'distribucion': 'fed:distribution'
	}
	
	# metadatos del recurso o distribucion
	distribution = {
		'identificador': 'dct:identifier',
		'nombre': 'dct:title',
		'urlAcceso': 'dcat:accessURL',
		'link': 'fed:link', # Nombre de campo y propiedad no definido en la NTI
		'formato': 'dcat:mediaType',
		'tamano': 'dcat:byteSize',
		'informacionAdicional': 'dct:relation'
	}