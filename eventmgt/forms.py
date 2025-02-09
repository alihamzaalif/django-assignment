from django import forms
from eventmgt.models import Participants, Event, Category

class StyledFormMixin:
    """Mixins to appply style to form"""
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500 hover:border-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class":self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    "class":self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("inside date")
                field.widget.attrs.update({
                    "class":"border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500 hover:border-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                # print("inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                # print("inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })
#Django Model Form
class EventForm(forms.Form):
    name = forms.CharField(max_length=100,label="Event Title")
    description = forms.CharField(widget=forms.Textarea,label="Event Details")
    date = forms.DateField(widget=forms.SelectDateWidget,label="Event Date")
    location = forms.CharField(max_length=100,label="Event Location")
    category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all())
    
    def __init__(self, *args, **kwargs):
        categories = kwargs.pop("categories", None)
        super().__init__(*args, **kwargs)
        if categories is not None:
            self.fields['category'].queryset = categories

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100,label="Category Name")
    description = forms.CharField(widget=forms.Textarea,label="Category Details")

class ParticipantForm(forms.Form):
    name = forms.CharField(max_length=100,label="Event Title")
    email = forms.EmailField(widget=forms.EmailInput,label="Email Address")
    event = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple,label="event")

    def __init__(self, *args, **kwargs):
        events = kwargs.pop("events",[])
        super().__init__(*args, **kwargs)
        self.fields['event'].choices = [evnt.name for evnt in events]

class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'category', 'status']
        widgets = {
            'date': forms.SelectDateWidget,
            'category': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.apply_styled_widgets()

class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participants
        fields = ['name', 'email', 'event']
        widgets = {
            'email' : forms.EmailInput,
            'event' : forms.CheckboxSelectMultiple
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

