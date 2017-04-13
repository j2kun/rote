
handlers = {
    'setup': None,
    'newdata': None,
    'foreach': None,
    'skipif': None,
    'describe': None,
    'teardown': None,
}


def wrap_in_try(f, with_teardown=True, msg=None):
    def wrapped(*args, **kwargs):
        if with_teardown:
            try:
                return f(*args, **kwargs)
            except:
                if msg:
                    print(msg)
                else:
                    print('{} failed!'.format(f.__name__))
                raise
            finally:
                handlers['teardown']()
        else:
            try:
                return f(*args, **kwargs)
            except:
                if msg:
                    print(msg)
                else:
                    print('{} failed!'.format(f.__name__))
                raise


def setup(f):
    wrapped = wrap_in_try(f, with_teardown=False)
    handlers['setup'] = wrapped
    return f


def newdata(f):
    wrapped = wrap_in_try(f)
    handlers['newdata'] = wrapped
    return f


def foreach(f):
    wrapped = wrap_in_try(f)
    handlers['foreach'] = wrapped
    return f


def teardown(f):
    wrapped = wrap_in_try(f, with_teardown=False)
    handlers['teardown'] = wrapped
    return f


def skipif(f):
    wrapped = wrap_in_try(f)
    handlers['skipif'] = wrapped
    return f


def describe(f):
    wrapped = wrap_in_try(f)
    handlers['decribe'] = wrapped
    return f


def run():
    setup = handlers['setup']
    newdata = handlers['newdata']
    foreach = handlers['foreach']
    skipif = handlers['skipif']
    describe = handlers['describe']
    teardown = handlers['teardown']

    if setup:
        existing_data = setup()
    else:
        existing_data = []

    if newdata:
        new_data = newdata(existing_data)
    else:
        new_data = []

    for item in new_data:
        if skipif and skipif(item):
            if describe:
                print('Skipping {}'.format(describe(item)))
            else:
                print('Skipping {}'.format(item))

        print(chr(27) + "[2J")
        if foreach:
            foreach(item, existing_data)

    if teardown:
        teardown(existing_data)
