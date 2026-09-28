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
- Admin: `/admin/`; usuário previsto para o deploy: `dtdev1`, criado quando as variáveis abaixo estiverem configuradas. A senha é definida no Beanstalk e não é publicada no GitHub.
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
não é necessário cadastrar `DJANGO_SECRET_KEY`.

### Criar o administrador sem SSH

No console **Elastic Beanstalk → ambiente → Configuração → Atualizações, monitoramento e registro → Editar → Propriedades do ambiente**, cadastre as três variáveis antes de enviar o novo ZIP:

| Variável | Valor |
| --- | --- |
| `DJANGO_SUPERUSER_USERNAME` | `dtdev1` |
| `DJANGO_SUPERUSER_EMAIL` | Seu e-mail |
| `DJANGO_SUPERUSER_PASSWORD` | Uma senha forte escolhida por você |

Não coloque a senha no código, README ou ZIP. Aguarde a aplicação das propriedades e envie o `app.zip` atualizado pelo console. Durante esse deploy, `bootstrap_admin` cria o usuário depois das migrações, diretamente no banco do servidor. Depois, acesse [Django Admin](http://lavourainteligentejg-env.eba-sqdkuvwv.us-east-1.elasticbeanstalk.com/admin/) com `dtdev1` e a senha configurada.

Se o usuário já existir, o comando preserva a conta e a senha; mudar a variável não redefine a senha existente. Sem nenhuma das três variáveis, a criação é ignorada. Para uma conta nova, configuração incompleta ou credenciais inválidas interrompem o deploy com uma mensagem sem expor a senha.

O banco local não vai no ZIP. O SQLite é criado na AWS e pode ser perdido em novos deploys ou substituições da instância. Manter as três variáveis permite recriar o administrador quando o banco for criado novamente. Se remover as três após o cadastro, será necessário configurá-las novamente para recriar a conta em um banco novo.

Referências: [propriedades do ambiente Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html) e [validação de senhas Django](https://docs.djangoproject.com/en/6.0/topics/auth/passwords/#password-validation).
As etapas completas estão na documentação AP1 vinculada acima.
