#!/usr/bin/env python3

import argparse
import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pathlib
import sys
import re

def image_selector(orig, type, soup, save_dir, extensions, level, dom):
    for img in soup.find_all(orig):
        src = img.get(type)
        if not src or len(src) == 0:
            continue
        if len(src.split(',')) > 1:
            for i in src.split(' '):
                if i.endswith(extensions):
                    download_image(i, save_dir)
        else:            
            parsed = urlparse(urljoin(dom, src.lstrip(' ')))
            src = urljoin(dom, parsed.path.lstrip(' '))
            if parsed.scheme not in\
                ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
                if parsed.scheme not in ('http', 'https', 'file'):
                    if src and any(src.endswith(ext) for ext in extensions) and requests.get('http://' + src).status_code == 200:
                        download_image('http://' + src, save_dir)
                    elif src and any(src.endswith(ext) for ext in extensions) and requests.get('https://' + src).status_code == 200:
                        download_image('https://' + src, save_dir)
                    elif src and any(src.endswith(ext) for ext in extensions) and requests.get('file://' + src).status_code == 200:
                        download_image('file://' + src, save_dir)
                elif parsed.scheme in ('http', 'https', 'file', ' http', ' https', ' file') and any(src.endswith(ext) for ext in extensions):
                    download_image(src, save_dir)
        # if src:
        #     ssrc = src.split(',')
        #     for i in ssrc:
        #         sss = i.split(' ')
        #         for s in sss:
        #             if s.endswith(extensions):
        #                 parsed = urlparse(urljoin(dom, s.lstrip(' ')))
        #                 src = urljoin(dom, parsed.path.lstrip(' '))
        #                 if parsed.scheme not in\
        #                     ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
        #                     if parsed.scheme not in ('http', 'https', 'file'):
        #                         if src and any(src.endswith(ext) for ext in extensions) and requests.get('http://' + src).status_code == 200:
        #                             download_image('http://' + src, save_dir)
        #                         elif src and any(src.endswith(ext) for ext in extensions) and requests.get('https://' + src).status_code == 200:
        #                             download_image('https://' + src, save_dir)
        #                         elif src and any(src.endswith(ext) for ext in extensions) and requests.get('file://' + src).status_code == 200:
        #                             download_image('file://' + src, save_dir)
        #                     elif parsed.scheme in ('http', 'https', 'file', ' http', ' https', ' file') and any(src.endswith(ext) for ext in extensions):
        #                         download_image(src, save_dir)
        sys.stdout.write('\r')
        sys.stdout.write("Level: [{}] --- Images Located: [{}]\r".format(level, _num_img))
        sys.stdout.flush()

def download_image(image_url, save_dir):
    global _num_img

    response = requests.get(image_url)
    if response.status_code == 200:
        filename = os.path.basename(urlparse(image_url).path)
        with open(os.path.join(save_dir, filename), 'wb') as f:
            f.write(response.content)
            _num_img += 1

def spider(url, recursive, level,save_dir, extensions, visited, dominio):
    if level < 0 or url in visited:
        return
    global _num_img
    visited.add(url)
    try:
        response = requests.head(url)
        if not "text/html" in response.headers['content-type']:
            return
        response = requests.get(url)
        if response.status_code != 200:
            print("ERROR WEB", url)
            return
    except:
        return
    if response.url != '#' and response.url != '':
        soup = BeautifulSoup(response.text, 'html.parser')
    dom = urlparse(response.request.url).scheme + "://" + urlparse(response.request.url).netloc
    image_selector('img', 'src', soup, save_dir, extensions, level, dom)
    image_selector('img', 'href', soup, save_dir, extensions, level, dom)
    image_selector('img', 'srcset', soup, save_dir, extensions, level, dom)
    image_selector('image', 'src', soup, save_dir, extensions, level, dom)
    image_selector('image', 'href', soup, save_dir, extensions, level, dom)
    image_selector('image', 'srcset', soup, save_dir, extensions, level, dom)
    image_selector('i', 'src', soup, save_dir, extensions, level, dom)
    image_selector('i', 'href', soup, save_dir, extensions, level, dom)
    image_selector('i', 'srcset', soup, save_dir, extensions, level, dom)
    for link in soup.find_all('div', style=True):
        stweb = link['style']
        ptr = re.search("http.*[)]", stweb)
        if ptr == None:
            continue
        url = stweb[ptr.start():ptr.end()-1]
        p = urlparse(url)
        upar = urljoin(dom, p.path)
        if upar.endswith(extensions):
            download_image(upar, save_dir)
    for link in soup.find_all('link', href= True):
        stweb = link['href']
        ptr = re.search("http.*", stweb)
        if ptr == None:
            continue
        url = stweb[ptr.start():ptr.end()]
        p = urlparse(url)
        upar = urljoin(dom, p.path)
        if upar.endswith(extensions):
            download_image(upar, save_dir)
    if recursive:
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href == '#' or href == '':
                continue
            if href and not href.startswith(('http://', 'https://')):
                href = urljoin(url, href)
            parsed = urlparse(href)
            if not parsed.netloc.endswith(dominio) or parsed.scheme in ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
                visited.add(urljoin(response.request.url, href))
                continue
            href = urljoin(response.request.url, href)
            if href not in visited and parsed.netloc.endswith(dominio):
                spider(href, recursive, level - 1, save_dir, extensions, visited, dominio)

    # print(visited)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descarga imágenes de un sitio web')
    parser.add_argument('url', help='URL del sitio web')
    parser.add_argument('-r', '--recursive', action='store_true', help='Descargar imágenes de forma recursiva')
    parser.add_argument('-l', '--level', type=int, default=5, help='Profundidad máxima de descarga recursiva')
    parser.add_argument('-p', '--path', default='./data/', help='Ruta donde se guardarán los archivos descargados')
    args = parser.parse_args()

    os.makedirs(args.path, exist_ok=True)

    extensions = ('jpg', 'jpeg', 'png', 'gif', 'bmp')
    visited = set()
    dominio = str(urlparse(args.url).netloc).lstrip("www.")
    global _num_img
    _num_img = 0
    lev = args.level
    spider(args.url, args.recursive, args.level, args.path, extensions, visited, dominio)
    downloaded = 0
    lst_down = []
    for path in pathlib.Path("./data").iterdir():
        if path.is_file():
            lst_down.append(path.name)
            downloaded += 1
    print()
    print()
    print("THE LIST OF IMAGES IS:")
    for el in lst_down:
        print(el)
    print()
    print("For level [{}], I located [{}], but without duplicates you have downloaded [{}] images".format(lev, _num_img, downloaded))