const fs = require("fs");
const path = require("path");

const H5P_FOLDER = ".";
const OUTPUT_FILE = "contenido-h5p.json";

// Limpia HTML
function stripHTML(html) {
  return html
    .replace(/<[^>]*>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const results = [];

const files = fs.readdirSync(H5P_FOLDER).filter(f => f.endsWith(".json"));

files.forEach(file => {
  const raw = fs.readFileSync(path.join(H5P_FOLDER, file), "utf-8");
  const h5p = JSON.parse(raw);

  for (const cid in h5p.contents) {
    const content = h5p.contents[cid];
    if (!content.jsonContent) continue;

    const json = JSON.parse(content.jsonContent);
    const slides = json.presentation?.slides || [];

    let text = "";

    slides.forEach((slide, slideIndex) => {
      slide.elements?.forEach(el => {
        if (el.action?.params?.text) {
          text += stripHTML(el.action.params.text) + "\n\n";
        }
      });
    });

    if (text.trim()) {
      results.push({
        title: `H5P – ${file.replace(".json", "")}`,
        source: file,
        text: text
      });
    }
  }
});

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(results, null, 2));
console.log(`✅ ${OUTPUT_FILE} generado con ${results.length} documentos`);
