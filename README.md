# 🦠 Simulador Epidemiológico SIR/SEIR

> Simulação computacional da propagação de doenças infecciosas com modelos matemáticos SIR e SEIR, interface web interativa e artigo científico em português.

---

## 📌 Índice

- [Nome do Projeto](#nome-do-projeto)
- [Descrição](#descrição)
- [Objetivo Acadêmico](#objetivo-acadêmico)
- [Como Funciona o Modelo SIR/SEIR](#como-funciona-o-modelo-sirseir)
- [Tecnologias Usadas](#tecnologias-usadas)
- [Como Executar Localmente](#como-executar-localmente)
- [Limitações do Modelo](#limitações-do-modelo)
- [⚠️ Aviso Importante](#️-aviso-importante)
- [Gerado com Auxílio de IA](#gerado-com-auxílio-de-ia)

---

## Nome do Projeto

**Simulador Epidemiológico SIR/SEIR** — Modelagem Computacional de Doenças Infecciosas

---

## Descrição

Este projeto é composto por três entregas integradas:

| Componente | Descrição |
|---|---|
| `epidemic_simulator.py` | Programa Python completo que simula epidemias usando modelos SIR e SEIR, com CLI interativa, gráficos e comparação de cenários |
| `index.html` *(interface web)* | Simulador interativo no navegador, sem necessidade de instalação, com controles deslizantes e gráficos em tempo real |
| `artigo_epidemiologia.docx` | Artigo científico em português descrevendo o modelo matemático, a implementação e os resultados |

O simulador permite ao usuário definir parâmetros como tamanho da população, taxa de transmissão (β), taxa de recuperação (γ) e duração da simulação, visualizando em tempo real como uma doença infecciosa hipotética se espalharia nessa população.

---

## Objetivo Acadêmico

Este projeto foi desenvolvido com fins **estritamente educacionais**, dentro do contexto de disciplinas de:

- Modelagem Computacional
- Epidemiologia e Saúde Pública
- Métodos Numéricos
- Programação Científica

O objetivo é demonstrar, de forma prática e visual, como equações diferenciais ordinárias (EDOs) são utilizadas para modelar fenômenos reais — no caso, a propagação de doenças infecciosas em uma população.

---

## Como Funciona o Modelo SIR/SEIR

### Modelo SIR

A população é dividida em três grupos (**compartimentos**):

```
S → I → R
```

| Compartimento | Nome | Significado |
|---|---|---|
| **S** | Suscetíveis | Pessoas que podem ser infectadas |
| **I** | Infectados | Pessoas atualmente doentes e transmissoras |
| **R** | Recuperados | Pessoas curadas (com imunidade) |

As equações que descrevem a dinâmica são:

```
dS/dt = −β · S · I / N
dI/dt =  β · S · I / N − γ · I
dR/dt =  γ · I
```

### Modelo SEIR

Adiciona o compartimento **E (Expostos)** — pessoas que foram infectadas mas ainda não transmitem (período de incubação):

```
S → E → I → R
```

```
dS/dt = −β · S · I / N
dE/dt =  β · S · I / N − σ · E
dI/dt =  σ · E − γ · I
dR/dt =  γ · I
```

### Parâmetros principais

| Parâmetro | Símbolo | Significado | Exemplo |
|---|---|---|---|
| Taxa de transmissão | β (beta) | Frequência de contágio por contato | 0.30 |
| Taxa de recuperação | γ (gamma) | Inverso da duração da doença | 0.10 → doença dura ~10 dias |
| Taxa de incubação | σ (sigma) | Inverso do período de latência (SEIR) | 0.20 → incubação ~5 dias |
| Reprodução básica | R₀ = β/γ | Quantas pessoas um infectado contagia | R₀ = 3 → epidemia cresce |

> **Regra de ouro:** Se R₀ > 1, a epidemia cresce. Se R₀ < 1, ela se extingue naturalmente.

---

## Tecnologias Usadas

### Simulador Python (`epidemic_simulator.py`)

| Biblioteca | Versão mínima | Função |
|---|---|---|
| Python | 3.10+ | Linguagem principal |
| NumPy | 1.23+ | Operações numéricas e vetorização |
| SciPy | 1.9+ | Integração das equações diferenciais (`odeint`) |
| Matplotlib | 3.6+ | Geração dos gráficos e painéis visuais |

### Interface Web (`index.html`)

| Tecnologia | Função |
|---|---|
| HTML5 / CSS3 | Estrutura e estilo da página |
| JavaScript (vanilla) | Lógica da simulação no navegador |
| Chart.js (CDN) | Renderização dos gráficos interativos |

> A interface web **não precisa de instalação** — roda diretamente no navegador.

---

## Como Executar Localmente

### Opção 1 — Interface Web (mais simples)

Basta abrir o arquivo `index.html` em qualquer navegador moderno:

```bash
# Clonar o repositório
git clone https://github.com/SEU_USUARIO/simulador-epidemiologico.git

# Entrar na pasta
cd simulador-epidemiologico

# Abrir no navegador (macOS)
open index.html

# Abrir no navegador (Linux)
xdg-open index.html

# Abrir no navegador (Windows)
start index.html
```

### Opção 2 — Simulador Python

**1. Pré-requisitos**

```bash
# Verificar se Python está instalado
python --version   # deve ser 3.10 ou superior

# Instalar as dependências
pip install numpy scipy matplotlib
```

**2. Modo interativo** (recomendado para iniciantes)

```bash
python epidemic_simulator.py
```

O programa irá guiar você com perguntas sobre os parâmetros.

**3. Modo por linha de comando**

```bash
# Simulação SIR básica
python epidemic_simulator.py --model SIR --N 100000 --beta 0.30 --gamma 0.10 --days 180

# Simulação SEIR
python epidemic_simulator.py --model SEIR --beta 0.30 --gamma 0.10 --sigma 0.20 --days 250

# Comparação de 4 cenários pré-definidos
python epidemic_simulator.py --compare

# Salvar o gráfico como imagem
python epidemic_simulator.py --model SIR --save meu_grafico.png
```

**4. Parâmetros disponíveis**

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--model` | SIR | Modelo a usar: `SIR` ou `SEIR` |
| `--N` | 100000 | Tamanho da população |
| `--beta` | 0.30 | Taxa de transmissão |
| `--gamma` | 0.10 | Taxa de recuperação |
| `--sigma` | 0.20 | Taxa de incubação (SEIR) |
| `--I0` | 10 | Infectados iniciais |
| `--days` | 180 | Dias de simulação |
| `--label` | "Run 1" | Nome do cenário nos gráficos |
| `--compare` | — | Executa comparação entre 4 cenários |
| `--save` | — | Caminho para salvar o gráfico |

---

## Limitações do Modelo

Os modelos SIR e SEIR são simplificações matemáticas da realidade. É importante compreender suas limitações:

- **Mistura homogênea:** o modelo assume que qualquer pessoa pode entrar em contato com qualquer outra com igual probabilidade. Na prática, redes sociais, estruturas familiares e desigualdades geográficas criam padrões muito mais complexos.

- **Parâmetros constantes:** β e γ são mantidos fixos ao longo de toda a simulação. Em epidemias reais, esses valores mudam com intervenções, comportamento humano e sazonalidade.

- **População fechada:** não há nascimentos, mortes naturais ou migrações. Esta hipótese é razoável para epidemias curtas em populações grandes, mas falha em contextos de longo prazo.

- **Sem estrutura etária:** todas as pessoas têm o mesmo risco de infecção e a mesma duração de doença. Doenças como COVID-19 e influenza apresentam risco muito maior em idosos.

- **Sem estocasticidade:** o modelo é determinístico — dadas as mesmas condições iniciais, produz sempre o mesmo resultado. Epidemias reais têm componentes aleatórios, especialmente em populações pequenas.

- **Sem dinâmica espacial:** a propagação geográfica, viagens entre cidades e diferenças regionais não são capturadas.

---

## ⚠️ Aviso Importante

> **Este sistema é exclusivamente educacional.**
>
> O simulador foi desenvolvido como ferramenta de aprendizado para disciplinas acadêmicas de modelagem computacional e epidemiologia introdutória. Os resultados produzidos são baseados em modelos matemáticos simplificados e **não devem, em nenhuma hipótese, ser utilizados para:**
>
> - Tomada de decisões em saúde pública
> - Previsão de epidemias reais
> - Assessoria médica ou sanitária
> - Políticas governamentais de controle de doenças
>
> Para análises epidemiológicas com fins práticos, consulte órgãos competentes como o Ministério da Saúde, a Organização Mundial da Saúde (OMS) e centros de pesquisa especializados.

---

## Gerado com Auxílio de IA

Este projeto foi desenvolvido com o suporte de ferramentas de Inteligência Artificial como auxílio à criação de código, texto científico e documentação. O uso de IA foi supervisionado e orientado pelo estudante responsável, que revisou, adaptou e validou o conteúdo gerado.

---

### 📋 Ficha de Registro

| Campo | Informação |
|---|---|
| **IA utilizada** | *(Claude Sonnet 4.6)* |
| **Prompt utilizado** | Ver arquivo [`prompts/prompt-codigo.md`](prompts/prompt-codigo.md) |
| **Data de geração** | *(04/05/2026)* |
| **Nome do estudante** | Taryk de Melo Barbosa Alves |

---

## 📁 Estrutura do Projeto

```
simulador-epidemiologico/
│
├── index.html                  # Interface web interativa (GitHub Pages)
├── epidemic_simulator.py       # Simulador Python completo (CLI)
├── artigo_epidemiologia.docx   # Artigo científico em português
├── README.md                   # Este arquivo
│
└── prompts/
    └── prompt-codigo.md        # Prompt original usado para gerar o código
```

---

## 📄 Licença

Este projeto é de uso **educacional e livre**. Pode ser copiado, modificado e redistribuído para fins não comerciais, desde que mantida a atribuição ao autor original e a menção ao uso de IA no desenvolvimento.
