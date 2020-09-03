
from django import forms
from mypro import models
#form验证

class CaseForm01(forms.Form):



    def save(self):
        return models.TestCase.objects.create(**self.cleaned_data)


class CaseForm02(forms.Form):


    def __init__(self,instance=None,*args,**kwargs):
        self.instance = instance
        super(CaseForm02,self).__init__(*args,**kwargs)

    def save(self):
        #如果instance有数据
        if self.instance is not None:
            for key,value in self.cleaned_data.items():
                #反射
                setattr(self.instance,key,value)
            self.instance.save()
            return self.instance
        else:
            return models.Case.objects.create(**self.cleaned_data)


