import flet as ft
from src.user_controllers.sheet import SheetController


async def main(page: ft.Page):
    async def page_close(e):
        await page.window_close_async()
    
    
    # параметры окна
    page.window_min_width = 330
    page.window_min_height = 540
    
    page.window_width = 330
    page.window_height = 540
    
    page.window_max_width = 640
    page.window_max_height = 540
    
    page.window_title_bar_hidden = True

    
    # элементы окна
    window_drag_area = ft.WindowDragArea(
        ft.Container(
            ft.Text("Sheet"),
            bgcolor=ft.colors.AMBER_300, padding=12
        ), expand=True
    )
    btn_close_window = ft.IconButton(ft.icons.CLOSE, on_click=page_close)
    sheet_controller = SheetController(page)
    
    await page.add_async(
        ft.Column([
            ft.Row([window_drag_area, btn_close_window]),
            sheet_controller
        ])
    )

ft.app(target=main)
