const fs = require('fs');
const path = require('path');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const folder = '.'; // carpeta con tus .html
const output = [];

fs.readdirSync(folder).forEach(file => {
  if (file.endsWith('.html')) {
    const html = fs.readFileSync(path.join(folder, file), 'utf-8');
    const dom = new JSDOM(html);
    const text = dom.window.document.body.textContent.replace(/\s+/g, ' ').trim();
    output.push({
      title: file.replace('.html', ''),
      text: text
    });
  }
});

fs.writeFileSync('contenido.json', JSON.stringify(output, null, 2));
console.log('contenido.json creado!');
