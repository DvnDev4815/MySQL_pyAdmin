import flet as ft
from mydb import dataBase

entry_user = ft.TextField(label= "Nombre de usuario")
entry_pass = ft.TextField(
    label= "Contraseña",
    can_reveal_password= True,
    password= True
)
dialog_err = ft.SnackBar(
    content= ft.Text("Error: Usuario o contraseña incorrectos")
)

conexionDB = dataBase()

def main(page : ft.Page):
    page.title = "Inicio de sesion"

    def connectToDatabase(e):
        if conexionDB._validateData(entry_user.value, entry_pass.value):
            page.client_storage.set("creds", [entry_user.value, entry_pass.value])
            page.go("/databases")
        else:
            page.snack_bar = dialog_err
            page.snack_bar.open = True
            page.update()

    login_frame = ft.Column(
        [
            ft.Row([
                ft.Text(
                    "Inicio de sesion", 
                    text_align= ft.TextAlign.CENTER,
                    size= 20,
                    expand= True
                )]
            ),

            ft.Column([
                    entry_user,
                    entry_pass
                ]
            ),

            ft.Row([
                ft.FilledButton(
                    icon= ft.icons.SEND,
                    text= "Continuar",
                    on_click= connectToDatabase,
                    autofocus= True
                )],
                alignment= ft.MainAxisAlignment.CENTER
            )
        ],
        width= 600,
    )

    return ft.View("/", [
            login_frame
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        vertical_alignment= ft.MainAxisAlignment.CENTER
    )