from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .backend import parser
from rest_framework import generics
from .models import AvitoData, AvitoPriceChange, AvitoNew
from .serializers import AvitoSerializer
from .forms import SettingsForm


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
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            '''
            parser.main_with_settings(form.cleaned_data['base_url'],
                                      form.cleaned_data['p_max'],
                                      form.cleaned_data['p_min'])
            '''
            #return HttpResponse("Form approved, Parsed Successfully")
            return redirect('new_ads')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SettingsForm(initial={'base_url': 'https://www.avito.ru/velikiy_novgorod/kvartiry/prodam-ASgBAgICAUSSA8YQ?',
                                     'p_max': 1200000,
                                     'p_min': 800000})

    #return HttpResponse("Start parsing page")
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




