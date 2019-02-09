from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys
from libinternetotv import InternetoTV
from functools import partial
import logging
import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('itv')


class RequestHandler(BaseHTTPRequestHandler):

  encoding = 'utf-8'

  cookie = ''

  def __init__(self, itv, *args, **kwargs):
    self.itv = itv
    super().__init__(*args, **kwargs)

  def do_GET(self):
    if self.path == '/itv.m3u':
      self.render_playlist()
    else:
      self.channel_url()
  
  def render_playlist(self):
      channels = self.itv.getChannels()
      host = self.headers.get('Host')
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b'#EXTM3U')
      for channel in channels:
        id = channel['id']
        title = channel['title']
        icon = channel['icon']
        self.wfile.write(bytes('#EXTINF:0 tvg-name="{}" tvg-logo="{}", {}\n'.format(id, icon, title), self.encoding))
        self.wfile.write(bytes('http://{}/{}\n'.format(host, id), self.encoding))
      
  def channel_url(self):
    url = ''
    for i in range(3):
      try:
        url = self.get_channel_url()
        break
      except Exception as e:
        logger.error('remote request failed', e)
        pass
    if url != '':
      self.send_response(301)
      self.send_header("Location", url)
      self.end_headers()
    else:
      self.send_response(500)

  def get_channel_url(self):
    self.check_itv_cookie()
    channel_id = self.path.replace('/', '')
    print(channel_id)
    urls = self.itv.getChannelUrls(channel_id)
    if 'login_failed' in urls:
      logger.debug('login failed, dropping cookie')
      self.cookie = ''
      self.check_itv_cookie()
      urls = self.itv.getChannelUrls(url)
    return urls['mp4_hls']

  def check_itv_cookie(self):
    if self.cookie == '':
      self.cookie = self.itv.getCookie()
    self.itv.setCookie(self.cookie);


itv = InternetoTV()
itv.setCredential(config.EMAIL, config.PASSWORD)
handler = partial(RequestHandler, itv)
httpd = HTTPServer((config.LISTEN, config.PORT), handler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
