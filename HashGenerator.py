import hashlib
import configparser
import ast

config = configparser.ConfigParser()
config.read('config.ini')

class policyhashObjects():
        def __init__(self,policyName=None,policyHash=None):
            self.policyName = policyName
            self.policyHash = policyHash

class hashgenerator():

    def calculatehashfromfile(self, fileName):
        hasher = hashlib.sha512()
        BLOCKSIZE = 65536
        # with open('./templates/policies/AM-Invalid_Request.xml', 'rb') as afile:
        with open(fileName, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

    def preparePolicyHash(self):
        __list__policy__names = ast.literal_eval(config.get("DEFAULT", "POLICY_FILES"))
        listPolicyHashObjects = []
        for policyName in __list__policy__names:
            __hash__value = self.calculatehashfromfile("./templates/policies/"+policyName)
            __hash__value = "SHA-512:"+__hash__value
            listPolicyHashObjects.append(policyhashObjects(policyName,__hash__value))
            # print(policyName,"-->"+__hash__value)
        return listPolicyHashObjects