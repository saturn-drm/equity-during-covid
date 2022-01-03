import requests
import bs4
import csv
import time

class Analyzation():

    def __init__(self, baseurl, suffix):
        self.url = baseurl + suffix

    def get_soup(self, proxies, headers):
        res = requests.get(self.url, proxies=proxies, headers=headers)
        res.raise_for_status()
        res.encoding = 'utf-8'
        self.soup = bs4.BeautifulSoup(res.text, 'lxml')

    def find_tag(self, tagName, attr, attrname):
        head = self.soup.find(tagName, {attr: attrname})
        next = head.nextSibling.nextSibling
        tagList = []
        while next.name != tagName:
            tagList.append(next.text)
            next = next.nextSibling.nextSibling
        return tagList

    def find_all_tag(self, tagName, attr, attrname, target):
        cities = self.soup.findAll(tagName, {attr: attrname})
        sites = {}
        for city in cities:
            cityList = []
            next = city.nextSibling.nextSibling
            if target == 'li':
                while next != None and next.name != tagName:
                    cityList.append(next.li.text)
                    next = next.nextSibling.nextSibling
            else:
                while True:
                    try:
                        next.name
                    except:
                        break
                    if next.name != tagName:
                        if next.text != '':
                            cityList.append(next.text)
                    else:
                        break
                    next = next.nextSibling.nextSibling
            sites[city.text] = cityList
        return sites

if __name__ == '__main__':
    proxies = {
        'https': 'https://127.0.0.1:58591',
        'http': 'http://127.0.0.1:58591'
    }
    headers = {
        'Referer': 'https://www.nychealthandhospitals.org/wp-content/themes/hhc/images/fb.png',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
    }

    baseurl = 'https://www.nychealthandhospitals.org/'
    suffixList = ['covid-19-testing-sites/', 'hospitals/', 'diagnostic-treatment-centers/', 'community-healthcare-centers/', 'long-term-care-facilities/']

    print('retrieving data from %s' % suffixList[0])
    testing_instance = Analyzation(baseurl, suffixList[0])
    print('getting soup')
    testing_instance.get_soup(None, headers)
    testingList = ['mobile', 'self', 'rapid']
    testingDict = {}
    print('searching tags')
    for testing in testingList:
        siteList = testing_instance.find_tag('h4', 'id', testing)
        testingDict[testing] = siteList
    print('writing files')
    with open('datas/05-physical/covid-19-testing-sites.csv', 'w') as f:
        w = csv.DictWriter(f, testingDict.keys())
        w.writeheader()
        w.writerow(testingDict)
    print('sleeping')
    time.sleep(3)

    for i in range(1, len(suffixList)):
        print('retrieving data from %s' % suffixList[i])
        instance = Analyzation(baseurl, suffixList[i])
        print('getting soup')
        instance.get_soup(None, headers)
        print('searching tags')
        if i != 3:
            sitesDict = instance.find_all_tag('h3', 'class', 'title-city', 'li')
        else:
            sitesDict = instance.find_all_tag('h3', 'class', 'title-city', 'p')
        print('writing files')
        with open('datas/05-physical/%s.csv' % suffixList[i].split('/')[0], 'w') as f:
            w = csv.DictWriter(f, sitesDict.keys())
            w.writeheader()
            w.writerow(sitesDict)
        print('sleeping')
        time.sleep(3)