---
name: skill-forge
description: "Sistema completo para criar, testar e otimizar skills do Claude Code com pipeline de rigor epistemico. Ativar quando o usuario quer: (1) criar uma nova skill do zero, (2) melhorar ou refatorar uma skill existente, (3) rodar evals e benchmarks para validar uma skill, (4) otimizar a description de ativacao, (5) comparar duas versoes de uma skill, (6) empacotar uma skill para distribuicao, (7) estudar um dominio antes de construir a skill, (8) extrair metodologia de um corpo de conhecimento, (9) validacao profunda com triagem de complexidade. Exemplos: crie uma skill para, melhore essa skill, teste essa skill, otimize o trigger, compare versoes, estude esse dominio, extraia a metodologia."
license: MIT
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Hackerdomarketing/skill-forge
# corpus-url: https://github.com/Hackerdomarketing/skill-forge/blob/77ad37247591e7dbeeb6829b8f3963a46724970b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Skill Forge v3

Sistema completo para criar, testar e otimizar skills do Claude Code.
Combina design rigoroso com validacao empirica e pipeline de rigor epistemico.

> Uma skill efetiva e como um guia de integracao para um novo especialista.
> Cada skill responde tres perguntas: quando ativar, o que executar, quais recursos usar.

---

## Pipeline

```
TRIAGE GATE (fast / medium / deep)
  → Stage A: Estudador (study bundle)
  → Stage B: Dissector (dissection package)
  → Stage C: Forge (6 fases de construcao)
```

| Caminho | Score | Stages executados |
|---------|-------|-------------------|
| **Fast** | <= 0 | Triage → Stage C (identico ao v2) |
| **Medium** | 1-2 | Triage → Stage A abreviado (niveis 1-3) → Stage C |
| **Deep** | >= 3 | Triage → Stage A completo → Stage B → Stage C |

---

## Principios Fundamentais

1. **Qualidade embutida, nao parafusada** — rigor em cada fase, nao so no final
2. **Teste antes de refinar** — evals empiricos antes de mudancas subjetivas
3. **Se o Claude ja sabe fazer, nao incluir** — evitar bloat de instrucoes
4. **Explique o porque, nao so o que** — LLMs respondem melhor a raciocinio do que a regras
5. **Generalize, nao sobreajuste** — skills que funcionam para muitos prompts, nao so para os testes
6. **Rigor epistemico** — distinguir fato validado de opiniao popular; classificar certeza por nivel
7. **Extracao de metodologia** — transformar conhecimento em processos replicaveis, nao em resumos

---

## Triage Gate

Classificar a complexidade do dominio ANTES de construir. Executar o Triagista (`agents/triagista.md`) ou `scripts/forge_triage.py`.

### Tabela de Sinais

| Sinal | Score | Como detectar |
|-------|-------|---------------|
| Documentacao oficial acessivel | -1 | Existe docs.X.com, man pages, spec oficial publica |
| Usuario diz "skill simples" | -1 | Usuario explicita que e algo simples/rapido |
| APIs recentes/mutaveis | +1 | API mudou nos ultimos 12 meses, deprecations frequentes |
| Contradicoes conhecidas no dominio | +2 | Respostas diferentes em fontes diferentes |
| Claude ja errou nesse dominio | +2 | Usuario reporta que IA errou 2+ vezes nesse topico |
| Conhecimento especializado ausente | +2 | Dominio de nicho, praticas nao-documentadas |
| Output de alto risco | +2 | Seguranca, financeiro, medico — erro tem consequencia real |

### Arvore de Decisao

```
Somar scores de todos os sinais aplicaveis
├── Score <= 0 → Fast Path (direto pro Stage C)
├── Score 1-2 → Medium Path (Stage A abreviado → Stage C)
└── Score >= 3 → Deep Path (Stage A completo → Stage B → Stage C)
```

