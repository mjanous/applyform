from django.forms.fields import Select

class ShirtSizeSelect(Select):
    """
    A Select widget that uses a list of shirt sizes as its choices.
    """
    def __init__(self, attrs=None):
        from shirts import SHIRT_CHOICES
        super(ShirtSizeSelect, self).__init__(attrs, choices=SHIRT_CHOICES)