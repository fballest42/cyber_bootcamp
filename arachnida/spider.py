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

def spider(url, recursive, level, save_dir, extensions, visited):
    if level <= 0 or url in visited:
        return
    visited.add(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and any(src.endswith(ext) for ext in extensions):
            download_image(src, save_dir)
    if recursive:
        for link in soup.find_all('a', href=True):
            # print(link)
            href = link.get('href')
            # print(href)
            if href and not href.startswith(('http://', 'https://')):
                href = urljoin(url, href)
            parsed = urlparse(href)
            if not parsed.scheme:
                href = '{}://{}'.format(parsed.scheme or 'http', parsed.netloc) + parsed.path
            if href not in visited and any(href.endswith(ext) for ext in extensions):
                spider(href, recursive, level - 1, save_dir, extensions, visited)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descarga imágenes de un sitio web')
    parser.add_argument('url', help='URL del sitio web')
    parser.add_argument('-r', '--recursive', action='store_true', help='Descargar imágenes de forma recursiva')
    parser.add_argument('-l', '--level', type=int, default=5, help='Profundidad máxima de descarga recursiva')
    parser.add_argument('-p', '--path', default='./data/', help='Ruta donde se guardarán los archivos descargados')
    args = parser.parse_args()

    os.makedirs(args.path, exist_ok=True)

    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    visited = set()
    spider(args.url, args.recursive, args.level, args.path, extensions, visited)
