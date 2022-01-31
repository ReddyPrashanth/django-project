from django import forms
from store.models import Size

CART_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=CART_QUANTITY_CHOICES, 
        coerce=int, 
        label='quantity',
        widget=forms.Select(attrs={'class': 'border outline-none rounded bg-transparent p-1 hover:border-black'})
    )
    update = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.HiddenInput
    )
    size = forms.CharField(
        required=True,
        widget=forms.HiddenInput,
        initial='small'
    )
    
    def clean_size(self):
        size = self.cleaned_data['size']
        if Size.objects.filter(slug=size).exists():
           return size 
        raise forms.ValidationError("Requested size does not exist")