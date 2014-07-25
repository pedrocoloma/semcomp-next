from django.shortcuts import render

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
from .config import *

@staff_required
def manage_overview(request):
	return render(request, 'management/overview.html', {'active_overview': True})
