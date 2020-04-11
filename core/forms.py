from django import forms 

# Custom imports
from .models import Item


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item 
        fields = [
            'item_name',
            'item_type',
            'model_num',
            'project_name',
            'item_serial_num',
            'quantity',
            'location',
            'calibration_date',
            'remarks',
            'slug'
        ] 