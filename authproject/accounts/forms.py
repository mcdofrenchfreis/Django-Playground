from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {f: "" for f in ("username", "password1", "password2")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent daisyUI classes to all fields (including non-model fields)
        for name, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " input input-bordered w-full").strip()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email
