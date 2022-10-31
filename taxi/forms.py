from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    LICENSE_LETTER_COUNT = 3
    LICENSE_DIGIT_COUNT = 5

    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            rf"^[A-Z]{{{LICENSE_LETTER_COUNT}}}"
            rf"[0-9]{{{LICENSE_DIGIT_COUNT}}}$",
            message=f"License number should contain {LICENSE_LETTER_COUNT} "
                    f"uppercase letters followed by {LICENSE_DIGIT_COUNT} "
                    "digits",
        )],
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
