#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webhelpers.feedgenerator

# Se encarga de crear el feed Atom con los datos que se le suministran
# Los datos suministrados deben estar bien formateados y en cadenas de caracteres.
# Est� clase se limita a construir el Feed.

from ckanext.feedNTI.NTIAtom1FeedTemplate import NTIAtom1FeedTemplate

class NTIAtom1Feed(webhelpers.feedgenerator.Atom1Feed):
    feedNTITemplate = NTIAtom1FeedTemplate()
    
    def __init__(self,
                nombre, link, descripcion, id=None, organoPublicador=None, tamanoCatalogo=None, 
                fechaCreacion=None, updated=None, idioma=None, coberturaGeografica=None, 
                category=[], terminosUso=None, **kwargs):
                
        super(NTIAtom1Feed,self).__init__(title=nombre, link=link, description=descripcion, categories=category,language=idioma, **kwargs)
        
        # Se a�aden los campos al directorio para construir luego el XML.
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

    # Se encarga de a�adir al array todos los atributos de la cabecerda
    # <feed>, namespaces, etc.
    def root_attributes(self):
        attrs = {}
        
        # Anadir  todos los namespaces definidos en el template
        for abrv in self.feedNTITemplate.namespaces:
            index = 'xmlns:' + abrv
            attrs[index] = self.feedNTITemplate.namespaces[abrv]
        # Se cambia el ns de atom para que sea el base
        attrs['xmlns'] = attrs['xmlns:atom']
        del attrs['xmlns:atom']

        # Anadir idioma al feed
        if 'idioma' in self.feed.keys():
            if self.feed['idioma'] is not None:
                attrs['xml:lang'] = self.feed['idioma']
        
        # Anadir los schemaLocation
        schemas = ""
        for schema in self.feedNTITemplate.schemaLocations:
            schemas = schemas + " " + self.feedNTITemplate.schemaLocations[schema] + " " + schema + " "
        attrs['xsi:schemaLocation'] = schemas

        return attrs
        
    # Genera las etiquetas XML para la cabecera del feed atom, a partir del array construido en el __init__
    def add_root_elements(self, handler):
        # Campos obligatorios (segun el constructor)
        handler.addQuickElement(self.feedNTITemplate.feed['nombre'], self.feed['nombre'])
        handler.addQuickElement(self.feedNTITemplate.feed['descripcion'], self.feed['descripcion'])
        handler.addQuickElement(self.feedNTITemplate.feed['link'], "", {u"rel": u"alternate", u"href": self.feed['link']})
        #handler.addQuickElement(self.feedNTITemplate.feed['paginaWeb'], self.feed['paginaWeb']) # ETiqueta NTI, no implementada de momento
        
        # Campos opcionales (constructor =None)
        # Se hace por if separados e indicando los campos para evitar generar etiquetas
        # que no est�n definidas en la plantilla Atom.
        if self.feed['id'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['id'], self.feed['id'])
        #if self.feed['identificador'] is not None:
        #    handler.addQuickElement(self.feedNTITemplate.feed['identificador'], self.feed['identificador'])
        if self.feed['organoPublicador'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['organoPublicador'], self.feed['organoPublicador'])
        if self.feed['tamanoCatalogo'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['tamanoCatalogo'], self.feed['tamanoCatalogo'])
        if self.feed['fechaCreacion'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['fechaCreacion'], self.feed['fechaCreacion'])
        #if self.feed['fechaActualizacion'] is not None:
        #    handler.addQuickElement(self.feedNTITemplate.feed['fechaActualizacion'], self.feed['fechaActualizacion'])
        if self.feed['updated'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['updated'], self.feed['updated'])
        if self.feed['idioma'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['idioma'], self.feed['idioma'])
        if self.feed['coberturaGeografica'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['coberturaGeografica'], self.feed['coberturaGeografica'])
        #if self.feed['tematica'] is []:
        #    handler.addQuickElement(self.feedNTITemplate.feed['tematica'], self.feed['tematica'])
        if self.feed['category'] is []:
            handler.addQuickElement(self.feedNTITemplate.feed['category'], self.feed['category'])
        if self.feed['terminosUso'] is not None:
            handler.addQuickElement(self.feedNTITemplate.feed['terminosUso'], self.feed['terminosUso'])

    # Construye el objeto que representa una distribuci�n para a�adirlo al array del feed.
    def add_distribution(self, link, formato, identificador=None, nombre=None, 
                            tamano=None, informacionAdicional=None):
        ntiDistribution = {
            'identificador': identificador,
            'nombre': nombre,
            #'urlAcceso': link, # Metadato NTI no usado en la plantilla, omitir de momento
            'link': link,
            'formato': formato,
            'tamano': tamano,
            'informacionAdicional': informacionAdicional
        }
        
        return ntiDistribution
        
    # Se encarga de a�adir al array cada uno de los datasets (entry)
    def add_item(self, nombre, summary, id, category=None,
                    keyword=None, published=None, updated=None, frecuenciaActualizacion=None,
                    idioma=None, organismoPublicador=None, condicionesUso=None,
                    coberturaGeografica=None, coberturaTemporal=None, vigenciaRecurso=None,
                    recursoRelacionado=None, normativa=None, distribucion = [], **kwargs):
        
        coberturaTemporalComienzo = ''
        coberturaTemporalFinal = ''
        if coberturaTemporal is not None:
            coberturaTemporalComienzo = coberturaTemporal['comienzo']
            coberturaTemporalFinal = coberturaTemporal['final']
        
        ntiItem = {
            'id' : id,
            #'identificador': id, # Campo NTI omitir de momento
            'nombre': nombre,
            #'descripcion': summary, # Campo NTI omitir de momento
            'summary': summary,
            #'tematica': category, # Campo NTI omitir de momento
            'category': category,
            #'etiqueta': keyword, # Campo NTI omitir de momento
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
            'coberturaTemporal': {
                    'comienzo': coberturaTemporalComienzo,
                    'final': coberturaTemporalFinal
                },
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
            dist_informacionAdicional = ''
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
            if dist['informacionAdicional'] is not None:
                dist_informacionAdicional = dist['informacionAdicional']
            newDist = self.add_distribution(link = dist_link,
                                        formato = dist_formato,
                                        identificador = dist_identificador,
                                        nombre = dist_nombre,
                                        tamano = dist_tamano,
                                        informacionAdicional = dist_informacionAdicional)
            ntiItem['distribucion'].append(newDist)
        
        # Se actualiza los argumentos, el constructor se encarga de a�adirlo al array
        kwargs.update(ntiItem);    
        
        super(NTIAtom1Feed, self).add_item(title=nombre,
                                            link=id,
                                            description=summary,
                                            **kwargs)
    
    # Genera las etiquetas XML para cada uno de los datasets (entry)
    # del feed atom, a partir del array construido en el add_item
    def add_item_elements(self, handler, item):
        # Campos obligatorios (segun el constructor)
        handler.addQuickElement(self.feedNTITemplate.entry['id'], item['id'])
        #handler.addQuickElement(self.feedNTITemplate.entry['identificador'], item['identificador']) # Campo NTI no implementado en la plantilla
        handler.addQuickElement(self.feedNTITemplate.entry['nombre'], item['nombre'])
        #handler.addQuickElement(self.feedNTITemplate.entry['descripcion'], item['descripcion']) # Campo NTI no implementado en la plantilla
        handler.addQuickElement(self.feedNTITemplate.entry['summary'], item['summary'])


        # Campos opcionales (constructor =None)
        # Se hace por if separados e indicando los campos para evitar generar etiquetas
        # que no est�n definidas en la plantilla Atom.
        #if item['tematica'] is not None:# No implementado en la plantilla NTI
        #    handler.addQuickElement(self.feedNTITemplate.entry['tematica'], item['tematica'])
        if item['category'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['category'], item['category'])
        #if item['etiqueta'] is not None:
        #    handler.addQuickElement(self.feedNTITemplate.entry['etiqueta'], item['etiqueta'])
        if item['keyword'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['keyword'], item['keyword'])
        if item['fechaCreacion'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['fechaCreacion'], item['fechaCreacion'])
        if item['published'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['published'], item['published'])
        #if item['fechaActualizacion'] is not None:
        #    handler.addQuickElement(self.feedNTITemplate.entry['fechaActualizacion'], item['fechaActualizacion'])
        if item['updated'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['updated'], item['updated'])
        if item['frecuenciaActualizacion'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['frecuenciaActualizacion'], item['frecuenciaActualizacion'])
        if item['idioma'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['idioma'], item['idioma'])
        if item['organismoPublicador'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['organismoPublicador'], item['organismoPublicador'])    
        if item['condicionesUso'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['condicionesUso'], item['condicionesUso'])    
        if item['coberturaGeografica'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['coberturaGeografica'], item['coberturaGeografica'])    
        if item['coberturaTemporal'] is not None:
            handler.startElement(self.feedNTITemplate.entry['coberturaTemporal']['etiqueta'], {})
            handler.startElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['etiqueta'], {})
            if item['coberturaTemporal']['comienzo'] is not None:
                handler.startElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['comienzo'], {})
                handler.startElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['instante'], {})
                handler.addQuickElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['datetime'],item['coberturaTemporal']['comienzo'])
                handler.endElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['instante'])
                handler.endElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['comienzo'])
            if item['coberturaTemporal']['final'] is not None:
                handler.startElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['final'], {})
                handler.startElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['instante'], {})
                handler.addQuickElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['datetime'],item['coberturaTemporal']['final'])
                handler.endElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['instante'])
                handler.endElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['final'])
            handler.endElement(self.feedNTITemplate.entry['coberturaTemporal']['intervalo']['etiqueta'])
            handler.endElement(self.feedNTITemplate.entry['coberturaTemporal']['etiqueta'])
                
        if item['vigenciaRecurso'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['vigenciaRecurso'], item['vigenciaRecurso'])    
        if item['recursoRelacionado'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['recursoRelacionado'], item['recursoRelacionado'])    
        if item['normativa'] is not None:
            handler.addQuickElement(self.feedNTITemplate.entry['normativa'], item['normativa'])    
        if item['distribucion'] is not None:
            for dist in item['distribucion']:
                handler.startElement(self.feedNTITemplate.entry['distribucion'],{})
                if dist['identificador'] is not None:
                    handler.addQuickElement(self.feedNTITemplate.distribution['identificador'], dist['identificador'])
                if dist['nombre'] is not None:
                    handler.addQuickElement(self.feedNTITemplate.distribution['nombre'], dist['nombre'])
                #if dist['urlAcceso'] is not None:
                #    handler.addQuickElement(self.feedNTITemplate.distribution['urlAcceso'], dist['urlAcceso'])
                if dist['link'] is not None:
                    handler.addQuickElement(self.feedNTITemplate.distribution['link'], "", {u"rel": u"enclosure", u"href": dist['link'], u"type": dist['formato'], u"length": dist['tamano']})
                if dist['formato'] is not None:
                    handler.addQuickElement(self.feedNTITemplate.distribution['formato'], dist['formato'])
                if dist['tamano'] is not None:
                    handler.addQuickElement(self.feedNTITemplate.distribution['tamano'], dist['tamano'])
                if dist['informacionAdicional'] is not None:
                    handler.addQuickElement(self.feedNTITemplate.distribution['informacionAdicional'], dist['informacionAdicional'])
                handler.endElement(self.feedNTITemplate.entry['distribucion'])