from . import api


@api.route('/')
def get_smth():
    return "hello world"
