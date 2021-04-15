import functools
import traceback


# code based on:
# http://stackoverflow.com/questions/19309514/getting-original-line-number-for-exception-in-concurrent-futures
def reraise_with_stack(func):
    """
    decorator for stack trace for futures
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback_str = traceback.format_exc(e)
            raise Exception(
                "Error occurred. Original traceback is\n%s\n" % traceback_str)

    return wrapped
