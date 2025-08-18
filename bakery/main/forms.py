from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        
        widgets = {
        "username":  forms.TextInput(attrs={"class": "form-control", "autocomplete": "username"}),
        "first_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "given-name"}),
        "last_name":  forms.TextInput(attrs={"class": "form-control", "autocomplete": "family-name"}),
        "email":      forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
    }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "line1", "line2", "city", "postal_code", "country", "is_default"]

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip()
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            # ensure profile exists, then set role
            profile = getattr(user, "profile", None)
            if profile is None:
                from main.models import Profile, Role
                profile = Profile.objects.create(user=user, role=Role.BUYER) #type:ignore
            else:
                from main.models import Role
                profile.role = Role.BUYER #type:ignore
                profile.save()

        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
