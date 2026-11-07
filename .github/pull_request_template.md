# 🚀 Pull Request: Scalable E-commerce Feature

## 🎯 Escopo do Incremento
- [ ] Autenticação & Usuários (Cadastro/JWT)
- [ ] Catálogo de Produtos (CRUD/Estoque)
- [ ] Checkout Transacional (Pedidos/Garantia ACID)

## 🔒 Checklist Arquitetural (Black Friday Readiness)
- [ ] **Desacoplamento:** Camada de serviço consome apenas abstrações (`AbstractRepository` via `abc.ABC`).
- [ ] **Injeção de Dependência:** Repositórios concretos injetados estritamente via construtor (`__init__`).
- [ ] **Resiliência ACID:** Operações de escrita envelopadas em blocos `try/except/rollback` para evitar sessões corrompidas no SQLAlchemy.
- [ ] **Tipagem Estática:** Livre de "Call expressions" em anotações de tipo; uso correto de `Mapped[]`.
- [ ] **Prevenção de Loops:** Rotas registradas exclusivamente em `app/routes.py` (evitando importações circulares).

## 🧪 Cobertura e Resultados dos Testes (Pytest)
Cole aqui o output do comando `uv run pytest app/tests/ -v`:
```text
# Insira os testes unitários, de rotas e integração validados aqui.
```