from django import forms
from eventmgt.models import Participants, Event, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
class StyledFormMixin:
    """Mixins to appply style to form"""
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
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

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text=None

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")
        
    def clean_password1(self): #field error
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append("Password must be at least 8 character long""Password must be at least 8 character long")
            
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
            errors.append("Password must include Uppercase, Lowercase, Number and special characters")

        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean(self): #non field error
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

        
