from django import forms
import inspect
from ...University.models import University, consignment,representativePush, representative
from ...account.models import User

class CreateUniversity(forms.ModelForm):
    class Meta():
        model = University
        fields = '__all__'

class CreateRepr(forms.ModelForm):
    class Meta():
        model = representative
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateRepr, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)


class consignmentForm(forms.ModelForm):
    class Meta():
        model = consignment
        fields = '__all__'
        exclude = ('user','totalPaid','consignmentID','totalCommission')


class representativePushForm(forms.ModelForm):
    class Meta():
        model = representativePush
        fields = '__all__'


class addMoneyForm(forms.ModelForm):
    class Meta():
        model = representativePush
        fields = ('pushMoney',)