from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Todo


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'text-input'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm the password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class TodoForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'text-input'}),
    )

    class Meta:
        model = Todo
        fields = ('title', 'description', 'due_date', 'priority', 'is_completed')
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'text-input', 'placeholder': 'Finish deployment notes'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'text-input',
                    'placeholder': 'Add more context for this task.',
                    'rows': 4,
                }
            ),
            'priority': forms.Select(attrs={'class': 'text-input'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }
