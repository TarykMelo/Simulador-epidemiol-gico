# Prompt Utilizado para Geração do Código

**Arquivo:** `prompts/prompt-codigo.md`  
**Estudante:** Taryk de Melo Barbosa Alves  
**Data de uso:** *04/05/2026*  
**IA utilizada:** *Claude Sonnet 4.6*

---

## Prompt 1 — Geração do Simulador Python

> Você é um especialista em modelagem computacional, epidemiologia e desenvolvimento de software. Sua tarefa é criar um programa completo e bem estruturado que modela a propagação de uma doença infecciosa em uma população, semelhante a calculadoras epidêmicas (ex: modelos SIR/SEIR).
>
> ### Requisitos:
>
> 1. **Linguagem de Programação:**
>    - Use Python (preferível) ou outra linguagem amplamente utilizada.
>    - O código deve ser limpo, modular e bem documentado.
>
> 2. **Modelo:**
>    - Implemente pelo menos um modelo epidemiológico (SIR ou SEIR).
>    - Inclua os seguintes compartimentos:
>      - Susceptible (S)
>      - Infected (I)
>      - Recovered (R)
>      - (Opcional) Exposed (E)
>
> 3. **Funcionalidades:**
>    - Permitir parâmetros definidos pelo usuário:
>      - Tamanho da população
>      - Taxa de infecção (beta)
>      - Taxa de recuperação (gamma)
>      - Tempo de simulação (dias)
>    - Simular a propagação ao longo do tempo usando equações diferenciais ou aproximação discreta.
>    - Gerar saída gráfica (ex: gráficos de linhas mostrando S, I, R ao longo do tempo).
>
> 4. **Visualização:**
>    - Use bibliotecas como matplotlib ou similares.
>    - Rotule claramente os eixos, legendas e título.
>
> 5. **Qualidade do Código:**
>    - Inclua comentários explicando cada parte do modelo.
>    - Estruture o código usando funções ou classes.
>    - Facilite a modificação dos parâmetros.
>
> 6. **Extra (opcional, mas recomendado):**
>    - Adicione uma interface interativa (CLI ou GUI simples).
>    - Permita múltiplas simulações com parâmetros diferentes.
>    - Inclua comparação entre cenários.
>
> ### Formato de saída:
> - Forneça o código completo.
> - Inclua instruções de como executá-lo.
> - Inclua um exemplo de execução.
>
> Pense passo a passo e garanta a correção científica no modelo epidemiológico.

---

## Prompt 2 — Geração do Artigo Científico

> Você é um pesquisador acadêmico especializado em epidemiologia e modelagem computacional.
> Escreva um artigo em estilo científico explicando um programa que simula a propagação de doenças infecciosas usando um modelo SIR ou SEIR.
>
> ### Requisitos:
>
> 1. **Idioma:** Escreva em português.
>
> 2. **Estrutura:** O artigo deve incluir:
>    - Título
>    - Resumo
>    - Introdução
>    - Metodologia
>    - Descrição do Modelo (explicação matemática do SIR/SEIR)
>    - Implementação (como o código funciona)
>    - Resultados e Discussão
>    - Conclusão
>    - Referências (pode incluir referências acadêmicas genéricas)
>
> 3. **Conteúdo:**
>    - Explique como as doenças infecciosas se propagam matematicamente.
>    - Descreva os parâmetros (beta, gamma, população).
>    - Explique como a simulação foi implementada em código.
>    - Interprete possíveis saídas e gráficos.
>
> 4. **Estilo:**
>    - Tom acadêmico formal.
>    - Escrita clara e objetiva.
>    - Em torno de 800–1500 palavras.
>
> 5. **Extra:**
>    - Inclua equações onde relevante.
>    - Torne a explicação compreensível para estudantes de graduação.
>
> ### Saída:
> - Forneça o artigo completo pronto para ser usado em um relatório ou PDF.

---

## Prompt 3 — Geração do README e Documentação

> Crie um readme sobre o que foi colocado em cima.
>
> O README.md deve conter:
>
> 1. Nome do projeto.
> 2. Descrição do projeto.
> 3. Objetivo acadêmico.
> 4. Explicação simples do modelo SIR/SEIR.
> 5. Tecnologias usadas.
> 6. Como executar localmente.
> 7. Como hospedar no GitHub Pages.
> 8. Limitações do modelo.
> 9. Aviso de que o sistema é educacional e não deve ser usado como ferramenta médica ou sanitária real.
> 10. Informação de que o projeto foi gerado com auxílio de IA.
> 11. Espaço para registrar:
>     - IA utilizada:
>     - Prompt utilizado:
>     - Data de geração:
>     - Nome do estudante: Taryk de Melo Barbosa Alves
>
> O arquivo prompts/prompt-codigo.md deve conter exatamente este prompt que estou usando para gerar o código.
>
> Depois de gerar os arquivos, explique brevemente:
>
> 1. Como cada arquivo funciona.
> 4. Quais partes do código são mais complexas para um aluno iniciante compreender.
>
> Não entregue apenas trechos soltos. Entregue o projeto completo, com todos os arquivos separados e identificados.

---

## Observações sobre o uso de IA

O conteúdo gerado pelos prompts acima foi **supervisionado, revisado e adaptado** pelo estudante Taryk de Melo Barbosa Alves. A IA foi utilizada como ferramenta de apoio ao desenvolvimento, não como substituto ao aprendizado ou à autoria intelectual do estudante.

Conforme boas práticas acadêmicas, o uso de IA generativa deve ser **declarado, documentado e contextualizado** — o que este arquivo faz.
