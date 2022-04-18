from django.shortcuts import render
from django.views import View


class CreateTopicView(View):
    template_name = 'create_top.html'

    def get(self, request):
        return render(request, 'create_top.html')
