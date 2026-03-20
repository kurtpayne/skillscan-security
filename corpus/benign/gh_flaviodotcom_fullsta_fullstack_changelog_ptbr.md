---
name: fullstack-changelog-ptbr
description: Atualiza e mantém changelog.md/CHANGELOG.md de projetos frontend e backend Java/Quarkus no padrão de tabela Markdown com colunas Versão, Descrição, Data Homologação e Data Produção. Escreve mensagens em português (pt-BR), aplica ponto final obrigatório nas novas descrições e valida acentuação/UTF-8 para evitar mojibake. Use quando houver bump de versão após conclusão da task.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: flaviodotcom/fullstack-changelog-ptbr
# corpus-url: https://github.com/flaviodotcom/fullstack-changelog-ptbr/blob/76513bf7d08b121ec0b51de2aaf505e5bcdc3e78/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Fullstack Changelog PT-BR

Atualizar changelog de forma consistente, sem quebrar a estrutura adotada no projeto.

## Padrão de Estrutura

Priorizar o padrão de tabela Markdown:

`| Versão | Descrição | Data Homologação | Data Produção |`

Regras de estrutura:

- Manter exatamente a ordem e os nomes das colunas do arquivo já existente.
- Inserir nova linha de versão no topo (logo após cabeçalho/separador da tabela).
- Preservar histórico antigo; não reescrever entradas anteriores.
- Preencher datas somente quando o usuário fornecer explicitamente.

Quando não existir changelog, criar usando `references/changelog-template.md`.

## Fluxo Obrigatório

1. Confirmar que a task está concluída e que existe bump de versão para esta entrega.
2. Ler `changelog.md`/`CHANGELOG.md` e confirmar estrutura em tabela.
3. Identificar mudanças da entrega atual a partir do contexto fornecido (diff, commits, PR, descrição da task).
4. Filtrar somente mudanças concluídas e relevantes para release notes.
5. Escrever a descrição em português (pt-BR), objetiva e com ponto final.
6. Inserir a nova linha da versão no topo da tabela, preservando histórico.
7. Executar validações de pontuação, acentuação e encoding.

## Regras Inegociáveis

- Atualizar changelog somente quando houver bump de versão.
- Preservar estrutura do arquivo existente (colunas, ordem, estilo de tabela).
- Não incluir trabalho incompleto, experimentos descartados ou detalhes internos sem valor para release notes.
- Não apagar histórico, exceto se o usuário pedir explicitamente.
- Não mudar idioma para inglês: mensagens devem permanecer em português (pt-BR).
- Em novas descrições, usar ponto final obrigatório (`.`), mesmo que entradas antigas não usem.

## Aderência Frontend e Backend

- Aplicar o mesmo padrão para frontend e backend.
- Se o backend Java/Quarkus ainda não tiver changelog, criar `changelog.md` com o template de tabela.
- Para backend, registrar versões somente quando a task estiver concluída e houver bump de versão.

## Versionamento

- Priorizar a versão informada pelo usuário.
- Se a versão não for informada, inferir do arquivo de build:
  - Maven: `pom.xml` (`<version>`)
  - Gradle: `build.gradle` ou `gradle.properties`
- Se houver conflito entre fontes, pedir confirmação antes de escrever.

## Estilo de Escrita (pt-BR)

Aplicar padrões de `references/ptbr-style.md`.
Aplicar validações de `references/text-quality-checks.md`.

Diretrizes rápidas:

- Frase única e objetiva na coluna `Descrição`.
- Começar com verbo no infinitivo (`Adicionar`, `Corrigir`, `Ajustar`, `Remover`, `Melhorar`).
- Finalizar com ponto final.
- Evitar linguagem vaga (`melhorias gerais`, `diversos ajustes`) sem detalhe mínimo.

## Validação Obrigatória de Qualidade de Texto

Antes de salvar:

- Confirmar que não existe mojibake (ex.: `Ã`, `Â`, `�`).
- Confirmar que palavras comuns estão acentuadas corretamente (`não`, `versão`, `descrição`, `produção`, `homologação`, `integração`, `correção`, `usuário`).
- Confirmar que a nova descrição termina com `.`.
- Garantir encoding UTF-8 no arquivo de saída.

Depois de salvar, executar:

`powershell -ExecutionPolicy Bypass -File scripts/validate-changelog-ptbr.ps1 -Path <caminho-do-changelog>`

Se o script retornar erro, corrigir os pontos reportados antes de concluir.
Por padrão, o script valida apenas a linha mais recente (nova versão), evitando falha por histórico legado.
Para auditoria completa do arquivo, usar `-CheckAllRows`.

## Saída Esperada

- Arquivo `changelog.md` ou `CHANGELOG.md` atualizado.
- Resumo final com:
  - versão registrada
  - data usada
  - formato aplicado (tabela)
  - quantidade de itens adicionados
  - status da validação de acentuação/encoding