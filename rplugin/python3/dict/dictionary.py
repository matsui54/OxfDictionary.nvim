import requests
import json


class OxfordDict:
    base_url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.fields = 'definitions'
        self.strictMatch = 'false'
        self.language = 'en-gb'

    def get_definition(self, word_id):
        url = self.base_url + self.language + '/' + word_id.lower() + '?fields=' + self.fields + '&strictMatch=' + self.strictMatch;

        r = requests.get(url, headers = {'app_id': self.app_id, 'app_key': self.app_key})
        json_load=json.loads(r.text)

        jresults = json_load['results']
        cntdef = 1
        definitions = ''
        for jresult in jresults:
            jles = jresult['lexicalEntries']
            for jle in jles:
                ents = jle['entries']
                for ent in ents:
                    sens = ent['senses']
                    for sen in sens:
                        defns=sen['definitions']
                        for defn in defns:
                            definitions+=defn+'\n'
                            cntdef+=1

        return definitions.rstrip()
