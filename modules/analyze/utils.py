def debugger(func):
    import traceback
    from datetime import datetime

    def wrapped(*args, **kwargs):
        try:
            start = datetime.now()
            res = func(*args, **kwargs)
            print(f'{func.__qualname__} took {datetime.now() - start}s')
            return res
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    return wrapped