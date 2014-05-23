#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock

from ckanext.feedNTI.NTIAtom1FeedTemplate import NTIAtom1FeedTemplate


class TestNTIAtom1FeedTemplate(unittest.TestCase):

    def setUp(self):
        self.ntiAtom1FeedTemplate = NTIAtom1FeedTemplate()
        self.resultNameSpaces = {
            'atom': 'http://www.w3.org/2005/Atom', 
            'xml' : 'http://www.w3.org/XML/1998/namespace', 
            'fed' : 'http://datos.gob.es/federador/ns',
            'time': 'http://www.w3.org/2006/time',
            'dct' : 'http://purl.org/dc/terms/',
            'dc'  : 'http://purl.org/dc/elements/1.1/',   
            'foaf': 'http://xmlns.com/foaf/0.1/',
            'xsi' : 'http://www.w3.org/2001/XMLSchema-instance'
        }
        
        self.resultSchemaLocations = {
            'atom.xsd'                                             : 'http://www.w3.org/2005/Atom',
            'http://dublincore.org/schemas/xmls/qdc/dcterms.xsd'   : 'http://purl.org/dc/terms/',
            'federador.xsd'                                        : 'http://datos.gob.es/federador/ns'
        }
        
        self.resultFeedFields = {
            'id': 'id', # Nombre de campo y propiedad no definido en la NTI
            'nombre': 'title',
            'descripcion': 'dct:description',
            'organoPublicador': 'dct:publisher',
            'tamanoCatalogo': 'dct:extent',
            'fechaCreacion': 'dct:issued',
            'updated': 'updated', # Nombre de campo y propiedad no definido en la NTI
            'idioma': 'dc:language',
            'coberturaGeografica': 'dct:spatial',
            'category': 'category', # Nombre de campo y propiedad no definido en la NTI
            'link': 'link', # Nombre de campo y propiedad no definido en la NTI
            'terminosUso': 'dct:license',
            'entry': 'entry' # Nombre de campo y propiedad no definido en la NTI
        }
        
        self.resultDistributionFields = {
            'identificador': 'dct:identifier',
            'nombre': 'dct:title',
            'urlAcceso': 'dcat:accessURL',
            'link': 'fed:link', # Nombre de campo y propiedad no definido en la NTI
            'formato': 'dcat:mediaType',    # A pesar de ser un metadato NTI, en la plantilla se pone en el atribute de link
            'tamano': 'dcat:byteSize',      # A pesar de ser un metadato NTI, en la plantilla se pone en el atribute de link
            'informacionAdicional': 'dct:relation'
        }
        
        self.resultEntryFields = {
            'id': 'id', # Nombre de campo y propiedad no definido en la NTI
            'nombre': 'title',
            'summary': 'summary', # Nombre de campo y propiedad no definido en la NTI
            'category': 'category', # Nombre de campo y propiedad no definido en la NTI
            'keyword': 'fed:keyword', # Nombre de campo y propiedad no definido en la NTI
            'fechaCreacion': 'dct:issued',
            'published': 'published', # Nombre de campo y propiedad no definido en la NTI
            'updated': 'updated', # Nombre de campo y propiedad no definido en la NTI
            'frecuenciaActualizacion': 'dct:accrualPeriodicity',
            'idioma': 'dc:language',
            'organismoPublicador': 'dct:publisher',
            'condicionesUso': 'dct:license',
            'coberturaGeografica': 'dct:spatial',
            'coberturaTemporal': {
                'etiqueta': 'dct:temporal',
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
            'distribucion': 'fed:distribution',
        }
        
    def testNameSpaces(self):
        self.assertEqual(len(self.resultNameSpaces), len(self.ntiAtom1FeedTemplate.namespaces), 
                         "No coincide la cantidad de namespaces")
        
        for key in self.resultNameSpaces:
            self.assertEqual(self.ntiAtom1FeedTemplate.namespaces[key], self.resultNameSpaces[key], 
                             "Error en el namespace (" + key + ", " + self.resultNameSpaces[key] + ")")
            
    def testSchemaLocations(self):
        self.assertEqual(len(self.resultSchemaLocations), len(self.ntiAtom1FeedTemplate.schemaLocations), 
                         "No coincide la cantidad de schemas")
        
        for key in self.resultSchemaLocations:
            self.assertEqual(self.ntiAtom1FeedTemplate.schemaLocations[key], self.resultSchemaLocations[key], 
                             "Error en el schema (" + key + ", " + self.resultSchemaLocations[key] + ")")
            
    def testFeedFields(self):
        self.assertEqual(len(self.resultFeedFields), len(self.ntiAtom1FeedTemplate.feed), 
                         "No coincide la cantidad de campos")
        
        for key in self.resultFeedFields:
            self.assertEqual(self.ntiAtom1FeedTemplate.feed[key], self.resultFeedFields[key], 
                             "Error en el feed (" + key + ", " + self.resultFeedFields[key] + ")")
            
    def testDistributionFields(self):
        self.assertEqual(len(self.resultDistributionFields), len(self.ntiAtom1FeedTemplate.distribution), 
                         "No coincide la cantidad de campos")
        
        for key in self.resultDistributionFields:
            self.assertEqual(self.ntiAtom1FeedTemplate.distribution[key], self.resultDistributionFields[key], 
                             "Error en la distribución (" + key + ", " + self.resultDistributionFields[key] + ")")
            
    def testEntryFields(self):
        self.assertEqual(len(self.resultEntryFields), len(self.ntiAtom1FeedTemplate.entry), 
                         "No coincide la cantidad de campos")
        self.assertEqual(len(self.resultEntryFields['coberturaTemporal']), len(self.ntiAtom1FeedTemplate.entry['coberturaTemporal']), 
                         "No coincide la cantidad de campos - Cobertura Temporal")
        self.assertEqual(len(self.resultEntryFields['coberturaTemporal']['intervalo']), len(self.ntiAtom1FeedTemplate.entry['coberturaTemporal']['intervalo']), 
                         "No coincide la cantidad de campos - Intervalo (Cobertura Temporal)")
        
        for key in self.resultEntryFields:
            if key != 'coberturaTemporal':
                self.assertEqual(self.ntiAtom1FeedTemplate.entry[key], self.resultEntryFields[key], 
                                 "Error en la entrada (" + key + ", " + self.resultEntryFields[key] + ")")

        for key in self.resultEntryFields['coberturaTemporal']:
            if key != 'intervalo':
                self.assertEqual(self.ntiAtom1FeedTemplate.entry['coberturaTemporal'][key], self.resultEntryFields['coberturaTemporal'][key], 
                                 "Error en la entrada (" + key + ", " + self.resultEntryFields['coberturaTemporal'][key] + ") - Cobertura Temporal")
        for key in self.resultEntryFields['coberturaTemporal']['intervalo']:
            self.assertEqual(self.ntiAtom1FeedTemplate.entry['coberturaTemporal']['intervalo'][key], self.resultEntryFields['coberturaTemporal']['intervalo'][key], 
                             "Error en la entrada (" + key + ", " + self.resultEntryFields['coberturaTemporal']['intervalo'][key] + ") - Intervalo (Cobertura Temporal)")
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()