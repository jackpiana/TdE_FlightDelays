import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Flight Delays"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.tf_compagnie = None
        self.btn_creaGrafo = None
        self.lv_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Flight Delays", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        # text field for the name
        self.tf_compagnie = ft.TextField(
            label="numero minimo compagnie",
            width=200,
            hint_text="inserisci numero minimo compagnie"
        )
        self.btn_creaGrafo = ft.ElevatedButton(text="Crea grafo",
                                                on_click=self._controller.handle_creaGrafo)


        row1 = ft.Row([self.tf_compagnie, self.btn_creaGrafo])
        self._page.controls.append(row1)


        # dropdown
        self.dropdown1 = ft.Dropdown(label="areoporto partenza")

        self.dropdown2 = ft.Dropdown(label="areoporto destinazione")

        self.btnVerificaConnessione = ft.ElevatedButton(text="Verifica connessione ",
                                        on_click=self._controller.handle_verificaConnessione)

        row2 = ft.Row([self.dropdown1, self.dropdown2, self.btnVerificaConnessione])
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.lv_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.lv_result)
        self._page.update()

    def show_loading_bar(self):
        # progress bar
        progress_loading = ft.ProgressBar(width=400,
                                          height=20,
                                          color="blue",
                                          bgcolor="#eeeeee")

        self.row_loadingBar = ft.Row([progress_loading],
                                     alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(self.row_loadingBar)
        self._page.update()

    def remove_loading_bar(self):
        self._page.controls.remove(self.row_loadingBar)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
