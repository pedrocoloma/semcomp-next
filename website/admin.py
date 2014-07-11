from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import SemcompUser
from .forms import UserSignupForm


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = SemcompUser
		fields = ('email', 'password', 'full_name', 'id_usp', 'is_active', 'is_staff')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]


class SemcompUserAdmin(UserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserSignupForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'full_name', 'id_usp', 'is_staff')
	list_filter = ('is_staff',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('full_name', 'id_usp')}),
		('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'full_name', 'id_usp', 'password')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(SemcompUser, SemcompUserAdmin)
