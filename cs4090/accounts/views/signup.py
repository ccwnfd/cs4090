from django.views.generic import View
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm


class SignUpView(View):
    """User registration view"""

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.canvas_api_key = form.cleaned_data.get("canvas_api_key")
            user.save()
            return redirect("accounts:signin")

        context = {"form": form}
        return render(request, self.template_name, context)
