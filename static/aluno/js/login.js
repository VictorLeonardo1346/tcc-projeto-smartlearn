document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = document.getElementById("nome").value.trim();
  const senha = document.getElementById("senha").value.trim();

  if (!nome || !senha) {
    alert("Preencha todos os campos.");
    return;
  }

  const resp = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ nome, senha })
  });

  if (resp.redirected) {
    window.location.href = resp.url;  // redireciona para /aluno
  } else {
    const data = await resp.text();
    alert("Usuário ou senha incorretos");
  }
});
