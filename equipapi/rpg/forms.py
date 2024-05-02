# rpg/forms.py
from django import forms
from .models import ItemTemplate

class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        fields = ['name', 'itemType', 'stats']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Item Name'}),
            'itemType': forms.Select(choices=ItemTemplate.ITEM_TYPES),
            'stats': forms.HiddenInput(),  # Initially hidden; handle via JavaScript if necessary
        }

    def clean_stats(self):
        stats = self.cleaned_data.get('stats')
        # Validate the stats JSON here, or continue using your model's clean method
        return stats