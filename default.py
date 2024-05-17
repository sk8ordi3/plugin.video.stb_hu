# -*- coding: utf-8 -*-

'''
    stb.hu Add-on
    Copyright (C) 2020 heg, vargalex

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
import sys
from resources.lib.indexers import navigator

if sys.version_info[0] == 3:
    from urllib.parse import parse_qsl
else:
    from urlparse import parse_qsl

params = dict(parse_qsl(sys.argv[2].replace('?', '')))

action = params.get('action')
url = params.get('url')

page_link = params.get('page_link')
page_id_num = params.get('page_id_num')
image = params.get('image')
title = params.get('title')
iframe_link = params.get('iframe_link')
source = params.get('source')
search_text = params.get('search_text')

if action is None:
    navigator.navigator().root(page_id_num)

elif action == 'legtobbszor_items':
    navigator.navigator().getLegtobbszorItems(page_link, page_id_num, image, title, source)

elif action == 'items':
    navigator.navigator().getItems(page_link, page_id_num, image, title, source)

elif action == 'get_search_items':
    navigator.navigator().getSearchItems(page_link, page_id_num, image, title, source, search_text)

elif action == 'ext_items':
    navigator.navigator().ExtrItems(iframe_link, page_id_num, image, title, source, page_link)

elif action == 'playmovie':
    navigator.navigator().playMovie(iframe_link)