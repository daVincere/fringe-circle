from django  import forms
from fringe_x import models


class ArticleForm(forms.ModelForm):
    class Meta:
        model=models.Article
        fields=('name','image_url')

