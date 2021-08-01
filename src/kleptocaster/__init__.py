import xml.etree.ElementTree as ET
import glob
import argparse
import os
import sys
import hashlib
import mimetypes
from email.utils import formatdate
from urllib.parse import urljoin
from urllib.parse import quote


def create_item_element(file: str, date: float, base_url: str) -> ET.Element:
    item = ET.Element('item')
    ET.SubElement(item, 'title').text = os.path.splitext(os.path.basename(file))[0].replace("_", " ")
    ET.SubElement(item, 'pubDate').text = formatdate(date)
    guid = ET.SubElement(item, 'guid')
    guid.set('isPermaLink', 'false')
    guid.text = hashlib.sha256(file.encode()).hexdigest()
    enclosure = ET.SubElement(item, "enclosure")
    enclosure.set('length', '0')
    enclosure.set('type', mimetypes.guess_type(file)[0])
    enclosure.set('url', urljoin(base_url, quote(os.path.basename(file))))
    ET.SubElement(item, "description")
    return item


def create_document(base_url: str, feed: str, img: str, descr: str, latest: float, title: str) -> ET.Element:
    doc = ET.Element('rss')
    doc.set('version', '2.0')
    doc.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    doc.set('xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
    channel = ET.SubElement(doc, 'channel')
    atom = ET.SubElement(channel, 'atom:link')
    atom.set('href', f'{base_url}{feed}')
    atom.set('rel', 'self')
    atom.set('type', 'application/rss+xml')
    ET.SubElement(channel, 'title').text = title
    if img:
        ET.SubElement(channel, 'itunes:image').set('href', f'{base_url}{img}')
    ET.SubElement(channel, 'language').text = 'en'
    if descr:
        ET.SubElement(channel, 'description').text = descr
    ET.SubElement(channel, 'lastBuildDate').text = formatdate(latest)
    return doc


def create_feed(directory: str, output: str, image: str, description: str, base_url: str, extensions: list[str], title: str):
    files = [p for p in glob.glob(f'{directory}/*') if p.rsplit(".")[-1].lower() in extensions]
    if len(files) == 0:
        sys.exit(f'No files found in directory {directory}\nExtensions: {",".join(extensions)}')
    dates = {fname: os.path.getmtime(fname) for fname in files}
    sorted_by_date = sorted(dates, key=dates.get, reverse=True)
    doc = create_document(base_url, output, image, description, dates[sorted_by_date[0]], title)
    for w in sorted_by_date:
        doc.append(create_item_element(w, dates[w], base_url))

    with open(f'{directory}/{output}', 'wb') as f:
        f.write(ET.tostring(doc, xml_declaration=True, encoding='UTF-8'))


def run():
    class SplitArgs(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, values.split(','))

    parser = argparse.ArgumentParser(description='Turn directory into RSS feed.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--baseurl', help="Base URL of podcast.")
    parser.add_argument('--title', help="Title of podcast.")
    parser.add_argument('--description', help="Description of podcast.")
    parser.add_argument('--image', help="Image of podcast (put file into content directory)")
    parser.add_argument('--directory', default="./", help="Directory with media files.")
    parser.add_argument('--output', default="feed.xml", help="filename of rss file.")
    parser.add_argument('--extensions', default=["mp3", "mp4", "aac"], metavar="ext", action=SplitArgs, help="File extensions to include, comma separated.")
    args = parser.parse_args()
    create_feed(args.directory, args.output, args.image, args.description, args.baseurl, args.extensions, args.title)
