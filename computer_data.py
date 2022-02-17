import getpass
import os
import globs
from netbios import *
from uuid import getnode as get_mac
import socket

class computer_data:
  def __init__(self):
    address= str(hex(get_mac()))
    address=address+":"
    self.address=address
    self.user=getpass.getuser()
    self.processor=os.getenv("PROCESSOR_IDENTIFIER")
    self.configpath=globs.configpath
    self.ip=socket.gethostbyname(socket.gethostname())
    s_identifier=self.user[:-3]+self.processor[:3]+self.configpath[-15:][:3]
    n_identifier=s_identifier.encode("hex")
    self.identifier=int(str(int(n_identifier,16))[:10])
#print (computer_data()).identifier
#print (computer_data()).configpath[-15:]
#print os.path.splitext((computer_data()).configpath)
