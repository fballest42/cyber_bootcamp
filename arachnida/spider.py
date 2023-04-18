#!/usr/bin/env python3

import argparse
import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def download_image(image_url, save_dir):
    response = requests.get(image_url)
    if response.status_code == 200:
        filename = os.path.basename(urlparse(image_url).path)
        with open(os.path.join(save_dir, filename), 'wb') as f:
            f.write(response.content)

def spider(url, recursive, level, save_dir, extensions, visited, dominio):
    if level < 0 or url in visited:
        return
    response = requests.get(url)
    if response.url != '#' and response.url != '':
        soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        parsed = urlparse(src)
        if parsed.netloc.endswith(dominio) and parsed.scheme not in\
            ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
            if parsed.scheme not in ('http', 'https', 'file'):
                print("HOLA2")
                if src and any(src.endswith(ext) for ext in extensions) and requests.get('http://' + src):
                    download_image('http://' + src, save_dir)
                    visited.add(url)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('https://' + src):
                    download_image('https://' + src, save_dir)
                    visited.add(url)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('file://' + src):
                    download_image('file://' + src, save_dir)
                    visited.add(url)
                else:
                    visited.add(url)
            elif parsed.scheme in ('http', 'https', 'file') and any(src.endswith(ext) for ext in extensions):
                download_image(src, save_dir)
                visited.add(url)
            else:
                visited.add(url)
        else:
            visited.add(url)
    for img in soup.find_all('image'):
        src = img.get('href')
        parsed = urlparse(src)
        if parsed.netloc.endswith(dominio) and parsed.scheme not in\
            ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
            if parsed.scheme not in ('http', 'https', 'file'):
                print("HOLA2")
                if src and any(src.endswith(ext) for ext in extensions) and requests.get('http://' + src):
                    download_image('http://' + src, save_dir)
                    visited.add(url)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('https://' + src):
                    download_image('https://' + src, save_dir)
                    visited.add(url)
                elif src and any(src.endswith(ext) for ext in extensions) and requests.get('file://' + src):
                    download_image('file://' + src, save_dir)
                    visited.add(url)
                else:
                    visited.add(url)
            elif parsed.scheme in ('http', 'https', 'file') and any(src.endswith(ext) for ext in extensions):
                download_image(src, save_dir)
                visited.add(url)
            else:
                visited.add(url)
        else:
            visited.add(url)    
    if recursive:
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href == '#' or href == '':
                continue
            if href and not href.startswith(('http://', 'https://')):
                href = urljoin(url, href)
            parsed = urlparse(href)
            if not parsed.netloc.endswith(dominio) or parsed.scheme in ('ftp', 'gopher', 'imap', 'mailto', 'mms', 'news', 'nntp', 'prospero', 'rsync', 'rtsp', 'rtspu', 'sftp', 'shttp', 'sip', 'sips', 'snews', 'svn', 'svn+ssh', 'telnet', 'wais', 'ws', 'wss'):
                continue
            print(parsed)
            if not parsed.scheme or parsed.scheme == '':
                # href = '{}://{}'.format(parsed.scheme or 'https', parsed.netloc) + parsed.path
                href = response.request.url + href
            if href not in visited: # and any(href.endswith(ext) for ext in extensions):
                spider(href, recursive, level - 1, save_dir, extensions, visited, dominio)           
    print(visited)

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
    spider(args.url, args.recursive, args.level, args.path, extensions, visited, dominio)
