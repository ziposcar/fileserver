#!/usr/bin/python 
# -*- coding: utf-8 -*-

__version__ = "0.6"

import os
import posixpath
import urllib
import urlparse
import cgi
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import shutil
import mimetypes

from app.config import current_config
from flask import render_template, jsonify

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


server_version = "SimpleHTTP/" + __version__


def do_GET():
    """Serve a GET request."""
    f = send_head()
    if f:
        try:
            copyfile(f, wfile)
        finally:
            f.close()


def do_HEAD():
    """Serve a HEAD request."""
    f = send_head()
    if f:
        f.close()


def send_head():
    """Common code for GET and HEAD commands.

    This sends the response code and MIME headers.

    Return value is either a file object (which has to be copied
    to the outputfile by the caller unless the command was HEAD,
    and must be closed by the caller under all circumstances), or
    None, in which case the caller has nothing further to do.

    """
    path = translate_path(path)
    f = None
    if os.path.isdir(path):
        parts = urlparse.urlsplit(path)
        if not parts.path.endswith('/'):
            # redirect browser - doing basically what apache does
            send_response(301)
            new_parts = (parts[0], parts[1], parts[2] + '/',
                         parts[3], parts[4])
            new_url = urlparse.urlunsplit(new_parts)
            send_header("Location", new_url)
            end_headers()
            return None
        for index in "index.html", "index.htm":
            index = os.path.join(path, index)
            if os.path.exists(index):
                path = index
                break
        else:
            return list_directory(path)
    ctype = guess_type(path)
    try:
        # Always read in binary mode. Opening files in text mode may cause
        # newline translations, making the actual size of the content
        # transmitted *less* than the content-length!
        f = open(path, 'rb')
    except IOError:
        send_error(404, "File not found")
        return None
    try:
        send_response(200)
        send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        send_header("Content-Length", str(fs[6]))
        send_header(
            "Last-Modified", date_time_string(fs.st_mtime))
        end_headers()
        return f
    except:
        f.close()
        raise


def list_directory(path):
    """Helper to produce a directory listing (absent index.html).

    Return value is either a file object, or None (indicating an
    error).  In either case, the headers are sent, making the
    interface the same as for send_head().

    """
    try:
        list = os.listdir(path)
    except os.error:
        return jsonify({'errno': 404, 'errmsg': "No permission to list directory: path: "+ path})
    list.sort(key=lambda a: a.lower())
    displaypath = cgi.escape(urllib.unquote(path))
    name_list = []
    for name in list:
        fullname = os.path.join(path, name)
        displayname = linkname = name
        # Append / for directories or @ for symbolic links
        if os.path.isdir(fullname):
            displayname = name + "/"
            linkname = name + "/"
        if os.path.islink(fullname):
            displayname = name + "@"
            # Note: a link to a directory displays with @ and links with /
        name_list.append((linkname, cgi.escape(displayname)))
    response = jsonify({'errno': 0, 'errmsg': '', 'data': {'displaypath': displaypath, 'name_list': name_list}})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def translate_path(path):
    """Translate a /-separated PATH to the local filename syntax.

    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)

    """
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    # Don't forget explicit trailing slash when normalizing. Issue17324
    trailing_slash = path.rstrip().endswith('/')
    path = posixpath.normpath(urllib.unquote(path))
    words = path.split('/')
    words = filter(None, words)
    path = current_config['static_folder']
    for word in words:
        if os.path.dirname(word) or word in (os.curdir, os.pardir):
            # Ignore components that are not a simple file/directory name
            continue
        path = os.path.join(path, word)
    if trailing_slash:
        path += '/'
    return path


def copyfile(source, outputfile):
    """Copy all data between two file objects.

    The SOURCE argument is a file object open for reading
    (or anything with a read() method) and the DESTINATION
    argument is a file object open for writing (or
    anything with a write() method).

    The only reason for overriding this would be to change
    the block size or perhaps to replace newlines by CRLF
    -- note however that this the default server uses this
    to copy binary data as well.

    """
    shutil.copyfileobj(source, outputfile)


def guess_type(path):
    """Guess the type of a file.

    Argument is a PATH (a filename).

    Return value is a string of the form type/subtype,
    usable for a MIME Content-type header.

    The default implementation looks the file's extension
    up in the table self.extensions_map, using application/octet-stream
    as a default; however it would be permissible (if
    slow) to look inside the data to make a better guess.

    """

    base, ext = posixpath.splitext(path)
    if ext in extensions_map:
        return extensions_map[ext]
    ext = ext.lower()
    if ext in extensions_map:
        return extensions_map[ext]
    else:
        return extensions_map['']


if not mimetypes.inited:
    mimetypes.init()  # try to read system mime.types
extensions_map = mimetypes.types_map.copy()
extensions_map.update({
    '': 'application/octet-stream',  # Default
    '.py': 'text/plain',
    '.c': 'text/plain',
    '.c++': 'text/plain',
    '.cc': 'text/plain',
    '.cpp': 'text/plain',
    '.hpp': 'text/plain',
    '.h': 'text/plain',
})
