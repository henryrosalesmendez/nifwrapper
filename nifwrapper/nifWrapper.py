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
                #print("text_r:",text_r)
                
                p = re.compile("[ \n\t\r.,:;'!?\"'\(\)\{\}\[\]]"+re_expresion+"[ \n\t\r.,:;'!?\"\(\)\{\}\[\]]")
                for m in p.finditer(text):
                    m_start = m.start()+1
                    #print(m_start, m.group(),"-->|",text[m_start:])
                    L.append({
                        "ini": m_start,
                        "fin": m_start + len(coref["resolved"]),
                        "label": coref["resolved"]
                        })
                
                #input("okk??")
                '''
                print("==> text:",text)
                while True:
                    pos = text[overall:].find(coref["resolved"])
                    print("-> pos:",pos)
                    if pos != -1:                       
                        L.append({
                        "ini": overall + pos,
                        "fin": overall + pos + len(coref["resolved"]),
                        "label": coref["resolved"]
                        })
                        print("L:",L)
                        overall = overall + pos + len(coref["resolved"])
                        print("overall:",overall)
                        print("text[overall:]:",text[overall:])
                    else: break
                '''

            #print("Final L:",L) 
            #input("conforme?")
            # --- step 2
            for l in L:
                _ini = l["ini"]
                _fin = l["fin"]
                _label = l["label"]
                
                #print("_ini:",_ini)
                #print("_fin:",_fin)
                #print("_label:",_label)
                
                pcoref = self.findSentencesInDocumentByAnyPosition(docuri, coref["start"])
                presolv = self.findSentencesInDocumentByAnyPosition(docuri, _ini)
                
                #print("pcoref:",pcoref)
                #print("presolv:",presolv)
                
                if pcoref!=-1 and presolv !=-1:
                    
                    s_coref = d.sentences[pcoref]
                    s_resolv = d.sentences[presolv]
                    
                    #print('00000000> oref["start"] - int(s_coref.getIni()):', coref["start"] - int(s_coref.getIni()))
                    #print('00000000> coref["end"] - int(s_coref.getIni()):', coref["end"] - int(s_coref.getIni()))
                    p_a_coref = s_coref.findByPosition(coref["start"] - int(s_coref.getIni()), coref["end"] - int(s_coref.getIni()))
                    p_a_resolv = s_resolv.findByPosition(_ini - int(s_resolv.getIni()), _fin - int(s_resolv.getIni()))
                    #print('8888888> _ini - int(s_resolv.getIni()):',_ini - int(s_resolv.getIni()))
                    #print('8888888> _fin - int(s_resolv.getIni()):', _fin - int(s_resolv.getIni()))
                    
                    #print("==> p_a_coref:",p_a_coref)
                    #print("==> p_a_resolv:", p_a_resolv)
                    
                    if p_a_coref == -1 and p_a_resolv != -1:
                        
                        ini_ = int(coref["start"]) - int(s_coref.getIni())
                        fin_ = int(coref["end"]) - int(s_coref.getIni())
                        label_ = s_coref.getText()[ini_:fin_]
                        
                        #print("ini_:",ini_)
                        #print("fin_:",fin_)
                        #print("label_:",label_)
                        
                        aURI = s_resolv.getUri() + "#char="+str(ini_)+","+str(fin_)
                        a = s_resolv.annotations[p_a_resolv]
                        
                        ann = NIFAnnotation(aURI, ini_, fin_, a.getAttribute("itsrdf:taIdentRef"))
                        ann.addAttribute("nif:anchorOf",label_,"xsd:string")
                        ann.addAttribute("nif:beginIndex",str(ini_),"xsd:nonNegativeInteger")
                        ann.addAttribute("nif:endIndex",str(fin_),"xsd:nonNegativeInteger")
                        self.documents[pd].sentences[pcoref].pushAnnotation(ann)
                        break
                        
                

                """
                found = False
                for si in range(len(d.sentences)):
                    s = d.sentences[si]
                    
                    print("===============\n","==> sentence:",s.getText())
                    print("==> s.getIni()",s.getIni())
                    
                    # is this the sentence of this annotation?
                    if ((si == 0 and _ini < int(s.getFin())) or 
                    (si == len(d.sentences)-1  and _ini >= int(s.getIni())) or 
                    (_ini >= int(s.getIni()) and _ini < int(s.getFin()))):
                        
                        _ini_ = _ini - int(s.getIni())
                        _fin_ = _fin - int(s.getIni())
                        _label_ = s.getText()[_ini_:_fin_]
                        
                        print("_ini_:",_ini_)
                        print("_fin_:",_fin_)
                        print("_label_:",_label_)
                        
                        if _label != _label_:
                            print("[WARNING] %s is different to the [start:end] position (%s) in the sentence."%(_label,_label_))
                        
                        print("-->",'coref["start"]:',coref["start"])
                        print("-->",'coref["end"]:',coref["end"])
                        pa = s.findByPosition(coref["start"], coref["end"])
                """
                
                """
                        print("---> PA:",pa)
                        input("ok=)")
                        if pa == -1: 
                            ini_ = int(coref["start"]) - int(s.getIni())
                            fin_ = int(coref["end"]) - int(s.getIni())
                            label_ = s.getText()[ini_:fin_]
                            
                            print("ini_:",ini_)
                            print("fin_:",fin_)
                            print("label_:",label_)
                            
                            
                            aURI = s.getUri() + "#char="+str(ini_)+","+str(fin_)
                            a = s.annotations[pa]
                            
                            print("a.attr:",a.attr)
                            input("OKKK???")
                            
                            ann = NIFAnnotation(aURI, ini_, fin_, a.getAttribute("itsrdf:taIdentRef"))
                            ann.addAttribute("nif:anchorOf",label_,"xsd:string")
                            ann.addAttribute("nif:beginIndex",str(ini_),"xsd:nonNegativeInteger")
                            ann.addAttribute("nif:endIndex",str(fin_),"xsd:nonNegativeInteger")
                            self.documents[pd].sentences[si].pushAnnotation(ann)
                            found = True
                            print("HEREEE", ann.toString())
                            break;
                    
                if found: break;
                """
                        
                            





