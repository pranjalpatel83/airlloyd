from django import forms
from .models import Passenger, Booking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, Field
from django.forms import inlineformset_factory

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['location', 'duration', 'date', 'time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Fragen zum Termin',
                'location',
                'duration',
                'date',
                'time_slot'
            )
        )

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['salutation', 'first_name', 'last_name', 'weight', 'phone', 'email', 'ticket_number']

    def __init__(self, *args, **kwargs):
        super(PassengerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Passagierdaten',
                'salutation',
                'first_name',
                'last_name',
                'weight',
                'phone',
                'email',
                'ticket_number'
            ),
            Div(
                Field('DELETE', template='bootstrap4/field.html')  # This line allows the delete checkbox
            )
        )

PassengerFormSet = inlineformset_factory(
    Booking, Passenger, form=PassengerForm, extra=1, can_delete=True
)
