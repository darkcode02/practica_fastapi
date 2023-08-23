from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="notes", version="0.0.1")

class Note(BaseModel):
    id_note: int = Field(default_factory=lambda: current_id, description="ID of the note")
    title: str = Field(..., min_length=5, max_length=15, description="Title of the note")
    content: str = Field(..., min_length=5, max_length=500, description="Content of the note")
    content_at: str = Field(..., min_length=1, max_length=15, description="Content date")

    class Config:
        schema_extra = {
            "example": {
                "id_note": 0,
                "title": "mi nota",
                "content": "contenido de esta nota",
                "content_at": "fecha"
            }
        }

notes = [
    {
       "id_note": 0,
       "title": "mi viaje",
       "content": "la historia de cómo viajé a Europa y conseguí trabajo",
       "content_at": "25 marzo 2023"
    }
]

current_id = 1  # Initialize with the last used id_note

@app.get('/', response_class=HTMLResponse, tags=['Home'])
def message():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App de Notas</title>
    <style>
        /* Estilos generales */
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            color: #333;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        header {
            background-color: #f0f0f0;
            padding: 20px;
            text-align: center;
            color: #333;
        }

        main {
            padding: 20px;
            text-align: center;
            background-color: #fff;
            max-width: 800px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        footer {
            text-align: center;
            padding: 10px;
            background-color: #f0f0f0;
        }

        p {
            font-size: 18px;
            line-height: 1.6;
            color: #555;
        }

        h1 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #333;
        }

        a {
            color: #ffcc00;
            text-decoration: none;
            transition: color 0.3s ease-in-out;
        }

        a:hover {
            color: #e6b800;
        }
    </style>
</head>
<body>
    <header>
        <h1>App de Notas</h1>
    </header>
    <main>
        <p>Bienvenido a la <strong>App de Notas</strong>. Aquí puedes organizar y gestionar tus notas de manera eficiente. Dirígete a la ruta <a href="/docs">/docs</a> para ver la documentación con Swagger.</p>
    </main>
    <footer>
        <p>&copy; 2023 App de Notas. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
"""

@app.post('/notes', tags=['notes'], response_model=dict, status_code=201)
def create_note(note: Note) -> dict:
    global current_id
    note.id_note = current_id
    current_id += 1  # Increment the id_note
    notes.append(note.dict())
    return {"message": "Se ha registrado la nota"}

@app.get('/notes', tags=['notes'], response_model=List[Note], status_code=200)
def get_notes() -> List[Note]:
    return notes

@app.get('/notes/{id_note}', tags=['notes'], response_model=Note)
def get_note(id_note: int = Path(..., ge=1, le=2000)) -> Note:
    for item in notes:
        if item["id_note"] == id_note:
            return item
    raise HTTPException(status_code=404, detail="Nota no encontrada")

@app.put('/notes/{id_note}', tags=['notes'], response_model=dict, status_code=200)
def update_note(id_note: int, note: Note) -> dict:
    for item in notes:
        if item["id_note"] == id_note:
            item.update(note.dict())
            return {"message": "Se ha modificado la nota"}
    raise HTTPException(status_code=404, detail="Nota no encontrada")

@app.delete('/notes/{id_note}', tags=['notes'], response_model=dict, status_code=200)
def delete_note(id_note: int) -> dict:
    for item in notes:
        if item["id_note"] == id_note:
            notes.remove(item)
            return {"message": "Se ha eliminado la nota"}
    raise HTTPException(status_code=404, detail="Nota no encontrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
