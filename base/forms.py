from django.forms import ModelForm
import django.forms as forms
from .models import Room

class RoomForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id':"room_name_input", 'name':"name", 'class': 'form-control'}))
    topic = forms.Select(attrs={'id':"room_topic_input", 'name':"topic", 'class': 'form-control'})
    class Meta:
        model = Room
        exclude = ['host', 'participants']