#!/usr/bin/env node
/**
 * Claude Code Skill Installer
 * 
 * Installs PaperPilot skills to Claude Code's skill directory
 * Default: ~/.config/claude-code/skills/
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS = [
  'paper-assistant',
  'paper-literature-review',
  'paper-hypothesis',
  'paper-code',
  'paper-experiment',
  'paper-writing'
];

function getClaudeCodeSkillsDir() {
  const home = os.homedir();
  return path.join(home, '.config', 'claude-code', 'skills');
}

function install() {
  const skillsDir = getClaudeCodeSkillsDir();
  const sourceDir = path.join(__dirname, '..');
  
  console.log('📦 Installing PaperPilot skills to Claude Code...');
  console.log(`   Target: ${skillsDir}`);
  
  // Create skills directory if not exists
  if (!fs.existsSync(skillsDir)) {
    fs.mkdirSync(skillsDir, { recursive: true });
  }
  
  let installed = 0;
  
  for (const skill of SKILLS) {
    const sourcePath = path.join(sourceDir, skill);
    const targetPath = path.join(skillsDir, skill);
    
    if (fs.existsSync(sourcePath)) {
      copyDir(sourcePath, targetPath);
      console.log(`   ✅ ${skill}`);
      installed++;
    } else {
      console.log(`   ⚠️  ${skill} not found, skipping`);
    }
  }
  
  console.log(`\n✨ Done! Installed ${installed} skills.`);
  console.log('\n📝 Usage in Claude Code:');
  console.log('   Skills will auto-load based on your prompts.');
}

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

install();
