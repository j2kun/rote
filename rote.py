import sys


class Rote(object):
    def __init__(self):
        self.handlers = {
            'setup': None,
            'newdata': None,
            'foreach': None,
            'skipif': None,
            'describe': None,
            'teardown': None,
        }

        self.accumulator = []
        self.new_data = []

    def wrap_in_try(self, f, with_teardown=True):
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except KeyboardInterrupt:
                print('\n\nQuitting after teardown...'.format(f.__name__))
                if with_teardown:
                    self.handlers['teardown'](self.accumulator)
                sys.exit(0)
            except:
                print('{} failed!'.format(f.__name__))
                if with_teardown:
                    self.handlers['teardown'](self.accumulator)
                raise

        return wrapped

    def setup(self, f):
        wrapped = self.wrap_in_try(f, with_teardown=False)
        self.handlers['setup'] = wrapped
        return f

    def newdata(self, f):
        wrapped = self.wrap_in_try(f)
        self.handlers['newdata'] = wrapped
        return f

    def foreach(self, f):
        wrapped = self.wrap_in_try(f)
        self.handlers['foreach'] = wrapped
        return f

    def teardown(self, f):
        wrapped = self.wrap_in_try(f, with_teardown=False)
        self.handlers['teardown'] = wrapped
        return f

    def skipif(self, f):
        wrapped = self.wrap_in_try(f)
        self.handlers['skipif'] = wrapped
        return f

    def describe(self, f):
        wrapped = self.wrap_in_try(f)
        self.handlers['decribe'] = wrapped
        return f

    def run(self):
        setup = self.handlers['setup']
        newdata = self.handlers['newdata']
        foreach = self.handlers['foreach']
        skipif = self.handlers['skipif']
        describe = self.handlers['describe']
        teardown = self.handlers['teardown']

        if setup:
            self.accumulator = setup()
        else:
            self.accumulator = []

        if newdata:
            self.new_data = newdata(self.accumulator)
        else:
            self.new_data = []

        for item in self.new_data:
            if skipif and skipif(item):
                if describe:
                    print('Skipping {}'.format(describe(item)))
                else:
                    print('Skipping {}'.format(item))

            if foreach:
                foreach(item, self.accumulator)

        if teardown:
            teardown(self.accumulator)
