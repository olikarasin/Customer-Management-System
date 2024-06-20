from django import forms
from .models import Customer, EmailReference, Technician, Contract, Credential

class EmailReferenceForm(forms.ModelForm):
    class Meta:
        model = EmailReference
        fields = ['email']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'has_contract', 'notes', 'address', 'contact_name', 'phone', 'transport_hours', 'transport_minutes', 'hide_transport_charges', 'hours_remaining', 'status', 'tech1_regular_hours', 'tech1_time_and_a_half_hours', 'tech1_double_time_hours', 'tech2_regular_hours', 'tech2_time_and_a_half_hours', 'tech2_double_time_hours', 'tech3_regular_hours', 'tech3_time_and_a_half_hours', 'tech3_double_time_hours']

    emails = forms.CharField(widget=forms.HiddenInput(), required=False)  # Renamed field

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['date', 'amount', 'rate', 'paid', 'invoice_number']

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name']

class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
