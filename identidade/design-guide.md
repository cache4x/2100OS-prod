# Identidade — [NOME DA SUA EMPRESA]

> Identidade visual base do seu sistema.
> Personalize este arquivo com as cores, fontes e estilo da sua marca.
> Skills de conteúdo, carrossel e postagem leem esse arquivo antes de criar.

---

## 🎯 Sobre este Template

Este é um template de identidade visual que você deve personalizar com a marca do seu cliente. 

**Áreas para personalizar:**
- **Fundo principal** - Substitua pela cor de fundo preferida
- **Cor de destaque / CTA** - Substitua pela cor principal da marca
- **Tipografia** - Ajuste as fontes conforme a identidade do cliente
- **Logo** - Substitua o logo placeholder pelo logo real do cliente

---

## Filosofia

[DESCRIÇÃO DA FILOSOFIA DA MARCA DO CLIENTE]

Exemplo:
- **Profissional:** Passa credibilidade no contexto do negócio
- **Moderna:** Design atual e relevante
- **Flexível:** Permite customização sem perder consistência
- **Perene:** Não segue tendências passageiras

---

## Cores

### Paleta Primária

- **Fundo principal:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Cor de destaque / CTA:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Texto principal:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Texto secundário:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Fundo alternativo / cards:** [COR_HEX]
- **Bordas:** [COR_HEX] — [DESCRIÇÃO_DA_COR]

### Paleta Semântica

- **Sucesso:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Atenção:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Erro:** [COR_HEX] — [DESCRIÇÃO_DA_COR]
- **Info:** [COR_HEX] — [DESCRIÇÃO_DA_COR]

### Variações de CTA

| Estado | Cor | Uso |
|--------|-----|-----|
| Primary | [COR_HEX] | CTA principal |
| Hover | [COR_HEX] | Interação |
| Disabled | [COR_HEX] | Desabilitado |
| Outline | transparent + [COR_HEX] | Secundário |

---

## Tipografia

### Sistema de Fontes

**Google Fonts (web):**
- **Títulos e destaques:** [NOME_DA_FONTE] (weight [PESO])
- **Corpo, subtítulos e botões:** [NOME_DA_FONTE] (weight [PESO])
- **Código/mono:** [NOME_DA_FONTE_MONO]

**Fallback (local):**
- **Títulos:** system-ui, -apple-system, sans-serif
- **Corpo:** system-ui, sans-serif

### Escala Tipográfica

| Uso | Tamanho | Weight | Line-height |
|-----|---------|--------|-------------|
| H1 | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |
| H2 | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |
| H3 | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |
| H4 | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |
| Body | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |
| Small | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |
| Caption | [TAMANHO]px | [PESO] | [LINE_HEIGHT] |

---

## Estilo Geral

**Palavra-chave:** [ESTILO_PRINCIPAL]

[DESCREVER_O_ESTILO_GERAL_DA_MARCA]

Exemplo:
- Espaçamento generoso (respiro)
- Hierarquia visual clara
- Zero decoração não-funcional
- Acentos coloridos criam pontos focais

**Vibe:** [DESCREVER_VIBE_DA_MARCA]

---

## Elementos-chave

### Bordas
- **Padrão:** [ESPECIFICAÇÃO]
- **Cards:** [ESPECIFICAÇÃO]
- **Input focado:** [ESPECIFICAÇÃO]

### Border-radius
- **Cards:** [VALOR]px ([DESCRIÇÃO])
- **Botões:** [VALOR]px ([DESCRIÇÃO])
- **Pills/badges:** [VALOR]px ([DESCRIÇÃO])
- **Containers grandes:** [VALOR]px

### Botões

**Primary:**
```css
background: [COR];
color: [COR];
border: [ESPECIFICAÇÃO];
border-radius: [VALOR]px;
padding: [ESPECIFICAÇÃO];
font-weight: [PESO];
transition: all 0.2s ease;
```

**Secondary:**
```css
background: transparent;
color: [COR];
border: [ESPECIFICAÇÃO];
border-radius: [VALOR]px;
padding: [ESPECIFICAÇÃO];
font-weight: [PESO];
```

