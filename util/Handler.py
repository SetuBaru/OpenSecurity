import datetime
from LoggingTool import Log


class Handler:
    def __init__(self):
        self.datetime = datetime.datetime
        self.LoggingModule = Log()
        self.eval_limit = 25
        self.counter = 0

    def handle(self, _object, log_result, limit=True):
        if limit is True and len(_object) >= self.eval_limit:
            print(f"{_object} has exceeded the Maximum Limit... Please try again or Set limit off. ")
            self.counter = self.counter + 1
            if self.counter == 2:
                x = input('Turn the limit off? (Y/N):  ')
                if x.lower() == 'y':
                    print('Limit has been turned off! \n')
                    self.handle(_object=_object, log_result=log_result, limit=False)
            self.handle(_object=_object, log_result=log_result, limit=True)
        else:
            try:
                eval(_object)
                return True
            except Exception as ExceptionError:
                error_code = f"*{_object} raised an Exception* :  '{ExceptionError}'"
                print(error_code)
                if log_result is True:
                    self.LoggingModule.Append(f"{error_code}")
                return ExceptionError

    def test(self):
        pass

    def log(self):
        pass
