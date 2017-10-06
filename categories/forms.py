from django import forms
from .models import Topic, Reply


class NewTopicForm(forms.ModelForm):
    #message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tanga igitekerezo aha ngaha'}), max_length=40000, help_text='inyuguti nyinshi ushobora kwandika ni 40000.')

    class Meta:
        model = Topic
        fields = ['subject',]




class PostForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tanga igitekerezo aha ngaha'}), max_length=40000, help_text='inyuguti nyinshi ushobora kwandika ni 40000.')

    class Meta:
        model = Reply
        fields =['message',]