#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, logging, logging.handlers

# loggging config
log_path        = "./log";
log_file        = "%s.log" % sys.argv[0]
format_str      = "[%(asctime)s %(levelname)-8s][%(module)s] %(message)s"
logging.basicConfig(level=logging.INFO,format=format_str);
filename= "%s/%s" % ( log_path, log_file );
handler = logging.handlers.RotatingFileHandler( filename, 'a', 1024*1024*10, 5 );
formatter = logging.Formatter ( format_str );
handler.setFormatter(formatter);
logging.getLogger().addHandler(handler)

