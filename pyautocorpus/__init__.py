ERROR = '''pyautocorpus is not currently supported on Windows.
If you have the expertise to add it, we would accept a pull request!'''

class Textifier:
    def __init__(self):
        raise NotImplementedError(ERROR)

    def textify(self, text):
        raise NotImplementedError(ERROR)
