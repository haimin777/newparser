from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .backend import parser
from rest_framework import generics
from .models import AvitoData, AvitoPriceChange, AvitoNew
from .serializers import AvitoSerializer
from .forms import SettingsForm
from django.views.generic import ListView

from my_parser.backend.settings import ConfigHandler, MainSettings

from django_tables2 import SingleTableView
from .tables import AvitoTable, AvitoChangeTable, AvitoNewTable


class AvitoList(generics.ListCreateAPIView):
    queryset = AvitoData.objects.all()
    serializer_class = AvitoSerializer





def index(request):

    return render(request, 'restaurant/base.html', {})


def auto_parse(request):

    parser.main()

    return HttpResponse('ok')


def parse_data(request):


    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SettingsForm(request.POST)
        # check whether it's valid:

        # save new settings to config file

        if form.is_valid():
            new_conf = ConfigHandler()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

            parser.main_with_settings(form.cleaned_data['base_url'],
                                      form.cleaned_data['p_max'],
                                      form.cleaned_data['p_min'])

            new_conf.set_setting(["paths", "url"], "base_url", form.cleaned_data['base_url'])
            new_conf.set_setting(["urls_settings"], "max_summ", form.cleaned_data['p_max'])
            new_conf.set_setting(["urls_settings"], "min_summ", form.cleaned_data['p_min'])

            print('settings changed!!\n')

            #return HttpResponse("Form approved, Parsed Successfully")
            return redirect('new-ads')

    # if a GET (or any other method) we'll create a blank form
    else:
        cur_settings = MainSettings()

        form = SettingsForm(initial={'base_url': cur_settings.base_url,
                                     'p_max': cur_settings.max_summ,
                                     'p_min': cur_settings.min_summ})

    return render(request, 'restaurant/parse_settings.html', {'form': form})


def all_ads(request):
    all_data = AvitoData.objects.all()

    return render(request, 'restaurant/all_data.html', {
                            'all_data': all_data
                                            })

def new_ads(request):
    changed_data = AvitoNew.objects.all()

    return render(request, 'restaurant/new_data.html', {
                            'changed_data': changed_data
                                            })


def deltas_ads(request):
    changed_data = AvitoPriceChange.objects.all()

    return render(request, 'restaurant/changed_data.html', {
                            'changed_data': changed_data
                                })


def analyze_methods(request):
    return HttpResponse('List of ML and DS features')


def show_settings(request):
    cur_settings = MainSettings()
    base_url = cur_settings.base_url
    p_max = cur_settings.max_summ
    p_min = cur_settings.min_summ
    return HttpResponse('Current Settings: ' + base_url + '\n' +p_max + '\n' + p_min)


class AvitoListView(SingleTableView):
    model = AvitoData
    table_class = AvitoTable
    template_name = 'restaurant/all_data.html'

class AvitoChangeListView(SingleTableView):
    model = AvitoPriceChange
    table_class = AvitoChangeTable
    template_name = 'restaurant/changed_data.html'


class AvitoNewListView(SingleTableView):
    model = AvitoNew
    table_class = AvitoNewTable
    template_name = 'restaurant/new_data.html'






