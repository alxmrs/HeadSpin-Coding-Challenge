### 2) HTTP and sockets.

Write a python program that inputs a full URL like
"http://www.url.com/path/a/b/c?p=1&p=2", sends the request, reads the
full response, and prints (a) the content type and response code (b)
the number of headers in the response and (c) the number of lines in
the body if the content type is text/html or text/plain. It's OK to
assume HTTP-only (no HTTPS).

The catch is: write this using only the `socket` library to
send/receive, and do not use any libraries for (a) crafting HTTP
requests and (b) processing HTTP responses — craft the request bytes
manually and process the response bytes manually. It's OK to use
`urlparse` to break down the input url.
