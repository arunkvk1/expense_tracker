from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum, Case, When, F, DecimalField
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TransactionForm
from .models import Transaction


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    balance = transactions.aggregate(
        total=Sum(
            Case(
                When(type=Transaction.INCOME, then=F("amount")),
                When(type=Transaction.EXPENSE, then=-F("amount")),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )["total"] or Decimal("0.00")

    today = timezone.localdate()
    spent_today = transactions.filter(type=Transaction.EXPENSE, date=today).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    recent = transactions[:30]

    context = {
        "balance": balance,
        "spent_today": spent_today,
        "transactions": recent,
    }
    return render(request, "wallet/dashboard.html", context)


@login_required
def add_transaction(request, kind):
    if kind not in (Transaction.INCOME, Transaction.EXPENSE):
        return redirect("dashboard")

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            tx.type = kind
            tx.save()
            label = "Added to wallet" if kind == Transaction.INCOME else "Expense recorded"
            messages.success(request, label)
            return redirect("dashboard")
    else:
        form = TransactionForm(initial={"date": timezone.localdate()})

    return render(
        request,
        "wallet/add_transaction.html",
        {"form": form, "kind": kind},
    )


@login_required
def delete_transaction(request, pk):
    tx = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        tx.delete()
        messages.success(request, "Entry deleted")
    return redirect("dashboard")
