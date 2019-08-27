from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'autocomplete': 'off'}))
    finish_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['executor'].queryset = project.users

    class Meta:
        model = Task
        fields = ['topic', 'start_date', 'finish_date', 'type', 'priority', 'estimate_time', 'executor', 'description']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        finish_date = cleaned_data.get("finish_date")

        if start_date and finish_date and finish_date < start_date:
            raise forms.ValidationError("Finish date should be greater than start date.")


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        fields = ['text', 'task', 'user']
        widgets = {
            'task': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }
