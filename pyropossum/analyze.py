#!/usr/bin/env python3

import json
import sys

class PPString(object):
    def __init__(self, value):
        self.value = value

class PPNumber(object):
    def __init__(self, value):
        pass






class PPBase(object):
    def __init__(self, classtype):
        self._type = classtype

def ClassFactory(name, argnames, BaseClass=BaseClass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # here, the argnames variable is the one passed to the
            # ClassFactory call
            if key not in argnames:
                raise TypeError("Argument %s not valid for %s" 
                    % (key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name[:-len("Class")])
    newclass = type(name, (BaseClass,),{"__init__": __init__})
    return newclass
    
base_types = {
    "string":str,
    "number":
}



fname = sys.argv[1]
with open(fname, 'r') as f:
    api = json.load(f)

call_names = [c["Name"] for c in api["Calls"]]

type_names = [t["Name"] for t in api["Types"]]
print(call_names)
print(type_names)
