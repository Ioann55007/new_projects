from django.shortcuts import render
from django.views import View


class MainPageView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class SingleTopicPageView(View):
    template_name = 'single-topic.html'

    def get(self, request):
        return render(request, self.template_name)
