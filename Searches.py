import sys
import feedparser
import random
import extraSearchesList

class Searches:
    
    feedURL = "http://www.google.com/trends/hottrends/atom/feed"

    def __init__(self, requiredNumSearches):
        self.requiredNumSearches = requiredNumSearches
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
            searchTerm = item["title"].replace(' ', '%20').encode("utf-8")
            if sys.version_info[0] >= 3:
                self.searchesList.append(str(searchTerm, 'utf-8'))    
            else:
                self.searchesList.append(str(searchTerm))
            description = (item["description"]).split(", ")
            for subStr in description:
                if len(subStr) != 0:
                    self.searchesList.append(subStr.replace(' ', '%20'))
                    
        if len(self.searchesList) < self.requiredNumSearches:
            extraSearches = extraSearchesList.additionalList
            random.shuffle(extraSearches)
            searchesToAdd = self.requiredNumSearches - len(self.searchesList)
            
            for additionalSearch in range(searchesToAdd+1):
                self.searchesList.append(extraSearches[additionalSearch])
            
        random.shuffle(self.searchesList)
        return self.searchesList

    def getSearchesList(self):
        return self.searchesList