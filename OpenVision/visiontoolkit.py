# Ensuring the right modules have been imported Successfully.
def load_modes():
    try:
        status = True
        print('Attempting to Initialized the required modules......')
        from FaceID import faceId as Fid, adaptiveLearning as Adapt
    except ImportError or ImportWarning or ModuleNotFoundError as UnexpectedFIDError:
        return f"Encountered an 'error-with FaceIDImport': Module probably not found...\terror msg:{UnexpectedFIDError}"
    except Exception as UnexpectedFIDError:
        return f"Encountered an 'ErrorWith FaceIDImport':\t\t\t\t{UnexpectedFIDError}"
    finally:
        if status is False:
            print('Sorry....Unable to Import Modules...\t\t\t\tPlease try again later.')
        else:
            print('Module Import Successful!')


# Calling the Module_Loader Function.
load_modes()
