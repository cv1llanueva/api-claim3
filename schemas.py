from pydantic import BaseModel
#from datetime import date

class Claim(BaseModel):
    poliza_id: int
    descripcion: str
    monto: float