import sys
import configparser
import calendar
import time
from simpletal import simpleTAL, simpleTALES
import os
import json
import HashGenerator

class flows(object):
    def __init__(self):
        self.flows = []
        self.policies =[]

class FreeMarkerWithSimpleTal:

    @staticmethod
    def initializeConfig():
        # Read Config file for configuration
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    # def __initalize_timestamp():
    #     return time_stamp = calendar.timegm(time.gmtime())

    def initializeFreeMarkerContext(self, config,__flowObj,__policyList):
        # Create the context that is used by the template
        context = simpleTALES.Context()
        time_stamp = calendar.timegm(time.gmtime())
        context.addGlobal ("basePath", __flowObj.__getattribute__("basePath"))
        context.addGlobal ("proxyRevision", "13")
        context.__setattr__("proxyName",__flowObj.__getattribute__("title"))
        context.addGlobal("proxyName",__flowObj.__getattribute__("title"))
        print("Value-->",config['DEFAULT']['CREATED_BY'])
        context.addGlobal("createdBy",config['DEFAULT']['CREATED_BY'] )
        context.addGlobal("encodingStyle",config['DEFAULT']['ENCODING'] )
        context.addGlobal("standAlone",config['DEFAULT']['STANDALONE'] )
        context.addGlobal("majorVersion",config['DEFAULT']['CONFIGURATION_VERSION_MAJOR'] )
        context.addGlobal("minorVersion",config['DEFAULT']['CONFIGURATION_VERSION_MINOR'] )
        context.addGlobal("Description",config['DEFAULT']['DESCRIPTION'] )
        context.addGlobal("CreatedAt",time_stamp )
        context.addGlobal("LastModifiedAt",time_stamp )
        proxyServerName = __flowObj.__getattribute__("title")+"-server"
        context.addGlobal("proxyServerName", proxyServerName)
        # Get List of conditional Flows
        _flowString = self.prepareFlowDetails(__flowObj)
        context.addGlobal("details",_flowString)
        # Get List of Policies and Hash
        self.policies = __policyList
        context.addGlobal("policies",self.policies)
        return context

    def prepareFlowDetails(self, __flowObj):
        # Get List of conditional Flows
        listOfFlows = __flowObj.__getattribute__("pathModules")
        # Initializing pathmodel to None so we can use in other scope
        _pathModel = ""
        dataList = []
        for pathObjects in listOfFlows:
            # Improvement. Instead of JSON, I should try to create Python Dicts directly.
            _pathModel = self.prepareStr(pathObjects.__getattribute__("pathId"),pathObjects.__getattribute__("operationType"),pathObjects.__getattribute__("description"),pathObjects.__getattribute__("operationId"))
            data = json.loads(_pathModel)
            dataList.append(dict(data))
            
        self.flows = dataList
        return  self

    
    def prepareStr(self,pathId,operationType,description,operationId):
        objectStr = "{\"pathId\":\""+pathId+"\",\"operationType\":\""+operationType+"\",\"description\":\""+description+"\",\"operationId\":\""+operationId+"\"}"
        return objectStr

    def createFolder(self,directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                os.removedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)
        
    def prepareProxyArtifacts(self,context):
        ## Improvement Extract common method outof it

        # Prepare proxies default.xml
        proxyTemplateFile = open ("./templates/proxies/default.xml", 'rt', encoding = 'utf-8')
        proxyDirectoryPath = "./apiproxy/proxies"
        self.createFolder(proxyDirectoryPath)
        proxyWriteFile = open(proxyDirectoryPath+"/default.xml",'w')
        template = simpleTAL.compileXMLTemplate (proxyTemplateFile)
        template.expand(context, proxyWriteFile)
        proxyTemplateFile.close()
        proxyWriteFile.close()
        print("Proxies....SUCCESSS!!!!!!!!!!!!!!!!!")


        # Prepare targets default.xml
        templateFile = open ("./templates/targets/default.xml", 'rt', encoding = 'utf-8')
        targetProxyDirectoryPath = "./apiproxy/targets"
        self.createFolder(targetProxyDirectoryPath)
        testWriteFile = open(targetProxyDirectoryPath+"/default.xml",'w')
        template = simpleTAL.compileXMLTemplate (templateFile)
        template.expand(context, testWriteFile)
        templateFile.close()
        testWriteFile.close()
        print("Proxies--Target....SUCCESSS!!!!!!!!!!!!!!!!!")

        # prepare hash for proxy default.xml
        __objecthashgenerator = HashGenerator.hashgenerator()
        _proxyHashValue =  __objecthashgenerator.calculatehashfromfile("./apiproxy/proxies/default.xml")
        context.addGlobal("proxyResourceName", "default")
        _proxyHashValue = "SHA-512:"+_proxyHashValue
        context.addGlobal("proxyHash", _proxyHashValue)
        _targetHashValue =  __objecthashgenerator.calculatehashfromfile("./apiproxy/targets/default.xml")
        _targetHashValue = "SHA-512:"+_targetHashValue
        context.addGlobal("targetResourceName", "default")
        context.addGlobal("targetHash", _targetHashValue)

        # prepare Manifest File i.e. manifest.xml
        templateFile = open ("./templates/manifests/manifest.xml", 'rt', encoding = 'utf-8')
        targetProxyDirectoryPath = "./apiproxy/manifests"
        self.createFolder(targetProxyDirectoryPath)
        testWriteFile = open(targetProxyDirectoryPath+"/manifest.xml",'w')
        template = simpleTAL.compileXMLTemplate (templateFile)
        template.expand(context, testWriteFile)
        templateFile.close()
        testWriteFile.close()
        print("Manifest....SUCCESSS!!!!!!!!!!!!!!!!!")

        # prepare Hash for Manifest file
        _proxyHashValue =  __objecthashgenerator.calculatehashfromfile("./apiproxy/manifests/manifest.xml")
        _proxyHashValue = "SHA-512:"+_proxyHashValue
        context.addGlobal("manifestHash", _proxyHashValue)

        # Prepare proxy info file
        templateFile = open ("./templates/template-info-v1.xml", 'rt', encoding = 'utf-8')
        testWriteFile = open("./apiproxy/"+context.__getattribute__("proxyName")+".xml",'w')
        template = simpleTAL.compileXMLTemplate (templateFile)
        template.expand(context, testWriteFile)
        templateFile.close()
        testWriteFile.close()
        print("SUCCESSS!!!!!!!!!!!!!!!!!")
