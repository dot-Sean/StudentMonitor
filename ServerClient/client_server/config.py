from os.path import join, dirname


HOST = ''  # '' czyli wszystkie interfejsy

PORT = 23081

DOCUMENTS_PATH = join(dirname(__file__), 'SM_FILES')  # dla klienta

from web_app.config import DOCS_DIR
DOCUMENTS_DIRECTORY = DOCS_DIR  # dla serwera

COLLECTING_TIME = 5

RECONNECT_TIME = 60

EOF_MSG = "*****EOF*****"

XML_NAME = 'document.xml'

SCREENSHOT_NAME = 'screenshot.jpg'