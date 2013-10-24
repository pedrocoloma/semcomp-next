from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def staff_required(function):
	def staff_test(user):
		if user.is_authenticated() and user.is_staff:
			return True
		raise PermissionDenied
	return user_passes_test(staff_test)(function)

