import socket
import select
from urllib.parse import urlparse

# socket.setdefaulttimeout(0.5)

CRLF = '\r\n'

BUFSIZE = 2048


## TODO Create socket class with `with` syntax
## https://stackoverflow.com/questions/3774328/implementing-use-of-with-object-as-f-in-custom-class-in-python


def send(soc, msg: bytes):
    msg_len = len(msg)
    total_sent = 0
    while total_sent < msg_len:
        sent = soc.send(msg[total_sent:])
        if sent == 0:
            raise RuntimeError('Socket connection broken.')
        total_sent += sent


def receive(soc):

    rlist, _, _ = select.select([soc], [], [])

    for s in rlist:

        chunks = []

        while True:
            chunk = s.recv(BUFSIZE)

            if chunk == b'':
                break

            chunks.append(chunk)

        return b''.join(chunks)

    return b''


def get(raw_url: str):
    """
    :param raw_url:
    :return:
    """
    url = urlparse(raw_url)

    path = '/' if url.path == '' else url.path

    full_path = path

    if url.query != '':
        full_path = path + '?' + url.query

    host = url.netloc
    port = 80

    request = ("GET {1} HTTP/1.1{0}"
               "Host: {2}{0}"
               "Connection: close{0}"
               "Accept-Encoding: gzip{0}"
               "Accept-Charset: ISO-8859-1,UTF-8;q=0.7,*;q=0.7{0}"
               "Cache-Control: no-cache{0}"
               "Accept-Language: en;q=0.7,en-us;q=0.3{0}{0}") \
                .format(CRLF, full_path, host)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:

        soc.settimeout(0.3)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        soc.connect((host, port))

        send(soc, request.encode('utf-8'))
        soc.shutdown(1)
        data = receive(soc)

    return data


def process_response(resp: bytes):
    """
    After getting the url, print the following:
    (a) the content type and response code
    (b) the number of headers in the response and
    (c) the number of lines in the body if the content type is text/html or text/plain.
    :param resp: response (bytearray)
    """
    resp_str = resp.decode('utf-8')
    header, *rest = resp_str.split(CRLF*2)

    # (a) Content type and response code
    content_type = find_header_value('Content-Type: ', header)
    status_code = find_header_value('HTTP/1.1 ', header)
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


def find_header_value(header_key, header, ignore_semicolon=False):
    begin = header.find(header_key)

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