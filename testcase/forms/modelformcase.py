
from django import forms
from mypro import models

#modelform验证
class CaseModelForm(forms.ModelForm):
    main_tasks = forms.CharField(required=False)

    class Meta:
        model = models.TestCase
        # fields = "__all__"
        # fields =(
        #     "product_id",
        # )

        exclude = ['is_delete']