**Overrides:**
- Usuario pede "estudo profundo" → Deep Path independente do score
- Usuario pede "rapido, sem estudo" → Fast Path independente do score
- Na duvida entre Fast e Medium → Medium
- Na duvida entre Medium e Deep → Deep

Apresentar resultado ao usuario: "Classifiquei como [path] porque [razoes]. Quer seguir assim?"

Detalhes e exemplos praticos: `references/guia-triage.md`

---

## Stage A: Estudo de Dominio

Executado no Medium Path (abreviado) e Deep Path (completo).

Protocolo completo: `references/protocolo-estudador.md`. Agente: `agents/triagista.md` (triagem) seguido de estudo direto.

### Resumo dos 7 Niveis

1. **Diagnostico de Lacuna** — classificar tipo de erro/incerteza
2. **Hierarquia de Fontes** — Ouro (primaria) > Prata > Bronze > Ferro > Chumbo
3. **Triangulacao** — 3+ fontes independentes; ativar Modo de Contradicao se divergencia
4. **Escavacao Sistemica** — leitura integral de docs, issues, changelogs
5. **Busca por Ausencia** — onde a evidencia DEVERIA estar e nao esta
6. **Sintese** — Mapa de Conhecimento + Manual Operacional + Pacote Especialista
7. **Monitoramento** — fontes a vigiar, gatilhos de reabertura

**Modo Abreviado (Medium):** Executar apenas niveis 1-3. Pular niveis 4-7.

**Output:** Study Bundle em `workspace/stage-a-study/<data>/<tema>/` com `index.json` e 9 arquivos. Schemas: `references/formatos-intermediarios.md`

---

## Stage B: Dissecacao de Processo

Executado apenas no Deep Path. Requer Study Bundle do Stage A como input.

Protocolo completo: `references/protocolo-dissector.md`. Agente: `agents/dissector.md`.

### Resumo das 8 Fases

1. **Recepcao** — ler index.json, validar completude do Study Bundle
2. **Mapeamento Estrutural** — claims por nivel de certeza, marcos de desenvolvimento
3. **Conhecimento Tacito** — padroes implicitos, regras invisiveis para iniciantes
4. **Arquitetura Conceitual** — hierarquias de ideias e dependencias
5. **Contexto e Continuidade** — fio condutor, evolucao gradual vs saltos
6. **Formalizacao de Tecnica** — praticas validadas em metodos step-by-step
7. **Modelo Replicavel** — process map, principios operacionais, ferramentas
8. **Padroes Metalinguisticos** — terminologia essencial e antipadroes

**Output:** Dissection Package em `workspace/stage-b-dissection/` com 5 arquivos + `dissection-manifest.json`. Schemas: `references/formatos-intermediarios.md`

---

## Stage C: Construcao da Skill (Forge)

Identico ao v2 no Fast Path. Enriquecido pelos Stages A/B no Medium e Deep Path.

### Fase 1: Descoberta Profunda

Coletar exemplos concretos antes de construir:

- Minimo 3 casos de uso reais e validados
- Triggers de ativacao: quando exatamente essa skill deve ativar?
- Outputs esperados: formato, estrutura e conteudo
- Ferramentas necessarias: quais tools do Claude
- Templates: formatos fixos de output
- Erros comuns: armadilhas que o Claude deve evitar
- Conhecimento de dominio: o que um especialista saberia que o Claude nao sabe
- Edge cases: inputs invalidos, vazios, ambiguos

**Enriquecimento Deep:** O `dissection-manifest.json` pre-popula a descoberta. A entrevista com o usuario vira CONFIRMACAO dos dados extraidos, nao coleta do zero. Usar `--from-dissection` no `forge_init.py`.

### Fase 2: Analise de Recursos

> Se o Claude ja sabe fazer algo naturalmente, NAO incluir na skill.
> So incluir o que e especifico, nao-obvio ou facil de errar.

