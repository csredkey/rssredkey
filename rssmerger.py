#!/usr/bin/python
import os
from dotenv import load_dotenv
import feedparser
import time
from feedgen.feed import FeedGenerator
sources = [
  'http://www.veracode.com/blog/feed/',
  'https://www.webroot.com/blog/feed/',
  'http://researchcenter.paloaltonetworks.com/unit42/feed/',
  'http://feeds.trendmicro.com/TrendMicroSimplySecurity',
  'https://www.sentinelone.com/labs/feed/',
  'https://blog.qualys.com/feed',
  'https://msrc-blog.microsoft.com/feed/',
  'https://www.microsoft.com/security/blog/feed/',
  'http://feeds.feedburner.com/fortinet/blog/threat-research',
  'https://www.crowdstrike.com/blog/category/threat-intel-research/',
  'https://blog.cloudflare.com/tag/security/rss',
  'https://research.checkpoint.com/feed/',
  'https://www.wired.com/feed/category/security/latest/rss',
  'https://www.techrepublic.com/rssfeeds/white-papers/',
  'https://www.techrepublic.com/rssfeeds/topic/cloud-security/',
  'https://www.techrepublic.com/rssfeeds/topic/artificial-intelligence/',
  'https://www.techrepublic.com/rssfeeds/topic/cybersecurity/',
  'https://www.techrepublic.com/rssfeeds/topic/startups/',
  'https://www.schneier.com/blog/atom.xml',
  'http://krebsonsecurity.com/feed/',
  'https://www.hackmageddon.com/feed/',
  'https://www.bleepingcomputer.com/feed',
  'https://arstechnica.com/tag/security/feed/',
  'https://www.nist.gov/blogs/cybersecurity-insights/rss.xml',
  'https://isc.sans.edu/rssfeed_full.xml',
  'https://us-cert.cisa.gov/ncas/analysis-reports.xml',
  'https://us-cert.cisa.gov/ncas/current-activity.xml',
  'http://www.darknet.org.uk/feed/',
  'https://medium.com/feed/@sebdraven',
  'https://www.bsi.bund.de/SiteGlobals/Functions/RSSFeed/RSSNewsfeed/RSSNewsfeed.xml',
  'https://www.enisa.europa.eu/resolveuid/db2b76c88ed899fa6686a5a4a16d7ef5/RSS',
  'https://www.enisa.europa.eu/resolveuid/67ae856777742cbaffa839d438e0b59f/RSS',
  'https://www.itgovernance.co.uk/blog/category/data-protection/feed',
  'https://formiti.com/blog/feed/',
  'https://privacyinternational.org/rss.xml'
]

fullList = []
for url in sources:
  feed = feedparser.parse(url)
  for item in feed['items']:
    fullList.append(item)

fullList.sort(key=lambda item: item['updated_parsed'], reverse=True)
outList = fullList [0:500]

load_dotenv()
name = os.getenv('NAME')
email = os.getenv('EMAIL')

fg = FeedGenerator()
fg.id('https://redkey.tech/allthethings')
fg.title('RedKey RSS Feed')
fg.subtitle('All The Cyber Things.')
fg.author( {'name':'{name}', 'email':'{email}'} )
fg.link( href='https://redkey.tech/',rel='alternate' )
fg.link( href='https://redkey.tech/feed.xml', rel='self' )
fg.language('en')

for item in outList:
  fe = fg.add_entry(order='append')
  fe.id(item['id'])
  fe.title(item['title'])
  fe.link(href=item['link'])
  if('updated' in item):
    fe.updated(item['updated'])
  # add author if present in original
  if('author' in item):
    fe.author(name=item['author'])
  if('summary' in item):
    # If the summary contains HTML code, set its type.
    summary_type = 'html' if '<' in item['summary'] else None
    fe.summary(summary=item['summary'], type=summary_type)
  if 'tags' in item:
    for tag in item.tags:
      fe.category(term=tag.term)
  if 'content' in item:
    for content in item.content:
      fe.content(content=content.value, type='html')

fg.rss_str(pretty=True)
fg.rss_file('feed.xml')