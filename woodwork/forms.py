from .models import ProductReview, Profile, ProductInstance
from django import forms
from django.contrib.auth.models import User

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('content', 'product', 'reviewer',)
        widgets = {'product': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class UserProductForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product', 'requirements', 'requestor', ]
        widgets = {'requestor': forms.HiddenInput()}

