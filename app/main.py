from fastapi import FastAPI
from app.routes import grades
import logging
from reactpy import html, component
from reactpy.backend.fastapi import configure

app = FastAPI()

app.include_router(grades.router, prefix="/api/v1")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

def Module(props):
    return html.li(
        {"key": props['id'], "style": modules_style},
        f"{props['text']}",
        html.button({"style": button_style, "onclick": lambda: handle_click(props['id'])}, f"{props['action']}")
    )


modules_style = {
    "background": "skyblue",
    "padding": "1rem",
    "border": "1px solid black",
    "margin": "2rem",
}
button_style = {
    "margin-left": "1rem",
    "padding": "0.5rem",
    "background": "yellow",
    "border": "none",
    "cursor": "pointer",
}


def handle_click(module_id):
    print(f"Modulo con id {module_id} fue seleccionado.")

@component
def ModulesList():
    modules = [
        {"id": 0, "text": "Registrar calificación", "action": "Registar"},
        {"id": 1, "text": "Ver calificaciones por parallel_id", "action": "Visualizar"},
        {"id": 2, "text": "Ver calificaciones por course_id", "action": "Visualizar"},
        {"id": 3, "text": "Consultar calificación por grade_id", "action": "Consultar"},
        {"id": 4, "text": "Eliminar calificación por grade_id", "action": "Eliminar"},
        {"id": 5, "text": "Ver calificaciones de un estudiante por student_id", "action": "Visualizar"},
        {"id": 6, "text": "Ver calificaciones por course_id", "action": "Visualizar"},
        {"id": 7, "text": "Actualizar calificación por course_id", "action": "Actualizar"},
    ]
    return html.ul([Module(module) for module in modules])




@component
def App():
    return html.div(
        {"style": {
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",  # Centra el contenido horizontalmente
            "justify-content": "center",  # Centra el contenido verticalmente
            "min-height": "100vh",  #  Altura de la ventana
            "text-align": "center",
            "font-family": "Arial, sans-serif"
        }},
        html.h1("Módulo de Calificaciones"),
        ModulesList()
    )
configure(app, App)


