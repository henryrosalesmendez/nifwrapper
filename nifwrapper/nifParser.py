#!/usr/bin/python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------
from .nifWrapper import NIFWrapper
from .nifAnnotation import NIFAnnotation
from .nifSentence import NIFSentence
from .nifDocument import NIFDocument
from .nifUtils import *
from random import randint
#------------------------------------------------------------------------------------------------------

class NIFParser:
    
    def __init__(self):
        self.D = {} # documents
        self.S = {} # sentences
        self.A = {} # annotations
        self.P = {} # prefix
        self.ET= {} # entity type    
        self.iddoc = 0
        self.showWarnings = True
        self.avoidR = False
        #self.avoidDuplicatedAnnotations = False # Its happen when two annotations of the same document but in the different sentences have same ini and fin position



    #------------
    def parser(text, _format = "turtle"):
        if _format == "turtle":
            return self.parser_turtle(text)
        return "The specified format is not supported"
    
    #------------
    def parser_turtle(self,text):      
        pos = 0
        nText = len(text)
        while pos < nText:
            res = self.newChunk(text, pos,".")
            res[1] = res[1] + 1
            chunk = text[res[0]:res[1]].strip(" \n\r\t")
            #print("-----------")
            #print(chunk)
            if len(chunk) != 0:
                self.mainTripleParser(chunk)            
            pos = res[1]+1

        wrp = self.createIntance()
        return wrp
    
    #------------
    def getParsedListUri(self,text):
        state = 0
        pos = 0
        ntext = len(text)
        L = []
        uri = ""
        while pos < ntext:
            ch = text[pos]
            if state == 0: #fw <
                if ch == "<":
                    state = 1
                if ch == "." or ch == ";":
                    return L
            elif state == 1: #rt >
                if ch == ">":
                    L.append(uri)
                    uri  = ""
                    state = 2
                else:
                    uri = uri + ch
            elif state == 2: #fw < , ; .
                if ch == "<":
                    state = 1
                elif ch == ";" or ch == ".":
                    return L;
            pos = pos + 1
        return L
    
    #------------
    def parsePrefix(self,_triple):
        try:
            nameP = _triple[7:].strip(" \n\r\t").split(":")[0]
            listURI = self.getParsedListUri(_triple)
            self.P[nameP] = listURI[0]
        except:
            #print(sys.exc_info()[0])
            if (self.showWarnings == True):
                print("[Error] trying to store @prefix")
                
                
    #------------
    
    def parseCandidates(self, parent_predicate, text_):
        """
        Parsing candidates information, e.g., for the text:
        
        [rdf:value (<http://exp.orga1> <http://exp.orga1>); exnif:source <http://a> ; exnif:orden 1],
                                [rdf:value (<http://exp.orgb1> <http://exp.orgb2>); exnif:source "Babelfy" ; exnif:orden 1] ;
        
        this parser will return,
        
        ['exnif:sortedCandidates', [
                {'source': 'http://a', 'listCandidates': ['http://exp.orga1', 'http://exp.orga1'], 'type_model_uri':URI}, 
                {'source': 'Babelfy', 'listCandidates': ['http://exp.orgb1', 'http://exp.orgb2'], 'type_model_uri': String}], 
                    'CANDIDATES']
        """
        state_ = -1
        p_ = 0
        ntext_ = len(text_)
        
        predicate_ = ""
        source_ = ""
        type_model_uri = ""
        L_ = []
        v_  = ""
        FinalL_ = []
        
        while p_<ntext_:
            ch_ = text_[p_]
            #print(p_,ch_,state_, "pred:",predicate_, " val:", v_)
            
            if state_ == -1:
                if notSpace(ch_):
                    if ch_ == "[":
                        state_ = 0
            
            elif state_ == 0:
                if ch_ == "]":
                    state_ = -1
                    FinalL_.append({"source": source_, "listCandidates": L_, "type_model_uri": type_model_uri})
                    source_ = ""
                    L_ = []
                    
                elif ch_ == ";":
                    pass
                elif ch_ == ".":
                    return [parent_predicate, text_.strip(" [];"), "BN"]
                elif notSpace(ch_): # fw chr
                    state_ = 1
                    p_ = p_ -1

            elif state_ == 1: # fw chr - predicate_
                if notSpace(ch_):
                    if ch_ == "]":
                        state_ = 0
                        p_ = p_ -1
                        predicate_ = ""
                    else: predicate_ = predicate_ + ch_
                else:                
                    if predicate_ == "rdf:value":                    
                        state_ = 2
                    elif predicate_ == "exnif:source":
                        state_ = 10
                    predicate_ = ""
            #----------------------------------------------------------
            # rdf:value
            elif state_ == 2: #fw a list of URI (<http://exp.orga1> ..) 
                if notSpace(ch_):
                    if ch_ == "(":
                        state_ = 3
                    else:
                        return [parent_predicate, text_.strip(" [];"), "BN"]
            
            elif state_== 3: #fw <
                if notSpace(ch_):
                    if ch_ == "<":
                        state_ = 4
                        v_ = ""
                    elif ch_ == ")":
                        state_ = 0
                    else:
                        return [parent_predicate, text_.strip(" [];"), "BN"]
            
            elif state_ == 4: #fw  URI >
                if notSpace(ch_):
                    state_ = 5
                    p_ = p_ -1
                    
            elif state_ == 5:
                if Space(ch_):
                    return [parent_predicate, text_.strip(" [];"), "BN"]
                elif ch_ == ">":
                    L_.append(v_)
                    v_ = ""
                    state_ = 3
                else:
                    v_ = v_ + ch_
            
            
            #-----------------------------------------------
            # exnif:source
            elif state_ == 10: # fw  <URI> or "Text"
                if notSpace(ch_):
                    if ch_ == "<":
                        state_ = 11
                        type_model_uri = "URI"
                        v_ = ""
                    elif ch_ == '"':
                        state_ = 13
                        type_model_uri = "String"
                    else:
                        return [parent_predicate, text_.strip(" [];"), "BN"]
                    
            elif state_ == 11: #fw no space
                if notSpace(ch_):
                    state_ = 12
                    p_ = p_ -1
                    
            elif state_ == 12: #fw URI>
                if Space(ch_):
                    return [parent_predicate, text_.strip(" [];"), "BN"]
                elif ch_ == ">":
                    source_ = v_
                    v_ = ""
                    state_ = 0
                else:
                    v_ = v_ + ch_
                    
            elif state_ == 13: #fw text" or ""text"""
                if ch_ == '"': # fw triple " string e.g. """Babelfy"""
                    state_ = 15
                else:
                    state_ = 14
                    v_ = ch_
                    
            elif state_ == 14:  #fw text"
                if ch_ == '"':
                    source_ = v_
                    v_ = ""
                    state_ = 0
                else:
                    v_ = v_ + ch_
                
            elif state_ == 15:
                if ch_ != '"':
                    return [parent_predicate, text_.strip(" [];"), "BN"]
                else:
                    state_ = 16
                    
            elif state_ == 16: #fw first letter of the value
                if ch_ != '"':
                    state_ = 17
                    v_ = ch_
            
            elif state_ == 17:
                if ch_ == '"':
                    source_ = v_
                    v_ = ""
                    state_ = 0
                else:
                    v_ = v_ + ch_

            p_ = p_ + 1
            
        if len(FinalL_):
            return [parent_predicate, FinalL_, "CANDIDATES"]
        
        return [parent_predicate, text_.strip(" [];"), "BN"]
        
    
    #------------
    def getParsePredicate_Object(self,text):
        state = 0
        p = 0
        ntext = len(text)
        
        predicate = ""
        value = None
        ptype = ""
        L = []
        v  = ""
        t = ""
        u = ""
        tag = ""
        
        while p<ntext:
            ch = text[p]
            #print(p,ch,state)
            if state == 0:
                if notSpace(ch): # fw chr
                    state = 1
                    p = p -1
                elif ch == "." or ch == ";":
                    return None
            elif state == 1: # fw chr - predicate
                if notSpace(ch):
                    predicate = predicate + ch
                else:
                    if predicate == "exnif:sortedCandidates":
                        return self.parseCandidates(predicate, text[p:])
                    state = 2
            elif state == 2: # fw not \s
                if notSpace(ch):
                    state = 3
                    p = p -1
            elif state == 3: #fw value
                if Space(ch): 
                    pass
                elif ch == "<":
                    state = 10
                elif ch == '"':
                    state = 20
                elif ch == "[":
                    state = 30
                elif ch == "(":
                    state = 60
                else:
                    state = 40
                    p = p - 1
            #-
            elif state == 10: #rt > --  URI LIST 
                if ch == ">":
                    L.append(u)
                    u  = ""
                    state = 11
                    
                    if ntext == p+1:
                        return [predicate,L,"URI LIST"];
                else:
                    u = u + ch
            elif state == 11: #fw < , ; .
                if ch == "<":
                    state = 10
                elif ch == ";" or ch == ".":
                    return [predicate,L,"URI LIST"];
            
            #-
            elif state == 20: #fw "/""" - type
                if ch == '"':
                    state = 26
                else:
                    state = 21
                    p = p - 1
            elif state == 21: # fw "
                if ch == '"':
                    state = 100
                elif ch == "\\":
                    state = 22
                else:
                    v = v + ch
            
            elif state == 22: # av /
                v = v + ch
                state = 21
                
            elif state == 26: # fw ""
                if ch == '"':
                    state = 27
                else:
                    v = v + '"' + ch
                    state = 21
                    
            elif state == 27: # rt """
                if ch == '"':
                    state = 28
                elif ch == "\\":
                    state = 29
                else:
                    v = v + ch
            
            elif state == 28: # rt ""
                if ch == '"':
                    state = 281
                else:
                    v = v + '"' + ch
                    state = 27
            
            elif state == 281:
                if ch == '"':
                    state = 100
                elif ch == "\\":
                    state = 29
                else:
                    v = v + '""' + ch
                    state = 27
            
            elif state == 29:
                v = v + ch
                state = 27
            
            #-
            elif state == 30: #fw Blank Node
                if ch == "]":
                    return [predicate,v,"BN"]
                else:
                    v = v + ch
            
            elif state == 40: #fw TAG LIST
                if ch == "." or ch == ";" or ntext == p+1:
                    if tag != "":
                        L.append(tag)
                    return [predicate, L, "TAG LIST"]
                elif Space(ch) or ch == ",":
                    state = 41
                    p = p - 1
                elif notSpace(ch):
                    tag = tag + ch
            elif state == 41:
                L.append(tag)
                tag = ""
                state = 42
            elif state == 42:
                if Space(ch) or ch == ",":
                    pass
                else:
                    p = p -1
                    state = 40    
            
            #-
            elif state == 60: #rt > --  COLLECTION
                if ch == "<":
                    state = 61
                    u = ""
                if ch == ")":
                    return [predicate,L,"COLLECTION"];
                
            elif state == 61:
                if ch == ">":
                    L.append(u)
                    u  = ""
                    state = 60
                    
                    if ntext == p+1:
                        return [predicate,L,"COLLECTION"];
                else:
                    u = u + ch
            
            #-
            elif state == 100: #fw text type "
                if Space(ch):
                    pass
                elif ch == "^":
                    state = 101
                else:
                    return [predicate,v,"xsd:string"]
            elif state == 101:
                if ch == "^":
                    state = 102
                else:
                    state = 102
                    p = p - 1
            elif state == 102:
                if Space(ch):
                    pass
                else:
                    state = 103
                    p = p -1
            elif state == 103:
                if Space(ch):
                    return [predicate,v,t]
                else:
                    t = t + ch

            p = p + 1
        
        if tag != "":
            L.append(tag)
            return [predicate, L, "TAG LIST"]

        if u!= "":
            L.append(u)
            return [predicate, u, "URI LIST"]
                
        
    #------------
    def parseTriple(self, _triple):       
        
        [pini,pfin] = self.newChunk(_triple,0,";")
        pfin = pfin + 1
        #print("-------------")
        #print("_triple:",_triple)
        #print("==>",_triple[pini:pfin])
        #print("____")
        uri = self.getParsedListUri(_triple[pini:pfin])[0]
        
        AttrList = []
        pos = pfin + 1 
        #print(_triple,"\n.......")
        while pos < len(_triple):
            #print("========================================")
            
            res = self.newChunk(_triple, pos,";")
            
            if res != None:
                pini = res[0]
                pfin = res[1]+1
                
                #print("=>",_triple[pini:pfin])
                
                L = self.getParsePredicate_Object(_triple[pini:pfin])
                if L != None:
                    AttrList.append(L)

                pos = pfin + 1
                while pos < len(_triple) and Space(_triple[pos]):
                    pos = pos + 1
            else: break;
        #print("//////////////////////////////////////////")
        #print("----------------> returning:", {"attr":AttrList, "uri":uri})
        #print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\a")
        return {"attr":AttrList, "uri":uri}
        
        
    
    #------------
    def mainTripleParser(self,_text):
        res = self.newChunk(_text, 0,".")
        res[1]= res[1] + 1
        triple = _text[res[0]:res[1]].strip(" \n\r\t")
        if len(triple)!=0:
            if triple.find("@prefix") == 0:
                self.parsePrefix(triple)
            
            elif triple.find("nif:sourceUrl") != -1:
                #print("DOCUMENT ===================================")
                #print(triple)

                doc = self.parseTriple(triple)
                #print("---------\n",doc)
                if doc["uri"] in self.D:
                    if (self.showWarnings == True):
                        print("[Error] The document "+doc["uri"]+" is duplicated.")
                else:
                    doc["index"] = self.iddoc
                    self.iddoc = self.iddoc + 1                    
                    self.D[doc["uri"]] = toDict(doc)
                    
            #elif triple.find("nif:Phrase") != -1  or  triple.find("anchorOf") != -1:
            elif triple.find("itsrdf:taIdentRef") != -1 or triple.find("nif:Phrase")!= -1:
                #print("ANNOTATION ===================================")
                #print(triple)
                
                ann = self.parseTriple(triple)
                #print("------")
                #print(ann)
                if ann["uri"] in self.A:
                    if (self.showWarnings == True):
                        print("[Error] The annotation "+ann["uri"]+" is duplicated.")
                    if (self.avoidR == False):
                        cc = 1
                        
                        if ann["uri"] in self.A:
                            while (ann["uri"] + ";" + str(cc)) in self.A:
                                cc = cc + 1
                            ann["uri"] = ann["uri"] + ";" + str(cc)
                        else:
                            ann["uri"] = ann["uri"] + ";" + str(cc)
                        
                        self.A[ann["uri"]] = toDict(ann)
                else:
                    self.A[ann["uri"]] = toDict(ann)
                
            
            elif triple.find("mnt:entityType") != -1:
                #print("ENTITY TYPE ===================================")
                #print(triple)
                etype_uri = self.getParsedListUri(triple)
                if etype_uri != None:
                    self.ET[etype_uri[0]] = triple.split("mnt:entityType")[1].strip(" \t\r\n")

            else:
                #print("SENTENCE ===================================")
                #print(triple)
                
                sent = self.parseTriple(triple)
                if sent["uri"] in self.S:
                    if (self.showWarnings == True):
                        print("[Error] The document "+sent["uri"]+" is duplicated.")
                else:
                    self.S[sent["uri"]] = toDict(sent)

            
                
            


    #------------
    def newChunk(self,_text, _pos, _mark = None): #Searching the next chunk
        if _mark == None:
            _mark = ";"
        state = -1
        nText = len(_text)
        tt = _text
        p = _pos
        pIni = p
        while p < nText:
            ch = tt[p]
            #print(p,ch,ord(ch),state,len(ch))
            if state == -1:
                if ch == " " or ch == "\n" or ch == "\t" or ch == "\r" or ch == "\s":
                    state = -1
                else:
                    state = 0;
                    pIni = p;
                    p = p -1
            elif state == 0:
                if ch == "<": 
                    state = 1
                elif ch == '"':
                    state = 10
                elif ch == "[":
                    state = 20
                elif ch == _mark:
                    return [pIni,p];

            elif state == 1:
                if ch == ">":
                    state = 0
                    
            elif state == 10:
                if ch == '"':
                    state = 11
                else:
                    state = 16
            elif state == 11:
                if ch == '"':
                    state = 12
                else:
                    state = 16
            elif state == 12: # fw """
                if ch == '\\':
                    state = 13
                elif ch == '"':
                    state = 14
                    
            elif state == 13: # avoiding next character
                state = 12
            
            elif state == 14: #rt "" 
                if ch == '"':
                    state = 15
                else:
                    state = 12
            
            elif state == 15: #ret " 
                if ch == '"':
                    state = 0
                else:
                    state = 12            
                
            elif state == 16: # rt "
                if ch == '"':
                    state = 0
                
            
            elif state == 20: # rt ]
                if ch == "]":
                    state = 0
                
            p = p + 1
        return [pIni,p]
    
    
    def sorting(self,dictOfObj,parentUri,nameKeyParent):
        AnnL = []
        for k_o in dictOfObj:
            o = dictOfObj[k_o]
            if o[nameKeyParent]["value"][0] == parentUri:
                AnnL.append(o)
        return AnnL   
    
    
    
    def createIntance(self):
        wrp = NIFWrapper()
        
        for uridoc in self.D:
            doc = self.D[uridoc]
            _doc = NIFDocument(uridoc)
           
            for urisent in self.S:
                sent = self.S[urisent]
                _sent = NIFSentence(urisent)
                
                #print("sent:",sent)
                urid = None
                _ms = {"nif:anchorOf":"nif:isString"}
                if "nif:broaderContext" in sent:
                    urid = sent["nif:broaderContext"]["value"][0]
                elif "nif:referenceContext" in sent:
                    urid = sent["nif:referenceContext"]["value"][0]
                    _ms["nif:referenceContext"] = "nif:broaderContext"
                    
                if urid != None:  
                    #if uridoc == urid:
                    if uridoc.split("#")[0] == urid.split("#")[0]:
                        for uriann in self.A:
                            ann = self.A[uriann]

                            pred = None
                            _m = {}
                            if "nif:sentence" in ann:
                                pred = "nif:sentence"
                                _m["nif:sentence"] = "nif:referenceContext"
                                _m["nif:referenceContext"] = "nif:context"
                            elif "nif:referenceContext" in ann:
                                pred = "nif:referenceContext"
                            if pred != None:
                                uris = ann[pred]["value"][0]
                                if urisent == uris:
                                    _ann = NIFAnnotation(uriann) 
                                    for key in ann:
                                        _ann.addAttribute(key,ann[key]["value"],ann[key]["type"],_m)
                                    _sent.pushAnnotation(_ann)
                            else:
                                if (self.showWarnings == True):
                                    print("[Error] Annotation with a not valid link to a Sentence")
                        sKeys = set([])
                        for key in sent:
                            sKeys.add(key)
                            #print("==> sent:",key,sent[key]["value"],sent[key]["type"])
                            _sent.addAttribute(key,sent[key]["value"],sent[key]["type"],_ms)
                        
                        #---  searching missing nif:beginIndex and nif:endIndex predicates
                        if not "nif:beginIndex" in sKeys:
                            ini = getIniFromUri(urisent)
                            if ini!=None:
                                _sent.addAttribute("nif:beginIndex",ini,"xsd:nonNegativeInteger")
                            else:
                                if (self.showWarnings == True):
                                    print("[Error] Imposible to locate predicate nif:beginIndex in <"+urisent+">")
                                
                        if not "nif:endIndex" in sKeys:
                            fin = getFinFromUri(urisent)
                            if fin!=None:
                                _sent.addAttribute("nif:endIndex",fin,"xsd:nonNegativeInteger")
                            else:
                                if (self.showWarnings == True):
                                    print("[Error] Imposible to locate predicate nif:nif:endIndex in <"+urisent+">")
                                
                        _doc.pushSentence(_sent)
                        del _sent
                else:
                    if (self.showWarnings == True):
                        print("[Error] Sentence without document uri specification")
                
                
            
            for key in doc:
                _doc.addAttribute(key,doc[key]["value"],doc[key]["type"])
            wrp.pushDocument(_doc)    
            
        wrp.setPrefix(self.P)  
        #wrp.sorting()
        return wrp
    

