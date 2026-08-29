"""Forms for registration, profile, and account settings."""
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from training.models import UserProfile


class StyledFormMixin:
    """Apply consistent DevMastery field classes."""

    def _style_fields(self):
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "dm-checkbox")
            elif isinstance(widget, forms.Textarea):
                field.widget.attrs.setdefault("class", "dm-textarea")
            elif isinstance(widget, forms.Select):
                field.widget.attrs.setdefault("class", "dm-select")
            else:
                field.widget.attrs.setdefault("class", "dm-input")
            field.widget.attrs.setdefault("placeholder", field.label or "")


class DevMasteryAuthenticationForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class DevMasteryUserCreationForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        help_text="Used for login recovery and progress updates.",
    )
    first_name = forms.CharField(max_length=150, required=False, label="First name")
    last_name = forms.CharField(max_length=150, required=False, label="Last name")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
        self.fields["username"].help_text = "Letters, digits, and @/./+/-/_ only."
        self.fields["password1"].help_text = "At least 8 characters. Avoid common passwords."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user


class UserAccountForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        labels = {
            "username": "Username",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ProfileDetailsForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "display_name",
            "bio",
            "location",
            "timezone",
            "company",
            "target_role",
            "years_experience",
            "github_url",
            "linkedin_url",
            "portfolio_url",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "years_experience": forms.NumberInput(attrs={"min": 0, "max": 50}),
        }
        labels = {
            "display_name": "Display name",
            "target_role": "Target role",
            "years_experience": "Years of experience",
            "github_url": "GitHub URL",
            "linkedin_url": "LinkedIn URL",
            "portfolio_url": "Portfolio URL",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class DevMasteryPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class DevMasteryPasswordResetForm(StyledFormMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class DevMasterySetPasswordForm(StyledFormMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
