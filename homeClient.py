

def pokeserver(socket, hostname, port, inputdict):
    # this function makes sure that the server can send info back
    port = int(port)
    server_address = (hostname, port)

    socket.sendto(str("poke").encode('utf-8'), server_address)
    pass






