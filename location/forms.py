from django import forms


class PhoneForm(forms.Form):
    number = forms.CharField(max_length=25, label='Phone Number')


class LocationForm(forms.Form):
    longitude = forms.CharField(max_length=25)
    latitude = forms.CharField(max_length=25)
