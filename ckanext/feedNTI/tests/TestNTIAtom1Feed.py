#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from StringIO import StringIO
from webhelpers.util import SimplerXMLGenerator
import xml.sax

from ckanext.feedNTI.NTIAtom1Feed import NTIAtom1Feed

class TestNTIAtom1Feed(unittest.TestCase):
    def setUp(self):
        self.resultDistribution = {
            'identificador': 'identificador',
            'nombre': 'nombre',
            'link': 'link',
            'formato': 'formato',
            'tamano': 'tamano',
            'informacionAdicional': 'informacionAdicional'
        }
        
        self.feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion')

    def testFeed_minimo(self):
        
        feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion')
        
        resultFeed = {
            'tamanoCatalogo': None,
            'organoPublicador': None,
            'updated': None,
            'subtitle': None,
            'description': 'descripcion',
            'author_link': None,
            'feed_copyright': None,
            'coberturaGeografica': None,
            'author_name': None,
            'tematica': [],
            'terminosUso': None,
            'link': 'link',
            'ttl': None,
            'descripcion': 'descripcion',
            'paginaWeb': 'link',
            'id': None,
            'categories': (),
            'category': [],
            'language': None,
            'feed_url': None,
            'title': 'nombre',
            'author_email': None,
            'identificador': None,
            'fechaCreacion': None,
            'fechaActualizacion': None,
            'nombre': 'nombre',            
            'idioma': None,
        }
        
        self.assertEqual(feed.feed, resultFeed, "No coinciden los campos en el array del feed. - Minimo")

    def testFeed_completo(self):
        feed = NTIAtom1Feed(
                    nombre='nombre',
                    link='link',
                    descripcion='descripcion',
                    id='id',
                    organoPublicador='publicador',
                    tamanoCatalogo='tamano', 
                    fechaCreacion='creacion',
                    updated='updated',
                    idioma='idioma',
                    coberturaGeografica='geografica', 
                    #category=['categoria'], # Da problemas con la funcion force_unicode en la MV
                    terminosUso='terminos')
        
        resultFeed = {
            'tamanoCatalogo': 'tamano',
            'organoPublicador': 'publicador',
            'updated': 'updated',
            'subtitle': None,
            'description': 'descripcion',
            'author_link': None,
            'feed_copyright': None,
            'coberturaGeografica': 'geografica',
            'author_name': None,
            'tematica': [], #['categoria'],
            'terminosUso': 'terminos',
            'link': 'link',
            'ttl': None,
            'descripcion': 'descripcion',
            'paginaWeb': 'link',
            'id': 'id',
            'categories': (), #['categoria'],
            'category': [], #['categoria'],
            'language': 'idioma',
            'feed_url': None,
            'title': 'nombre',
            'author_email': None,
            'identificador': 'id',
            'fechaCreacion': 'creacion',
            'fechaActualizacion': 'updated',
            'nombre': 'nombre',            
            'idioma': 'idioma',
        }
        
        self.assertEqual(feed.feed, resultFeed, "No coinciden los campos en el array del feed. - Completo")

    def testRootAtrbitues(self):
        feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion',
                        idioma='idioma')
        
        attrsResult = {
            'xmlns'      : 'http://www.w3.org/2005/Atom',
            'xmlns:xml'  : 'http://www.w3.org/XML/1998/namespace',
            'xmlns:fed'  : 'http://datos.gob.es/federador/ns',
            'xmlns:time' : 'http://www.w3.org/2006/time',
            'xmlns:dct'  : 'http://purl.org/dc/terms/',
            'xmlns:dc'   : 'http://purl.org/dc/elements/1.1/',
            'xmlns:foaf' : 'http://xmlns.com/foaf/0.1/',
            'xmlns:xsi'  : 'http://www.w3.org/2001/XMLSchema-instance',
            'xml:lang'   : 'idioma',
            'xsi:schemaLocation' : ' http://www.w3.org/2005/Atom atom.xsd http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/dcterms.xsd http://datos.gob.es/federador/ns federador.xsd '
        }
        
        attrs = feed.root_attributes()
        
        attrs['xsi:schemaLocation'] = attrs['xsi:schemaLocation'].split()
        attrsResult['xsi:schemaLocation'] = attrsResult['xsi:schemaLocation'].split()
        
        self.assertEqual(attrs, attrsResult, "Error en los atributos del feed.")
        
    def testAddItem_minimo(self):
        feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion')
        
        feed.add_item(
            nombre = 'item_nombre',
            summary = 'item_summary',
            id = 'item_id')
        
        itemResult = [
            {
                'fechaCreacion': None,
                'updated': None,
                'description': 'item_summary',
                'pubdate': None,
                'author_link': None,
                'fechaActualizacion': None,
                'coberturaGeografica': None,
                'published': None,
                'vigenciaRecurso': None,
                'author_name': None,
                'recursoRelacionado': None,
                'link': 'item_id',
                'ttl': None,
                'normativa': None,
                'condicionesUso': None,
                'enclosure': None,
                'categories': (),
                'category': [],
                'item_copyright': None,
                'organismoPublicador': None,
                'keyword': [],
                'title': 'item_nombre',
                'author_email': None,
                'id': 'item_id',
                'comments': None,
                'summary': 'item_summary',
                'coberturaTemporal': None,
                'distribucion': [],
                'nombre': 'item_nombre',
                'idioma': None,
                'unique_id': None,
                'frecuenciaActualizacion': None
            }
        ]
        
        self.assertEqual(feed.items, itemResult, "Error en los atributos del item.")
        
    def testAddItem_completo(self):
        feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion')
        
        feed.add_item(
            nombre = 'item_nombre',
            summary = 'item_summary',
            id = 'item_id', 
            category = ['item_category'],
            keyword = ['item_tag'],
            published = 'item_published',
            updated = 'item_update',
            frecuenciaActualizacion = 'item_frecAct',
            idioma = 'item_idioma',
            organismoPublicador = 'item_orgPub',
            condicionesUso = 'item_condUso',
            coberturaGeografica = 'item_cobGeo',
            coberturaTemporalComienzo = 'co',
            coberturaTemporalFinal = 'fi',
            vigenciaRecurso = 'item_vig',
            recursoRelacionado = 'item_Rel',
            normativa = 'item_normativa',
            distribucion = [])
        
        itemResult = [
            {
                'fechaCreacion': 'item_published',
                'updated': 'item_update',
                'description': 'item_summary',
                'pubdate': None,
                'author_link': None,
                'fechaActualizacion': 'item_update',
                'coberturaGeografica': 'item_cobGeo',
                'published': 'item_published',
                'vigenciaRecurso': 'item_vig',
                'author_name': None,
                'recursoRelacionado': 'item_Rel',
                'link': 'item_id',
                'ttl': None,
                'normativa': 'item_normativa',
                'condicionesUso': 'item_condUso',
                'enclosure': None,
                'categories': (),
                'category': ['item_category'],
                'item_copyright': None,
                'organismoPublicador': 'item_orgPub',
                'keyword': ['item_tag'],
                'title': 'item_nombre',
                'author_email': None,
                'id': 'item_id',
                'comments': None,
                'summary': 'item_summary',
                'coberturaTemporal': {'comienzo': 'co', 'final': 'fi'},
                'distribucion': [],
                'nombre': 'item_nombre',
                'idioma': 'item_idioma',
                'unique_id': None,
                'frecuenciaActualizacion': 'item_frecAct'
            }
        ]
        
        self.assertEqual(feed.items, itemResult, "Error en los atributos del item.")
            
    def testAddDistribution_minimo(self):
        dist = self.feed.add_distribution(
                    link=self.resultDistribution['link'],
                    formato=self.resultDistribution['formato'])
        
        okResult = {
            'link': self.resultDistribution['link'],
            'formato': self.resultDistribution['formato'],
            'identificador': None,
            'nombre': None,
            'tamano': None,
            'informacionAdicional': None
        }
        self.assertEqual(dist, okResult, "Error al crear el sub-arbol distribution - Minimo")
        
    def testAddDistribution_completo(self):        
        dist = self.feed.add_distribution(
                    link=self.resultDistribution['link'],
                    formato=self.resultDistribution['formato'],
                    identificador=self.resultDistribution['identificador'],
                    nombre=self.resultDistribution['nombre'], 
                    tamano=self.resultDistribution['tamano'],
                    informacionAdicional=self.resultDistribution['informacionAdicional'])
        
        self.assertEqual(dist, self.resultDistribution, "Error al crear el sub-arbol distribution - Completo")
        
    def testAddRootElements(self):
        feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion')
        
        xmlResult = ('<?xml version="1.0" encoding="utf-8"?>\n'
                     '<feed xmlns="http://www.w3.org/2005/Atom"><title>nombre</title><dct:description>descripcion</dct:description><link href="link" rel="alternate"></link></feed>')
        s = StringIO()
        handler = SimplerXMLGenerator(s, 'utf-8')
        handler.startDocument()
        handler.startElement(u'feed', {'xmlns': 'http://www.w3.org/2005/Atom'})
        
        feed.add_root_elements(handler)
        
        handler.endElement(u"feed")
        
        self.assertEqual(s.getvalue(), xmlResult, "Error en la salida del feed xml")
        
    def testAddItemElements(self):
        # Los campos vacios no los publica
        feed = NTIAtom1Feed(
                        nombre='nombre',
                        link='link',
                        descripcion='descripcion')
        
        xmlResult = ('<?xml version="1.0" encoding="utf-8"?>\n'
                     '<feed><entry><id>id</id><title>nombre</title><summary>summary</summary></entry></feed>')
        s = StringIO()
        handler = SimplerXMLGenerator(s, 'utf-8')
        handler.startDocument()
        handler.startElement(u'feed', {})
        
        handler.startElement(u"entry", {})
        
        item = {
            'id': 'id',
            'nombre': 'nombre',
            'summary': 'summary',
            'category': [],
            'keyword': [],
            'fechaCreacion': None,
            'published': None,
            'updated': None,
            'frecuenciaActualizacion': None,
            'idioma': None,
            'organismoPublicador': None,    
            'condicionesUso': None, 
            'coberturaGeografica': None,
            'coberturaTemporal': None,
            'vigenciaRecurso': None,    
            'recursoRelacionado': None,    
            'normativa': None,
            'distribucion': None
        }

        feed.add_item_elements(handler, item)

        handler.endElement(u"entry")        
        handler.endElement(u"feed")
        
        self.assertEqual(s.getvalue(), xmlResult, "Error en la salida del feed xml")
        
    """def testTemplateNTI(self):
        s = StringIO()
        handler = xml.sax.saxutils.XMLGenerator(s, 'utf-8')
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        parser.parse("files/PlantillaATOM.atom")
        
        feed = NTIAtom1Feed(
                        nombre='@@TEXTO-título-idioma1@@',
                        link='@@URI-homepage-catálogo@@',
                        descripcion='@@TEXTO-descripción-idioma1@@')
        
        f = open('files/NTIAtomFeed.atom', 'w')
        
        feed.write(f, 'utf-8');
        
        f.close()
    """   
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()