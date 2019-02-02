# nifWrapper

The NLP Interchange Format (NIF) is a RDF/OWL-based format wich allows the spotting of words from text corpora and its metada such as part-of-speech tags, knowledge-base links, entity type, etc. Likewise other Python libraries (e.g., [pynif](https://github.com/wetneb/pynif)), this library transform NIF data to python classes in order to better proccessing this information. 

If you want to create/visualizate NIF data see NIFify in [GitHub](https://github.com/henryrosalesmendez/NIFify_v2) or a [demo](https://users.dcc.uchile.cl/~hrosales/NIFify_v2.html).

## Example

Install first the library:

pip install -i https://test.pypi.org/simple/ nifwrapper


```python
from nifwrapper import *


t = '''
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542>
a nif:String , nif:Context  , nif:RFC5147String ;
nif:isString """Unemployment in the EU at record low since 2008. According to the latest Eurostat figures the unemployment has hit its lowest rate since December 2008 for the second month in a row in June. According to the latest Eurostat findings, the unemployment in the EU was 7.7 percent in June 2017, the same rate as in May, and down from 8.6 percent in June 2016. The current rate is the lowest recorded in the EU since December 2008. The euro area seasonally-adjusted unemployment was 9.1 percent in June 2017, down from 9.2 percent in May 2017 and down from 10.1 percent in June 2016. This is the lowest rate recorded in the euro area since February 2009. Eurostat estimates that 18.725 million men and women in the EU28, of whom 14.718 million in the euro area, were unemployed in June 2017. Among the Member States, the lowest unemployment in June 2017 was recorded in the Czech Republic (2.9 percent), Germany (3.8 percent) and Malta (4.1percent). The highest unemployment were observed in Greece (21.7 percent in April 2017) and Spain (17.1 percent). Compared with a year ago, unemployment fell in all Member States for which data is comparable over time, except Estonia which showed an increase (from 6.5 percent in May 2016 to 6.9 percent in May 2017). The largest decreases were registered in Spain (from 19.9 percent to 17.1 percent) and Croatia (from 13.3 percent to 10.6 percent). As a comparison, in June 2017, the unemployment in the United States was 4.4 percent, up from 4.3 percent in May 2017 but down from 4.9 percent in June 2016. """^^xsd:string ;
nif:beginIndex "0"^^xsd:nonNegativeInteger ;
nif:endIndex "1542"^^xsd:nonNegativeInteger ;
nif:sourceUrl <http://www.voxeurop.eu/en/2017/social-issues-5121271> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,48>
a nif:String , nif:Context , nif:RFC5147String ;
nif:isString """Unemployment in the EU at record low since 2008."""^^xsd:string ;
nif:beginIndex "0"^^xsd:nonNegativeInteger ;
nif:endIndex "48"^^xsd:nonNegativeInteger ;
nif:broaderContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,12>
a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
nif:referenceContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,48> ;
nif:Context <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> ;
nif:anchorOf """Unemployment"""^^xsd:string ;
nif:beginIndex "0"^^xsd:nonNegativeInteger ;
nif:endIndex "12"^^xsd:nonNegativeInteger ;
itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Unemployment> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=20,22>
a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
nif:referenceContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,48> ;
nif:Context <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> ;
nif:anchorOf """EU"""^^xsd:string ;
nif:beginIndex "20"^^xsd:nonNegativeInteger ;
nif:endIndex "22"^^xsd:nonNegativeInteger ;
itsrdf:taIdentRef <https://en.wikipedia.org/wiki/European_Union> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=43,47>
a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
nif:referenceContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,48> ;
nif:Context <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> ;
nif:anchorOf """2008"""^^xsd:string ;
nif:beginIndex "43"^^xsd:nonNegativeInteger ;
nif:endIndex "47"^^xsd:nonNegativeInteger ;
itsrdf:taIdentRef <https://en.wikipedia.org/wiki/2008> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=49,189>
a nif:String , nif:Context , nif:RFC5147String ;
nif:isString """According to the latest Eurostat figures the unemployment has hit its lowest rate since December 2008 for the second month in a row in June."""^^xsd:string ;
nif:beginIndex "49"^^xsd:nonNegativeInteger ;
nif:endIndex "189"^^xsd:nonNegativeInteger ;
nif:broaderContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=24,32>
a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
nif:referenceContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=49,189> ;
nif:Context <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> ;
nif:anchorOf """Eurostat"""^^xsd:string ;
nif:beginIndex "24"^^xsd:nonNegativeInteger ;
nif:endIndex "32"^^xsd:nonNegativeInteger ;
itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Eurostat> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=45,57>
a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
nif:referenceContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=49,189> ;
nif:Context <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> ;
nif:anchorOf """unemployment"""^^xsd:string ;
nif:beginIndex "45"^^xsd:nonNegativeInteger ;
nif:endIndex "57"^^xsd:nonNegativeInteger ;
itsrdf:taIdentRef <https://en.wikipedia.org/wiki/Unemployment> .

<http://www.voxeurop.eu/en/2017/social-issues-5121271#char=88,96>
a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;
nif:referenceContext <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=49,189> ;
nif:Context <http://www.voxeurop.eu/en/2017/social-issues-5121271#char=0,1542> ;
nif:anchorOf """December"""^^xsd:string ;
nif:beginIndex "88"^^xsd:nonNegativeInteger ;
nif:endIndex "96"^^xsd:nonNegativeInteger ;
itsrdf:taIdentRef <https://en.wikipedia.org/wiki/December> .
'''


parser = NIFParser()
wrp = parser.parser_turtle(t)
print(wrp.toString())
```

