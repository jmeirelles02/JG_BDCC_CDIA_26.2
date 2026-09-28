# AP1 — Lavoura Inteligente

## 1. Requisitos e estrutura

A [versão publicada da AP1](https://jonh-carvalho.github.io/BDCC_CDIA_26.2_8001/Avalia/ap1/#cenario) pede duas classes relacionadas ao tema, um app com nome relacionado ao tema, acesso ao Django Admin e deploy com `app.zip`. Para a pontuação integral, o nome do projeto Django também deve acompanhar o tema.

A implementação fica em `src/DeployEB`:

| Item | Nome |
| --- | --- |
| Projeto Django | `lavouraInteligente_JG` |
| App Django | `lavouras` |
| Classes | `Talhao` e `Lote` |
| Aplicação AWS Elastic Beanstalk | `lavouraInteligente_JG` |
| Ambiente AWS recomendado | `lavouraInteligente-JG-env` |

Um talhão pode possuir vários lotes. Cada lote referencia exatamente um talhão. A geometria é armazenada como JSON; esta etapa não executa análises espaciais ou decisões automáticas de conformidade.

## 2. Arquivos alterados

- `manage.py`: utiliza `lavouraInteligente_JG.settings`.
- `lavouraInteligente_JG/settings.py`: registra o app `lavouras`, configura banco SQLite, hosts, arquivos estáticos e variáveis de ambiente.
- `lavouraInteligente_JG/urls.py`: publica health check, Admin e APIs.
- `lavouraInteligente_JG/wsgi.py` e `asgi.py`: carregam o novo módulo de settings.
- `lavouras/models.py`: contém os dois modelos relacionados.
- `lavouras/serializers.py`, `views.py` e `urls.py`: expõem os campos atuais e as operações da API.
- `lavouras/admin.py`: registra os modelos no Admin.
- `lavouras/apps.py`: configura `LavourasConfig`.
- `lavouras/migrations/0001_initial.py`: migração gerada pelo comando do Django.
- `lavouras/management/commands/bootstrap_admin.py`: cria o administrador no deploy por variáveis de ambiente, sem SSH, preservando contas existentes.
- `Procfile`, `.ebextensions/django.config` e `.elasticbeanstalk/config.yml`: apontam para os novos nomes.
- `requirements.txt`: dependências do servidor Django; `requirements-docs.txt`: dependências da documentação.
- O workflow MkDocs instala `requirements-docs.txt`.
- `empacotar.py`: gera o ZIP para o Beanstalk.

Os pacotes e o banco anteriores foram arquivados em um backup local em `src/.task-backups/`, fora do repositório do projeto e do ZIP. A pasta RestEB permanece como o exemplo original da disciplina.

## 3. Modelos e endpoints

`Talhao` contém código único, nome, cultura, produtor, geometria JSON e data de criação.

`Lote` contém código único, talhão de origem, status e data de criação. Os status aceitos são `APROVADO`, `REVISAO` e `BLOQUEADO`; o padrão é `REVISAO`.

| Endereço | Uso |
| --- | --- |
| `/` | Health check: retorna HTTP 200 |
| `/admin/` | Interface administrativa com login |
| `/api/talhoes/` | Listar e cadastrar talhões |
| `/api/talhoes/<id>/` | Consultar, editar e excluir talhão |
| `/api/lotes/` | Listar e cadastrar lotes |
| `/api/lotes/<id>/` | Consultar, editar e excluir lote |

As operações de API seguem a configuração de acesso do protótipo. O Admin exige autenticação. Um talhão com lotes vinculados não pode ser excluído; a API retorna HTTP 400 nessa tentativa.

## 4. Preparar e iniciar localmente

No PowerShell:

```powershell
cd "C:\Users\dtdev1\Documents\Ibmec\BDCC_CDIA_26.2_8001\src\DeployEB"
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

O ambiente virtual e o banco local já estão preparados nesta máquina. Para iniciar agora, basta executar o último comando a partir de DeployEB. Mantenha o terminal aberto e acesse `http://127.0.0.1:8000/admin/`.

O administrador local é `dtdev1`, com a senha definida pelo usuário durante a configuração, sem espaço no final. Sua conta e o hash da senha foram preservados na reorganização do banco. Use Ctrl+C para parar o servidor.

Para criar um administrador em outra instalação:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser --username dtdev1
```

## 5. Migrações realizadas por comando

Foi feito backup do banco antigo. Suas tabelas de negócio estavam vazias. O banco local foi reconstruído com o novo app, preservando a conta administrativa existente.

Comandos executados:

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations lavouras
.\.venv\Scripts\python.exe manage.py migrate --noinput
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py showmigrations lavouras
```

O resultado é `[X] 0001_initial` no app `lavouras`. As migrações do Django também estão aplicadas. Não edite migrações aplicadas; mudanças futuras nos modelos devem gerar novas migrações.

## 6. Teste manual do Admin e da API

1. Inicie o servidor e entre em `/admin/`.
2. Cadastre um talhão.
3. Cadastre um lote selecionando o talhão criado.
4. Consulte `/api/talhoes/` e `/api/lotes/`.
5. Edite o status do lote e confira a resposta da API.
6. Para excluir um talhão, exclua seus lotes primeiro.

Exemplo para cadastrar um talhão:

```json
{
  "codigo": "TALHAO-001",
  "nome": "Área norte",
  "cultura": "Soja",
  "produtor": "Produtor exemplo",
  "geometria": {
    "type": "Polygon",
    "coordinates": [[[-47, -22], [-47.01, -22], [-47.01, -22.01], [-47, -22]]]
  }
}
```

Exemplo para cadastrar um lote, usando o ID real do talhão:

```json
{
  "codigo": "LOTE-001",
  "talhao": 1,
  "status": "REVISAO"
}
```

## 7. Nomes do Beanstalk e configurações

Em `.elasticbeanstalk/config.yml`, `global.application_name` identifica a aplicação AWS usada pela EB CLI. Está configurado como `lavouraInteligente_JG`. Se escolher outro nome na AWS, altere esse campo para o nome exato escolhido.

`branch-defaults.main.environment` identifica o ambiente, configurado como `lavouraInteligente-JG-env`. Aplicação AWS e ambiente são recursos distintos.

O ambiente usa hífens porque a AWS não permite `_` nesse nome. O projeto Django e a aplicação AWS usam `lavouraInteligente_JG`.

Para upload manual pelo console, selecione a aplicação e o ambiente desejados; `config.yml` é a configuração local da EB CLI e não é usado pelo console para escolher o destino do ZIP.

O nome do arquivo `django.config` não precisa corresponder ao nome da aplicação AWS. Seu `WSGIPath` aponta para `lavouraInteligente_JG.wsgi:application`, e `DJANGO_SETTINGS_MODULE` aponta para `lavouraInteligente_JG.settings`. O `Procfile` usa o mesmo módulo WSGI e a porta 8000.

Referências oficiais: [configuração da EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-configuration.html), [Django no Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html) e [Procfile Python](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-configuration-procfile.html).

## 8. Configuração antes do deploy

Selecione Python 3.12 no Beanstalk. Não é necessário cadastrar `DJANGO_SECRET_KEY`. Para criar o administrador sem SSH, cadastre `DJANGO_SUPERUSER_USERNAME=adminJG` e `DJANGO_SUPERUSER_PASSWORD` com uma senha forte nas propriedades do ambiente antes de enviar o ZIP atualizado. O e-mail é opcional: omita ou remova `DJANGO_SUPERUSER_EMAIL` para criar a conta com e-mail vazio.

`DJANGO_DEBUG=False` já está definido em django.config. O primeiro comando do deploy gera uma chave aleatória em `/var/app/django-secrets/secret-key`, com permissões 600, em uma pasta com permissões 700, pertencente a `webapp`. Esse arquivo fica fora do código e do ZIP. Novos deploys na mesma instância reutilizam a chave existente. O Django lê esse arquivo quando DEBUG é False; a variável `DJANGO_SECRET_KEY` continua como alternativa opcional.

No console, abra **Elastic Beanstalk → ambiente → Configuração → Atualizações, monitoramento e registro → Editar → Propriedades do ambiente**. Adicione as duas variáveis, aplique e aguarde a atualização. A criação automática usa as propriedades do ambiente e não precisa de par de chaves EC2.

`DJANGO_ALLOWED_HOSTS` é opcional: por padrão aceita localhost e domínios `.elasticbeanstalk.com`. Para um domínio próprio, acrescente o hostname. `DJANGO_CSRF_TRUSTED_ORIGINS` pode receber a URL completa caso seja necessário usar um domínio ou origem adicional.

Não grave a senha administrativa ou a chave secreta em arquivos versionados.

## 9. Empacotar e publicar

A partir de DeployEB:

```powershell
.\.venv\Scripts\python.exe empacotar.py
```

Envie o `app.zip` produzido à aplicação `lavouraInteligente_JG`. O ZIP contém `manage.py`, `Procfile`, `requirements.txt`, `.ebextensions/`, `lavouraInteligente_JG/` e `lavouras/`, com os arquivos na raiz e sem pasta pai.

São excluídos banco local, ambiente virtual, caches, backups, documentação e credenciais. A configuração `.elasticbeanstalk/config.yml` fica no repositório local para uso da EB CLI, fora do ZIP.

Durante o deploy, django.config executa:

1. `migrate --noinput`;
2. `bootstrap_admin`, que cria a conta administrativa quando configurada;
3. `collectstatic --noinput`;
4. ajuste das permissões do SQLite para o usuário da aplicação.

Antes desses comandos, o deploy gera ou reutiliza a chave privada descrita na seção 8.

Todos os comandos seguem a ordem numérica, sem `leader_only`, pois o ambiente usa SingleInstance. No Beanstalk, comandos com `leader_only` seriam executados antes dos demais, mesmo quando seu nome tem número posterior; isso faria a migração preceder a criação da chave. Os comandos Python ativam explicitamente `/var/app/venv/*/bin/activate` antes de executar. Referência: [ordem dos container commands](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html#linux-container-commands).

Depois do deploy, acesse `http://ENDERECO-DO-BEANSTALK/admin/` com o usuário `adminJG` e a senha definida nas propriedades do ambiente. O usuário só estará disponível após um deploy bem-sucedido com usuário e senha configurados.

O comando preserva qualquer usuário existente com o mesmo nome, sem alterar senha ou permissões. Sem nenhuma variável de criação, ignora a criação. Se precisar criar uma conta, exige usuário válido e senha aprovada pelos validadores do Django; o e-mail é validado somente se informado. Erros interrompem o deploy sem registrar os valores das credenciais. Alterar a variável de senha não redefine a senha de uma conta existente.

O protótipo está configurado como SingleInstance. O SQLite permanece no disco da instância e pode ser perdido em substituições ou novos deployments. Manter as duas variáveis permite recriar o administrador em um banco novo. Se remover as variáveis de criação após o cadastro, será necessário configurar usuário e senha novamente quando precisar recriar a conta. A chave interna do Django também é recriada se a instância for substituída. O ZIP não contém banco nem credenciais locais.

Referências: [propriedades do ambiente Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html) e [validação de senhas Django](https://docs.djangoproject.com/en/6.0/topics/auth/passwords/#password-validation).

## 10. Verificações e entrega

Na conferência final, o app.zip foi extraído em pasta temporária e testado com banco vazio: migrações, collectstatic (incluindo CSS do Admin), importação WSGI, cadastro e consulta pela API, proteção do talhão com lote e login administrativo passaram. O teste usou DEBUG=False com o arquivo privado simulado, sem alterar o banco local. Também foram conferidos os 20 arquivos do ZIP contra as fontes, a ausência dos pacotes antigos, a ordem dos comandos YAML e `pip check`. O ambiente Linux e os serviços AWS ainda precisam ser validados após publicar.

Após a renomeação para `lavouraInteligente_JG`, foram conferidos: `manage.py check`, ausência de novas migrações e `[X] 0001_initial`; sintaxe YAML; integridade do ZIP de 20 arquivos, sem banco local e sem o antigo pacote; geração e reutilização da chave em arquivo temporário; importação WSGI com DEBUG=False e leitura do arquivo privado simulada. As URLs de API e o login Admin também foram verificados localmente. Os comandos Linux do deploy e do SSH ainda precisam ser confirmados na instância AWS.

A verificação local cobre cadastro, consulta, edição e exclusão dos dois modelos, integridade do relacionamento, login e páginas administrativas, consistência das migrações e coleta dos arquivos estáticos. Os registros usados nos testes são revertidos ao final.

DeployEB possui seu próprio repositório Git. Para preparar as alterações:

```powershell
git add .
```

Banco local, ZIP, ambiente virtual e arquivos estáticos gerados são ignorados pelo Git. Os integrantes já estão listados no README; confira os nomes antes de entregar.

Ainda é necessário publicar na AWS, conferir o status do ambiente, testar as URLs publicadas, preencher o link real da API no README e adicionar o professor como colaborador. A validação local não representa um deploy AWS concluído.
