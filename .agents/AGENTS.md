# 🤖 Manifesto de Agentes e Diretrizes do Repositório (.agents/AGENTS.md)

Este documento governa o comportamento de codificação automática, arquitetura de software e conformidade técnica para agentes de IA (Codex, Cursor, Claude Code) operando neste repositório.

## 🚀 Automação de Ciclo de Vida (Agent Hooks)

Sempre que um agente de IA gerar ou modificar código, execute os comandos shell abaixo, individualmente e em sequência. Eles formatam o código, corrigem o estilo (PEP 8) e
validam a tipagem estática do ecossistema.

Subscribed to: PreToolUse

```bash
# 1. Corrige automaticamente erros comuns e organiza imports (Isort) conforme o pyproject.toml
uv run ruff check app/ --fix || true

# 2. Formata fisicamente as quebras de linha e strings para o limite estendido de 88 caracteres
uv run ruff format app/

# 3. Executa a auditoria de checagem de tipos estáticos barrando assinaturas inválidas
uv run mypy app/
```

---

## 🛠️ Extensões de Instrução (Skills)
- **Criação de Módulos:** Sempre que for iniciar uma nova funcionalidade, consuma e obedeça as diretrizes descritas em `.agents/skills/create_module.md`.

---

## 1. Arquitetura Física e Divisão de Camadas
Toda e qualquer nova funcionalidade introduzida no pacote principal `app/` deve seguir rigorosamente a separação de conceitos (Separation of Concerns).

```text
/app
├── config.py, database.py, extensions.py  # Orquestração e Inicialização Core
├── /errors                                # Centralizador Global de Handlers de Erro
├── /modules                               # Domínios de Negócio Isolados
│   └── /[modulo]
│       ├── [modulo]_schema.py             # Camada 1: Contratos de Entrada/Saída (Schema)
│       ├── [modulo]_interfaces.py         # Camada 2: Contratos Abstratos (Interfaces ABC)
│       ├── [modulo]_model.py              # Camada 3: Entidade Física ORM (db.Model)
│       ├── [modulo]_repo.py               # Camada 4: Persistência Concreta (Repository)
│       ├── [modulo]_service.py            # Camada 5: Regras de Negócio e Transações (Service)
│       └── [modulo]_routes.py             # Camada 6: Endpoints HTTP (APIBlueprint)
└── /tests                                 # Pirâmide Modular de Testes
    └── /modules/[modulo]                  # Pasta espelhada contendo conftest.py, unitários e integração
```

---

## 2. Restrições Rígidas de Código (Anti-Pattern Guardrails)

Para evitar quebras em tempo de compilação ou loops, os agentes
**DEVEM** obedecer a estas regras negativas:

| Regra / Ação | O que NÃO fazer (Proibido) | O que FAZER (Obrigatório) |
| :--- | :--- | :--- |
| **Anotação de Tipo** | `id: db.Column(db.Integer...)` | `id: Mapped[int] = mapped_column(...)` |
| **Herança de Model** | Herdar de `db.Base` ou declarativas puras. | Herdar estritamente de `db.Model`. |
| **Injeção Dep.** | Importar repo estático no Service. | Injetar repo via `__init__`. |
| **Garantia ACID** | Executar `db.session.commit()` em rotas ou repo. | Controlar transações no Service com `try/except`. |
| **Import Circular** | Registrar Blueprints no core `app/__init__.py`. | Registrar Blueprints no agregador `app/routes.py`. |
| **Tamanho de Linha** | Deixar linhas ou strings ultrapassarem 88 chars. | Quebrar linhas manualmente ou usar o formatador. |
| **Estilo (PEP 8)** | Ignorar formatação ou ordenação de imports. | Seguir o PEP 8 validado via `uv run ruff check`. |
| **Tipagem Estática** | Mapear tipos genéricos ou omitir assinaturas. | Validar todas as camadas via `uv run mypy app/`. |

---

## 3. Comandos de Execução e Automação (CLI Environment)

O runtime é gerenciado estritamente via **`uv`**. Sempre que o agente precisar rodar ou validar o ambiente, ele deve utilizar estes comandos de terminal de forma direta:

- **Instalação Local:** `uv sync --dev`
- **Subir Aplicação:** `docker compose up --build` *(Disponível na porta 5000)*
- **Esteira de Testes Completa:** `uv run pytest`
- **Esteira de Testes do Módulo:** `uv run pytest app/tests/modules/[modulo]/ -v`
- **Formatação de Código:** `uv run ruff format app/`
- **Auditoria de Linters:** `uv run pre-commit run --all-files`
- **Auditoria de Tipagem:** `uv run mypy app/`
- **Migração de Banco:** `uv run alembic upgrade head`

---

## 4. Diretrizes de Testes e Cobertura
- **Nomenclatura:** Arquivos devem ser prefixados com `test_*.py` e funções de asserção com `test_*`.
- **Isolamento de Fixtures:** Fixtures globais (ex: SQLite em memória) residem em
  `app/tests/conftest.py`. Fixtures e classes de `MockRepository` de domínio residem
  no `conftest.py` interno do subdiretório do módulo.
- **Tipos de Testes OBRIGATÓRIOS por Módulo:**
  1. `test_[modulo]_service.py`: Valida as regras de negócio usando o Mock do repositório.
  2. `test_[modulo]_routes.py`: Valida se os Schemas barram ou filtram dados HTTP.
  3. `test_[modulo]_integration.py`: Executa o fluxo de ponta a ponta contra o banco em memória.

---

## 5. Padrão de Entrega (Commits e Pull Requests)
- **Mensagem de Commit:** Use o modo imperativo curto (Ex: `Add product lookup endpoint`).
- **Abertura de PR:** Preencha obrigatoriamente o arquivo
  `.github/pull_request_template.md` anexando o log do comando
  `uv run pre-commit run --all-files` demonstrando status verde de aprovação.
- **Segurança:** Nunca armazene ou commite segredos. Use `.env` local não rastreado.
