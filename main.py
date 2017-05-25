import re
import requests
from HTMLParser import HTMLParser

###
# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
###


def wordFrequency(event, context):
    
    with requests.Session() as s:
        
        #make request =>
        # strip html and nonalphanumeric
        # convert all to lowercase
        # split into list

        print 'Requesting the page:', event['url']
        r = s.get(event['url'])
        _html = re.sub(r'([^\s\w]|_)+', '', strip_tags(r.content))
        wordList = _html.lower().split()
        uniqueWords = set(wordList)
        
        print len(wordList),'total words,', len(uniqueWords), 'unique.'

        payload = {
            'count': {
                'unique' : len(uniqueWords),
                'total' : len(wordList)},
            'words' : []}

        #count frequency of each unique word and append to payload['words'] array
        for word in uniqueWords:
            payload['words'].append({'word':word, 'count':wordList.count(word)})

        #done
        return payload
        
if __name__ == "__main__":
    pass

    
