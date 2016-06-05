import sys
import feedparser

class Searches:
    
    feedURL = "http://www.google.com/trends/hottrends/atom/feed"

    def __init__(self):
        self.generateSearchesListfromXML(self.getxml())
        
    def getxml(self):
        if sys.version_info.major <= 2:
            import urllib2
            return urllib2.urlopen(Searches.feedURL).read()

        elif sys.version_info.major >= 3:
            import urllib.request
            return urllib.request.urlopen(Searches.feedURL).read()
            
    def generateSearchesListfromXML(self,xml):

        self.searchesList = []
        trendsRss = feedparser.parse(xml)
        for item in trendsRss[ "items" ]:
            self.searchesList.append(item["title"].replace(' ', '%20'))
            description = (item["description"]).split(", ")
            for subStr in description:
                if len(subStr) != 0:
                    self.searchesList.append(subStr.replace(' ', '%20'))
        return self.searchesList

    def getSearchesList(self):
        return self.searchesList