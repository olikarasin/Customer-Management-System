from django import forms
from .models import Timesheet
from datetime import datetime

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = [
            'timesheet_id', 'date', 'time_in', 'time_out', 'pause_hours', 'pause_minutes', 'technician', 
            'technician_level', 'special_rate', 'file', 'notes', 'display_notes_to_customer', 'manual_charge_hours', 
            'manual_charge_amount'
        ]
        widgets = {
            'timesheet_id': forms.TextInput(attrs={'class': 'form-control timesheet-id-input'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY/MM/DD'}),
            'time_in': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HHMM'}),
            'time_out': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HHMM'}),
            'pause_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hours'}),
            'pause_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'technician': forms.Select(attrs={'class': 'form-control'}),
            'technician_level': forms.Select(attrs={'class': 'form-control'}),
            'special_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'required': False, 'id': 'id_file'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manual_charge_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'manual_charge_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args, **kwargs)
        self.fields['timesheet_id'].label = "Timesheet ID"
        self.fields['date'].label = "Work Date (YYYY/MM/DD)"
        self.fields['time_in'].label = "Time In (HHMM)"
        self.fields['time_out'].label = "Time Out (HHMM)"
        self.fields['pause_hours'].label = "Pause Hours"
        self.fields['pause_minutes'].label = "Pause Minutes"
        self.fields['technician_level'].label = "Technician Level"
        self.fields['technician'].label = "Technician"
        self.fields['file'].label = "Upload File"
        self.fields['file'].required = False  # Make the file field optional
        self.fields['notes'].label = "Additional Notes"
        self.fields['display_notes_to_customer'].label = "Display Notes to Customer"
        self.fields['manual_charge_hours'].label = "Manual Charge Hours"
        self.fields['manual_charge_amount'].label = "Manual Charge Amount"

    def clean_date(self):
        date = self.cleaned_data.get('date')
        try:
            datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            raise forms.ValidationError("Enter a valid date in YYYY/MM/DD format.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        if date:
            cleaned_data['date'] = datetime.strptime(date, '%Y/%m/%d').strftime('%Y/%m/%d')  # This ensures date is stored as YYYY/MM/DD

        time_in = cleaned_data.get('time_in')
        if time_in and len(time_in) == 4 and time_in.isdigit():
            cleaned_data['time_in'] = datetime.strptime(time_in, '%H%M').strftime('%H:%M')
        elif time_in and len(time_in) == 5 and time_in[2] == ':':
            cleaned_data['time_in'] = time_in
        else:
            raise forms.ValidationError("Enter a valid time in HHMM format.")

        time_out = cleaned_data.get('time_out')
        if time_out and len(time_out) == 4 and time_out.isdigit():
            cleaned_data['time_out'] = datetime.strptime(time_out, '%H%M').strftime('%H:%M')
        elif time_out and len(time_out) == 5 and time_out[2] == ':':
            cleaned_data['time_out'] = time_out
        else:
            raise forms.ValidationError("Enter a valid time in HHMM format.")

        return cleaned_data
