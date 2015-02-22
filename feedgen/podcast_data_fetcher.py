'''
Created on 08.02.2015

@author: Sebastian Gerhards
'''

import urllib2
from bs4 import BeautifulSoup

if __name__ == '__main__':
    pass

class PuppetLabsPodcastDataFetcher(object):
    
    def __init__(self, podcast_baseurl = 'http://puppetlabs.com', startpage_suffix='/resources/podcasts'):
        self.podcast_baseurl = podcast_baseurl
        self.url_suffix = startpage_suffix
        self.startpage_url = '%s%s' % (podcast_baseurl, startpage_suffix)

    def get_page_urls(self):
        urls = [self.startpage_url]
        html = urllib2.urlopen(self.startpage_url).read()
        soup = BeautifulSoup(html)
        page_items = soup.find_all('li', {'class':'pager-item'})
        for item in page_items:
            tag = item.find('a')
            attrs = tag.attrs
            href = attrs['href']
            audio_url = '%s%s' % (self.podcast_baseurl, href)
            urls.append(audio_url)
        return urls

    def get_podcast_urls(self):
        page_urls = self.get_page_urls()
        podcast_urls = []
        for page_url in page_urls:
            podcast_urls_on_page = self.get_podcast_urls_from_page(page_url)
            podcast_urls.extend(podcast_urls_on_page)
        return podcast_urls 

    def get_podcast_urls_from_page(self, page_url):
        urls = []
        f = urllib2.urlopen(page_url)
        html = f.read()
        soup = BeautifulSoup(html)
        tags = soup.find_all('a')
        for tag in tags:
            attrs = tag.attrs
            if attrs.has_key('href'):
                href = attrs['href']
                if href.startswith('/podcasts'):
                    audio_url = '%s%s' % (self.podcast_baseurl, href)
                    if audio_url not in urls:
                        urls.append(audio_url)
        return urls

    def get_podcast_data_from_podcast_page(self, page_url):
        data = {}
        f = urllib2.urlopen(page_url)
        html = f.read()
        soup = BeautifulSoup(html)
        title = soup.title.text
        data['title'] = title
        
        summary_div = soup.find('div', {'class':'field-type-text-with-summary'})
        summary_tags = summary_div.find_all('p')
        
        summary_texts = []
        for summary_tag in summary_tags:
            tag_text = summary_tag.text
            summary_texts.append(tag_text)
        summary = '\n'.join(summary_texts)
        data['summary'] = summary

        audio_tag = soup.find('audio')
        audio_url = audio_tag.attrs['src']
        data['audio_url'] = audio_url
        return data
