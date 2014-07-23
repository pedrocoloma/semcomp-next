from website.utils import signup_allowed

def semcomp(request):
	print 'oi pessoas'
	return {
		'signup_allowed': signup_allowed
	}
