from django.contrib.webdesign import lorem_ipsum
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from management.forms import CompanyForm

from .common import ManagementTest

class CompaniesTest(ManagementTest):
	urls = 'management.urls'

	def test_add_company(self):
		post_data = {
			'name': 'Super Empresa',
			'logo': SimpleUploadedFile('imagem.png', self.get_blank_image().read()),
			'url': 'http://semcomp.icmc.usp.br',
			'type': 'B',
			'description': lorem_ipsum.words(20, False),
			'in_fair': True,
		}

		response = self.client.post(
			reverse('management_companies_add'),
			post_data
		)
		self.assertEventCreated('management-company')


