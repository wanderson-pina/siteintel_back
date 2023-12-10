from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Amostra, Model
from logger import logger
from schemas import *
from flask_cors import CORS



# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
amostra_tag = Tag(name="Amostra", description="Adição, visualização, remoção e predição de amostras potaveis")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de amostras
@app.get('/amostras', tags=[amostra_tag],
         responses={"200": AmostraViewSchema, "404": ErrorSchema})
def get_amostras():
    """Lista todas as amostras cadastradas na base
    Retorna uma lista de amostras cadastradas na base.
    
    Args:
        cod (str): lote da amostra
        
    Returns:
        list: lista de amostras cadastradas na base
    """
    session = Session()
    
    # Buscando todas as amostras
    amostras = session.query(Amostra).all()
    
    if not amostras:
        logger.warning("Não há amostras cadastradas na base :/")
        return {"message": "Não há amostras cadastradas na base :/"}, 404
    else:
        logger.debug(f"%d amostras econtrados" % len(amostras))
        return apresenta_amostras(amostras), 200


# Rota de adição de amostra
@app.post('/amostra', tags=[amostra_tag],
          responses={"200": AmostraViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: AmostraSchema):
    """Adiciona uma nova amostra à base de dados
    Retorna uma representação das amostras e diagnósticos associados.
    
    Args:
        lote (str): lote da amostra
        aph (float): ph da agua: ph
        hard (float): dureza da agua: Hardness
        soli (float): indice de solidos na agua: Solids
        chlo (float): indice de cloro: Chloramines
        sulf (float): indice de sulfato: Sulfate
        condu (float): condutibidade da agua: Conductivity
        organ (float): indice de carbono organico: Organic_carbon
        triha (float):  indice de trihalometanos (residuos cancerigenos): Trihalomethanes
        turbi (float): turvacao: Turbidity
        
    Returns:
        dict: representação da amostra e diagnóstico associado
    """                   
      

    # Carregando modelo
    ml_path = 'ml_model/modelwaterb.pkl'
    modelo = Model.carrega_modelo(ml_path)

   # Chamar preditor
    Model.preditor(modelo, form)    
   

    amostra = Amostra(
        lote=form.lote.strip(),
        aph=form.aph,
        hard=form.hard,
        soli=form.soli,
        chlo=form.chlo,
        sulf=form.sulf,
        condu=form.condu,
        organ=form.organ,
        triha=form.triha,
        turbi=form.turbi,
        potability=Model.preditor(modelo, form)
    )
    logger.debug(f"Adicionando produto de nome: '{amostra.lote}'")
   

    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se amostra já existe na base
        if session.query(Amostra).filter(Amostra.lote == form.lote).first():
            error_msg = "Amostra já existente na base :/"
            logger.warning(f"Erro ao adicionar amostra '{amostra.lote}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando amostra
        session.add(amostra)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado amostra de lote: '{amostra.lote}'")
        return apresenta_amostra(amostra), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar amostra '{amostra.lote}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em codigo
# Rota de busca de amostra por codigo
@app.get('/amostra', tags=[amostra_tag],
         responses={"200": AmostraViewSchema, "404": ErrorSchema})
def get_amostra(query: AmostraBuscaSchema):    
    """Faz a busca por uma amostra cadastrada na base a partir do codigo

    Args:
        cod (str): lote da amostra
        
    Returns:
        dict: representação da amostra e diagnóstico associado
    """
    
    amostra_cod = query.lote
    logger.debug(f"Coletando dados sobre produto #{amostra_cod}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    amostra = session.query(Amostra).filter(Amostra.lote == amostra_cod).first()
    
    if not amostra:
        # se a amostra não foi encontrada
        error_msg = f"Amostra {amostra_cod} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{amostra_cod}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Amostra econtrado: '{amostra.lote}'")
        # retorna a representação da amostra
        return apresenta_amostra(amostra), 200
   
    
# Rota de remoção de amostra por codigo
@app.delete('/amostra', tags=[amostra_tag],
            responses={"200": AmostraViewSchema, "404": ErrorSchema})
def delete_amostra(query: AmostraBuscaSchema):
    """Remove uma amostra cadastrada na base a partir do codigo

    Args:
        cod (str): lote da amostra
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    amostra_cod = unquote(query.lote)
    logger.debug(f"Deletando dados sobre amostra #{amostra_cod}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando amostra
    amostra = session.query(Amostra).filter(Amostra.lote == amostra_cod).first()
    
    if not amostra:
        error_msg = "Amostra não encontrada na base :/"
        logger.warning(f"Erro ao deletar amostra '{amostra_cod}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(amostra)
        session.commit()
        logger.debug(f"Deletado amostra #{amostra_cod}")
        return {"message": f"Amostra {amostra_cod} removido com sucesso!"}, 200