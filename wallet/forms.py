from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["description", "amount", "date"]
        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "What's this for?", "autofocus": True}
            ),
            "amount": forms.NumberInput(
                attrs={"placeholder": "0.00", "min": "0.01", "step": "0.01", "inputmode": "decimal"}
            ),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
