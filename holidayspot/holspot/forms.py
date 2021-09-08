
from django.core.exceptions import ValidationError
from django import forms
from .models import Review ,Search,FeedBack
from django.forms import fields

class CommentForm(forms.ModelForm):
    comment = forms.CharField()
    rating = forms.IntegerField()

    class Meta:
        model = Review
        fields = ('comment','rating',)


    def clean_rating(self):
        rating = self.cleaned_data['rating']
        print(rating )
        if rating < 1 or rating>5:
            print("hi")
            raise ValidationError('Rating must be between 1 to 5')
        return rating



class SearchForm(forms.ModelForm):
    query = forms.CharField()

    class Meta:
        model = Search
        fields = ('query',)


class FeedBackForm(forms.ModelForm):

    name = forms.CharField()
    email = forms.CharField()
    feedback = forms.CharField( widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = FeedBack
        fields = ('name','email','feedback',)



