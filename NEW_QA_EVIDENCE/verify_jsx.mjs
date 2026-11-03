// Source parser only. NOT a Vite build, module resolver, or browser execution.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url);
const ts=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/typescript/lib/typescript.js');
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):/\.(jsx|js|mjs)$/.test(e.name)?[path.join(dir,e.name)]:[])}
const files=[...walk('src'),...walk('tests'),...walk('e2e'),...['vite.config.js','tailwind.config.js','postcss.config.js','playwright.config.js']];
let errors=0;
for(const f of files){const src=fs.readFileSync(f,'utf8');const ast=ts.createSourceFile(f,src,ts.ScriptTarget.Latest,true,f.endsWith('.jsx')?ts.ScriptKind.JSX:ts.ScriptKind.JS);for(const d of ast.parseDiagnostics){errors++;console.log(`${f}: ${d.messageText}`)}}
console.log(`Parsed ${files.length} JavaScript/JSX files; syntax errors: ${errors}`);process.exitCode=errors?1:0;
