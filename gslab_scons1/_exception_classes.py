class BadExecutableError(Exception):
	def __init__(self, message = ''):
		print 'Error: ' + message

class BadExtensionError(Exception):
	def __init__(self, message = ''):
		print 'Error: ' + message

class LFSError(Exception):
	def __init__(self, message = ''):
		print 'Error: ' + message

class ReleaseError(Exception):
    def __init__(self, message = ''):
        print 'Error: ' + message
