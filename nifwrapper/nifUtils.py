#!/usr/bin/python3
# -*- coding: utf-8 -*-

import functools 

def notSpace(ch):
    return (" \n\r\t".find(ch) == -1)

def Space(ch):
    return (" \n\r\t".find(ch) != -1)


def toDict(obj):
    L = obj["attr"]
    d = {}
    for l in L:
        if not l[0] in d:
            d[l[0]] = {
                "value" : l[1],
                "type" : l[2]
                }
        elif (l[0] in d) and (l[2] == "URI LIST") and (d[l[0]]["type"] == "URI LIST"):
            d[l[0]]["value"] = d[l[0]]["value"] + l[1]

    return d


def attr2nif(attr,except_set, passedValues=None):
    s = ""
    #print("except_set:",except_set)
    for key in attr:
        a = attr[key]
        a_value = a["value"]
        
        if passedValues and key in passedValues:
            a_value = passedValues[key]["value"]
        #print(key,"=>",a)
        if not key in except_set:
            if a["type"] == "BN":
                s = s + '        %s [%s] ;\n'%(key,a_value)
            elif a["type"] == "URI LIST":
                if key in ['nif:context', 'nif:broaderContext'] and "nif:beginIndex" in attr and "nif:endIndex" in attr:
                    ini = attr["nif:beginIndex"]["value"]
                    fin = attr["nif:endIndex"]["value"]
                    s = s + '        %s %s ;\n'%(key,", ".join(["<"+standarURI(x, ini, fin)+">" for x in a_value]))
                else: s = s + '        %s %s ;\n'%(key,", ".join(["<"+x+">" for x in a_value]))
            elif a["type"] == "TAG LIST":
                if a_value == None or a_value == [] or a_value[0].find("nif:Phrase") != -1:
                    continue
                s = s + '        %s %s ;\n'%(key,", ".join(a_value))
            elif a["type"] == "xsd:nonNegativeInteger":
                s = s + '        %s "%s"^^%s ;\n'%(key,a_value,a["type"])
            else:
                s = s + '        %s """%s"""^^%s ;\n'%(key,a_value,a["type"])
    
    
    return s[:len(s)-2] +  ".\n"



def standarURI(uri,ini,fin):
    if uri.find("#") != -1:
        return "<"+uri+">"
    else:
        return "<"+uri+"#char="+str(ini)+","+str(fin)+">"


def getIniFromUri(uri):
    if uri.find("#char=") != -1:
        L = uri.strip(" \n<>\t\r").split("char=")
        [ini,fin] = L[1].split(",")
        return ini
    return None    


def getFinFromUri(uri):
    if uri.find("#char=") != -1:
        L = uri.strip(" \n<>\t\r").split("char=")
        [ini,fin] = L[1].split(",")
        return ini
    return None




def compare_ini_fin(o1,o2):    
    #
    ini1 = o1.getIni()
    fin1 = o1.getFin()
    
    ini2 = o2.getIni()
    fin2 = o2.getFin()
    
    #
    if ini1<ini2:
        return -1
    elif ini1>ini2:
        return 1
    elif fin1 < fin2:
        return -1
    elif fin1 > fin2:
        return 1
    
    return 0
        
cmp_ = functools.cmp_to_key(compare_ini_fin)


def uriShort(t):
    L = t.split("/")
    if len(L) != 0:
        return L[-1]
    return t

