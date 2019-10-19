#!/usr/bin/python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------
from .nifDocument import NIFDocument
from .nifAnnotation import NIFAnnotation
import re
#------------------------------------------------------------------------------------------------------
class NIFWrapper:
    """
    Here, you can handle your NIF corpora. NIFWrapper is the class that will store the sets of document.
    """

    def __init__(self):
        self.documents = []
        self.dictD = {}
        self.prefix = {}
        self.addAlwaysPositionsToUriInSentence = True
        
    def getCantAnnotations(self):
        _cant = 0        
        for dd in self.documents:
            for ss in dd.sentences:
                _S = set([tuple([x.getIni(),x.getFin()]) for x in ss.annotations])
                _cant  =_cant + len(_S)
        return _cant

    def setPrefix(self, _prefix):
        self.prefix = _prefix
        
    def pushDocument(self,_doc):
        self.dictD[_doc.getUri()] = len(self.documents)
        self.documents.append(_doc)
        
    def sorting(self):
        for d in self.documents:
            d.sorting()
        
        self.dictD = {} 
        pos = 0
        for d in self.documents:
            self.dictD[d.uri] = pos
            pos = pos + 1
    
    
    def KeepOnlyTag(self,tag):
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                for a in s.annotations:
                    if ("itsrdf:taClassRef" in a.attr and tag in set(a.attr["itsrdf:taClassRef"]["value"])):
                        tempA.append(a)
                        tempDictA[a.uri] = pos_
                        pos_ = pos_ + 1
                    else:
                        #print("----------\n",a.attr["itsrdf:taClassRef"]["value"])
                        #print(self.documents[di].sentences[si].dictA)
                        key = a.uri
                        #print("--->",self.documents[di].sentences[si].dictA[key])
                        #input("aa")
                        del self.documents[di].sentences[si].dictA[key]
                        #print(self.documents[di].sentences[si].dictA)
                        #input("bb")
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
                #del tempA
    
    
    # e.g. Ltag = [el:Mnt-Full, el:PoS-NounSingular, el:Olp-None, el:Ref-Direct]
    def KeepOnlyListTag(self,Ltag):
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                for a in s.annotations:
                    sss = set(a.attr["itsrdf:taClassRef"]["value"])
                    intt = set(Ltag).intersection(sss)
                    #if ("itsrdf:taClassRef" in a.attr and (len(intt) == len(Ltag) )  ):
                    if ("itsrdf:taClassRef" in a.attr and (len(intt) == len(sss) )  ):
                        tempA.append(a)
                        tempDictA[a.uri] = pos_
                        pos_ = pos_ + 1
                    else:
                        #print("----------\n",a.attr["itsrdf:taClassRef"]["value"])
                        #print(self.documents[di].sentences[si].dictA)
                        key = a.uri
                        #print("--->",self.documents[di].sentences[si].dictA[key])
                        #input("aa")
                        del self.documents[di].sentences[si].dictA[key]
                        #print(self.documents[di].sentences[si].dictA)
                        #input("bb")
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
                #del tempA
    
    
    # e.g. LLtag = [
    #  [el:Mnt-Full, el:PoS-NounSingular, el:Olp-None, el:Ref-Direct], 
    #  [el:Mnt-Short, el:PoS-NounPlural, el:Olp-Minimal, el:Ref-Metaphoric], 
    #  [el:Mnt-Full, el:PoS-NounPlural, el:Olp-None, el:Ref-Metaphoric], 
    #]
    def KeepOnlyListOfListTag(self,LLtag):
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                for a in s.annotations:
                    
                    found = False
                    for Ltag in LLtag:
                        sss = set(a.attr["itsrdf:taClassRef"]["value"])
                        intt = set(Ltag).intersection(sss)
                        #if ("itsrdf:taClassRef" in a.attr and (len(intt) == len(Ltag) )  ):
                        if ("itsrdf:taClassRef" in a.attr and (len(intt) == len(sss) )  ):
                            tempA.append(a)
                            tempDictA[a.uri] = pos_
                            pos_ = pos_ + 1
                            found = True
                            break
                            
                    if not found:
                        #print("----------\n",a.attr["itsrdf:taClassRef"]["value"])
                        #print(self.documents[di].sentences[si].dictA)
                        key = a.uri
                        #print("--->",self.documents[di].sentences[si].dictA[key])
                        #input("aa")
                        del self.documents[di].sentences[si].dictA[key]
                        #print(self.documents[di].sentences[si].dictA)
                        #input("bb")
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
                #del tempA
            

    ##---------- POR HACER
    # Only keep those annotations with membership grathen or equal than parameter tau
    def KeepOnlyTau(self,tau,m = None):
        numDelete = 0
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                for a in s.annotations:
                    if m == None and "el:membership" in a.attr:
                        val = float(a.getAttribute("el:membership"))
                    elif m != None and a.uri in m:
                        val = m[a.uri]
                    else:
                        continue
                    
                    if (val>= tau):
                        tempA.append(a)
                        tempDictA[a.uri] = pos_
                        pos_ = pos_ + 1
                    else:
                        print("[See] -> deleting annotation <%s>"%(a.uri))
                        numDelete = numDelete + 1
                        pass
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
        print("[TOTAL DELETED]: ",numDelete)

    
    
    ## Assign to each annotations an membership score according the average of their categories' punctuations
    def setMembershipAttribute(self,mcat):
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                for a in s.annotations:
                    #print("-->",a.getAttribute("nif:anchorOf"))
                    a_ = NIFAnnotation()
                    A = a.attr.items()
                    a_.attr = dict([ (k, dict([ (k1,v1) for k1,v1 in v.items()])  ) for k,v in a.attr.items() ]) 
                    a_.uri = a.uri
                    if ("itsrdf:taClassRef" in a_.attr):
                        avg_ = 0
                        LAvg = []
                        cn = 0
                        for tag in a_.attr["itsrdf:taClassRef"]["value"]:
                            if tag == "tax:Ambiguous": continue
                            cn = cn + 1
                            if tag in mcat:
                                avg_ = avg_ + mcat[tag]  
                                LAvg.append(mcat[tag]  )
                                    
                            else:
                                avg_ = avg_ + 1
                                print("[ERROR] the tag '"+tag+"' is not contained in the Map-Degree mapping")
                                input("???")
                        avg_ = avg_/cn
                        val_ = min(LAvg)
                        #print("=>",a_.getAttribute("nif:anchorOf"),"  avg:",avg_)
                        ####a_.addAttribute("el:membership",str(round(avg_,3)),"xsd:nonNegativeInteger")
                        a_.addAttribute("el:membership",str(round(val_,3)),"xsd:nonNegativeInteger")
                    tempA.append(a_)
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
    
    
    ## This function deal with mutiple annotations for the same (ini,fin) mention. Here, we join those in only one
    def beSureOnlyOneAnnotation(self):
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                st = {}
                for a in s.annotations:
                    
                    tinifin = tuple([a.getIni(), a.getFin()])
                    if tinifin in st:
                        #print("==> 1")
                        #update getUri
                        pp = st[tinifin]
                        tempA[pp].attr["itsrdf:taIdentRef"]["value"] = tempA[pp].attr["itsrdf:taIdentRef"]["value"] + a.getUrlList()
                        
                        #update tags
                        if ("itsrdf:taClassRef" in a.attr)  and  ("itsrdf:taClassRef" in tempA[pp].attr):
                            tempA[pp].attr["itsrdf:taClassRef"]["value"] =  tempA[pp].attr["itsrdf:taClassRef"]["value"] + a.attr["itsrdf:taClassRef"]["value"]
                        elif ("itsrdf:taClassRef" in a.attr)  and  not ("itsrdf:taClassRef" in tempA[pp].attr):
                            tempA[pp].attr["itsrdf:taClassRef"]["value"] =  a.attr["itsrdf:taClassRef"]["value"]
                            
                        #update membership
                        if (("el:membership" in a.attr) and ("el:membership" in tempA[pp].attr)):
                            #av = (float(tempA[pp].attr["el:membership"]["value"])  +  float(a.attr["el:membership"]["value"])  )/2
                            #OJOOOO---------- cambiamos aqui al maximo
                            av = max(float(tempA[pp].attr["el:membership"]["value"]), float(a.attr["el:membership"]["value"]))
                            tempA[pp].attr["el:membership"]["value"] = str(av)
                            

                    else:
                        #print("==> 2",tinifin)
                        st[tinifin]  = pos_
                        tempA.append(a)
                        tempDictA[a.uri] = pos_
                        pos_ = pos_ + 1
                        #print(st)
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
    
    
    
    # We will associate to each annotation of the current object those scores from the equivalent annotaiton in the parameter 'wrp_'. When there is not a corresponding annotation we associate then the default value.
    def ImportMembershipAccording(self,wrp_, default=None):
        if default == None:
            default = 1

        for di in range(len(self.documents)):
            d = self.documents[di]           
            #print("---------------------------")
            #print("doc Uri->",d.uri)
            
            _b_d = d.uri in wrp_.dictD
            pd = -1
            
            if (_b_d):
                pd = wrp_.dictD[d.uri]
            else:
                print("[WARNING] Document <%s> is not contained in the passed object"%(d.uri))
                
            #print("b_d:",_b_d)
            
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                #print("===========")
                #print("Sent Uri -> ",s.uri)
                
                ps = wrp_.documents[pd].findByPosition(s.getIni(), s.getFin())
                _b_s = (ps != -1)
                
                
                for ai in range(len(s.annotations)):
                    a = s.annotations[ai]
                    #print("Ann URI-->",a.uri)
                    #print("_b_s:",_b_s)
                    
                    v = default
                    
                    
                    
                    if (_b_s): 
                        #print(":)")
                        pa = wrp_.documents[pd].sentences[ps].findByPosition(a.getIni(), a.getFin())
                        if pa!=-1:
                            ann = wrp_.documents[pd].sentences[ps].annotations[pa]       
                            #print("==>",ann.uri)
                            if "el:membership" in ann.attr:
                                #print("OK")
                                v = ann.attr["el:membership"]["value"]
                        
                    
                    self.documents[di].sentences[si].annotations[ai].addAttribute("el:membership",str(v),"xsd:nonNegativeInteger")
    
    
    
    
    
    # We keep only those annotation that are also in wrp_
    def KeepOnlyAnnotationsOf(self,wrp_):
        
        for di in range(len(self.documents)):
            d = self.documents[di]       
            
            _b_d = d.uri in wrp_.dictD
            pd = -1
            
            if (_b_d):
                pd = wrp_.dictD[d.uri]
            else:
                print("[WARNING] Document <%s> is not contained in the passed object"%(d.uri))
                
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                #print("===========")
                #print("Sent Uri -> ",s.uri)
                
                ps = wrp_.documents[pd].findByPosition(s.getIni(), s.getFin())
                _b_s = (ps != -1)
                
                for ai in range(len(s.annotations)):
                    a = s.annotations[ai]
                    
                    if (_b_s): 
                        #print(":)")
                        pa = wrp_.documents[pd].sentences[ps].findByPosition(a.getIni(), a.getFin())
                        if pa!=-1:
                            tempA.append(a)
                            tempDictA[a.uri] = pos_
                            pos_ = pos_ + 1    
                            
                                
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
    
    
    
    def toString(self):
        s = ""
        for p in self.prefix:
            s = s + "@prefix %s: <%s> .\n"%(p,self.prefix[p])
        s = s + "\n"
        
        
        for d in self.documents:
            d.addAlwaysPositionsToUriInSentence = self.addAlwaysPositionsToUriInSentence
            s = s + d.toString()
            s = s + "\n"
        
        return s
    


    #
    # For a Given document and position. Here we return the sentences that contain this position inside.
    def findSentencesInDocumentByAnyPosition(self,docuri,pos):
        
        _b_d = docuri in self.dictD
        pd = -1
        
        if (_b_d):
            pd = self.dictD[docuri]
        else:
            print("[WARNING -findSentencesInDocumentByAnyPosition-] Document <%s> is not contained in the passed object"%(docuri))
            
        d = self.documents[pd]
        for si in range(len(d.sentences)):
            s = d.sentences[si]
            
            # is this the sentence of this annotation?
            if ((si == 0 and pos < int(s.getFin())) or 
            (si == len(d.sentences)-1  and pos >= int(s.getIni())) or 
            (pos >= int(s.getIni()) and pos < int(s.getFin()))):
                
                return si
        return -1


    # Extending the annotations of this document with coreferences. 
    #
    # Suppose we have the sentence:
    #    "[[Barack Obama]] was the president of the [[USA]]. He was the best of them." 
    # where 'Barack Obama' and 'USA' have been annotated by a EL system. We passed as parameter the Coreference-Resolution
    # system output of this sentence, for example, the followings:
    #
    # I) He -> Barack Obama
    # II) them -> president
    #
    # Due to we know the corresponding KB entity of "Barack Obama", we link "He" with it. However, the EL system does'nt
    # find any annotation for "president", so, we exclude "them" of the final annotations.
    #
    # The prameter with the coreference information looks like:
    #    CorefL = [{'start': 31, 'end': 34, 'text': 'him', 'resolved': 'a dog', 
    #               'fullInformation': [{'start': 14, 'end': 19, 'text': 'a dog'}]} ...]
    
    
    def extendsDocWithCoref(self, CorefL, docuri):
         for coref in CorefL:
            #print("------------------------\n")
            #print("-->",coref)

            _b_d = docuri in self.dictD
            pd = -1
            
            if (_b_d):
                pd = self.dictD[docuri]
            else:
                print("[WARNING] Document <%s> is not contained in the passed object"%(docuri))
                
            d = self.documents[pd]
            text = d.getText()
            
            
            # --- step 1. Finding if one of the chain references is already annotated 
            L = []
            if "fullInformation" in coref:
                # Great. I have a list of possible mentions with start/end positions
                for e in coref["fullInformation"]:
                    L.append({
                        "ini": e["start"],
                        "fin": e["end"],
                        "label": e["text"]
                        })
                
            else:
                # Saddly, I will see the ocurrences of the resolved reference in the text,
                # and see if one of they is already annotated 
                overall = 0
                text = text
                
                re_expresion = coref["resolved"]
                re_expresion = re_expresion.replace("(","\(")
                re_expresion = re_expresion.replace(")","\(")
                re_expresion = re_expresion.replace("[","\[")
                re_expresion = re_expresion.replace("]","\]")

                
                
                
                print("--------")
                
                p = re.compile("[ \n\t\r.,:;'!?\"'\(\)\{\}\[\]]"+re_expresion+"[ \n\t\r.,:;'!?\"\(\)\{\}\[\]]")
                for m in p.finditer(text):
                    m_start = m.start()+1
                    L.append({
                        "ini": m_start,
                        "fin": m_start + len(coref["resolved"]),
                        "label": coref["resolved"]
                        })
                
    
            # --- step 2
            for l in L:
                _ini = l["ini"]
                _fin = l["fin"]
                _label = l["label"]
                
                pcoref = self.findSentencesInDocumentByAnyPosition(docuri, coref["start"])
                presolv = self.findSentencesInDocumentByAnyPosition(docuri, _ini)
                
                if pcoref!=-1 and presolv !=-1:
                    
                    s_coref = d.sentences[pcoref]
                    s_resolv = d.sentences[presolv]

                    p_a_coref = s_coref.findByPosition(coref["start"] - int(s_coref.getIni()), coref["end"] - int(s_coref.getIni()))
                    p_a_resolv = s_resolv.findByPosition(_ini - int(s_resolv.getIni()), _fin - int(s_resolv.getIni()))
                    
                    if p_a_coref == -1 and p_a_resolv != -1:
                        
                        ini_ = int(coref["start"]) - int(s_coref.getIni())
                        fin_ = int(coref["end"]) - int(s_coref.getIni())
                        label_ = s_coref.getText()[ini_:fin_]
                        
                        aURI = s_resolv.getUri() + "#char="+str(ini_)+","+str(fin_)
                        a = s_resolv.annotations[p_a_resolv]
                        
                        ann = NIFAnnotation(aURI, ini_, fin_, a.getAttribute("itsrdf:taIdentRef"))
                        ann.addAttribute("nif:anchorOf",label_,"xsd:string")
                        ann.addAttribute("nif:beginIndex",str(ini_),"xsd:nonNegativeInteger")
                        ann.addAttribute("nif:endIndex",str(fin_),"xsd:nonNegativeInteger")
                        self.documents[pd].sentences[pcoref].pushAnnotation(ann)
                        break
                            

    #
    # Here, I return a list of all the position of the annotation by each sentence, and each document
    # E.g., [("hrrp://doc1.com", "http://doc1/sentence1.com", 1,3, sister), ....]
    def wrapper2tuples(self):
        L = []
        for pd in range(len(self.documents)):
            d = self.documents[pd]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                for ai in range(len(s.annotations)):
                    a = s.annotations[ai]
                    L.append(tuple([d.uri, s.uri, a.getIni(), a.getFin(), a.getAttribute("nif:anchorOf")]))
        return L
    
    
    # Extending the annotations of this document with WSD. 
    #
    # Suppose we have the sentence:
    #    "Barack Obama was the president of the USA. He was the best of them." 
    # where 'Barack Obama' and 'USA' have been annotated by a EL system. We passed as parameter the Coreference-Resolution
    # system output of this sentence, for example, the followings:
    #
    # I) He -> Barack Obama
    # II) them -> president
    #
    # Due to we know the corresponding KB entity of "Barack Obama", we link "He" with it. However, the EL system does'nt
    # find any annotation for "president", so, we exclude "them" of the final annotations.
    #
    # The prameter with the coreference information looks like:
    #    WSDL = [{'start': 38, 'end': 41, 'label': 'USA', 'link': 'United_States_Army'} .... ]
    
    
    def extendsDocWithWSD(self, WSDL, docuri): 
         for wsd in WSDL:
            _b_d = docuri in self.dictD
            pd = -1
            
            if (_b_d):
                pd = self.dictD[docuri]
            else:
                print("[WARNING] Document <%s> is not contained in the passed object"%(docuri))
                
            d = self.documents[pd]
            text = d.getText()
            
            
         
            # --- step 2

            
            pwsd = self.findSentencesInDocumentByAnyPosition(docuri, wsd["start"])
            
            if pwsd!=-1:
                
                s_wsd = d.sentences[pwsd]
                p_a = s_wsd.findByPosition(wsd["start"] - int(s_wsd.getIni()), wsd["end"] - int(s_wsd.getIni()))

                
                if p_a == -1:                    
                    ini_ = int(wsd["start"]) - int(s_wsd.getIni())
                    fin_ = int(wsd["end"]) - int(s_wsd.getIni())
                    label_ = s_wsd.getText()[ini_:fin_]
                    
                    aURI = s_wsd.getUri() + "#char="+str(ini_)+","+str(fin_)#+";1"
                    
                    ann = NIFAnnotation(aURI, ini_, fin_, [wsd["link"]])
                    ann.addAttribute("nif:anchorOf",label_,"xsd:string")
                    ann.addAttribute("nif:beginIndex",str(ini_),"xsd:nonNegativeInteger")
                    ann.addAttribute("nif:endIndex",str(fin_),"xsd:nonNegativeInteger")
                    self.documents[pd].sentences[pwsd].pushAnnotation(ann)
                    
                    
                    
    ##
    #  The idea here is to recieve as input other NifWrapper. This wrapper should be the same as this, but, with 
    #  more annotaitons. This function take those annotations that are not in the current wrapper but are in the
    #  passed wrapper as a parameter.
    #
    def mergeWrapper(self, wrp_):
        
        for di in range(len(wrp_.documents)):
            d = wrp_.documents[di]           
            
            _b_d = d.uri in self.dictD
            pd = -1
            
            if (_b_d):
                pd = self.dictD[d.uri]
            else:
                print("[WARNING] Document <%s> is not contained in the passed object"%(d.uri))
            
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                
                ps = self.documents[pd].findByPosition(s.getIni(), s.getFin())
                _b_s = (ps != -1)
                
                
                for ai in range(len(s.annotations)):
                    a = s.annotations[ai]
                    
                    if (_b_s): 
                        a_ini = a.getIni()
                        a_fin = a.getFin()
                        
                        
                        
                        pa = self.documents[pd].sentences[ps].findByPosition(a_ini, a_fin)
                        if pa == -1:      
                            
                            
                            
                            ini_ = int(a_ini)
                            fin_ = int(a_fin)
                            tt = s.getText()
                            
                            label_ = tt[ini_:fin_]
                            
                            aURI = s.getUri() + "#char="+str(ini_)+","+str(fin_)
                            
                            ann = NIFAnnotation(aURI, ini_, fin_, a.getAttribute("itsrdf:taIdentRef"))
                            ann.addAttribute("nif:anchorOf",label_,"xsd:string")
                            ann.addAttribute("nif:beginIndex",str(ini_),"xsd:nonNegativeInteger")
                            ann.addAttribute("nif:endIndex",str(fin_),"xsd:nonNegativeInteger")
                            self.documents[pd].sentences[ps].pushAnnotation(ann)
    
        
        
    
    
    #
    #  This function keeps only in the wrapper the first ocurrence of each pair-link. For example
    #  Suppose that we have the following sentence:
    #
    #                                                                 ---> wiki:Obama
    #                                                                | 
    #  input:  [Barack Obama] and [Michelle Obama] are [married]. [Barack Obama] is a good man.
    #  -----          |                 |                  |
    #                  --> wiki:Obama    --> wiki:Obama     --> wiki:marriage
    # 
    #
    #  output: [Barack Obama] and [Michelle Obama] are [married]. [Barack Obama] is a good man.
    #  ------         |                 |                  |
    #                  --> wiki:Obama    --> wiki:Obama     --> wiki:marriage
    #
    #
    def keep_only_first_annotation_link(self):
        S = set([])
        for di in range(len(self.documents)):
            d = self.documents[di]
            for si in range(len(d.sentences)):
                s = d.sentences[si]
                tempA = []
                tempDictA = {}
                pos_ = 0
                for a in s.annotations:
                    key = "-".join([a.attr["nif:anchorOf"]["value"]]+a.getUrlList())
                    #print("key:",key)
                    if not key in S:
                        S.update([key])
                        tempA.append(a)
                        tempDictA[a.uri] = pos_
                        pos_ = pos_ + 1
                    else:
                        key = a.uri
                        del self.documents[di].sentences[si].dictA[key]
                        
                self.documents[di].sentences[si].annotations = [x for x in tempA]
                self.documents[di].sentences[si].dictA = tempDictA
        



