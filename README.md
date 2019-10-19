# nifWrapper

The NLP Interchange Format (NIF) is a RDF/OWL-based format wich allows the spotting of words from text corpora and its metada such as part-of-speech tags, knowledge-base links, entity type, etc. Likewise other Python libraries (e.g., [pynif](https://github.com/wetneb/pynif)), this library transform NIF data to python classes in order to better proccessing this information. 

If you want to create/visualizate NIF data see NIFify in [GitHub](https://github.com/henryrosalesmendez/NIFify_v2) or a [demo](https://users.dcc.uchile.cl/~hrosales/NIFify_v2.html).

## Example

Install first the library:

```
pip install nifwrapper
```

and then, try:

```python
from nifwrapper import *


gold_ttl = '''
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .

<https://example.org/doc1>
        a nif:String , nif:Context  , nif:RFC5147String ;
        nif:isString """Kiev is an important industrial, scientific, educational and cultural center of Eastern Europe."""^^xsd:string ;
        nif:beginIndex "0"^^xsd:nonNegativeInteger ;
        nif:endIndex "95"^^xsd:nonNegativeInteger ;
        nif:sourceUrl <https://example.org/doc1> .

<https://example.org/doc1#char=0,95>
        a nif:String , nif:Context , nif:RFC5147String ;
        nif:isString """Kiev is an important industrial, scientific, educational and cultural center of Eastern Europe."""^^xsd:string ;
        nif:beginIndex "0"^^xsd:nonNegativeInteger ;
        nif:endIndex "95"^^xsd:nonNegativeInteger ;
        nif:broaderContext <https://example.org/doc1> .

<https://example.org/doc1#char=0,4>
        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
        nif:referenceContext <https://example.org/doc1#char=0,95> ;
        nif:context <https://example.org/doc1> ;
        nif:anchorOf """Kiev"""^^xsd:string ;
        nif:beginIndex "0"^^xsd:nonNegativeInteger ;
        nif:endIndex "4"^^xsd:nonNegativeInteger ;
        itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Kiev> .

<https://example.org/doc1#char=33,43>
        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
        nif:referenceContext <https://example.org/doc1#char=0,95> ;
        nif:context <https://example.org/doc1> ;
        nif:anchorOf """scientific"""^^xsd:string ;
        nif:beginIndex "33"^^xsd:nonNegativeInteger ;
        nif:endIndex "43"^^xsd:nonNegativeInteger ;
        itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Education> .

<https://example.org/doc1#char=45,56>
        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
        nif:referenceContext <https://example.org/doc1#char=0,95> ;
        nif:context <https://example.org/doc1> ;
        nif:anchorOf """educational"""^^xsd:string ;
        nif:beginIndex "45"^^xsd:nonNegativeInteger ;
        nif:endIndex "56"^^xsd:nonNegativeInteger ;
        itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Education> .

<https://example.org/doc1#char=80,94>
        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
        nif:referenceContext <https://example.org/doc1#char=0,95> ;
        nif:context <https://example.org/doc1> ;
        nif:anchorOf """Eastern Europe"""^^xsd:string ;
        nif:beginIndex "80"^^xsd:nonNegativeInteger ;
        nif:endIndex "94"^^xsd:nonNegativeInteger ;
        itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Eastern_Europe> .
'''

## ---- parsing
parser = NIFParser()
wrp_gold = parser.parser_turtle(gold_ttl)

## ---- displaying turtle format
print(wrp_gold.toString()) 

## --- Benchmark

# - inline NIF corpus creation
wrp_sys = NIFWrapper()
doc = NIFDocument("https://example.org/doc1")
#--
sent = NIFSentence("https://example.org/doc1#char=0,95")
sent.addAttribute("nif:isString","Kiev is an important industrial, scientific, educational and cultural center of Eastern Europe.","xsd:string")
sent.addAttribute("nif:broaderContext",["https://example.org/doc1"],"URI LIST")

#-- 
a1 = NIFAnnotation("https://example.org/doc1#char=0,4", "0", "4", ["https://en.wikipedia.org/wiki/Kiev"], ["dbo:Place"])
a1.addAttribute("nif:anchorOf","Kiev","xsd:string")
a1.addAttribute("ex:newPredicate","This is a test","xsd:string")
sent.pushAnnotation(a1)

#--
a2 = NIFAnnotation("https://example.org/doc1#char=45,56", "45", "56", ["https://en.wikipedia.org/wiki/University"], ["dbo:Organization"])
a2.addAttribute("nif:anchorOf","educational","xsd:string")
sent.pushAnnotation(a2)

#--
a3 = NIFAnnotation("https://example.org/doc1#char=80,94", "80", "94", ["https://en.wikipedia.org/wiki/Eastern_Europe"], ["dbo:Organization"])
a3.addAttribute("nif:anchorOf","Eastern Europe","xsd:string")
sent.pushAnnotation(a3)
#--
doc.pushSentence(sent)
wrp_sys.pushDocument(doc)


## Quality Evaluation
bmk = NIFBenchmark(wrp_sys, wrp_gold)
print(bmk.microF())
```

