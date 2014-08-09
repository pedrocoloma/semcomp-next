from django.dispatch import receiver

from signup.signals import user_signed_up, user_activated

from stats import add_event


@receiver(user_signed_up)
def user_signed_up_callback(sender, **kwargs):
	user = kwargs.pop('user')

	add_event(
		'signup-users',
		{
			'action': 'signup',
			'user': {
				'id': user.pk,
				'name': user.full_name,
			},
		}
	)

@receiver(user_activated)
def user_activated_callback(sender, **kwargs):
	user = kwargs.pop('user')

	add_event(
		'signup-users',
		{
			'action': 'activate',
			'user': {
				'id': user.pk,
				'name': user.full_name,
			}
		}
	)

