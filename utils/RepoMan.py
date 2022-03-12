class Module:
    def __init__(self):
        self.defaults = ['os', 'sys']
        # Loading Default Modules
        self.load()

    # A function that loads and verifies module existence.
    def load(self, modules=None, module_path=None, defaults=None):
        if defaults is None:
            defaults = self.defaults
        try:
            if modules is None:
                print('Loading environment defaults.....')

                if isinstance(defaults, list):
                    for default in defaults:
                        print(f'importing the {default} module...')
                        eval(f'import {str(default)}')

                elif isinstance(defaults, str):
                    print(f'importing the {defaults} module...')
                    eval(f'import {str(defaults)}')

            elif modules is not None and module_path is None:
                print('Module path set to current path....')

            elif isinstance(modules, str) and module_path is not None:
                print(f'Importing the {modules} module...')
                eval(f"from {module_path} import {modules}")

            elif isinstance(modules, str) and module_path is None:
                print(f'Importing the {modules} module...')
                eval(f'import {modules}')

            elif isinstance(modules, list) and module_path is not None:
                for location in module_path:
                    for module in modules:
                        print(f'Importing the {modules} module...')
                        eval(f"from {location} import {str(module)}")

            elif isinstance(modules, list) and module_path is not None:
                for location in module_path:
                    for module in modules:
                        print(f'Importing the {modules} module...')
                        eval(f"from {location} import {str(module)}")

        except ImportError or ImportWarning or ModuleNotFoundError as ModuleLoadError:
            return f"'ModuleLoadError': Module probably not found...\terror msg:{ModuleLoadError}"

        except Exception as UnexpectedError:
            return f"'UnexpectedError Encountered during the loading of modules':\t\t\t\t{UnexpectedError}"

        finally:
            if modules is not None:
                return f'{modules} Imported successful!\n'
            else:
                return f'{defaults} Imported successful!\n'


# UNIT TESTING
if __name__ == "__main__":
    mod = Module()
