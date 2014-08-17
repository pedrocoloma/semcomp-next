from django.shortcuts import render

from semcomp_contact_form.models import Message

from ..decorators import staff_required

from .messages import *
from .events import *
from .places import *
from .lectures import *
from .users import *
from .courses import *
from .companies import *
from .processes import *
from .business import *
from .attendance import *
from .config import *

@staff_required
def manage_overview(request):
	context = {
		'active_overview': True,
		'unanswered_messages': Message.objects.unanswered()
	}

	return render(request, 'management/overview.html', context)
