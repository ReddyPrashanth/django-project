from django import forms
from .models import UserProfile

class BaseForm(forms.ModelForm):
    classes = 'w-full border rounded p-1 outline-none text-sm'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            attrs = {
                'class': self.classes,
                'placeholder': field.label
            }
            field.widget.attrs.update(attrs)       

class UserProfileForm(BaseForm):
    
    job = forms.CharField(
        label='Job',
        widget=forms.TextInput()
    )
    
    address = forms.CharField(
        label='Address',
        widget=forms.TextInput()
    )
    
    city = forms.CharField(
        label='City',
        widget=forms.TextInput()
    )
    
    state = forms.CharField(
        label='State',
        widget=forms.TextInput()
    )
    phone = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput()
    )
    
    zipcode = forms.CharField(
        label='Zip Code',
        widget=forms.TextInput()
    )
    
    class Meta:
        model = UserProfile
        fields = ['job', 'address', 'city', 'state', 'phone', 'zipcode']
        
    def save(self, user=None):
        profile = super(UserProfileForm, self).save(commit=False)
        if user:
            profile.user = user
        profile.save()
        return profile        
    