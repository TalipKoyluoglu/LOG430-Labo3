from magasin.services.uc6_service import (
    get_demandes_en_attente,
    valider_demande,
    rejeter_demande
)

class UC6_ValidationControleur:
    def get_demandes_en_attente(self):
        return get_demandes_en_attente()

    def valider_demande(self, demande_id):
        return valider_demande(demande_id)

    def rejeter_demande(self, demande_id):
        return rejeter_demande(demande_id)
