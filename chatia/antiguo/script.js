async function sendMessage() {
  const input = document.getElementById("msg");
  const chat = document.getElementById("chat");
  const msg = input.value.trim();
  
  if (!msg) return; // No enviar mensajes vacíos

  chat.innerHTML += `<p><b>Tú:</b> ${msg}</p>`;
  input.value = "";
  
  // Scroll hacia abajo
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("/.netlify/functions/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    chat.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
    chat.scrollTop = chat.scrollHeight; // Scroll tras respuesta
  } catch (error) {
    chat.innerHTML += `<p style="color:red;">Error al conectar con el servidor.</p>`;
  }
}

// Permitir enviar con la tecla Enter
document.getElementById("msg").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});