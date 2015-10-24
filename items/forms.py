from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from models import Person, InventoryPhoto, LocationPhoto

# class TestForm(forms.Form):
#     date = forms.DateField(
#         widget=BootstrapDateInput(),
#     )
#     title = forms.CharField(
#         max_length=100,
#         help_text=u'This is the standard text input',
#     )
#     body = forms.CharField(
#         max_length=100,
#         help_text=u'This is a text area',
#         widget=forms.Textarea(
#             attrs={
#                 'title': 'I am "nice"',
#             }
#         ),
#     )
#     disabled = forms.CharField(
#         max_length=100,
#         required=False,
#         help_text=u'I am disabled',
#         widget=forms.TextInput(attrs={
#             'disabled': 'disabled',
#             'placeholder': 'I am disabled',
#         })
#     )
#     uneditable = forms.CharField(
#         max_length=100,
#         help_text=u'I am uneditable and you cannot enable me with JS',
#         initial=u'Uneditable',
#         widget=BootstrapUneditableInput()
#     )
#     content = forms.ChoiceField(
#         choices=(
#             ("text", "Plain text"),
#             ("html", "HTML"),
#         ),
#         help_text=u'Pick your choice',
#     )
#     email = forms.EmailField()
#     like = forms.BooleanField(required=False)
#     fruits = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=(
#             ("apple", "Apple"),
#             ("pear", "Pear"),
#         ),
#         help_text=u'As you can see, multiple checkboxes work too',
#     )
#     number = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple(attrs={
#             'inline': True,
#         }),
#         choices=(
#             ("3", "Three"),
#             ("33", "Thirty three"),
#             ("333", "Three hundred thirty three"),
#         ),
#         help_text=u'And can be inline',
#     )
#     color = forms.ChoiceField(
#         widget=forms.RadioSelect(attrs={'data-demo-attr': 'bazinga'}),
#         choices=(
#             ("#f00", "red"),
#             ("#0f0", "green"),
#             ("#00f", "blue"),
#         ),
#         help_text=u'And we have <i>radiosets</i>',
#     )
#     prepended = forms.CharField(
#         max_length=100,
#         help_text=u'I am prepended by a P',
#         widget=BootstrapTextInput(prepend='P'),
#     )
# 
#     def clean(self):
#         cleaned_data = super(TestForm, self).clean()
#         raise forms.ValidationError("This error was added to show the non field errors styling.")
#         return cleaned_data




class TestInlineForm(forms.Form):
    query = forms.CharField(required=False, label="")
    vegetable = forms.ChoiceField(
        choices=(
            ("broccoli", "Broccoli"),
            ("carrots", "Carrots"),
            ("turnips", "Turnips"),
        ),
    )
    active = forms.ChoiceField(widget=forms.RadioSelect, label="", choices=(
        ('all', 'all'),
        ('active', 'active'),
        ('inactive', 'inactive')
        ), initial='all')
    mine = forms.BooleanField(required=False, label='Mine only', initial=False)


class FormSetInlineForm(forms.Form):
    foo = forms.CharField()
    bar = forms.CharField()


class PersonCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PersonCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class InventoryDetailImageUploadForm(forms.Form):
#     """Image upload form."""
#     image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))


class ImageUploadForm(ModelForm):
    class Meta:
        fields = ['image', 'title', 'caption']
        widgets = {'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
                   'caption': forms.TextInput()}


class InventoryImageUploadForm(ImageUploadForm):
    class Meta(ImageUploadForm.Meta):
        model = InventoryPhoto


class LocationImageUploadForm(ImageUploadForm):
       class Meta(ImageUploadForm.Meta):
        model = LocationPhoto
