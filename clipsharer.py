import argparse
import logging
import socket
import threading
import time

import pyperclip
import sys


MAX_CLIPBOARD_SIZE = 8192

logger = logging.getLogger("clipsharer")
out = logging.StreamHandler(sys.stdout)
logger.addHandler(out)

mutex = threading.Lock()


class ReceiverThread(threading.Thread):
  def __init__(self, socket):
    self.socket = socket

  def run(self):
    while True:
      logger.debug("Waiting for clipboard on socket in recv.")
      new_clipboard = self.sock.recv(MAX_CLIPBOARD_SIZE)
      if (len(new_clipboard) == 0):
        self.socket.shutdown()
        return True
      mutex.acquire()
      logger.debug("Received clipboard from server: %s" % new_clipboard)
      pyperclip.copy(new_clipboard)
      mutex.release()


class SenderThread(threading.Thread):
  def __init__(self, sock):
    self.sock = sock

  def run(self):
    clipboard = ""
    while True:
      mutex.acquire()
      new_clipboard = pyperclip.paste()
      if new_clipboard != clipboard:
        logger.debug("Clibpard state changed. Sending to client. New "
                     "clipboard: %s" % new_clipboard)
        clipboard = new_clipboard
        mutex.release()
        self.sock.sendall(new_clipboard)
      else:
        mutex.release()
      time.sleep(0.1)


def run_server(hostname, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  logger.debug("Creating socket on hostname %s and port %d" % (
    hostname, port))
  sock.bind((hostname, port))
  sock.listen(5)
  while True:
    (clientsock, address) = sock.accept()
    logger.debug("Got new client")
    SenderThread(clientsock).run()
    ReceiverThread(clientsock).run()


def run_client(hostname, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((hostname, port))
  logger.debug("Connected to server")
  SenderThread(sock).run()
  ReceiverThread(sock).run()


def parse_arguments():
  parser = argparse.ArgumentParser(
    description='Application for sharing clipboard')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("-s", "--server", action="store_true", help="Run as server")
  group.add_argument("-c", "--client", action="store_true", help="Run as client")
  parser.add_argument('-d', "--debug", action='store_true', help="Run as debug")
  parser.add_argument("hostname")
  parser.add_argument("port", default=32872)
  return parser.parse_args()


if __name__ == '__main__':
  args = parse_arguments()
  if args.debug:
    logger.setLevel('DEBUG')
  else:
    logger.setLevel('INFO')
  if args.server:
    run_server(args.hostname, int(args.port))
  elif args.client:
    run_client(args.hostname, int(args.port))
  else:
    raise Exception()
