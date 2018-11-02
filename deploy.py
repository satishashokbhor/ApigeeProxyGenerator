import base64
import http.client
import zipfile
import json

class DeployProxy(object):

    httpScheme = None
    httpHost = None

    def httpCall(self,verb, uri, headers, body,authorizationHeader):
        if self.httpScheme == 'https':
            conn = http.client.HTTPSConnection(self.httpHost)
        else:
            conn = http.client.HTTPConnection(self.httpHost)

        if headers == None:
            hdrs = dict()
        else:
            hdrs = headers

        hdrs['Authorization'] = authorizationHeader
        conn.request(verb, uri, body, hdrs)

        return conn.getresponse()


    def deployZiptoApigee(self, config , proxyName, authorizationHeader):

        # Configurations should be fetched from Config.ini
        ApigeeHost = config['DEFAULT']['APIGEE_HOST']
        Organization = config['DEFAULT']['ORGANIZATION']
        # Improvement to get the details from USER
        # USERPW = config['DEFAULT']['USERNAME']+":"+config['DEFAULT']['USERPASS']
        # encodedBytes = base64.b64encode(USERPW.encode('utf-8'))
        # authorizationHeader_ = encodedBytes.decode("utf-8")
        # I thought environment is required.. Its bummer ;-)
        # Environment = config['DEFAULT']['ENVIRONMENT']
        # Improvement : need to get schema and host dynamicaly
        self.httpScheme = 'https'
        self.httpHost = ApigeeHost

        # Upload the bundle to the API
        hdrs = {'Content-Type': 'application/octet-stream',
                'Accept': 'application/json'}
        uri = '/v1/organizations/%s/apis?action=import&name=%s' % \
                    (Organization, proxyName)
        resp = self.httpCall('POST', uri, hdrs,open('apiproxy.zip','rb'),authorizationHeader)

        if resp.status != 200 and resp.status != 201:
            print ('Import failed to %s with status %i:\n%s' % \
                    (uri, resp.status, resp.read()))

        deployment = json.load(resp)
        revision = int(deployment['revision'])

        print ('Imported new proxy version %i' % revision)


