from fastapi import APIRouter
from modelos.papel import Papel
from modelos.solicitacoes.atualiza_papel import AtualizarPapel
from controle.uteis.adicionar_controle import adicionar_controle
from controle.uteis.modificar_controle import modificar_controle
from controle.uteis.pegar_controle import pegar_controle
from controle.uteis.pegar_tudo_controle import pegar_tudo_controle
from controle.uteis.deletar_controle import deletar_controle


rota = APIRouter()  # isso cria uma rota para a criação do @app que já foi criado no main



# NOTA: esse banco de dados e feito de forma assincrona então vamos adiconar o "async"


@rota.post('/')
@adicionar_controle  # esse aqui não passamos papel como parametro
async def adicionar_papel(entidade: Papel):
    pass
# na coluna de "papel" mós passamos o "id" do papel que queremos relacionar
# na coluna "horario" pode colocar da sequinte forma: "2022-01-02T12:00:00"


@rota.get('/')
@pegar_tudo_controle(Papel)
async def listar_papeis():
    pass


@rota.get('/{id}')
@pegar_controle(Papel)
async def pegar_papel(id: int):
    pass


@rota.patch('/{id}')
@modificar_controle(Papel)
async def modificar_papel(propriedades_atualizacao: AtualizarPapel, id: int):
    pass


@rota.delete('/{id}')
@deletar_controle(Papel)  # a entidade que ele está trabalhando é Papel, lá da pasta solicitacoes
async def deletar_papel(id: int):
    pass
