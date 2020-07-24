from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from collections import OrderedDict, defaultdict

def index(request):
    template_name = 'app/registration/index.html'
    return render(request, template_name, {})


class Dashboard(View):
    template_name = 'app/app_files/index.html'

    data = defaultdict()
    data["css_files"] = []
    data["js_files"] = []
    data["active_link"] = 'Dashboard'

    def get(self, request):
        return render(request, self.template_name, self.data)
