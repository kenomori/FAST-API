from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # aqui ta dizendo que vai fazer um ligin por senha e o tipo de login é Bearer
from jose import jwt
from pydantic import BaseModel, ValidationError

from modelos.usuario import Usuario
from seguranca import SECRET_KEY, JWT_ALGORITHM


# aqui ele vai puxar o token caso o sub n tenho ele vai colocar o valor none como padrão
class TokenPayload(BaseModel):
    sub: Optional[int] = None


# isso aqui é para dizer que tipo de login eu estou usando,
reusable_oauth2 = OAuth2PasswordBearer(
    # aqui ele vai criar um sistema de login na parte de cima do fastAPI para manter o token
    tokenUrl="/usuarios/login"  # aqui estamos dizendo q o endpoint de login e esse
)


# metodo para pegar usuario logado no momento
async def pegar_usuario_logado(
    token: str = Depends(reusable_oauth2)  # essa string q ele vai receber é o token que está na requicição
) -> Usuario:
    try:
        payload = jwt.decode(
            # aqui ele vai decodificar o token usando a senha que colocamos e com o algoritimo
            # então vamos validar o arquivo
            token, SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        # se der certo vamos colocar os dados do tokendata dentro do token
        # se der certo significa que o token está valido, se n der certo ele vai pro o JWTError ou ValidationError
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possivel validar as credencias do usuario",
        )
    # o token sendo valido ele vai vir procurar o usuario que tenha o mesmo ID, q está no mesmo token
    user = await Usuario.objects.get_or_none(id=token_data.sub)
    # se der none ele vai dar um erro 404
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return user


# aqui temos a lista de funções que por padrão é uma lista vazia
# se eu entregar uma lista vazia eu quero q qualquer usuario logado possa entrar
def pegar_usuario_com_funcao(funcoes: List[str] = []):
    # o "Depends()" do fastAPI vai querer entregar alguma coisa chamavel
    # então vamos definir uma funçã interna que vai fazer a verificação
    # afim de saber se o usuario tem ou não a função
    # aqui ele vai aproveitar o "Depends()" para pegar o mesmo codigo do usuario logado
    def inner(usuario_logado: Usuario = Depends(pegar_usuario_logado)) -> Usuario:
        if not len(funcoes):  # se a lista for vazia, qualquer usuario pode acessar
            return usuario_logado

        for funcao in funcoes:  # se ela nã oestiver vazia
            # ela vai de função em função que tem dentro da lista "funcoes", para verificar se tem a
            # função dentro do usuario logado
            if funcao in usuario_logado.funcoes:
                return usuario_logado

        raise HTTPException(
            status_code=403, detail="O usuário não possui permissão para realizar essa ação!"
        )

    return inner
