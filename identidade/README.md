# Identidade Visual — Template para Clientes

## 🎯 Sobre este diretório

Este diretório contém templates de identidade visual que devem ser personalizados com a marca do seu cliente.

## 📁 Arquivos

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `design-guide.md` | Template de guia de identidade visual | ⚠️ **PERSONALIZAR** |
| `tokens.css` | Template de design tokens | ⚠️ **PERSONALIZAR** |
| `logo.svg` | Logo placeholder do cliente | ⚠️ **SUBSTITUIR** |

## 🚀 Como usar

### Para cada cliente novo:

1. **Personalize o design-guide.md:**
   - Substitua todos os campos `[EM_COLCHETES]` pelas informações da marca
   - Defina cores, tipografia e estilo específicos do cliente
   - Mantenha a estrutura base para compatibilidade com skills

2. **Substitua o logo:**
   - Salve o logo do cliente como `logo.svg` (vetorial)
   - Crie versão PNG como `logo.png` (raster)
   - Para dark mode, salve como `logo-white.svg`

3. **Atualize os tokens:**
   - Edite `tokens.css` com as cores específicas da marca
   - Mantenha a estrutura de variáveis CSS

## 📋 Estrutura do design-guide.md

O arquivo deve conter:
- **Filosofia da marca** - Valores e posicionamento
- **Paleta de cores** - Primária e semântica
- **Tipografia** - Fontes e escala
- **Estilo geral** - Vibe e diretrizes
- **Elementos-chave** - Botões, cards, bordas
- **Design tokens** - Variáveis CSS

## 🔧 Integração com Skills

Skills do 2100OS leem automaticamente este arquivo:
- `/mmc-carrossel` - Usa cores e fontes para criar posts
- `/mmc-publicar-tema` - Aplica identidade visual em conteúdos
- Outras skills de conteúdo seguem as diretrizes aqui definidas

## ⚠️ Importante

- **Nunca entregue para o cliente com os valores placeholder**
- **Sempre mantenha backup do design-guide original**
- **Teste as cores antes de finalizar** (contraste, acessibilidade)
- **Valide com o cliente** antes de implementar

## 📞 Suporte

Para dúvidas sobre customização, consulte:
- Documentação do 2100OS
- Skills de design disponíveis
- Exemplos em `templates/identidade/`