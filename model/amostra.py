from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = ph,Hardness,Solids, Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity,Potability 

class Amostra(Base):
    __tablename__ = 'amostras'
    
    id = Column(Integer, primary_key=True)
    lote= Column("Lote", String(50))
    aph = Column("ph", Float)
    hard = Column("Hardness", Float)
    soli = Column("Solids", Float)
    chlo = Column("Chloramines", Float)
    sulf = Column("Sulfate", Float)
    condu = Column("Conductivity", Float)
    organ = Column("Organic_carbon", Float)
    triha = Column("Trihalomethanes", Float)
    turbi = Column("Turbidity", Float)
    potability = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, lote:str, aph:float, hard:float, soli:float,
                 chlo:float, sulf:float, condu:float, 
                 organ:float, triha:float, turbi:float, 
                 potability:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Amostra

        Arguments:
        lote: lote da amostra
            aph: ph da agua
            hard: dureza da agua
            soli: indice de solidos na agua
            chlo: indice de cloro
            sulf: indice de sulfato
            condu: condutibidade da agua
            organ: indice de carbono organico
            triha: indice de trihalometanos (residuos cancerigenos)
            turbi: turvacao
            potability: diagnóstico
            data_insercao: data de quando a amostra foi inserida à base
        """
        self.lote=lote
        self.aph = aph
        self.hard = hard
        self.soli = soli
        self.chlo = chlo
        self.sulf = sulf
        self.condu = condu
        self.organ = organ
        self.triha =  triha
        self.turbi = turbi
        self.potability = potability
        

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao