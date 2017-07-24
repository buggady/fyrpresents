from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from address.forms import AddressField
from django.contrib.auth.models import User
from users.models import UserProfile

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'userForm'
        self.helper.form_class = 'GeneralForm shake'
        self.helper.form_tag = False

        #self.helper.layout.append(Submit('save', 'save', css_class='btn-system btn-large'))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'profileForm'
        self.helper.form_class = 'GeneralForm shake'
        self.helper.include_media = False
        self.helper.form_tag = False

        #self.helper.layout.append(Submit('save', 'save', css_class='btn-system btn-large'))

    class Meta:
        model = UserProfile
        fields = ['home_address']