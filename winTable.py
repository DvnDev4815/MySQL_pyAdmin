import flet as ft
from mydb import dataBase

conexionDB = dataBase()

def main(page : ft.Page, id_database : str):
    conexionDB._validateData(
        page.client_storage.get("creds")[0],
        page.client_storage.get("creds")[1],
    )

    if not conexionDB._selectDataBase(id_database):
        page.go("/databases")

    def tableData(table : str, limit : str):
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
                ft.DataRow([ft.DataCell(ft.Text(f"{cell}")) for cell in row])
            )

        return data

    def updateWindow(e):
        if(int(limitConsult.value) <= 0):
            limitConsult.value = 1

        table_data.columns = tableData(dropdown_tables.value, limitConsult.value)["columns"]
        table_data.rows = tableData(dropdown_tables.value, limitConsult.value)["rows"]
        page.update()

    def exitWindow(e):
        page.go("/databases")

    limitConsult = ft.TextField(
        on_submit= updateWindow,
        label= "Limite",
        max_length= 3,
        width= 100,
        value= 50,
    )

    dropdown_tables = ft.Dropdown(options=[ft.dropdown.Option(f"{table}") for table in conexionDB._getTablesData()],
        prefix_icon= ft.icons.TABLE_VIEW,
        on_change= updateWindow,
        label= "Tabla",
        expand= True,
    )

    table_data = ft.DataTable(
        columns= tableData(dropdown_tables.value, limitConsult.value)["columns"],
        rows= tableData(dropdown_tables.value, limitConsult.value)["rows"],
        expand= True,
        width= 600
    )

    return ft.View("/panel", 
        [
            ft.Row([
                dropdown_tables,
                limitConsult
            ]),
            
            ft.Row([table_data]),

            ft.Row([
                ft.FilledButton(
                    on_click= exitWindow,
                    icon= ft.icons.EXIT_TO_APP,
                    text= "Panel",
                )
            ])
        ]
    )