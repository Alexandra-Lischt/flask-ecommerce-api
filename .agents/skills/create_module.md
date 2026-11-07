# 🛠️ Skill: Criação de Novos Módulos de Domínio (DDD/Modular)

Sempre que o usuário solicitar a criação de uma nova entidade, funcionalidade ou
módulo (Ex: "Crie o módulo de checkout"), você deve executar este protocolo de
geração isolada em camadas.

---

## 📐 1. Árvore Física Estruturada (Obrigatório)

Você deve criar fisicamente a pasta `app/modules/[modulo]/` contendo exatamente
estes 6 arquivos padronizados:

```text
/app/modules/[modulo]
├── [modulo]_schema.py       # Camada 1: Contratos Pydantic V2 (Input/Output)
├── [modulo]_interfaces.py   # Camada 2: Interfaces Abstratas ABC (Contratos)
├── [modulo]_model.py        # Camada 3: Modelo Físico ORM SQLAlchemy 2.0
├── [modulo]_repo.py         # Camada 4: Repositório Concreto (SQLAlchemy)
├── [modulo]_service.py      # Camada 5: Regras de Negócio e Transações ACID
└── [modulo]_routes.py       # Camada 6: Endpoints HTTP (Flask Blueprint)
```

---

## 🚨 2. Restrições e Guardrails de Codificação

Você deve obedecer cegamente a estas regras físicas e de sintaxe ao gerar o código:

1. **Limite Rígido de Linha:** Nenhuma linha de código ou comentário pode passar de
   88 caracteres (conforme `pyproject.toml`). Quebre as linhas verticalmente.
2. **Estilo Ruff (I001):** Organize os blocos de imports seguindo estritamente a
   ordem do PEP 8: Biblioteca Padrão -> Pacotes Terceiros -> Módulos Internos (`app/`).
3. **Identidade UUID:** Toda chave primária de nova entidade deve herdar de
   `UUIDIDMixin` e toda auditoria temporal deve herdar de `TimestampMixin` (de `app.database`).
4. **Isolamento ACID:** Repositórios e Rotas NÃO fazem `db.session.commit()`. O
   controle transacional reside puramente no `Service` usando blocos `try/except/rollback`.
5. **Injeção de Dependência:** O `Service` deve receber a interface abstrata do
   repositório via método construtor `__init__(self, repo: AbstractRepository)`.

---

## 📋 3. Roteiro Sequencial de Implementação

Gere os arquivos estritamente nesta ordem cronológica para evitar quebras de contexto:

- **Passo 1: `[modulo]_model.py`** -> Declare a tabela ORM herdando de `Model`, `UUIDIDMixin` e `TimestampMixin`.
- **Passo 2: `[modulo]_schema.py`** -> Monte os Schemas de entrada e saída via Pydantic V2.
- **Passo 3: `[modulo]_interfaces.py`** -> Crie a classe abstrata `AbstractRepository` com `@abstractmethod`.
- **Passo 4: `[modulo]_repo.py`** -> Monte a persistência usando `db.session.add` ou `db.session.get`.
- **Passo 5: `[modulo]_service.py`** -> Monte as regras de negócio controlando o commit e o rollback.
- **Passo 6: `[modulo]_routes.py`** -> Instancie o Blueprint e vincule as rotas serializando com o Schema.

---

## 🚀 4. Protocolo de Encerramento e Validação

Imediatamente após criar os arquivos do módulo, você é obrigado a executar estes
comandos de auditoria no terminal antes de entregar a resposta:

```bash
# 1. Registre o Blueprint no agregador central `app/routes.py`
# 2. Formate fisicamente e limpe o código gerado
uv run ruff format app/modules/[modulo]/
uv run ruff check app/modules/[modulo]/ --fix
```
