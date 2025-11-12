"""Forms for todoapp."""
from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    """Form for creating and editing todos."""
    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter todo title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description (optional)',
                'rows': 4
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
