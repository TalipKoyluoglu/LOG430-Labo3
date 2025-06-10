from django.shortcuts import render, redirect
from django.contrib import messages  # type: ignore
from magasin.controllers.uc6_validation import UC6_ValidationControleur

controleur = UC6_ValidationControleur()


def uc6_demandes(request):
    demandes = controleur.get_demandes_en_attente()
    return render(request, "magasin/uc6_demandes.html", {"demandes": demandes})


def uc6_valider(request, demande_id):
    success = controleur.valider_demande(demande_id)
    if success:
        messages.success(request, "Demande approuvée et stock transféré.")
    else:
        messages.error(request, "Échec : stock central insuffisant ou erreur.")
    return redirect("uc6_demandes")


def uc6_rejeter(request, demande_id):
    success = controleur.rejeter_demande(demande_id)
    if success:
        messages.success(request, "Demande rejetée avec succès.")
    else:
        messages.error(request, "Échec du rejet de la demande.")
    return redirect("uc6_demandes")
