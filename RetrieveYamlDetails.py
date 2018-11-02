import json
import yaml
import jsonpath_rw_ext as jp

class FlowModule(object):
    def __init__(self,basePath=None,title=None):
        self.basePath = basePath
        self.title = title
        self.pathModules = []
        

class PathModule(object):
    def __init__(self,pathId=None,operationType=None,description=None,operationId=None):
        self.pathId = pathId
        self.operationType = operationType
        self.description = description
        self.operationId = operationId

  

class RetrieveYamlDetails():

    def readYamlData(self, file_):
        # yamlObj = yaml.load(open("Test.yaml").read())
        yamlObj = yaml.load(file_.stream)
        json_str = json.dumps(yamlObj)
        data = json.loads(json_str)
        return data

    def fetchYamlDetails(self,data):
        __basePath = data["basePath"]
        __title = jp.match('$..[title]',data).__getitem__(0)
        json_paths = data["paths"]
        __flowObj = FlowModule()
        __flowObj.__setattr__("basePath",__basePath)
        __flowObj.__setattr__("title",__title)

        # Create an Empty List
        pathModulesList=[]
        for __pathKey,__pathValue in json_paths.items():
                for __operationKey,__operationBody in __pathValue.items():
                    __pathObj= PathModule()
                    __pathObj.__setattr__("pathId",__pathKey)
                    __pathObj.__setattr__("operationType",__operationKey)
                    for __paramKey,__paramValue in __operationBody.items():
                        if __paramKey == 'description':
                            __pathObj.__setattr__("description",__paramValue)
                        elif __paramKey == 'operationId':
                            __pathObj.__setattr__("operationId",__paramValue)
                    pathModulesList.append(__pathObj)
        __flowObj.__setattr__("pathModules",pathModulesList)
        # return Flow Objects
        return __flowObj