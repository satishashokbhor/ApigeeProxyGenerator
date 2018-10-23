import freemarkerinterpreter
import HashGenerator
import RetrieveYamlDetails
import PrepareProxyZip

class YamlToProxyConverter:

    # Start reading YAML and get Details
    __yamlData = RetrieveYamlDetails.RetrieveYamlDetails()
    __data = __yamlData.readYamlData()
    __flowObj = __yamlData.fetchYamlDetails(__data)

    # Start preparing hash signature for policy files
    __objecthashgenerator = HashGenerator.hashgenerator()
    policyList = __objecthashgenerator.preparePolicyHash()
    print("Hash generated successfully----")
    
    # Start preparing Template
    __templateObject = freemarkerinterpreter.FreeMarkerWithSimpleTal()

    __config__obj__ = __templateObject.initializeConfig()

    __context = __templateObject.initializeFreeMarkerContext(__config__obj__,__flowObj,policyList)

    __templateObject.prepareProxyArtifacts(__context)
    
    print("Done Preparing Template.....")

    # Create Zip from Apigee Proxy
    __prepareProxyZip = PrepareProxyZip.PrepareProxyZip()
    __prepareProxyZip.prepareZipFile()

    print("Done.preparing Zip file....")