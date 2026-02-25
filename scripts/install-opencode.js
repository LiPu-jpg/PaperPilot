#!/usr/bin/env node
/**
 * OpenCode Skill Installer
 * 
 * Installs PaperPilot skills to OpenCode's skill directory
 * Default: ~/.opencode/skills/
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

function getOpenCodeSkillsDir() {
  const home = os.homedir();
  // Try common OpenCode config locations
  const candidates = [
    path.join(home, '.config', 'opencode', 'skills'),
    path.join(home, '.opencode', 'skills'),
    path.join(home, '.local', 'share', 'opencode', 'skills')
  ];
    path.join(home, '.opencode', 'skills'),
    path.join(home, '.config', 'opencode', 'skills'),
    path.join(home, '.local', 'share', 'opencode', 'skills')
  ];
    path.join(home, '.config', 'opencode', 'skills'),
    path.join(home, '.opencode', 'skills'),
    path.join(home, '.local', 'share', 'opencode', 'skills')
  ];
  
  for (const dir of candidates) {
    if (fs.existsSync(dir)) {
      return dir;
  }
  
  // Default to first candidate
  return candidates[0];
}

function install() {
  const skillsDir = getOpenCodeSkillsDir();
  const sourceDir = path.join(__dirname, '..');
  
  console.log('📦 Installing PaperPilot skills to OpenCode...');
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
      // Copy skill directory
      copyDir(sourcePath, targetPath);
      console.log(`   ✅ ${skill}`);
      installed++;
    } else {
      console.log(`   ⚠️  ${skill} not found, skipping`);
    }
  }
  
  console.log(`\n✨ Done! Installed ${installed} skills.`);
  console.log('\n📝 Usage in OpenCode:');
  console.log('   1. Restart OpenCode');
  console.log('   2. Use skills like: "帮我写论文" or "帮我搜索文献"');
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
