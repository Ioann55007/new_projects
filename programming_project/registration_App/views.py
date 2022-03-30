from django.shortcuts import render
from django.views import View


class SimpleSignupView(View):
    template_name = 'simple-signup.html'

    def get(self, request):
        return render(request, self.template_name)
