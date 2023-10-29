import winLogin, winDataB, winTable
import flet as ft

def main(page : ft.Page):
    def viewPop(e):
        page.views.pop()
        page.go(page.views[-1].route)

    def routeChange(e):
        RTemplate_main = ft.TemplateRoute(page.route)
        page.views.clear()

        if RTemplate_main.match("/"):
            page.views.append(winLogin.main(page))

        elif RTemplate_main.match("/databases"):
            page.views.append(winDataB.main(page))

        elif RTemplate_main.match("/databases/:database_id/panel"):
            page.views.append(winTable.main(page, RTemplate_main.database_id))
            
        
        page.update()

    page.on_route_change = routeChange
    page.on_view_pop = viewPop
    page.window_height = 400
    page.window_width = 720

    page.go(page.route)

if __name__ == "__main__":
    ft.app(main)