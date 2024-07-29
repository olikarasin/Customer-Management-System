from django import forms
from .models import Customer, EmailReference, Technician, Contract, Credential
import random
import string
from datetime import datetime  # Import datetime module

class EmailReferenceForm(forms.ModelForm):
    class Meta:
        model = EmailReference
        fields = ['email']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'has_contract', 'notes', 'address', 'contact_name', 'phone', 
            'transport_hours', 'transport_minutes', 'hide_transport_charges', 
            'hours_remaining', 'status', 'tech1_regular_hours', 'tech1_time_and_a_half_hours', 
            'tech1_double_time_hours', 'tech2_regular_hours', 'tech2_time_and_a_half_hours', 
            'tech2_double_time_hours', 'tech3_regular_hours', 'tech3_time_and_a_half_hours', 
            'tech3_double_time_hours'
        ]

    emails = forms.CharField(widget=forms.HiddenInput(), required=False)

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['date', 'amount', 'rate', 'paid', 'invoice_number', 'manual_charge_hours', 'manual_charge_amount']
        widgets = {
            'date': forms.TextInput(attrs={'placeholder': 'YYYYMMDD'}),
        }

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = "Date (YYYYMMDD)"
        self.fields['invoice_number'].label = "Timesheet Number"

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if len(date) != 8 or not date.isdigit():
            raise forms.ValidationError("Enter a valid date in YYYYMMDD format.")
        try:
            # Validate the date by attempting to create a datetime object
            datetime.strptime(date, '%Y%m%d')
        except ValueError:
            raise forms.ValidationError("Enter a valid date in YYYYMMDD format.")
        return date  # Return as a string

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
