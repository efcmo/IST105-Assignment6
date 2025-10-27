from django import forms

class NumberForm(forms.Form):
    a = forms.FloatField(label="Number A")
    b = forms.FloatField(label="Number B")
    c = forms.FloatField(label="Number C")
    d = forms.FloatField(label="Number D")
    e = forms.FloatField(label="Number E")
