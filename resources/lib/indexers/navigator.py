# -*- coding: utf-8 -*-

'''
    stb.hu Addon
    Copyright (C) 2023 heg, vargalex

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os, sys, re, xbmc, xbmcgui, xbmcplugin, xbmcaddon, locale, base64
import requests
import urllib.parse
from resources.lib.modules.utils import py2_decode, py2_encode
import html
import resolveurl as urlresolver

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
addonFanart = xbmcaddon.Addon().getAddonInfo('fanart')

version = xbmcaddon.Addon().getAddonInfo('version')
kodi_version = xbmc.getInfoLabel('System.BuildVersion')

base_log_info = f'stb.hu | v{version} | Kodi: {kodi_version[:5]}'
xbmc.log(f'{base_log_info}', xbmc.LOGINFO)

base_url = 'https://www.stb.hu'

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.stb.hu',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

if sys.version_info[0] == 3:
    from xbmcvfs import translatePath
    from urllib.parse import urlparse, quote_plus, unquote_plus
else:
    from xbmc import translatePath
    from urlparse import urlparse
    from urllib import quote_plus

class navigator:
    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, "hu_HU.UTF-8")
        except:
            try:
                locale.setlocale(locale.LC_ALL, "")
            except:
                pass
        self.base_path = py2_decode(translatePath(xbmcaddon.Addon().getAddonInfo('profile')))

    def root(self, page_id_num):
        page_id_num = str(page_id_num) if page_id_num is not None else '0'
        if page_id_num == '0':
            page_id_num = 0
        else:
            page_id_num = int(page_id_num) + 1

        self.addDirectoryItem("LEGTÖBBSZÖR LETÖLTÖTT VIDEÓK", f"legtobbszor_items&page_id_num={page_id_num}", '', 'DefaultFolder.png')
        self.addDirectoryItem("Filmek & Sorozatok", f"items&page_id_num={page_id_num}", '', 'DefaultFolder.png')
        self.addDirectoryItem("Keresés", f"get_search_items&page_id_num={page_id_num}", '', 'DefaultFolder.png')
        
        self.endDirectory()


    def getLegtobbszorItems(self, page_link, page_id_num, image, title, source):
        import requests
        import re
    
        headers_0 = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.stb.hu',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        data_0 = {
            'page': '0',
        }
        
        resp_0 = requests.post('https://www.stb.hu/main/get_more_video_search', headers=headers_0, data=data_0).json()
        
        for stuffs in resp_0['data']['recently']:
        
            title = stuffs['title']
            id = int(stuffs['id'])
            source = stuffs['source']
            video_id = stuffs['video_id']
            image = f'https://{source}.stb.hu/{video_id}.jpg'
            page_link = f'https://www.stb.hu/{source}/{video_id}'
            
            self.addDirectoryItem(f'[B]{title} ({source})[/B]', f'ext_items&page_link={quote_plus(page_link)}&page_id_num={page_id_num}&image={image}&title={title}&source={source}', image, 'DefaultMovies.png', isFolder=True, meta={'title': f'{title}'})
        
        self.endDirectory('series')

    def getItems(self, page_link, page_id_num, image, title, source):
        page_id_num = str(page_id_num) if page_id_num is not None else '0'
        if page_id_num == '0':
            page_id_num = 0
        else:
            page_id_num = int(page_id_num)
    
        import requests
        import re
    
        headers_0 = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.stb.hu',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        data_0 = {
            'page': page_id_num + 1,
        }
        
        resp_0 = requests.post('https://www.stb.hu/main/get_more_video_search', headers=headers_0, data=data_0).json()
        
        for stuffs in resp_0['data']['recently']:
        
            title = stuffs['title']
            id = int(stuffs['id'])
            source = stuffs['source']
            video_id = stuffs['video_id']
            image = f'https://{source}.stb.hu/{video_id}.jpg'
            page_link = f'https://www.stb.hu/{source}/{video_id}'
            
            self.addDirectoryItem(f'[B]{title} ({source})[/B]', f'ext_items&page_link={quote_plus(page_link)}&page_id_num={page_id_num}&image={image}&title={title}&source={source}', image, 'DefaultMovies.png', isFolder=True, meta={'title': f'{title}'})
    
        try:
            page_id_num += 1
            self.addDirectoryItem('[I]Következő oldal[/I]', f'items&page_id_num={page_id_num}', '', 'DefaultFolder.png')
        except (AttributeError, IndexError):
            xbmc.log(f'{base_log_info}| getItems | next_page | csak egy oldal található', xbmc.LOGINFO)
        
        self.endDirectory('series')

    def getSearchItems(self, page_link, page_id_num, image, title, source, search_text):
        page_id_num = str(page_id_num) if page_id_num is not None else '0'
        if page_id_num == '0':
            page_id_num = 0
        else:
            page_id_num = int(page_id_num)

        if not search_text:
            keyb = xbmc.Keyboard('', u'Add meg a keresendő film címét')
            keyb.doModal()
            if keyb.isConfirmed():
                search_text = keyb.getText()
        
        import requests
        import re
    
        headers_0 = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.stb.hu',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        data_0 = {
            'page': page_id_num,
            'param': search_text,
        }
        
        resp_0 = requests.post('https://www.stb.hu/main/get_more_video_search', headers=headers_0, data=data_0).json()
        
        for stuffs in resp_0['data']['recently']:
            title = stuffs['title']
            id = int(stuffs['id'])
            source = stuffs['source']
            video_id = stuffs['video_id']
            image = f'https://{source}.stb.hu/{video_id}.jpg'
            page_link = f'https://www.stb.hu/{source}/{video_id}'
            
            self.addDirectoryItem(
                f'[B]{title} ({source})[/B]',
                f'ext_items&page_link={quote_plus(page_link)}&page_id_num={page_id_num}&image={image}&title={title}&source={source}&search_text={search_text}',
                image,
                'DefaultMovies.png',
                isFolder=True,
                meta={'title': f'{title}'}
            )
    
        try:
            page_id_num += 1
            self.addDirectoryItem(
                '[I]Következő oldal[/I]',
                f'get_search_items&page_link={quote_plus(page_link)}&page_id_num={page_id_num}&image={image}&title={title}&source={source}&search_text={search_text}',
                '',
                'DefaultFolder.png'
            )
        except (AttributeError, IndexError):
            xbmc.log(f'{base_log_info}| getItems | next_page | csak egy oldal található', xbmc.LOGINFO)
    
        self.endDirectory('series')

    def ExtrItems(self, iframe_link, page_id_num, image, title, source, page_link):
        import requests
        import re
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        
        response = requests.get(page_link, headers=headers).text
        
        iframe_link = re.findall(r'iframe.*player.*src=\"(.*?)\"', response)[0].strip()
        
        self.addDirectoryItem(f'[B]{title}[/B]', f'playmovie&iframe_link={quote_plus(iframe_link)}&page_id_num={page_id_num}&image={image}&title={title}&source={source}&page_link={page_link}', image, 'DefaultMovies.png', isFolder=False, meta={'title': f'{title}'})

        self.endDirectory('series')

    def playMovie(self, iframe_link):
        try:
            direct_url = urlresolver.resolve(iframe_link)
            
            xbmc.log(f'{base_log_info}| playMovie | direct_url: {direct_url}', xbmc.LOGINFO)
            play_item = xbmcgui.ListItem(path=direct_url)
            xbmcplugin.setResolvedUrl(syshandle, True, listitem=play_item)
        except:
            xbmc.log(f'{base_log_info}| playMovie | name: No video sources found', xbmc.LOGINFO)
            notification = xbmcgui.Dialog()
            notification.notification("stb.hu", "Törölt tartalom", time=5000)

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True, Fanart=None, meta=None, banner=None):
        url = f'{sysaddon}?action={query}' if isAction else query
        if thumb == '':
            thumb = icon
        cm = []
        if queue:
            cm.append((queueMenu, f'RunPlugin({sysaddon}?action=queueItem)'))
        if not context is None:
            cm.append((context[0].encode('utf-8'), f'RunPlugin({sysaddon}?action={context[1]})'))
        item = xbmcgui.ListItem(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb, 'poster': thumb, 'banner': banner})
        if Fanart is None:
            Fanart = addonFanart
        item.setProperty('Fanart_Image', Fanart)
        if not isFolder:
            item.setProperty('IsPlayable', 'true')
        if not meta is None:
            item.setInfo(type='Video', infoLabels=meta)
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, type='addons'):
        xbmcplugin.setContent(syshandle, type)
        xbmcplugin.endOfDirectory(syshandle, cacheToDisc=True)
