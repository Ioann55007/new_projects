from django import forms

from forum.models import Topic, Category, User


class TopicForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    name = forms.CharField(label='Name question', widget=forms.TextInput(attrs={'size': '100'}))
    tags = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'size': '13'}))
    author = forms.ModelChoiceField(queryset=User.objects.all(), label='Author')
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))




    class Meta:
        model = Topic
        fields = ['name', 'tags', 'author', 'category', 'content']