### Sombras

```css
/* Card sutil */
box-shadow: [ESPECIFICAÇÃO];

/* Card com hover */
box-shadow: [ESPECIFICAÇÃO];

/* Dropdown/modal */
box-shadow: [ESPECIFICAÇÃO];
```

### Spacing

Escala baseada em [VALOR]px:
- xs: [VALOR]px
- sm: [VALOR]px
- md: [VALOR]px
- lg: [VALOR]px
- xl: [VALOR]px
- 2xl: [VALOR]px
- 3xl: [VALOR]px

---

## O que NUNCA fazer

- ❌ [REGRAS_ESPECÍFICAS_DA_MARCA]
- ❌ [REGRAS_ESPECÍFICAS_DA_MARCA]
- ❌ [REGRAS_ESPECÍFICAS_DA_MARCA]

---

## Logo

### Marca [NOME_DA_EMPRESA]

**Conceito:** [CONCEITO_DO_LOGO]

**Especificações:**
- **Arquivo:** `identidade/logo.svg` (vector), `identidade/logo.png` (raster)
- **Versão dark mode:** `identidade/logo-white.svg`
- **Font:** [NOME_DA_FONTE], weight [PESO]
- **Cor:** [COR] (light mode), [COR] (dark mode)
- **Accent:** [DESCRIÇÃO]

### Uso do Logo

| Contexto | Tamanho | Versão |
|----------|---------|--------|
| Header de site | [TAMANHO] altura | SVG |
| Slide final carrossel | [TAMANHO] largura | PNG |
| PDF/propostas | [TAMANHO] largura | SVG |
| Favicon | [TAMANHO] | Ícone específico |

### Clear space

Manter espaço mínimo ao redor do logo igual à [ESPECIFICAÇÃO].

---

## Templates e Componentes

### Card Base

```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card description with proper hierarchy.</p>
</div>
```

```css
.card {
  background: [COR];
  border: [ESPECIFICAÇÃO];
  border-radius: [VALOR]px;
  padding: [VALOR]px;
}
```

### Badge/Pill

```css
.badge {
  display: inline-block;
  padding: [ESPECIFICAÇÃO];
  background: [COR];
  color: [COR];
  border-radius: [VALOR]px;
  font-size: [TAMANHO]px;
  font-weight: [PESO];
}
```

### Section Break

```css
.section-divider {
  height: [VALOR]px;
  background: [COR];
  margin: [VALOR]px 0;
}
```

---

## Design Tokens

```css
:root {
  /* Cores */
  --color-bg-primary: [COR];
  --color-bg-card: [COR];
  --color-accent: [COR];
  --color-text-primary: [COR];
  --color-text-secondary: [COR];
  --color-border: [COR];

  /* Tipografia */
  --font-sans: '[NOME_DA_FONTE]', system-ui, sans-serif;
  --font-mono: '[NOME_DA_FONTE_MONO]', monospace;

  /* Spacing */
  --space-xs: [VALOR]px;
  --space-sm: [VALOR]px;
  --space-md: [VALOR]px;
  --space-lg: [VALOR]px;
  --space-xl: [VALOR]px;

  /* Border radius */
  --radius-sm: [VALOR]px;
  --radius-md: [VALOR]px;
  --radius-lg: [VALOR]px;
  --radius-pill: [VALOR]px;

  /* Sombras */
  --shadow-sm: [ESPECIFICAÇÃO];
  --shadow-md: [ESPECIFICAÇÃO];
  --shadow-lg: [ESPECIFICAÇÃO];
}
```

---

## Observações finais

**Criado:** [DATA]
**Versão:** [VERSAO]
**Status:** Template para customização pelo cliente

**Instruções:**
1. Substitua todos os campos [EM_COLCHETES] pelas informações da marca do cliente
2. Mantenha a estrutura base para compatibilidade com skills do 2100OS
3. Salve o logo do cliente como `logo.svg`, `logo.png` e `logo-white.svg`
4. Atualize `tokens.css` com as cores da marca