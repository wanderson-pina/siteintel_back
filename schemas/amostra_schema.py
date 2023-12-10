from pydantic import BaseModel
from typing import Optional, List
from model.amostra import Amostra
import json
import numpy as np

class AmostraSchema(BaseModel):
    """ Define como uma nova amostra a ser inserida deve ser representada
    """
    lote: str = "A001"
    aph: float = 7.65
    hard: float = 200.52
    soli: float = 21754.70
    chlo: float = 6.17
    sulf: float = 325.65
    condu: float = 374.48
    organ: float = 14.37
    triha: float = 67.90
    turbi: float = 3.55
    
class AmostraViewSchema(BaseModel):
    """Define como uma amostra será retornada
    """
    id: int = 1
    lote: str = "A001"
    aph: float = 7.65
    hard: float = 200.52
    soli: float = 21754.70
    chlo: float = 6.17
    sulf: float = 325.65
    condu: float = 374.48
    organ: float = 14.37
    triha: float = 67.90
    turbi: float = 3.55
    potability: int = None
    
class AmostraBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no lote da amostra.
    """
    lote: str = "A001"

class ListaAmostrasSchema(BaseModel):
    """Define como uma lista de amostras será representada
    """
    amostras: List[AmostraSchema]

    
class AmostraDelSchema(BaseModel):
    """Define como uma amostra para deleção será representada
    """    
    lote: str = "A001"

# Apresenta apenas os dados de uma amostra  
def apresenta_amostra(amostra: Amostra):
    """ Retorna uma representação de uma amostra de acordo com o schema definido em
        AmostraViewSchema.
    """
    return {
        "id": amostra.id,
        "lote": amostra.lote,
        "aph": amostra.aph,
        "hard": amostra.hard,
        "soli": amostra.soli,
        "chlo": amostra.chlo,
        "sulf": amostra.sulf,
        "condu": amostra.condu,
        "organ": amostra.organ,
        "triha": amostra.triha,
        "turbi": amostra.turbi,
        "potability": amostra.potability
    }
    

# Apresenta uma lista de amostras
def apresenta_amostras(amostras: List[Amostra]):
    """ Retorna uma representação da amostra seguindo o schema definido em
        AmostraViewSchema.
    """
    result = []
    for amostra in amostras:
        result.append({
           "id": amostra.id,
           "lote": amostra.lote,
           "aph": amostra.aph,
           "hard": amostra.hard,
           "soli": amostra.soli,
           "chlo": amostra.chlo,
           "sulf": amostra.sulf,
           "condu": amostra.condu,
           "organ": amostra.organ,
           "triha": amostra.triha,
           "turbi": amostra.turbi,
           "potability": amostra.potability   
           
        })

    return {"amostras": result}

