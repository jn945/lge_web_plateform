def get_ip():
    import socket

    return socket.gethostbyname(socket.getfqdn())
