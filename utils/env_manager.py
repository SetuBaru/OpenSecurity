def load_modules(modules, module_path):
    try:
        if isinstance(modules, str):
            eval(f"from {module_path} import {modules}")
        elif isinstance(modules, list):
            for location in module_path:
                for module in modules:
                    print('Attempting to Initialized the required modules......')
                    eval(f"from {location} import {str(module)}")
    except ImportError or ImportWarning or ModuleNotFoundError as ModuleLoadError:
        return f"'ModuleLoadError': Module probably not found...\terror msg:{ModuleLoadError}"
    except Exception as UnexpectedError:
        return f"'UnexpectedError while loading FaceID modules':\t\t\t\t{UnexpectedError}"
    finally:
        return f'{modules} Imported successful!\n'