| O que e? | Onde vai? | Quando incluir? |
|---|---|---|
| Codigo executavel | `scripts/` | Validacao, automacao, calculos |
| Documentacao tecnica | `references/` | Dominio especializado, padroes |
| Templates de output | `assets/` | Formatos fixos, boilerplates |
| Instrucoes de processo | `SKILL.md` corpo | Sempre — e o core |
| Avisos e armadilhas | `SKILL.md` corpo | Erros que o Claude comete sem orientacao |

**Enriquecimento Deep:** Os niveis de certeza do Study Bundle informam a Regra de Ouro. Claims `Strong Probable` ou acima = SEMPRE incluir na skill. Claims `Popular sem Validacao` = incluir como WARNING explicito. Claims `Indeterminado` = excluir ou marcar como julgamento do usuario.

### Fase 3: Arquitetura

Selecionar padrao arquitetural. Consultar `references/arquiteturas.md`.

```
As etapas sao sequenciais e obrigatorias?
├── Sim → Fluxo de Trabalho
└── Nao → As operacoes sao independentes?
    ├── Sim → Baseado em Tarefas
    └── Nao → E sobre padroes/regras?
        ├── Sim → Referencia e Diretrizes
        └── Nao → Baseado em Capacidades
```

**Enriquecimento Deep:** O `skill_recommendations.architecture_pattern` do manifest pre-seleciona a arquitetura. Validar pela arvore de decisao acima. Se divergir, justificar e escolher o mais adequado.

### Fase 4: Implementacao

Inicializar com `forge_init.py`:

```bash
python3 scripts/forge_init.py nome-da-skill                              # instala global (~/.claude/skills/)
python3 scripts/forge_init.py nome --local                               # instala no projeto atual (.claude/skills/)
python3 scripts/forge_init.py nome --path /caminho/custom                # caminho customizado
python3 scripts/forge_init.py nome --pipeline-mode deep                  # com workspace de pipeline
python3 scripts/forge_init.py nome --from-dissection manifest.json       # pre-populado via dissecacao
```

**Default:** Sem `--path` ou `--local`, instala em `~/.claude/skills/` (global). Skills globais sao auto-descobertas pelo Claude Code em qualquer projeto, sem necessidade de referencia em CLAUDE.md. Usar `--local` apenas quando a skill for especifica de um unico projeto.

**Caminhos por OS:** macOS/Linux: `~/.claude/skills/`. Windows: `%USERPROFILE%\.claude\skills\`.

Escrever SKILL.md: frontmatter (name + description ate 1024 chars) + corpo (max 500 linhas).
Usar voz imperativa. Consultar `references/frontmatter-exemplos.md`.

**Enriquecimento Deep:** O corpo da skill e escrito a partir de: `01-process-map.md` (esqueleto do workflow), `02-operational-principles.md` (principios), antipadroes do manifest (secao "Nao Faca"). Claims com `claude_knows: false` do manifest DEVEM estar no SKILL.md.

### Fase 5: Avaliacao & Benchmark

1. Criar 2-3 prompts realistas em `evals/evals.json`
2. Rodar evals A/B: `forge_eval.py --skill-path X --evals Y`
3. Avaliar com agentes: Avaliador, Comparador, Analisador
4. Agregar benchmark: `forge_benchmark.py --workspace X --iteration N`
5. Gerar visualizador: `forge_report.py --workspace X --iteration N`
6. Otimizar description (opcional): `forge_optimize.py --skill-path X --iterations 5`

**Enriquecimento Deep:** Assertions do `evals.json` sao semeadas por `05-validation-tests.md` do Dissection Package. Adicionar metrica `knowledge_accuracy` (ver secao abaixo). Rodar: `forge_knowledge_accuracy.py --skill-path X --study-bundle Y`

### Fase 6: Iteracao

- Melhorar com base em padroes, nao em exemplos individuais
- Se um problema aparece em 1 eval, pode ser edge case
- Se aparece em 2+ evals, e padrao que precisa de correcao
- Parar quando: usuario satisfeito, feedbacks vazios, ou pass rate estabilizado
- Empacotar: `forge_package.py caminho/skill --output dist/`

**Enriquecimento Deep:** Na iteracao, e possivel voltar ao Stage A para re-estudar um sub-topico especifico que falhou nos evals. Isso gera um Study Bundle parcial que alimenta uma nova rodada do Forge sem refazer o pipeline inteiro.

---

## Deploy em Projetos

Apos criar/atualizar o Skill Forge, propagar para projetos que o usam:

```bash
# Deploy em um projeto especifico
python3 scripts/forge_deploy.py --project /caminho/projeto --git-push

