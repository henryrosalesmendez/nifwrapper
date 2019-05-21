#!/usr/bin/python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------
from .nifDocument import NIFDocument
from .nifAnnotation import NIFAnnotation

#------------------------------------------------------------------------------------------------------
class NIFWrapper:
    """
    Here, you can handle your NIF corpora. NIFWrapper is the class that will store the sets of document.
    """

    def __init__(self):
        self.documents = []
        self.dictD = {}
        self.prefix = {}
        
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
            s = s + d.toString()
            s = s + "\n"
        
        return s
    
















