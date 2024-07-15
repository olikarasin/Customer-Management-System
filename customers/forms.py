from django import forms
from .models import Customer, EmailReference, Technician, Contract, Credential
import random
import string

class EmailReferenceForm(forms.ModelForm):
    class Meta:
        model = EmailReference
        fields = ['email']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'has_contract', 'notes', 'address', 'contact_name', 'phone', 'transport_hours', 'transport_minutes', 'hide_transport_charges', 'hours_remaining', 'status', 'tech1_regular_hours', 'tech1_time_and_a_half_hours', 'tech1_double_time_hours', 'tech2_regular_hours', 'tech2_time_and_a_half_hours', 'tech2_double_time_hours', 'tech3_regular_hours', 'tech3_time_and_a_half_hours', 'tech3_double_time_hours']

    emails = forms.CharField(widget=forms.HiddenInput(), required=False)

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['date', 'amount', 'rate', 'paid', 'invoice_number']

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name']

class CredentialForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Credential
        fields = ['username', 'password']

    def generate_password(self):
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(10))
        self.fields['password'].initial = password

    def __init__(self, *args, **kwargs):
        super(CredentialForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['password'].widget.attrs.pop('readonly', None)  # Allow manual input by default
