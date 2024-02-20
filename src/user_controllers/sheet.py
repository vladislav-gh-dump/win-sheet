import flet as ft
from dataclasses import dataclass
from src.clerk import Clerk


@dataclass
class SheetViewerSettings:
    extension_set: ft.MarkdownExtensionSet | str


@dataclass
class SheetEditorSettings:
    multiline: bool
    text_size: ft.OptionalNumber
    hint_text: str
    min_lines: int
    
    
@dataclass
class SheetControllerSettings:
    ...
    

class SheetController(ft.UserControl):
    
    def __init__(self, page: ft.Page):
        super().__init__()
        
        self.__btn_edit = ft.ElevatedButton("Edit", on_click=self.click_edit)
        self.__btn_save = ft.ElevatedButton("Save", on_click=self.click_save)
        self.__btn_go_prev = ft.ElevatedButton("<", on_click=self.click_go_prev)
        self.__btn_go_next = ft.ElevatedButton(">", on_click=self.click_go_next)
        
        self.__controllers = ft.Row([
            self.__btn_edit, 
            self.__btn_save, 
            self.__btn_go_prev, 
            self.__btn_go_next
        ])
        
        
        viewer_settings = SheetViewerSettings(extension_set="gitHubWeb")
        self.__viewer = ft.Markdown(
            extension_set=viewer_settings.extension_set,
            on_tap_link=lambda e: page.launch_url_async(e.data)
        )
        
        
        self.__is_editing = False
        editor_settings = SheetEditorSettings(
            multiline=True, 
            text_size=14,
            hint_text="Please enter text here",
            min_lines=24
        )
        self.__editor = ft.TextField(
            multiline=editor_settings.multiline, 
            text_size=editor_settings.text_size,
            hint_text=editor_settings.hint_text,
            min_lines=editor_settings.min_lines,
            on_change=self.change_text
        )
        
        
        self.__clerk = Clerk()
        self.__clerk.load()
        self.__editor.value = self.__clerk.get_text()
        self.__viewer.value = self.__editor.value
        
        
        self.__sheets = ft.Row([
            self.__contain(self.__viewer, padding=12,
                           border=ft.border.all(1, ft.colors.BLACK), border_radius=5)
        ])
        self.__sheet_objects = ft.Column([
            self.__controllers,
            self.__sheets
        ])
        
    def __contain(self, item, padding = None, border = None, border_radius = None):
        return ft.Container(item, width=300, height=420, padding=padding, border=border, border_radius=border_radius)
    
    async def click_edit(self, e):
        if not self.__is_editing:
            self.__is_editing = True
            self.__clerk.load()
            self.__editor.value = self.__clerk.get_text()
            self.__viewer.value = self.__editor.value
            
            self.__sheet_objects.controls[1].controls = [
                self.__contain(self.__editor),
                self.__contain(self.__viewer, padding=12,
                            border=ft.border.all(1, ft.colors.BLACK), border_radius=5)
            ]
            
            await self.update_async()
        
    async def click_save(self, e):
        if self.__is_editing:
            self.__is_editing = False
            self.__editor.value = self.__clerk.get_text()
            self.__viewer.value = self.__editor.value
            self.__clerk.save()
            
            self.__sheet_objects.controls[1].controls = [
                self.__contain(self.__viewer, padding=12,
                            border=ft.border.all(1, ft.colors.BLACK), border_radius=5)
            ]
            
            await self.update_async()
        
    async def click_go_prev(self, e):
        if self.__is_editing:
            self.__clerk.go_prev_text()
            self.__editor.value = self.__clerk.get_text()
            self.__viewer.value = self.__editor.value
            
            await self.update_async()
        
    async def click_go_next(self, e):
        if self.__is_editing:
            self.__clerk.go_next_text()
            self.__editor.value = self.__clerk.get_text()
            self.__viewer.value = self.__editor.value
            
            await self.update_async()
            
    async def change_text(self, e):
        self.__clerk.write(e.data)
        self.__viewer.value = self.__editor.value
            
        await self.update_async()
    
    def build(self):
        return self.__sheet_objects