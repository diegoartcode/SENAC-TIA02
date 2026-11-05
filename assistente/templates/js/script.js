// comentario
const caixa = document.getElementById('mensagens');
console.log(caixa);

function mostrar(texto, classe){
    const div = document.createElement('div');
    div.className = classe;
    div.textContent = texto;

    caixa.appendChild(div);

    caixa.scrollTop = caixa.scrollHeight;
}

const formulario = document.getElementById('formulario');

formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();

    const campo = document.getElementById('texto');

    const mensagem = campo.value.trim();

    if (!mensagem) return;

    mostrar(mensagem, 'cliente');

    campo.value = "";

    const resposta = await fetch("/api/chat", {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mensagem:mensagem,
            id_cliente: "C03"
        })
    });
    const dados = await resposta.json();

    mostrar(dados.texto, 'bot');

    dados.sugestoes.forEach(p => {
        mostrar(
            `${p.nome} - R$ ${p.preco.toFixed(2)}`,
            'bot'
        )
 
    });
});