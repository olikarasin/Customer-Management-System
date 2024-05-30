# timesheets/forms.py
from django import forms
from .models import Timesheet

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['date', 'time_in', 'time_out', 'technician_level', 'technician', 'special_rate', 'file', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'time_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'technician_level': forms.Select(attrs={'class': 'form-control'}),
            'technician': forms.Select(attrs={'class': 'form-control'}),  # Add this line
            'special_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = "Work Date"
        self.fields['time_in'].label = "Time In (24hr)"
        self.fields['time_out'].label = "Time Out (24hr)"
        self.fields['technician_level'].label = "Technician Level"
        self.fields['technician'].label = "Technician"  # Add this line
        self.fields['file'].label = "Upload File"
        self.fields['notes'].label = "Additional Notes"
