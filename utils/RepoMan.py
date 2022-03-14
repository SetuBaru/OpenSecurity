class Module:
    def __init__(self):
        self.defaults = ['os', 'sys']
        # Loading Default Modules

    # A function that loads and verifies module existence.
    def load(self, _path=None, modules=None, defaults=None):
        if defaults is None:
            defaults = self.defaults
        try:
            if modules is None:
                print('Setting up defaults...')
                if isinstance(defaults, list):
                    for default in defaults:
                        print(f'importing the {default} module...')
                        eval(f'import {str(default)}')
                elif isinstance(defaults, str):
                    print(f'importing the {defaults} module...')
                    eval(f'import {str(defaults)}')

            else:
                if _path is None:
                    print('Module path set to current path....')
                    if isinstance(modules, str):
                        print(f'Importing the {modules} module...')
                        eval(f'import {str(modules)}')
                    elif isinstance(modules, list):
                        for module in modules:
                            print(f'Importing the {module} module...')
                            eval(f"import {str(module)}")
                else:
                    if isinstance(modules, str):
                        print(f'Importing the {modules} module...')
                        eval(f"from {str(_path)} import {str(modules)}")
                    elif isinstance(modules, list):
                        for module in modules:
                            print(f'Importing the {module} module...')
                            eval(f"from {str(_path)} import {str(module)}")

        except ImportError or ImportWarning or ModuleNotFoundError as ModuleLoadError:
            return f"'ModuleLoadError': Module probably not found...\terror msg:{ModuleLoadError}"
        except Exception as UnexpectedError:
            return f"'UnexpectedError Encountered during the loading of modules':\t\t\t\t{UnexpectedError}"
        if modules is not None:
            mode = modules
        else:
            mode = defaults
        if isinstance(mode, list):
            mode = mode.__str__()
            return f'{str(mode)} Imported successful!\n'
        else:
            return f'{str(mode)} Imported successful!\n'


# UNIT TESTING
if __name__ == "__main__":
    mod = Module()
