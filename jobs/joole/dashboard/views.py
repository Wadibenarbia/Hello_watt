from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ClientForm
from .models import Conso_eur, Conso_watt


class ClientFormView(View):
    def get(self, request):
        return render(request, 'dashboard/accueil.html')

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            client_id = form.cleaned_data['client']
            return redirect('dashboard:results', client_id=client_id)

def results(request, client_id):
    conso_euro2016 = []
    conso_euro2017 = []
    conso_watt2016 = []
    conso_watt2017 = []
    months = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]
    annual_costs = [0, 0]
    is_elec_heating = False
    dysfunction_detected = False

    try:
        for month in months:
            conso_euro2016.append(Conso_eur.objects.all().filter(client_id = client_id).filter(year=2016).values_list(month, flat=True)[0])
            conso_euro2017.append(Conso_eur.objects.all().filter(client_id = client_id).filter(year=2017).values_list(month, flat=True)[0])
            conso_watt2016.append(Conso_watt.objects.all().filter(client_id = client_id).filter(year=2016).values_list(month, flat=True)[0])
            conso_watt2017.append(Conso_watt.objects.all().filter(client_id = client_id).filter(year=2017).values_list(month, flat=True)[0])

        test = (conso_watt2016[5] + conso_watt2016[6] + conso_watt2016[7])/3
        moyenne_conso_hiver = (conso_watt2016[0] + conso_watt2016[10] + conso_watt2016[11])/3

        i = 0
        moyenne_conso_2016 = 0
        moyenne_conso_2017 = 0
        while i < 12:
            moyenne_conso_2016 = moyenne_conso_2016 + conso_watt2016[i]
            moyenne_conso_2017 = moyenne_conso_2016 + conso_watt2017[i]
            i = i + 1
        moyenne_conso_2016 = moyenne_conso_2016/3
        moyenne_conso_2017 = moyenne_conso_2017/3

        if(moyenne_conso_2016 <= 30/100*moyenne_conso_2017):
            dysfunction_detected = True
        if(test >= 40/100*moyenne_conso_hiver):
            is_elec_heating = False
        else:
            is_elec_heating = True

        context = {
            "conso_euro2017": conso_euro2017,
            "conso_watt2017": conso_watt2017,
            "annual_costs": annual_costs,
            "is_elec_heating": is_elec_heating,
            "dysfunction_detected": dysfunction_detected,
            "months": months,
            "moyenne_conso_2016": moyenne_conso_2016,
            "moyenne_conso_2017": moyenne_conso_2017,
            "moyenne_conso_hiver": moyenne_conso_hiver,
            "test": test,
        }
        return render(request, 'dashboard/results.html', context)
    except:
        context = {
        "conso_euro2016": conso_euro2016,
        "conso_watt2016": conso_watt2016,
        "annual_costs": annual_costs,
        "is_elec_heating": is_elec_heating,
        "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)