# Re-deploy em todos os projetos registrados
python3 scripts/forge_deploy.py --all --git-push

# Simular antes de executar
python3 scripts/forge_deploy.py --project /caminho/projeto --dry-run

# Listar projetos registrados
python3 scripts/forge_deploy.py --list

# Instalar triggers no CLAUDE.md global (pos-instalacao)
python3 scripts/forge_deploy.py --setup
```

O deploy automatiza: (1) injecao da secao SKILL FORGE no CLAUDE.md do projeto, (2) adicao de `skills: [skill-forge]` nos agentes construtores, (3) git commit + push. Registro em `workspace/deploy-registry.json`.

O `--setup` injeta os triggers de ativacao (frases como "crie uma skill", "extraia metodo", "transforme em processo") no `~/.claude/CLAUDE.md` global, garantindo ativacao automatica com 100% de certeza. Deve ser rodado uma vez apos instalar o Skill Forge.

---

## Fast Path (Score <= 0)

Quando o dominio e simples e bem documentado, pular Stages A e B. Executar diretamente:

1. Fase 1 (Descoberta) → 2. Fase 2 (Analise) → 3. Fase 3 (Arquitetura) → 4. Fase 4 (Implementacao) → 5. Fase 5 (Avaliacao) → 6. Fase 6 (Iteracao)

Identico ao Skill Forge v2. Sem estudo de dominio, sem dissecacao.

---

## Metrica: knowledge_accuracy

Compara o output da skill contra claims validados do Study Bundle (Stage A).

**Calculo:**
```
knowledge_accuracy = claims_corretos_no_output / claims_validados_no_bundle
```

**Niveis:**
- >= 0.90: Excelente — skill reproduz conhecimento validado com fidelidade
- 0.70-0.89: Aceitavel — revisar claims nao cobertos
- < 0.70: Insuficiente — requer re-estudo ou reescrita

Executar: `forge_knowledge_accuracy.py --skill-path X --study-bundle Y`

Aplicavel apenas em Medium e Deep paths (Fast Path nao tem Study Bundle).

---

## Adaptacao por Ambiente

| Ambiente | Subagentes | Evals A/B | Visualizador | Otimizacao |
|----------|-----------|-----------|-------------|------------|
| Claude Code (CLI) | Paralelos | Completo | HTML no browser | Via `claude -p` |
| Claude.ai (Web) | Nao | Sequencial, sem baseline | Inline no chat | Manual |
| Cowork (Headless) | Sim | Completo | `--static` HTML | Via subprocess |

---

## Antipadroes

| Antipadrao | Por que e ruim | Fazer em vez disso |
|---|---|---|
| Descriptions vagas | Claude nao sabe quando ativar | Incluir cenarios concretos e formatos de arquivo |
| Explicar conceitos basicos | Desperdica tokens de contexto | So incluir conhecimento especifico do dominio |
| Instrucoes com "pode" ou "talvez" | Cria ambiguidade | Usar imperativo: "Fazer X" |
| Duplicar info entre arquivos | Inconsistencia e bloat | Uma fonte de verdade por conceito |
| Scripts nao testados | Falhas em producao | Testar com inputs variados antes de incluir |
| Sobreajustar para testes | Skill falha com prompts reais | Generalizar a partir de padroes |
| SKILL.md > 500 linhas | Consome contexto excessivo | Mover detalhes para references/ |
| Pular a Fase 5 | "Funciona" nao e evidencia | Rodar evals A/B para validar |
| Tratar opiniao como fato | Skill propaga erros | Classificar certeza por nivel (Ouro/Prata/Bronze) |
| Resumir em vez de extrair | Conhecimento nao-acionavel | Extrair metodologia replicavel com steps concretos |

---

## Referencia de Scripts

| Script | Proposito | Uso |
|---|---|---|
| `forge_init.py` | Scaffolding de nova skill | `forge_init.py nome [--path destino] [--local] [--pipeline-mode X] [--from-dissection Y]` |
| `forge_validate.py` | Validacao estrutural + pipeline | `forge_validate.py caminho --verbose` |
| `forge_analyze.py` | Analise de skill existente | `forge_analyze.py caminho` |
| `forge_eval.py` | Executar evals A/B | `forge_eval.py --skill-path X --evals Y` |
| `forge_benchmark.py` | Agregar benchmarks + pipeline metadata | `forge_benchmark.py --workspace X --iteration N` |
| `forge_optimize.py` | Otimizar description | `forge_optimize.py --skill-path X --iterations 5` |
| `forge_report.py` | Gerar visualizador HTML | `forge_report.py --workspace X --iteration N` |
| `forge_package.py` | Empacotar .skill | `forge_package.py caminho --output dist/` |
| `forge_deploy.py` | Deploy em projetos | `forge_deploy.py --project X [--git-push] [--dry-run] [--all] [--list]` |
| `forge_triage.py` | Triage Gate scorer | `forge_triage.py --topic X --signals Y --output Z` |
| `forge_pipeline.py` | Orquestrador do pipeline completo | `forge_pipeline.py --topic X --path fast\|medium\|deep` |
| `forge_knowledge_accuracy.py` | Comparar output vs claims validados | `forge_knowledge_accuracy.py --skill-path X --study-bundle Y` |
| `estudador_save_bundle.py` | Salvar Study Bundle no workspace | `estudador_save_bundle.py --tema X --output Y` |
| `estudador_normalize_sources.py` | Normalizar fontes para formato padrao | `estudador_normalize_sources.py --input X --output Y` |
| `dissector_extract.py` | Extracao auxiliar de dissecacao | `dissector_extract.py --bundle X --output Y` |
| `dissector_validate.py` | Validar Dissection Package | `dissector_validate.py --manifest X --verbose` |

## Referencia de Agentes

| Agente | Proposito | Input | Output |
|---|---|---|---|
| `triagista.md` | Classificar complexidade do dominio | Descricao + contexto | `triage.json` |
| `dissector.md` | Extrair metodologia replicavel | Study Bundle | Dissection Package + `dissection-manifest.json` |
| `avaliador.md` | Grading de assertions | Output + assertions | `grading.json` |
| `comparador.md` | Comparacao cega A/B | Dois outputs anonimos | `comparison.json` |
| `analisador.md` | Analise pos-comparacao | Winner/loser + transcricoes | `analysis.json` |

## Referencia de Documentos

| Documento | Conteudo |
|---|---|
| `references/arquiteturas.md` | 4 padroes arquiteturais com arvore de decisao |
| `references/checklist-qualidade.md` | Checklist de validacao em 8 categorias |
| `references/frontmatter-exemplos.md` | 3 formulas comprovadas de description |
| `references/padroes-codigo.md` | 8 padroes para documentar codigo |
| `references/schemas.md` | Schemas JSON para todos os dados |
| `references/protocolo-estudador.md` | Protocolo completo do Stage A (7 niveis) |
| `references/protocolo-dissector.md` | Protocolo completo do Stage B (8 fases) |
| `references/guia-triage.md` | Guia de triagem com exemplos praticos |
| `references/formatos-intermediarios.md` | Schemas de handoff entre stages |