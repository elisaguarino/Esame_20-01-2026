import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        num_album=self._view.txtNumAlbumMin.value
        try:
            num_album=int(self._view.txtNumAlbumMin.value)
        except:
            self._view.show_alert("inesrire un valore valido")

        self._model.load_artists_with_min_albums(num_album)
        self.popola_dd()
        self._model.build_graph()

    def handle_connected_artists(self, e):


    def popola_dd(self):
        self.artisti = self._model.get_artisti()
        for a in self.artisti:
            self._view.ddArtist.options.append(ft.dropdown.Option(key=a.id, text=a))
        self._view.update_page()

    def gestisci_dd(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        valore = e.control.value
        self.artist_map = self._model.get_artist_map()
        valore = int(valore)
        self.artista_selezionato = self.artist_map[valore]


