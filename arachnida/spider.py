#!/usr/bin/env python3

import argparse
import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pathlib
import sys

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
    response = requests.get(url)
    if response.status_code != 200:
        print("ERROR WEB", url)
        return
    if response.url != '#' and response.url != '':
        soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        parsed = urlparse(src)
        if parsed.netloc.endswith(dominio) and parsed.scheme not in\
            ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
            if parsed.scheme not in ('http', 'https', 'file'):
                if src and any(src.endswith(ext) for ext in extensions) and requests.get('http://' + src):
                    download_image('http://' + src, save_dir)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('https://' + src):
                    download_image('https://' + src, save_dir)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('file://' + src):
                    download_image('file://' + src, save_dir)
            elif parsed.scheme in ('http', 'https', 'file') and any(src.endswith(ext) for ext in extensions):
                download_image(src, save_dir)
    for img in soup.find_all('image'):
        src = img.get('href')
        parsed = urlparse(src)
        if parsed.netloc.endswith(dominio) and parsed.scheme not in\
            ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
            if parsed.scheme not in ('http', 'https', 'file'):
                print("HOLA3")
                if src and any(src.endswith(ext) for ext in extensions) and requests.get('http://' + src):
                    download_image('http://' + src, save_dir)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('https://' + src):
                    download_image('https://' + src, save_dir)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('file://' + src):
                    download_image('file://' + src, save_dir)
            elif parsed.scheme in ('http', 'https', 'file') and any(src.endswith(ext) for ext in extensions):
                num_img = download_image(src, save_dir)
    sys.stdout.write('\r')
    sys.stdout.write("Level: [{}] --- Images Located: [{}]\r".format(level, _num_img))
    sys.stdout.flush()
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
                # href = '{}://{}'.format(parsed.scheme or 'https', parsed.netloc) + parsed.path
            href = urljoin(response.request.url, href)
            if href not in visited and parsed.netloc.endswith(dominio): # and any(href.endswith(ext) for ext in extensions):
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