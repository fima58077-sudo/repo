#!/usr/bin/env python3
"""Пересобирает Packages / Packages.gz / Packages.bz2 / Release для репозитория Sileo/Zebra.
Положи .deb в папку debs/ и запусти:  python3 build_repo.py
Нужен только Python 3, больше ничего."""
import os, io, gzip, bz2, hashlib, tarfile, lzma

HERE = os.path.dirname(os.path.abspath(__file__))
DEBS = os.path.join(HERE, "debs")

REPO_NAME = "Моя тема-репа"
REPO_DESC = "Темы для SnowBoard: Cats, Material You, iOS 26"

def read_control(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"!<arch>\n":
        raise ValueError("не deb: " + path)
    pos = 8
    while pos < len(data):
        name = data[pos:pos+16].decode().strip().rstrip("/")
        size = int(data[pos+48:pos+58].decode().strip())
        body = data[pos+60:pos+60+size]
        if name.startswith("control.tar"):
            if name.endswith(".gz"):
                tf = tarfile.open(fileobj=io.BytesIO(gzip.decompress(body)))
            elif name.endswith(".xz"):
                tf = tarfile.open(fileobj=io.BytesIO(lzma.decompress(body)))
            elif name.endswith(".bz2"):
                tf = tarfile.open(fileobj=io.BytesIO(bz2.decompress(body)))
            else:
                raise ValueError("формат " + name + " не поддерживается, собери deb с gzip/xz")
            for m in tf.getmembers():
                if m.name.lstrip("./") == "control":
                    return tf.extractfile(m).read().decode("utf-8").strip()
        pos += 60 + size + (size % 2)
    raise ValueError("нет control в " + path)

def hashes(b):
    return hashlib.md5(b).hexdigest(), hashlib.sha1(b).hexdigest(), hashlib.sha256(b).hexdigest()

entries = []
for fn in sorted(os.listdir(DEBS)):
    if not fn.endswith(".deb"):
        continue
    p = os.path.join(DEBS, fn)
    data = open(p, "rb").read()
    md5, sha1, sha256 = hashes(data)
    ctrl = read_control(p)
    ctrl += f"\nFilename: ./debs/{fn}\nSize: {len(data)}\nMD5sum: {md5}\nSHA1: {sha1}\nSHA256: {sha256}"
    entries.append(ctrl)

packages = ("\n\n".join(entries) + "\n").encode("utf-8")
open(os.path.join(HERE, "Packages"), "wb").write(packages)
open(os.path.join(HERE, "Packages.gz"), "wb").write(gzip.compress(packages, 9))
open(os.path.join(HERE, "Packages.bz2"), "wb").write(bz2.compress(packages, 9))

lines = []
for name in ("Packages", "Packages.gz", "Packages.bz2"):
    b = open(os.path.join(HERE, name), "rb").read()
    lines.append((name, len(b)) + hashes(b))

rel = [
    f"Origin: {REPO_NAME}",
    f"Label: {REPO_NAME}",
    "Suite: stable",
    "Version: 1.0",
    "Codename: ios",
    "Architectures: iphoneos-arm iphoneos-arm64",
    "Components: main",
    f"Description: {REPO_DESC}",
    "MD5Sum:",
] + [f" {md5} {size} {name}" for name, size, md5, sha1, sha256 in lines] + ["SHA1:"] + \
    [f" {sha1} {size} {name}" for name, size, md5, sha1, sha256 in lines] + ["SHA256:"] + \
    [f" {sha256} {size} {name}" for name, size, md5, sha1, sha256 in lines]
open(os.path.join(HERE, "Release"), "w", encoding="utf-8").write("\n".join(rel) + "\n")
print("Готово, пакетов:", len(entries))
