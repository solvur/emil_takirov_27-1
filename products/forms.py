from django import forms


class ProductCreateForm(forms.Form):
    image = forms.FileField(required=False)
    title = forms.CharField(min_length=2, max_length=225)
    description = forms.CharField(widget=forms.Textarea())
    best_before_date = forms.CharField(min_length=11, max_length=8)


class ReviewCreateForm(forms.Form):
    text = forms.CharField(min_length=2, max_length=225)
