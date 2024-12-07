from django import forms
from .models import ItemList
from .models import Item

class CategoryForm(forms.ModelForm):
    class Meta:
        model = ItemList
        fields = ['Category_name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['Item_name','description','Price','Category','Image']