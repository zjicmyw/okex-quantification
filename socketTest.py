import requests
import socket
import socks
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
socket.socket = socks.socksocket

#  pip3 install Pysocks

resp=requests.get("http://icanhazip.com/")
print(resp.text)
