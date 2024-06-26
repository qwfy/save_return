import os
import pickle
import datetime
import functools
from glob import glob
import logging

def save(value_id: str, save_dir=None):
    """
    Save the return value of a function into a pickle file.
    :param value_id: The return value of the function will be saved at `{save_dir}/{value_id}/{version}.pkl`.
    :param save_dir: When not set: if in jupyter, then `data/save_return/{notebook_basename}.var`, otherwise `data/save_return`
    :return: The decorated function, which will save the return value to a pickle file.
    """

    if save_dir is None:
        notebook_name = os.environ.get('JPY_SESSION_NAME')
        if notebook_name is not None:
            notebook_name = os.path.basename(notebook_name)
            save_dir = os.path.join('data/save_return', f'{notebook_name}.var')
        else:
            save_dir = 'data/save_return'
    value_dir = os.path.join(save_dir, value_id)

    def prepare_save():
        numbers = [
            int(os.path.basename(f).split('.')[-2].split('_')[-1])
            for f in glob(os.path.join(value_dir, '*.pkl'))
        ]
        if not numbers:
            next_number = 0
        else:
            next_number = max(max(numbers) + 1, len(numbers))

        version = datetime.datetime.now().strftime(f'%Y%m%d_%H%M%S_%f') + f'_{next_number:05d}'

        save_path = os.path.join(value_dir, f'{version}.pkl')

        if not os.path.exists(value_dir):
            os.makedirs(value_dir, exist_ok=True)

        with open(os.path.join(value_dir, 'test_permission'), 'w') as _:
            pass

        return save_path

    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            save_path = prepare_save()

            ret = func(*args, **kwargs)

            try:
                with open(save_path, 'wb') as f:
                    pickle.dump(ret, f)
            except Exception:
                logging.warning(
                    f'Failed to save the return value of `{func.__name__}` to `{save_path}`. '
                    f'The return value will not be saved, but otherwise `{func.__name__}` functions as normal.',
                    exc_info=True
                )

            return ret
        return wrapped

    return decorator


def load(path):
    """
    Just a wrapper around `pickle.load`, saves you a `import pickle`
    :param path: The path to the pickle file.
    :return: The value contained in the pickel file `path`.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)
