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
from django.http import JsonResponse, HttpResponse
from .permissions import paid_user_required

from .models import Portfolio, Share, DividendCalculation, PaidRequests
from .forms import PortfolioForm, ShareForm, DividendPortfolioForm
from .utils import *
from django.core.cache import cache
from hashlib import md5
from django.views import View
from pathlib import Path

from datetime import datetime


@method_decorator(paid_user_required, name='dispatch')
class DividendReportDownload(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Fetch the DividendCalculation object based on the provided primary key (pk)
        try:
            dividend_calculation = DividendCalculation.objects.get(pk=pk)
        except DividendCalculation.DoesNotExist:
            return HttpResponse("DividendCalculation not found.", status=404)

        buffer = create_dividend_report(dividend_calculation)
        filename = f"dividend_report_{pk}.pdf"
        response = HttpResponse(
            buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


@method_decorator(paid_user_required, name='dispatch')
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = DividendCalculation
    success_url = reverse_lazy(
        "portfolio_calculator_list_view"
    )

    def get(self, request, *args, **kwargs):
        return redirect('portfolio_calculator_list_view')


@method_decorator(paid_user_required, name='dispatch')
class DividendCalculatorReportView(LoginRequiredMixin, DetailView):

    model = DividendCalculation
    template_name = "portfolio/dividend_calculator_detail_view.html"
    context_object_name = "report"
    object: DividendCalculation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_details = self.object.get_results()

        if str(self.object.capital).split('.')[1] == '0':
            self.object.capital = int(self.object.capital)

        result_list = []
        for key in payment_details['date']:
            result_list.append({
                'payment_date': payment_details['date'][key],
                'avg_dividend_yield': payment_details['avg_div'][key],
                'payment_amount': payment_details['dividends_return'][key]
            })
        context["data"] = result_list
        context["delete_confirmation_message"] = _(
            "Are you sure you want to delete this report?"
        )
        return context


@method_decorator(paid_user_required, name='dispatch')
class DividendCalculatorListView(LoginRequiredMixin, ListView):
    template_name = "portfolio/dividend_calculator_list_view.html"
    context_object_name = "reports"
    model = DividendCalculation

    def get_queryset(self):
        reports = DividendCalculation.objects.filter(user=self.request.user)
        return reports


@method_decorator(paid_user_required, name='dispatch')
class DividendCalculatorView(LoginRequiredMixin, FormView):
    template_name = "portfolio/dividend_calculator.html"
    form_class = DividendPortfolioForm
    success_url = reverse_lazy('portfolio_calculator')

    def form_valid(self, form: DividendPortfolioForm):
        context = self.get_context_data()
        cache_key = md5(str(form.cleaned_data).encode('utf-8')).hexdigest()
        dividends_data = cache.get(f'div_calc_{cache_key}')
        if self.request.POST.get('action') == 'validate' and form.check_ticker_name():
            data = form.calculate_dividends_return()
            if not data.empty:
                dividends_data = data.to_dict()
                data.columns = ['Est. Payment date',
                                'Avg. Dididend yeild', 'Return on Capital $']
                context['dividends_table'] = data.to_html(
                    classes='table table-striped', index=False, justify='left')
                context['form'] = form
                cache.set(f'div_calc_{cache_key}',
                          dividends_data, timeout=1200)
            else:
                return super().form_invalid(form)

            return self.render_to_response(context)
        elif self.request.POST.get('action') == 'save' and dividends_data:
            dividends_data = cache.get(f'div_calc_{cache_key}')
            object_ = DividendCalculation.objects.create(
                user=self.request.user,
                **form.cleaned_data
            )
            object_.set_results(dividends_data)
            object_.save()
            cache.delete(f'div_calc_{cache_key}')
            return redirect('portfolio_calculator_detailt_view', pk=object_.id)

        return super().form_invalid(form)


class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = "portfolio/portfolio_list.html"
    context_object_name = "portfolios"

    def get_queryset(self):
        portfolios = Portfolio.objects.filter(user=self.request.user)

        for portfolio in portfolios:
            shares: list[type[Share]] = portfolio.shares.all()
            profit = 0
            for share in shares:
                current_price = get_current_price(share)
                profit = round(float((current_price * share.qty)) -
                               float((share.price * share.qty)), 3)

            setattr(portfolio, "profit", profit)
        return portfolios


class PortfolioDetailView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = "portfolio/portfolio_detail.html"
    context_object_name = "portfolio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shares: list[type[Share]] = self.object.shares.all()
        for share in shares:
            current_price = get_current_price(share)
            upcoming_dividends = get_upcomming_dividends(share)
            for div_pay in upcoming_dividends:
                div_pay["amount_payable"] = share.qty * div_pay["cash_amount"]

            share_data = {
                "current_price": current_price,
                "upcoming_dividends": [{'cash_amount': div['cash_amount'], 'pay_date': div['pay_date'], 'amount_payable': round(share.qty * div['cash_amount'], 3)} for div in upcoming_dividends],
                "profit": round(float((current_price * share.qty)) - float((share.price * share.qty)), 3)
            }
            setattr(share, "data", share_data)

        context['profit_overall'] = round(
            sum([share.data.get('profit', 0) for share in shares]), 3)
        context["shares"] = shares
        context["delete_confirmation_message"] = _(
            "Are you sure you want to delete this portfolio?"
        )
        return context


class PortfolioCreateView(LoginRequiredMixin, TemplateView):
    # TODO update for portfolio review before create
    template_name = "portfolio/portfolio_create.html"

    def get(self, *args, **kwargs):

        portfolio_form = PortfolioForm()
        ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
        formset = ShareFormSet(queryset=Share.objects.none())
        return self.render_to_response(
            {"portfolio_form": portfolio_form, "share_formset": formset,
                "page_title": 'Create New Portfolio'}
        )

    def post(self, *args, **kwargs):
        current_step = self.request.POST.get('current_step')
        if current_step == '1':
            portfolio_form = PortfolioForm(self.request.POST)
            if portfolio_form.is_valid():
                return JsonResponse({"success": True})
            # Collect form errors
            errors = {f'errors-step1_{field}': error_list for field,
                      error_list in portfolio_form.errors.items()}
            return JsonResponse({"success": False, "errors": errors})

        elif current_step == '2':
            portfolio_form = PortfolioForm(self.request.POST)
            ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
            formset = ShareFormSet(self.request.POST)
            if portfolio_form.is_valid() and formset.is_valid():
                return JsonResponse({"success": True,
                                     'name': portfolio_form.cleaned_data['name'],
                                     'shares': [form.cleaned_data for form in formset]})

            errors = {}
            for form in formset:
                for field, error_list in form.errors.items():
                    errors[f"errors-step2_{form.prefix}_{field}"] = error_list

            return JsonResponse({"success": False, "errors": errors})
        else:
            portfolio_form = PortfolioForm(self.request.POST)
            ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
            formset = ShareFormSet(self.request.POST)
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
                    reverse_lazy("portfolio_detail", kwargs={
                                 "pk": portfolio.id})
                )
            else:
                errors = {}
                for form in formset:
                    for field, error_list in form.errors.items():
                        errors[f"errors-step2_{form.prefix}_{field}"] = error_list
                return HttpResponse()


class PortfolioDeleteUpdateView(PortfolioCreateView):
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
            self.get_context_data(
                portfolio_form=form, share_formset=formset, page_title='Update Portfolio')
        )

    def post(self, *args, **kwargs):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs.get("pk"))
        form = PortfolioForm(self.request.POST, instance=portfolio)
        current_step = self.request.POST.get('current_step')
        if current_step == '1':
            if form.is_valid():
                return JsonResponse({"success": True})
            # Collect form errors
            errors = {f'errors-step1_{field}': error_list for field,
                      error_list in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors})

        elif current_step == '2':
            ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
            formset = ShareFormSet(self.request.POST)
            if form.is_valid() and formset.is_valid():
                return JsonResponse({"success": True})

            errors = {}
            for form in formset:
                for field, error_list in form.errors.items():
                    errors[f"errors-step2_{form.prefix}_{field}"] = error_list

            return JsonResponse({"success": False, "errors": errors})
        else:
            ShareFormSet = modelformset_factory(Share, form=ShareForm, extra=1)
            formset = ShareFormSet(self.request.POST)
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
                    reverse_lazy("portfolio_detail", kwargs={
                                 "pk": portfolio.id})
                )
            else:
                errors = {}
                for form in formset:
                    for field, error_list in form.errors.items():
                        errors[f"errors-step2_{form.prefix}_{field}"] = error_list
                return HttpResponse()


class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    model = Portfolio
    success_url = reverse_lazy(
        "portfolio_list"
    )
    template_name = "portfolio/portfolio_confirm_delete.html"


class ForbiddenForNonPaid(LoginRequiredMixin, TemplateView):
    model = Portfolio
    template_name = "portfolio/403_forbidden_non_paid.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_paid:
            return redirect('index')

        has_paid_requests = PaidRequests.objects.filter(
            user=self.request.user).exists()
        if has_paid_requests:
            return self.render_to_response({'status': 'Awaiting approval'}, status=403)
        else:
            return self.render_to_response({'status': None}, status=403)

    def post(self, *args, **kwargs):
        if self.request.user.is_paid:
            return redirect('index')

        PaidRequests.objects.create(user=self.request.user)
        return self.render_to_response({'status': 'Awaiting approval'}, status=403)
