from django import forms


class SummarizeForm(forms.Form):
    chart = forms.ChoiceField(choices=[('true', 'Summarize')])