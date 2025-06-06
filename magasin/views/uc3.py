from django.shortcuts import render # type: ignore
from magasin.controllers.uc3_performance import UC3_PerformanceControleur

controleur = UC3_PerformanceControleur()

def uc3_dashboard(request):
    indicateurs = controleur.get_indicateurs_par_magasin()
    return render(request, "magasin/uc3_dashboard.html", {"indicateurs": indicateurs})
