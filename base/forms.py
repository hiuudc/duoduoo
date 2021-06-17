from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # course = forms.ModelChoiceField(
    #     queryset=Course.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class SearchCourse(forms.Form):

#     language = forms.ChoiceField(choices=languages, required=True,
#                                  widget=forms.Select(attrs={'onchange': 'submit();'}))
#     fields = ('language')


class UserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

        # widgets = {
        #     'username': forms.TextInput(attrs={'required': True}),
        #     'email': forms.EmailInput(attrs={'required': True}),
        # }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = '__all__'
        exclude = ['course', 'user']


class WordTransForm(forms.ModelForm):
    class Meta:
        model = WordTranslation
        fields = '__all__'
        exclude = ['word', 'user', 'course', 'user_liked']

    # def __init__(self, *args, **kwargs):
    #     super(WordTransForm, self).__init__(*args, **kwargs)

        # self.fields['word'].widget.attrs['disabled'] = 'disabled'
        # self.fields['user'].widget.attrs['disabled'] = 'disabled'

        #self.fields[''].widget.attrs['readonly'] = True


class PhraseForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = '__all__'
        exclude = ['course', 'user']


class PhraseTransForm(forms.ModelForm):
    class Meta:
        model = PhraseTranslation
        fields = '__all__'
        exclude = ['phrase', 'user', 'course', 'user_liked']


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = '__all__'
        exclude = ['course', 'user', 'user_liked']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        exclude = ['course', 'user', 'user_liked']


# class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
# def label_from_instance(self, member):
#     """ Customises the labels for checkboxes"""
#     return "%s" % member.name


# class CreateMealForm(forms.ModelForm):

# def __init__(self, *args, **kwargs):
#     """ Grants access to the request object so that only members of the current user
#     are given as options"""

#     self.request = kwargs.pop('request')
#     super(CreateMealForm, self).__init__(*args, **kwargs)
#     self.fields['members'].queryset = Member.objects.filter(
#         user=self.request.user)


# def clean_content(self):
    # content = self.cleaned_data.get("content")
    # if something:
    #     raise forms.ValidationError(message)
    # return content


# class Meta:
#     model = Course
#     fields = ['name']

# name = forms.CharField()

# members = CustomModelMultipleChoiceField(
#     queryset=None,
#     widget=forms.CheckboxSelectMultiple
# )
