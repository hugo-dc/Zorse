import os

INSTALL_PATH = os.getcwd()

INSTALL_PATH = INSTALL_PATH.replace('\\\\', '/')
INSTALL_PATH = INSTALL_PATH.replace('\\', '/') + '/'

IMG_PATH = INSTALL_PATH + 'images/'

KEYWORDS_FILE = INSTALL_PATH + 'keywords.conf'
