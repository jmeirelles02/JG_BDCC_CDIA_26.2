# Lavoura Inteligente — Plataforma de Telemetria Agrícola

## Sobre

A proposta da Lavoura Inteligente recebe leituras de sensores agrícolas, avalia
limiares de cada cultura e consolida dados para painéis e relatórios. A implementação
da AP1 contém a API de talhões e lotes, com SQLite. A arquitetura planejada prevê
PostgreSQL para o portal administrativo e DynamoDB para o fluxo de telemetria.

## Documentação local

```bash
pip install -r requirements-docs.txt
mkdocs build --strict
mkdocs serve
```

O pipeline valida o build estrito em pull requests e publica o site após mudanças na
branch `main`.

## Implementação da AP1

A API Django usa o projeto `lavouraInteligente_JG` e o app `lavouras`, com as classes
`Talhao` e `Lote`. Cada lote referencia o talhão de origem.

### Modificações realizadas

- Criados os modelos `Talhao` e `Lote`, sua migração inicial e o relacionamento entre eles.
- Implementadas as rotas REST com Django REST Framework para consultar e manter talhões e lotes.
- Registrados os modelos no Django Admin e adicionado um health check na raiz (`/`).
- Configurados SQLite, arquivos estáticos e os ajustes necessários para executar no AWS Elastic Beanstalk.
- Incluídos `Procfile`, configurações de deploy e `empacotar.py` para gerar o pacote `app.zip`.
- [Etapas de implementação, migrações, Admin e deploy](docs/Construcao/ap1.md)
- Endpoints: `/api/talhoes/` e `/api/lotes/`.
- Admin: `/admin/`; usuário local `dtdev1`, com a senha definida durante a configuração.
- API publicada: [http://lavourainteligentejg-env.eba-sqdkuvwv.us-east-1.elasticbeanstalk.com/](http://lavourainteligentejg-env.eba-sqdkuvwv.us-east-1.elasticbeanstalk.com/)
- Base da API: [http://lavourainteligentejg-env.eba-sqdkuvwv.us-east-1.elasticbeanstalk.com/api/](http://lavourainteligentejg-env.eba-sqdkuvwv.us-east-1.elasticbeanstalk.com/api/)

### Executar localmente

Requer Python 3.12. No PowerShell, a partir desta pasta, prepare o ambiente e instale as dependências:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
```

Inicie o servidor:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

A API fica disponível em `http://127.0.0.1:8000/api/`; os endpoints são `/api/talhoes/` e `/api/lotes/`. A raiz `/` responde ao health check e o painel fica em `http://127.0.0.1:8000/admin/`. Para criar um administrador local em um banco novo, execute `\.venv\Scripts\python.exe manage.py createsuperuser`. O banco SQLite é criado localmente pelas migrações. Pressione Ctrl+C para parar o servidor.

O pacote para upload é `app.zip`, gerado com `.\.venv\Scripts\python.exe empacotar.py`.
A aplicação Beanstalk foi configurada como `lavouraInteligente_JG`, com ambiente
`lavouraInteligente-JG-env`. Selecione a plataforma Python 3.12. A chave interna
do Django é gerada automaticamente em um arquivo privado no servidor;
não é necessário cadastrar chaves ou senhas nas propriedades do ambiente.
O banco local não vai no ZIP. Depois do deploy, crie o administrador por SSH:

```bash
cd /var/app/current
source /var/app/venv/*/bin/activate
sudo -u webapp env DJANGO_DEBUG=False "$(which python)" manage.py createsuperuser --username dtdev1
```

Informe o e-mail e a senha nos prompts, depois acesse `/admin/` na URL publicada.
O acesso SSH precisa estar configurado na instância. As etapas completas estão
na documentação AP1 vinculada acima.
