require("dotenv").config();
const express = require("express");
const cors = require("cors");
const fetch = require("node-fetch");
const path = require("path");

const contenido = require("contenido.json");

const app = express();
app.use(cors());
app.use(express.json());

// Servir archivos estáticos desde /chatbot/public
app.use(express.static(path.join(__dirname, "public")));

const PORT = 3001; // Usamos 3001 para no chocar con tu web principal

// ===============================
// RAG simple
// ===============================
function buscarContexto(message) {
  const keywords = message.toLowerCase().split(" ");
  
  const matches = contenido.filter(c =>
    keywords.some(word => c.text.toLowerCase().includes(word))
  ).slice(0, 3);

  return matches.map(m => m.text).join("\n\n");
}

// ===============================
// Endpoint del chat
// ===============================
app.post("/chat", async (req, res) => {
  try {
    let { message } = req.body;

    if (!message) {
      return res.status(400).json({ reply: "No se recibió mensaje." });
    }

    message = message.replace(/[\n\r]/g, " ").slice(0, 500);

    const contextText = buscarContexto(message);

    const prompt = contextText
      ? `Usa este contexto para responder:\n${contextText}\n\nPregunta: ${message}\nRespuesta:`
      : `Responde claramente: ${message}`;

    const response = await fetch(
      "https://router.huggingface.co/v1/chat/completions",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "Qwen/Qwen3-4B-Instruct-2507:nscale",
          messages: [{ role: "user", content: prompt }],
          temperature: 0.7,
          max_tokens: 300
        })
      }
    );

    const data = await response.json();

    let reply = "No tengo respuesta.";
    if (data?.choices?.length > 0) {
      reply = data.choices[0].message.content;
    }

    res.json({ reply });

  } catch (err) {
    console.error(err);
    res.status(500).json({ reply: "Error en el servidor." });
  }
});

app.listen(PORT, () => {
  console.log(`Chatbot funcionando en http://localhost:${PORT}`);
});
