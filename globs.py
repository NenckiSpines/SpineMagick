from scipy import *
import sys, os
import ConfigParser

global config

version="spines023"
config = ConfigParser.ConfigParser()
pathname = os.path.dirname(sys.argv[0])
configpath=os.path.abspath(pathname)
config_name=configpath+'\\config.cfg'
config.read(config_name)
output_dir=str(config.get("other", "output_dir"))
xsize=int(config.get("window", "xsize"))
ysize=int(config.get("window", "ysize"))
try:
	renumbering=str(config.get("other", "numbering"))
except:
	renumbering="auto"
#ftp data
address='ftp.drivehq.com'
user_name="nuclei_statistics"
ftp_dir="PublicFolder"

class save_record:
  def __init__(self,section, option, value):
	global config
	config.set( section, option, value) 
	write_file=open(config_name, "w")
	config.write(write_file)
	write_file.close
