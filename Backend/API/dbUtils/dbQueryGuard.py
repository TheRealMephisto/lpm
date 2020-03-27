
class dbQuearyGuard:

    def __init__(self):
        pass

    # https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def sanitiseQuery(self, query):
        pass