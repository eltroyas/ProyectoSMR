// netlify/functions/chat.js
const fetch = require("node-fetch");
const contenido = require("../../contenido.json"); // tu contenido de la web

exports.handler = async function(event, context) {
  try {
    const { message } = JSON.parse(event.body || "{}");
    if (!message) {
      return { statusCode: 400, body: JSON.stringify({ reply: "No se recibió mensaje." }) };
    }

    // ---------------------------
    // Búsqueda básica en tu contenido (RAG)
    // ---------------------------
    const matches = contenido.filter(c =>
      message.split(" ").some(word =>
        c.text.toLowerCase().includes(word.toLowerCase())
      )
    );
    const contextText = matches.map(m => m.text).join("\n\n");

    const prompt = contextText
      ? `Usa este contexto de mi web para responder la pregunta:\n${contextText}\n\nPregunta: ${message}\nRespuesta:`
      : `Responde de la mejor manera posible a la pregunta: ${message}`;

    // ---------------------------
    // Hugging Face Chat Completions API
    // ---------------------------
    const HF_TOKEN = process.env.HF_TOKEN;
    if (!HF_TOKEN) throw new Error("HF_TOKEN no configurado en Netlify");

    const MODEL = "Qwen/Qwen3-4B-Instruct-2507:nscale"; // versión válida
    const HF_URL = "https://router.huggingface.co/v1/chat/completions";

    // Timeout de 9 segundos (Netlify free tier = 10s)
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 9000);

    let data;
    try {
      const res = await fetch(HF_URL, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: MODEL,
          messages: [{ role: "user", content: prompt }],
          temperature: 0.7,
          max_new_tokens: 200
        }),
        signal: controller.signal
      });

      data = await res.json();
    } catch (err) {
      console.error("Error Hugging Face:", err);
      return {
        statusCode: 500,
        body: JSON.stringify({ reply: "El servidor tardó demasiado o hubo un error en Hugging Face." })
      };
    } finally {
      clearTimeout(timeout);
    }

    // ---------------------------
    // Extraer respuesta segura
    // ---------------------------
    let reply = "Lo siento, no tengo respuesta.";
    if (data?.choices && Array.isArray(data.choices)) {
      reply = data.choices[0]?.message?.content || reply;
    } else if (data?.error) {
      reply = "Error Hugging Face: " + data.error;
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ reply })
    };

  } catch (err) {
    console.error("Error en la función:", err);
    return {
      statusCode: 500,
      body: JSON.stringify({ reply: "Error interno en el servidor." })
    };
  }
};

