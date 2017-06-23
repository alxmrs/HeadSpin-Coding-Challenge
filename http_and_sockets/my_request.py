import socket
from urllib.parse import urlparse

from http_and_sockets.socket_wrapper import SocketWrapper

CRLF = '\r\n'


def GET(url):
    """
    Makes a GET request.
    Parses the input URL, formats it into a HTTP request, sends it via socket, then receives and returns the response.
    :param url: string, a URL
    :return: bytearray, the response from the request
    """
    parsed_url = urlparse(url)

    path = '/' if parsed_url.path == '' else parsed_url.path

    full_path = path

    if parsed_url.query != '':
        full_path = path + '?' + parsed_url.query

    host = parsed_url.netloc
    port = 80

    request = ('GET {1} HTTP/1.1{0}'
               'Host: {2}{0}'
               'Connection: close{0}'
               'Accept-Encoding: application/xml,application/xhtml+xml,text/html;q=0.9,'
               ' text/plain;q=0.8,image/png,*/*;q=0.5{0}'
               'Accept-Charset: ISO-8859-1,UTF-8;q=0.7,*;q=0.7{0}'
               'Cache-Control: no-cache{0}'
               'Accept-Language: en;q=0.7,en-us;q=0.3{0}{0}')\
        .format(CRLF, full_path, host)\
        .encode('utf-8')

    with SocketWrapper(socket.AF_INET, socket.SOCK_STREAM, timeout=1) as sw:
        sw.connect(host, port)
        sw.send(request)
        data = sw.receive()

    return data


def process_response(resp):
    """
    After getting the url, print the following:
    (a) the content type and response code
    (b) the number of headers in the response and
    (c) the number of lines in the body if the content type is text/html or text/plain.
    :param resp: bytearray, response
    """
    resp_str = resp.decode('utf-8')
    header, *rest = resp_str.split(CRLF*2)

    # (a) Content type and response code
    content_type = _find_header_value('Content-Type: ', header)
    status_code = _find_header_value('HTTP/1.1 ', header)
    print('Content type: {0}'.format(content_type))
    print('Status: {0}'.format(status_code))

    # (b) the number of headers in the response
    num_headers = header.count(': ')
    print('Number of headers: {0}'.format(num_headers))

    # (c) the number of lines in the body if the content type is text/html or text/plain
    if 'text/' in content_type:
        body = rest[0]
        num_lines = body.count('\n')
        num_lines += 1  # account for last line
        print('Number of lines in body: {0}'.format(num_lines))


def _find_header_value(header, header_section, ignore_semicolon=False):
    """
    Finds the value associated with a header in a HTTP response.
    Throws an `AssertionError` if the header is not found in the response header section.
    Optionally can return the value before hitting a semicolon instead of the end of the line.
    :param header: string, header "key" to find associated value
    :param header_section: string, all the text of the header section
    :param ignore_semicolon: boolean (optional) will stop if it reaches a semicolon
    :return: string, associated value of the header.
    """
    begin = header_section.find(header)

    assert begin != -1, 'Header must exist.'

    end_of_line = header_section.find(CRLF, begin)

    if ignore_semicolon:
        end = end_of_line
    else:
        semi_colon = header_section.find(';', begin, end_of_line)
        end = end_of_line if semi_colon == -1 else semi_colon

    return header_section[begin + len(header):end]


if __name__ == '__main__':
    resp = GET('http://www.google.com/search?q=HeadSpin')
    process_response(resp)
