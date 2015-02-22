'''
Created on 08.02.2015

@author: Sebastian Gerhards

'''

if __name__ == '__main__':
    pass

from feedgen.feed import FeedGenerator
from podcast_data_fetcher import PuppetLabsPodcastDataFetcher

fg = FeedGenerator()
fg.load_extension('podcast')

fg.podcast.itunes_category('Technology', 'Podcasting')

fg.id('Puppetlabs Podcasts')
fg.title('Puppetlabs Podcasts')
fg.author({'name':'Sebastian Gerhards', 'email':'noreply@example.com'})
fg.link(href='http://puppetlabs.com/resources/podcasts', rel='alternate')
logo_url = 'http://puppetlabs.com/sites/default/files/puppet-labs-podcast-icon.png'
fg.logo(logo_url)
fg.subtitle('All Puppet Labs podcast')
fg.language('en')


f = PuppetLabsPodcastDataFetcher()
podcast_urls = f.get_podcast_urls()

for podcast_url in podcast_urls:
    podcast_data = f.get_podcast_data_from_podcast_page(podcast_url)
    fe = fg.add_entry()
    fe.id(podcast_url)
    title = podcast_data['title']
    fe.title(title)
    description = podcast_data['summary']
    fe.description(description)
    audio_url = podcast_data['audio_url']
    fe.enclosure(audio_url, 0, 'audio/mpeg')

fg.rss_str(pretty=True)
fg.rss_file('podcast.xml')
