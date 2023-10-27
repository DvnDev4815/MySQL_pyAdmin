import flet as ft
from mydb import dataBase

conexionDB = dataBase()

entry_pass = ft.TextField(label= "Contraseña", can_reveal_password= True, password= True)
entry_user = ft.TextField(label= "Nombre de usuario")
error_dialog = ft.AlertDialog(
    title= ft.Text("Usuario Incorrecto"),
    content= ft.Text("El usuario o contraseña son incorrectos")
)  


def main(page : ft.Page):
    page.title = "Conexion a base de datos"

    def connectToDatabase(e):
        if not conexionDB._validateData(entry_user.value, entry_pass.value):
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()
        else:
            page.client_storage.set("isLogin", True)
            page.go("/databases")

    def viewPop(e):
        page.view.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def routeChange(e):
        page.views.clear()
        rTemplate = ft.TemplateRoute(page.route)

        if rTemplate.match("/"):
            page.views.append(
                ft.View("/", [
                    login_frame,
                ], 
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                vertical_alignment= ft.MainAxisAlignment.CENTER,
            ))

        elif rTemplate.match("/databases"):
            def databaseSelected(e):
                if conexionDB._selectDataBase(e.content.value):
                    page.go(f"/databases/{e.content.value}/panel")
                else:
                    page.go("/databases")

            def getDatabases():
                items = []
                for row in conexionDB._getDataBases():
                    items.append(
                        ft.DataRow([
                            ft.DataCell(ft.Text(f"{row}"))
                        ],
                        on_select_changed= lambda e: databaseSelected(e.control.cells[0])
                    ))   
                return items

            def logOut(e):
                page.client_storage.remove("isLogin")
                conexionDB._logOut()
                page.go("/")

            database_table = ft.DataTable(
                columns=[ft.DataColumn(
                    ft.Text(
                        "Base de datos:", 
                        size= 16, 
                        weight= ft.FontWeight.BOLD, 
                    ))
                ],
                rows= getDatabases(),
                border_radius= 10,
            )

            page.title = f"{conexionDB._getUsername()}"
            page.views.append(ft.View("/databases", [
                    ft.Column(controls=[
                        ft.Text("Selecciona la base de datos", size=20),
                        database_table,

                        ft.ElevatedButton(
                            "Salir",
                            on_click= logOut
                        )

                    ]),
                ],
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                vertical_alignment= ft.MainAxisAlignment.CENTER,
            ))

        elif rTemplate.match("/databases/:database_id/panel"):
            if not conexionDB._selectDataBase(rTemplate.database_id):
                page.go("/databases")

            def tableData(table:str, limit : int):
                if table == None:
                    table = dropdown_tables.options[0].key
                
                data = {
                    "columns" : [],
                    "rows" : []
                }

                for columna in conexionDB._getColumnsFrom(table):
                    data["columns"].append(
                        ft.DataColumn(ft.Text(f"{columna[0]}"))
                    )

                for row in conexionDB._getRowsFrom(table, limit):
                    data["rows"].append(
                        ft.DataRow(cells = [ft.DataCell(ft.Text(f"{cell}")) for cell in row])
                    )

                return data

            def updateWindow(e):
                if(int(limitConsult.value) <= 0):
                    limitConsult.value = 1

                table_data.columns = tableData(dropdown_tables.value, limitConsult.value)["columns"]
                table_data.rows = tableData(dropdown_tables.value, limitConsult.value)["rows"]
                page.update()

            def exitToDatabases(e):
                page.go("/databases")
            
            limitConsult = ft.TextField(
                label = "Limite",
                max_length= 3,
                value= 50,
                on_submit= updateWindow,
                width= 100
            )

            dropdown_tables = ft.Dropdown(
                options= [
                    ft.dropdown.Option(f"{table}") for table in conexionDB._getTablesData()
                ],
                on_change= updateWindow,
                label= "Tabla",
                expand= True,
                prefix_icon= ft.icons.TABLE_VIEW,
            )

            table_data = ft.DataTable(
                columns= tableData(dropdown_tables.value, limitConsult.value)["columns"],
                rows= tableData(dropdown_tables.value, limitConsult.value)["rows"],
                expand = True,
                width=600,
            )

            page.views.append(
                ft.View("/panel", [
                ft.Row( controls=[
                    dropdown_tables,
                    limitConsult
                ]),

                ft.Row([
                    table_data
                ],
                    expand= True
                ),

                ft.Row(controls=[
                        ft.FilledButton(icon= ft.icons.EXIT_TO_APP, on_click= exitToDatabases, text="Panel")
                    ])
                ],
                horizontal_alignment= ft.CrossAxisAlignment.CENTER
            ))
        
        else:
            page.go("/")

        page.update()

    login_frame = ft.Column(
        width= 600,
        controls= [
            ft.Row(controls= [
                ft.Text(
                    "Inicio de sesion", 
                    text_align= ft.TextAlign.CENTER,
                    size= 20,
                    expand= True
                )]
            ),

            ft.Column( controls= [
                    entry_user,
                    entry_pass
                ]
            ),

            ft.Row( controls= [
                ft.FilledButton(
                    icon= ft.icons.SEND,
                    text= "Continuar",
                    on_click= connectToDatabase,
                    autofocus= True
                )],
                alignment= ft.MainAxisAlignment.CENTER
            )
        ],
    )

    page.window_height = 400
    page.window_width = 720

    page.on_route_change = routeChange
    page.on_viewPop = viewPop

    page.go(page.route)

ft.app(main)