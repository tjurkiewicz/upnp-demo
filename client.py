import signal
import socketserver
import miniupnpc

port = 1444

class RequestHandler(socketserver.BaseRequestHandler):
  """ Sends back reversed data """

  def handle(self):
    data = self.request.recv(1024).strip()
    ret_data = '{}\n'.format(data[::-1]).encode('utf-8')
    self.request.sendall(ret_data)
    print('Data handled: {}'.format(data))


def forward_port(signum, frame):
  print('Enable forwarding')
  external_port = internal_port = port

  upnp = miniupnpc.UPnP()
  upnp.discoverdelay = 20
  print (upnp.discover())

  upnp.selectigd()
  return upnp.addportmapping(external_port, 'TCP', upnp.lanaddr, internal_port, '', '')


if __name__ == '__main__':
  signal.signal(signal.SIGTERM, forward_port)

  server = socketserver.TCPServer(('0.0.0.0', port), RequestHandler)
  server.serve_forever()

