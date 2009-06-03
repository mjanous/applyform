from django.forms.fields import Select

class USStateSelect(Select):
    """
    A Select widget that uses a list of U.S. states/territories as its choices.
    """
    def __init__(self, attrs=None):
        from us_states import STATE_CHOICES
        super(USStateSelect, self).__init__(attrs, choices=STATE_CHOICES)