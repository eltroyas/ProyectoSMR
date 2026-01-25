// netlify/functions/chat.js
const fetch = require("node-fetch");
const contenido = require("../../contenido.json");

exports.handler = async function(event, context) {
  try {
    const { message } = JSON.parse(event.body);

    const matches = contenido.filter(c =>
      message.split(" ").some(word =>
        c.text.toLowerCase().includes(word.toLowerCase())
      )
    );
    const contextText = matches.map(m => m.text).join("\n\n");

    const prompt = contextText
      ? `Usa este contexto de mi web para responder la pregunta:\n${contextText}\n\nPregunta: ${message}\nRespuesta:`
      : `Responde de la mejor manera posible a la pregunta: ${message}`;

    const HF_TOKEN = process.env.HF_TOKEN;
    const MODEL = "nomic-ai/gpt4all-j";
    const HF_URL = `https://api-inference.huggingface.co/models/${MODEL}`;

    // Timeout de 9 segundos
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
        body: JSON.stringify({ inputs: prompt }),
        signal: controller.signal
      });
      data = await res.json();
    } catch (err) {
      console.error("Error Hugging Face:", err);
      return {
        statusCode: 500,
        body: JSON.stringify({ reply: "El servidor tardó demasiado o hubo un error." })
      };
    } finally {
      clearTimeout(timeout);
    }

    let reply = "Lo siento, no tengo respuesta";
    if (Array.isArray(data)) {
      reply = data[0]?.generated_text || reply;
    } else if (typeof data === "string") {
      reply = data;
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
