import socket
from urllib.parse import urlparse

from http_and_sockets.socket_wrapper import SocketWrapper

CRLF = '\r\n'


def get(raw_url):
    """
    TODO: document
    :param raw_url:
    :return:
    """
    parsed_url = urlparse(raw_url)

    path = '/' if parsed_url.path == '' else parsed_url.path

    full_path = path

    if parsed_url.query != '':
        full_path = path + '?' + parsed_url.query

    host = parsed_url.netloc
    port = 80

    request = ("GET {1} HTTP/1.1{0}"
               "Host: {2}{0}"
               "Connection: close{0}"
               "Accept-Encoding: gzip{0}"
               "Accept-Charset: ISO-8859-1,UTF-8;q=0.7,*;q=0.7{0}"
               "Cache-Control: no-cache{0}"
               "Accept-Language: en;q=0.7,en-us;q=0.3{0}{0}")\
        .format(CRLF, full_path, host)\
        .encode('utf-8')

    with SocketWrapper(socket.AF_INET, socket.SOCK_STREAM) as sw:
        sw.connect(host, port)
        sw.send(request)
        data = sw.receive()

    return data


def process_response(resp):
    """
    TODO: add doctest
    After getting the url, print the following:
    (a) the content type and response code
    (b) the number of headers in the response and
    (c) the number of lines in the body if the content type is text/html or text/plain.
    :param resp: response (bytearray)
    """
    resp_str = resp.decode('utf-8')
    header, *rest = resp_str.split(CRLF*2)

    # (a) Content type and response code
    content_type = _find_header_value('Content-Type: ', header)
    status_code = _find_header_value('HTTP/1.1 ', header)
    print("Content type: {0}".format(content_type))
    print("Status: {0}".format(status_code))

    # (b) the number of headers in the response
    num_headers = header.count(': ')
    print('Number of headers: {0}'.format(num_headers))

    # (c) the number of lines in the body if the content type is text/html or text/plain
    if 'text/' in content_type:
        body = rest[0]
        num_lines = body.count('\n')
        print('Number of lines in body: {0}'.format(num_lines))


def _find_header_value(header_key, header, ignore_semicolon=False):
    """
    TODO: document
    TODO: add doc tests
    :param header_key:
    :param header:
    :param ignore_semicolon:
    :return:
    """
    begin = header.find(header_key)

    assert begin != -1, 'Header must exist!'

    end_of_line = header.find(CRLF, begin)

    if ignore_semicolon:
        end = end_of_line
    else:
        semi_colon = header.find(';', begin, end_of_line)
        end = end_of_line if semi_colon == -1 else semi_colon

    return header[begin+len(header_key):end]


if __name__ == '__main__':

    resp = get("http://google.com")
    process_response(resp)