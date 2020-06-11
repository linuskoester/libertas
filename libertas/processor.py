import os


def libertas_version(request):
    if os.environ.get('LIBERTAS_VERSION') is None:
        try:
            file = open('version.txt', 'r')
            version = file.read()
            file.close()
        except FileNotFoundError:
            version = 'DEV'

        if version == '':
            os.environ['LIBERTAS_VERSION'] = 'DEV'
        else:
            os.environ['LIBERTAS_VERSION'] = version

    return {'libertas_version': os.environ.get('LIBERTAS_VERSION')}
