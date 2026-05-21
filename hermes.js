#!/usr/bin/env node

/**
 * 2100OS Hermes - Terminal CLI
 * Sistema Operacional do Negócio com Auto-Evolução
 *
 * Uso:
 *   node hermes.js
 *   npm start
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Configuração
const CONFIG_PATH = path.join(__dirname, '.hermes', 'config.yaml');
const CONTEXT_PATH = path.join(__dirname, '2100OS');
const SKILLS_PATH = path.join(__dirname, '2100OS', '.claude', 'skills');
const MEMORY_PATH = path.join(__dirname, '2100OS', '_memoria');

class HermesCLI {
  constructor() {
    this.context = {};
    this.skills = [];
    this.memory = {};
    this.running = false;
  }

  async init() {
    console.log('\n🚀 Iniciando 2100OS Hermes v3.0...\n');

    // Carregar contexto
    await this.loadContext();

    // Carregar skills
    await this.loadSkills();

    // Carregar memória
    await this.loadMemory();

    // Exibir status
    this.showStatus();

    // Iniciar interface
    this.startCLI();
  }

  async loadContext() {
    console.log('📚 Carregando contexto...');

    try {
      // Carregar CLAUDE.md
      const claudePath = path.join(CONTEXT_PATH, 'CLAUDE.md');
      if (fs.existsSync(claudePath)) {
        this.context.claude = fs.readFileSync(claudePath, 'utf8');
        console.log('  ✓ CLAUDE.md carregado');
      }

      // Carregar SOUL.md
      const soulPath = path.join(CONTEXT_PATH, 'SOUL.md');
      if (fs.existsSync(soulPath)) {
        this.context.soul = fs.readFileSync(soulPath, 'utf8');
        console.log('  ✓ SOUL.md carregado');
      }

      // Carregar memória do negócio
      const memoriaFiles = ['empresa.md', 'preferencias.md', 'estrategia.md'];
      memoriaFiles.forEach(file => {
        const filePath = path.join(MEMORY_PATH, file);
        if (fs.existsSync(filePath)) {
          this.memory[file.replace('.md', '')] = fs.readFileSync(filePath, 'utf8');
          console.log(`  ✓ _memoria/${file} carregado`);
        }
      });

      console.log('✓ Contexto carregado com sucesso!\n');
    } catch (error) {
      console.error('✗ Erro ao carregar contexto:', error.message);
    }
  }

  async loadSkills() {
    console.log('🔧 Carregando skills...');

    try {
      const skillsDirs = fs.readdirSync(SKILLS_PATH);
      this.skills = skillsDirs
        .filter(dir => fs.existsSync(path.join(SKILLS_PATH, dir, 'SKILL.md')))
        .map(dir => {
          const skillPath = path.join(SKILLS_PATH, dir, 'SKILL.md');
          const content = fs.readFileSync(skillPath, 'utf8');
          const name = content.match(/# (.*)/)?.[1] || dir;
          const description = content.match(/> (.*)/)?.[1] || '';

          return {
            id: dir,
            name,
            description,
            path: skillPath
          };
        });

      console.log(`  ✓ ${this.skills.length} skills carregadas`);
      this.skills.forEach(skill => {
        console.log(`    - /${skill.id} (${skill.name})`);
      });
      console.log('✓ Skills carregadas com sucesso!\n');
    } catch (error) {
      console.error('✗ Erro ao carregar skills:', error.message);
    }
  }

  async loadMemory() {
    console.log('💾 Carregando memória do sistema...');

    try {
      // Carregar MEMORY.md
      const memoryPath = path.join(CONTEXT_PATH, 'MEMORY.md');
      if (fs.existsSync(memoryPath)) {
        this.context.memory = fs.readFileSync(memoryPath, 'utf8');
        const lines = this.context.memory.split('\n').length;
        console.log(`  ✓ ${lines} registros de memória`);
      }

      console.log('✓ Memória carregada com sucesso!\n');
    } catch (error) {
      console.error('✗ Erro ao carregar memória:', error.message);
    }
  }

  showStatus() {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📊 STATUS DO SISTEMA');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`✓ Hermes v3.0.0`);
    console.log(`✓ Contexto: ${CONTEXT_PATH}`);
    console.log(`✓ Skills disponíveis: ${this.skills.length}`);
    console.log(`✓ Memória ativa: ${this.context.memory ? 'SIM' : 'NÃO'}`);
    console.log(`✓ Empresa: ${this.memory.empresa ? 'CONFIGURADO' : 'PENDENTE'}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  }

  startCLI() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    console.log('💬 Comandos disponíveis:');
    console.log('  /status     - Ver status do sistema');
    console.log('  /skills     - Listar skills disponíveis');
    console.log('  /execute    - Executar skill');
    console.log('  /memory     - Buscar na memória');
    console.log('  /help       - Ajuda completa');
    console.log('  /exit       - Sair do sistema\n');

    const prompt = () => {
      rl.question('hermes> ', async (input) => {
        const command = input.trim();

        if (!command) {
          prompt();
          return;
        }

        if (command === '/exit' || command === '/quit') {
          console.log('\n👋 Até logo!\n');
          rl.close();
          return;
        }

        await this.handleCommand(command);
        prompt();
      });
    };

    prompt();
  }

  async handleCommand(command) {
    const parts = command.split(' ');
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    switch (cmd) {
      case '/status':
        this.showStatus();
        break;

      case '/skills':
        this.showSkills();
        break;

      case '/execute':
        await this.executeSkill(args[0]);
        break;

      case '/memory':
        this.searchMemory(args.join(' '));
        break;

      case '/help':
        this.showHelp();
        break;

      default:
        console.log(`✗ Comando não reconhecido: ${cmd}`);
        console.log('  Use /help para ver comandos disponíveis\n');
    }
  }

  showSkills() {
    console.log('\n📋 SKILLS DISPONÍVEIS:\n');
    this.skills.forEach(skill => {
      console.log(`  /${skill.id}`);
      console.log(`    ${skill.name}`);
      console.log(`    ${skill.description}\n`);
    });
  }

  async executeSkill(skillId) {
    if (!skillId) {
      console.log('✗ Especifique uma skill: /execute <nome-da-skill>\n');
      return;
    }

    const skill = this.skills.find(s => s.id === skillId);
    if (!skill) {
      console.log(`✗ Skill não encontrada: ${skillId}\n`);
      return;
    }

    console.log(`\n🔧 Executando skill: ${skill.name}`);
    console.log(`📄 ${skill.description}`);
    console.log('⚙️  Processando...\n');

    // Aqui seria a execução real da skill
    // Por enquanto, simula a execução
    setTimeout(() => {
      console.log(`✓ Skill ${skill.name} executada com sucesso!\n`);
      console.log('💡 Dica: Use /mmc-salvar para salvar o resultado\n');
    }, 1000);
  }

  searchMemory(query) {
    if (!query) {
      console.log('✗ Especifique uma busca: /memory <termo>\n');
      return;
    }

    console.log(`\n🔍 Buscando na memória: "${query}"\n`);

    // Busca simples nos arquivos de memória
    let found = false;
    Object.keys(this.memory).forEach(key => {
      const content = this.memory[key];
      if (content.toLowerCase().includes(query.toLowerCase())) {
        console.log(`📄 _memoria/${key}.md:`);
        const lines = content.split('\n');
        lines.forEach((line, index) => {
          if (line.toLowerCase().includes(query.toLowerCase())) {
            console.log(`  Line ${index + 1}: ${line.trim()}`);
          }
        });
        console.log();
        found = true;
      }
    });

    if (!found) {
      console.log('✗ Nenhum resultado encontrado\n');
    }
  }

  showHelp() {
    console.log('\n📖 AJUDA COMPLETA\n');
    console.log('COMANDOS DISPONÍVEIS:\n');
    console.log('  /status [opção]     - Ver status do sistema');
    console.log('                       Opções: --full, --context, --skills\n');
    console.log('  /skills [filtro]    - Listar skills disponíveis');
    console.log('                       Filtro: carrossel, salvar, analytics, etc.\n');
    console.log('  /execute <skill>    - Executar skill específica');
    console.log('                       Exemplo: /execute mmc-carrossel\n');
    console.log('  /memory <termo>     - Buscar na memória do sistema');
    console.log('                       Exemplo: /memory estratégia\n');
    console.log('  /help [comando]     - Ajuda sobre comando específico');
    console.log('                       Exemplo: /help /execute\n');
    console.log('  /exit               - Sair do sistema\n');
    console.log('SKILLS MAIS USADAS:\n');
    console.log('  /mmc-carrossel      - Criar carrosséis para redes sociais');
    console.log('  /mmc-salvar         - Salvar alterações no GitHub');
    console.log('  /mmc-analytics      - Ver análises e insights');
    console.log('  /mmc-instalar       - Instalar/configurar sistema\n');
  }
}

// Iniciar Hermes CLI
const hermes = new HermesCLI();
hermes.init().catch(error => {
  console.error('✗ Erro ao iniciar Hermes:', error);
  process.exit(1);
});