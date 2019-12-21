from django import forms
from .models import localAddress

class AddressForm(forms.ModelForm):
    class Meta:
        model = localAddress
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['fname'].label = "First Name"
        self.fields['lname'].label = "Last Name"
        self.fields['address'].label = "Address"
        self.fields['phoneNumber'].label = "Phone Number"
        self.fields['university'].label = "Select Your College"
        self.fields['address'].widget.attrs.update(style='max-width: 20em')