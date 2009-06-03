from django.contrib.localflavor.us.us_states import STATE_CHOICES

STATE_CHOICES = list(STATE_CHOICES)
STATE_CHOICES.insert(0, ('', '---------'))