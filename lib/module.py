import logging
import importlib.util
import os.path
from .probe import get_probe


# Function to dynamically import a module given its full path
def import_module_from_path(path):
    # Create a module spec from the given path
    spec = importlib.util.spec_from_file_location("module_name", path)
    if spec is None or spec.loader is None:
        raise Exception(f'no module spec for path: {path}')

    # Load the module from the created spec
    module = importlib.util.module_from_spec(spec)
    if module is None:
        raise Exception(f'failed to load module form path: {path}')

    # Execute the module to make its attributes accessible
    spec.loader.exec_module(module)

    # Return the imported module
    return module


async def get_module(file_id: int):
    module_path = f'/tmp/script{file_id}.py'
    if not os.path.isfile(module_path):
        blob = await get_probe().download_file(file_id=file_id)
        try:
            content = blob.decode()
        except Exception:
            raise Exception(f'File ID {file_id} is not UTF-8 encoded')

        try:
            with open(module_path, 'w') as fp:
                fp.write(content)
        except Exception as e:
            raise Exception(
                f'Failed to write content for file ID {file_id}: {e}')

    module = import_module_from_path(module_path)
    try:
        assert module.export.__bases__[0].__name__ == 'TestBase'
    except Exception:
        raise Exception(
            f'File ID {file_id} script is missing export to a `TestBase` '
            'subclass. For example: `export = MyTest`')

    return module
