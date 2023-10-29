import flet as ft
from mydb import dataBase

conexionDB = dataBase()

def main(page : ft.Page):
    conexionDB._validateData(
        page.client_storage.get("creds")[0],
        page.client_storage.get("creds")[1],
    )

    def databaseSelected(e):
        if conexionDB._selectDataBase(e.content.value):
            page.go(f"/databases/{e.content.value}/panel")
        else:
            page.go("/databases")

    def getDatabases():
        items = []
        for row in conexionDB._getDataBases():
            items.append(
                ft.DataRow(
                    [
                        ft.DataCell(ft.Text(f"{row}"))
                    ],
                    on_select_changed= lambda e: databaseSelected(e.control.cells[0])
                )
            )
        return items

    def logOut(e):
        page.client_storage.remove("creds")
        page.go("/")

    database_table = ft.DataTable(
        columns= [ ft.DataColumn(
                ft.Text("Base de datos", size= 16, weight= ft.FontWeight.BOLD)
            )
        ],
        rows= getDatabases(),
        border_radius= 10
    )

    page.title = f"{conexionDB._getUsername()}"
    
    return ft.View("/", 
        [ ft.Column([
                ft.Text("Seleciona la base de datos", size= 20),
                database_table,

                ft.ElevatedButton(
                    "Salir",
                    on_click= logOut
                )
            ])
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        vertical_alignment= ft.MainAxisAlignment.CENTER
    )