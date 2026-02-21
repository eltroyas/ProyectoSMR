async function sendMessage() {
  const input = document.getElementById("msg");
  const chat = document.getElementById("chat");
  const msg = input.value.trim();

  if (!msg) return;

  addMessage(msg, "user");
  input.value = "";

  try {
    const res = await fetch("http://localhost:3001/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    addMessage(data.reply, "bot");

  } catch (error) {
    addMessage("Error conectando con el servidor.", "bot");
  }
}

function addMessage(text, type) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

document.getElementById("msg").addEventListener("keypress", function(e) {
  if (e.key === "Enter") sendMessage();
});
