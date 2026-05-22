#!/usr/bin/env python3
import sys
import zipfile
import os
import xml.etree.ElementTree as ET

OPF_NS = "http://www.idpf.org/2007/opf"
CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"


def find_cover(epub_path):
    with zipfile.ZipFile(epub_path, "r") as z:
        container = z.read("META-INF/container.xml")
        root = ET.fromstring(container)
        opf_path = root.find(
            f".//{{{CONTAINER_NS}}}rootfile"
        ).get("full-path")
        opf_dir = os.path.dirname(opf_path)

        opf_root = ET.fromstring(z.read(opf_path))

        cover_id = None
        for meta in opf_root.iter(f"{{{OPF_NS}}}meta"):
            if meta.get("name") == "cover":
                cover_id = meta.get("content")
                break

        cover_href = None
        for item in opf_root.iter(f"{{{OPF_NS}}}item"):
            media = item.get("media-type", "")
            if "image" not in media:
                continue
            props = item.get("properties", "")
            item_id = item.get("id", "")
            if "cover-image" in props:
                cover_href = item.get("href")
                break
            if cover_id and item_id == cover_id:
                cover_href = item.get("href")
                break
            if item_id in ("cover", "cover-image", "cover_image"):
                cover_href = item.get("href")

        if not cover_href:
            return None

        cover_path = os.path.normpath(
            (opf_dir + "/" + cover_href) if opf_dir else cover_href
        )
        return z.read(cover_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    try:
        data = find_cover(sys.argv[1])
        if data:
            sys.stdout.buffer.write(data)
        else:
            sys.exit(1)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
