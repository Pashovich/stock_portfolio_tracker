from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.forms import modelformset_factory, inlineformset_factory
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from .permissions import paid_user_required

from .models import Portfolio, Share
from .forms import PortfolioForm, ShareForm, DividendPortfolioForm
from .finance_api import FinanceApi

from datetime import datetime

@method_decorator(paid_user_required, name='dispatch')
class DividendPortfolioView(LoginRequiredMixin, FormView):
    template_name = "portfolio/dividend_calculator.html"
    form_class = DividendPortfolioForm
    success_url = reverse_lazy('dividend_calculator')

    def form_valid(self, form : DividendPortfolioForm):
        context = self.get_context_data()
        data = form.calculate_dividends_return()
        context['dividends_table'] = data.to_html(classes='table table-striped', index=False)
        context['form'] = form 
        return self.render_to_response(context)
    
class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = "portfolio/portfolio_list.html"
    context_object_name = "portfolios"

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioDetailView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = "portfolio/portfolio_detail.html"
    context_object_name = "portfolio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shares: list[type[Share]] = self.object.shares.all()
        for share in shares:
            current_price = self.get_current_price(share)
            upcoming_dividends = self.get_upcomming_dividends(share)
            for div_pay in upcoming_dividends:
                div_pay["amount_payable"] = share.qty * div_pay["cash_amount"]
            share_data = {
                "current_price": current_price,
                "upcoming_dividends": upcoming_dividends,
            }
            setattr(share, "data", share_data)
        context["shares"] = shares
        context["delete_confirmation_message"] = _(
            "Are you sure you want to delete this portfolio?"
        )
        return context

    def get_upcomming_dividends(self, share: Share) -> float:
        key = f"{share.name}:upcomming_dividends"
        dividends = cache.get(key)
        if dividends is None:
            dividends = FinanceApi.get_upcoming_dividends(share.name)
            cache.set(key, dividends, timeout=60 * 30)
        return dividends

    def get_current_price(self, share: Share) -> float:
        key = f"{share.name}:current_price"
        current_price = cache.get(key)
        if not current_price:
            current_price = FinanceApi.get_stock_price(share.name)
            cache.set(key, current_price, timeout=120)
        return current_price


class PortfolioCreateView(LoginRequiredMixin, TemplateView):
    template_name = "portfolio/portfolio_create.html"

    def get(self, *args, **kwargs):

        portfolio_form = PortfolioForm()
        ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
        formset = ShareFormSet(queryset=Share.objects.none())

        return self.render_to_response(
            {"portfolio_form": portfolio_form, "share_formset": formset}
        )

    def post(self, *args, **kwargs):

        portfolio_form = PortfolioForm(self.request.POST)
        ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
        formset = ShareFormSet(data=self.request.POST)

        if portfolio_form.is_valid() and formset.is_valid():

            portfolio = portfolio_form.save(commit=False)
            portfolio.user = self.request.user
            portfolio.save()
            shares = formset.save(commit=False)
            for share in shares:
                share.save()
                portfolio.shares.add(share)

            portfolio.save()
            return redirect(
                reverse_lazy("portfolio_detail", kwargs={"pk": portfolio.id})
            )

        return self.render_to_response(
            {"portfolio_form": portfolio_form, "share_formset": formset}
        )


class PortfolioDeleteUpdateView(LoginRequiredMixin, FormView):
    template_name = "portfolio/portfolio_create.html"
    form_class = PortfolioForm
    success_url = reverse_lazy(
        "portfolio_list"
    )

    def get(self, request, *args, **kwargs):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs.get("pk"))
        form = PortfolioForm(instance=portfolio)
        ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=0)
        formset = ShareFormSet(queryset=portfolio.shares.all())
        return self.render_to_response(
            self.get_context_data(portfolio_form=form, share_formset=formset)
        )

    def post(self, request, *args, **kwargs):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs.get("pk"))
        form = PortfolioForm(request.POST, instance=portfolio)
        ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=0)
        formset = ShareFormSet(data=self.request.POST)
        if form.is_valid() and formset.is_valid():
            portfolio = form.save()
            existing_shares = set(portfolio.shares.all())
            updated_shares = set()
            for form in formset:
                if form.cleaned_data.get("name"):
                    share = form.save(commit=False)
                    share.save()
                    updated_shares.add(share)

            shares_to_remove = existing_shares - updated_shares

            portfolio.shares.set(updated_shares)

            portfolio.shares.remove(*shares_to_remove)

            portfolio.save()

            return redirect(
                reverse_lazy("portfolio_detail", kwargs={"pk": portfolio.id})
            )

        return self.render_to_response(
            self.get_context_data(portfolio_form=form, share_formset=formset)
        )


class PortfolioDeleteView(LoginRequiredMixin , DeleteView):
    model = Portfolio
    success_url = reverse_lazy(
        "portfolio_list"
    )
    template_name = "portfolio/portfolio_confirm_delete.html"
