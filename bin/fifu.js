#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// This script aims to run the 'fifu' command.
// If installed via pip, 'fifu' should be in the PATH.
// If using the bundled binary, it would be different, 
// but for an npm package that isn't pulling down binaries, 
// we assume the user has the python environment or we point them to it.

const child = spawn('fifu', process.argv.slice(2), {
  stdio: 'inherit',
  shell: true
});

child.on('error', (err) => {
  if (err.code === 'ENOENT') {
    console.error('Error: "fifu" command not found.');
    console.error('Please install the python package first: pip install fifu');
  } else {
    console.error(`Error: ${err.message}`);
  }
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code);
});
