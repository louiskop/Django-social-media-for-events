from django import forms
from party.models import Post, Comment

COUNTRY_CHOICES = (
    ('southafrica','South Africa'),
    ('america', 'America'),
    ('england','England'),
    ('russia','Russia'),
    ('china','China'),
)
class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'enter a title..',
            'name':'title'
        }
    ))
    drinks = forms.BooleanField(widget = forms.CheckboxInput(attrs={'class':'form-check-input','name':'thecheckbox'}),required = False)
    age = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'theage','placeholder':'eg. 18 or above'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','name':'thedate','placeholder':'month/day/year'}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control','name':'thetime','placeholder':'eg. 12:00'}))
    timeend = forms.TimeField(widget=forms.TextInput(attrs={'class':'form-control','name':'thetimeend','placeholder':'eg. 12:00'}),required=True)
    color = forms.ChoiceField(required=True,choices=COUNTRY_CHOICES)
    image = forms.ImageField(required=False)
    color.widget.attrs.update({'class':'form-control','name':'thecountry'})
    image.widget.attrs.update({'class':'form-control','name':'theimage'})
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'thelocation','placeholder':'City/neighbourhood'}),required=True)
    keyword = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'thekeyword','placeholder':'Anything really'}),required=False)

    class Meta:
        model = Post
        fields = ("title","date","time","age","drinks","timeend","color","image","location","keyword")

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
