
import os
import sys

# GET THE BASE DIRECTORY FOR THE APP
basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir", basedir)
def create_folder_if_not_exist(base_folder=basedir, folder=None):
    if folder is None:
        raise ValueError("We need a folder")
    if not os.path.exists(os.path.join(base_folder, folder)):
        # TODO: validate if exists but is a file
        #  with the same name or
        #  if we have privileges to
        #  write/read in the project dolder
        try:
            os.makedirs(os.path.join(base_folder, folder))
            return  True
        except OSError as error:
            return f"Unable to create Logs Folder:\n Error {str(error)}"


class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # TODO
    #  comment this lines on production
    #  Change MESSAGING NUNO MOURA FOR OTHER NAME
    TWILLIO_SID = os.environ.get('TWILLIO_SID')
    TWILLIO_TOKEN = os.environ.get('TWILLIO_TOKEN')

    MESSAGING_NM = os.environ.get('MESSAGING_NM')
    MESSAGING_HORTASNAVARANDA = os.environ.get('MESSAGING_HORTASNAVARANDA')



    # TODO: uncomment this lines in production
    # MESSAGING_NUNOMOURA = os.environ.get('MESSAGING_NUNOMOURA') or None
    # if MESSAGING_NUNOMOURA is None:
    #    raise EnvironmentError("'MESSAGING_NUNOMOURA' environment variable not Found. Check the docks and configure it")

    # TWILLIO_SID = os.environ.get('TWILLIO_SID') or None
    # if TWILLIO_SID is None:
    #    raise EnvironmentError("'TWILLIO_SID' environment variable not Found. Check the docks and configure it")

    # TWILLIO_TOKEN = os.environ.get('TWILLIO_TOKEN') or None
    # if TWILLIO_TOKEN is None:
    #    raise EnvironmentError("'TWILLIO_TOKEN' environment variable not Found. Check the docks and configure it")

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    TEMPLATE_FOLDER = "MessageTemplates"
    # check if folder exists adn create it
    try:
        create_folder_if_not_exist(base_folder=basedir, folder=TEMPLATE_FOLDER)
    except ValueError as error:
        sys.exit(error)
    #TEMPLATE_FOLDER = os.path.join(ROOT_DIR, TEMPLATE_FOLDER)

    LOG_FILE = "TwilioLog.log"
    LOG_FOLDER = "Logs"
    # check if folder exists adn create it
    try:
        create_folder_if_not_exist(base_folder=basedir, folder=LOG_FOLDER)
    except ValueError as error:
        sys.exit(error)

    LOG_FOLDER = os.path.join(ROOT_DIR, LOG_FOLDER)
    LOG_FILE = os.path.join(LOG_FOLDER, LOG_FILE)

