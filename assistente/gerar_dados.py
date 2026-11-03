"""
gerar_dados.py — Base de dados fictícia da LojaTech para a UC10.

Execute UMA vez, na pasta do projeto:
    python gerar_dados.py

O script cria a pasta dados/ com todos os arquivos usados nas aulas.
Todos os nomes, e-mails e telefones são fictícios.
"""
import csv
import os
from datetime import date, timedelta

os.makedirs("dados", exist_ok=True)


def salvar_csv(nome, cabecalho, linhas):
    """Grava uma lista de linhas em dados/<nome> no formato CSV (UTF-8)."""
    with open(f"dados/{nome}", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)
    print(f"dados/{nome:<28} {len(linhas):>4} linhas")


# ------------------------------------------------------------------
# 1. Catálogo de produtos
# ------------------------------------------------------------------
produtos = [
    # id, nome, categoria, preço, estoque e (na linha de baixo) a descrição
    (1, "Mouse Óptico Flow", "Periféricos", 69.90, 40,
     "mouse óptico sem fio ergonômico para escritório"),
    (2, "Teclado Mecânico Spark", "Periféricos", 349.90, 25,
     "teclado mecânico gamer rgb switch azul"),
    (3, "Monitor IPS 24 Vision", "Monitores", 899.90, 12,
     "monitor ips 24 polegadas full hd para escritório e jogos"),
    (4, "SSD NVMe 1 TB", "Armazenamento", 429.90, 30,
     "ssd nvme 1tb alta velocidade para upgrade do computador"),
    (5, "Mouse Gamer Strike", "Periféricos", 189.90, 35,
     "mouse gamer rgb 16000 dpi com botões programáveis"),
    (6, "Headset Gamer Echo", "Áudio", 299.90, 18,
     "headset gamer som surround com microfone"),
    (7, "Webcam Full HD Meet", "Acessórios", 249.90, 22,
     "webcam full hd com microfone para reuniões e home office"),
    (8, "Headset Office Talk", "Áudio", 159.90, 28,
     "headset com microfone para home office e reuniões"),
    (9, "Memória RAM 16 GB", "Componentes", 279.90, 20,
     "memória ram ddr4 16gb para upgrade de desempenho"),
    (10, "HD Externo 2 TB", "Armazenamento", 389.90, 15,
     "hd externo 2tb portátil para backup usb"),
    (11, "Cadeira Gamer Pro", "Móveis", 1199.90, 6,
     "cadeira gamer ergonômica reclinável"),
    (12, "Suporte Articulado Monitor", "Acessórios", 159.90, 14,
     "suporte articulado para monitor ergonomia no escritório"),
    (13, "Mousepad Gamer XL", "Periféricos", 79.90, 50,
     "mousepad gamer grande com borda rgb"),
    (14, "Pen Drive 64 GB", "Armazenamento", 39.90, 80,
     "pen drive 64gb usb portátil"),
    (15, "Notebook Pro 14", "Computadores", 3499.90, 8,
     "notebook 14 polegadas 16gb ssd para trabalho e estudo"),
    (16, "Hub USB-C 7 em 1", "Acessórios", 199.90, 0,
     "hub usb-c com hdmi para notebook e home office"),
    (17, "Controle Gamer Sem Fio", "Periféricos", 229.90, 20,
     "controle gamer sem fio para pc e console"),
    (18, "Microfone USB Podcast", "Áudio", 349.90, 10,
     "microfone usb para reuniões lives e podcast"),
    (19, "SSD Externo 500 GB", "Armazenamento", 459.90, 12,
     "ssd externo 500gb portátil usb-c alta velocidade para backup"),
    (20, "Luminária LED de Mesa", "Acessórios", 129.90, 25,
     "luminária led de mesa para escritório e home office"),
]
salvar_csv("produtos.csv",
           ["id_produto", "nome", "categoria", "preco", "estoque",
            "descricao"],
           produtos)

# ------------------------------------------------------------------
# 2. Clientes (dados pessoais fictícios — usados na aula de LGPD)
# ------------------------------------------------------------------
clientes = [
    # id, nome, e-mail, telefone, cidade, cadastro, aceita personalização
    ("C01", "Ana Souza", "ana@exemplo.test", "(11) 90000-0001",
     "São Paulo", "2025-03-10", "sim"),
    ("C02", "Bruno Lima", "bruno@exemplo.test", "(21) 90000-0002",
     "Rio de Janeiro", "2025-06-22", "sim"),
    ("C03", "Carla Mendes", "carla@exemplo.test", "(31) 90000-0003",
     "Belo Horizonte", "2024-11-05", "sim"),
    ("C04", "Davi Rocha", "davi@exemplo.test", "(41) 90000-0004",
     "Curitiba", "2025-01-18", "sim"),
    ("C05", "Elisa Prado", "elisa@exemplo.test", "(51) 90000-0005",
     "Porto Alegre", "2025-08-02", "sim"),
    ("C06", "Felipe Alves", "felipe@exemplo.test", "(11) 90000-0006",
     "Campinas", "2026-02-14", "sim"),
    ("C07", "Gabi Nunes", "gabi@exemplo.test", "(71) 90000-0007",
     "Salvador", "2025-09-30", "sim"),
    ("C08", "Heitor Dias", "heitor@exemplo.test", "(61) 90000-0008",
     "Brasília", "2024-07-12", "sim"),
    ("C09", "Iara Costa", "iara@exemplo.test", "(81) 90000-0009",
     "Recife", "2025-04-25", "nao"),
    ("C10", "João Pires", "joao@exemplo.test", "(85) 90000-0010",
     "Fortaleza", "2026-05-03", "sim"),
    ("C11", "Lia Martins", "lia@exemplo.test", "(11) 90000-0011",
     "São Paulo", "2026-10-01", "sim"),
    ("C12", "Marcos Teles", "marcos@exemplo.test", "(19) 90000-0012",
     "Sorocaba", "2026-10-20", "sim"),
]
salvar_csv("clientes.csv",
           ["id_cliente", "nome", "email", "telefone", "cidade",
            "data_cadastro", "aceita_personalizacao"], clientes)

# ------------------------------------------------------------------
# 3. Interações (comportamento de navegação e compra)
#    setembro até 14/out = histórico | 16/out em diante = período de teste
# ------------------------------------------------------------------
perfis = {
    # cliente: (compras,    visualizações,  carrinho,  compras no teste)
    "C01": ([5, 13, 2],     [6, 11, 3],     [6],       [6, 17]),
    "C02": ([5, 2, 6],      [13, 11, 17],   [11],      [13, 11]),
    "C03": ([7, 8, 1],      [12, 3, 20],    [12],      [3, 12]),
    "C04": ([3, 12, 7],     [8, 15],        [16],      [8, 20]),
    "C05": ([4, 9, 14],     [10],           [10],      [10, 19]),
    "C06": ([4, 9, 19],     [2, 6],         [2],       [2, 13]),
    "C07": ([2, 6, 17],     [5, 11, 13],    [],        [5]),
    "C08": ([15, 16, 18],   [7, 3, 8],      [7],       [7, 3]),
    "C09": ([1, 14, 20],    [5, 4],         [],        [8]),
    "C10": ([10, 14],       [4, 9, 19],     [],        [4]),
    "C11": ([],             [3],            [],        []),
    "C12": ([],             [],             [],        []),
}

inicio_historico = date(2026, 9, 1)
inicio_teste = date(2026, 10, 16)
interacoes = []
for i, (cliente, perfil) in enumerate(perfis.items()):
    compras, vistos, carrinho, futuras = perfil
    k = 0
    eventos = (("visualizacao", vistos), ("carrinho", carrinho),
               ("compra", compras))
    for evento, lista in eventos:
        for produto in lista:
            dia = inicio_historico + timedelta(days=(i * 3 + k * 5) % 44)
            interacoes.append([cliente, produto, evento, dia.isoformat()])
            k += 1
    for j, produto in enumerate(futuras):
        dia = inicio_teste + timedelta(days=(i + j * 4) % 15)
        interacoes.append([cliente, produto, "compra", dia.isoformat()])

# problemas propositais para a aula de preparação de dados (Aula 2)
duplicada = next(linha for linha in interacoes
                 if linha[:3] == ["C01", 5, "compra"])
interacoes.append(list(duplicada))                          # linha duplicada
interacoes.append(["C04", "", "visualizacao", "2026-09-20"])  # sem produto
interacoes.append(["C07", 13, " Compra ", "2026-10-02"])     # fora do padrão
interacoes.sort(key=lambda linha: (linha[3], linha[0]))
salvar_csv("interacoes.csv", ["id_cliente", "id_produto", "evento", "data"],
           interacoes)

# ------------------------------------------------------------------
# 4. Avaliações explícitas (nota de 1 a 5 dada após a compra)
# ------------------------------------------------------------------
notas_especiais = {("C01", 2): 3, ("C02", 6): 4, ("C03", 1): 3, ("C04", 7): 5,
                   ("C05", 14): 3, ("C06", 19): 4, ("C07", 17): 4,
                   ("C08", 16): 2, ("C09", 20): 4, ("C10", 14): 2}
avaliacoes = []
for cliente, (compras, *_resto) in perfis.items():
    for produto in compras:
        nota = notas_especiais.get((cliente, produto), 5)   # padrão: nota 5
        avaliacoes.append([cliente, produto, nota])
salvar_csv("avaliacoes.csv", ["id_cliente", "id_produto", "nota"], avaliacoes)

# ------------------------------------------------------------------
# 5. Pedidos (consultados pelo assistente virtual)
# ------------------------------------------------------------------
pedidos = [
    (1001, "C01", "ENTREGUE", "2026-10-05"),
    (1002, "C02", "EM TRANSPORTE", "2026-11-06"),
    (1003, "C03", "EM SEPARAÇÃO", "2026-11-09"),
    (1004, "C04", "ENTREGUE", "2026-10-12"),
    (1005, "C05", "CANCELADO", ""),
    (1006, "C06", "EM TRANSPORTE", "2026-11-05"),
    (1007, "C07", "AGUARDANDO PAGAMENTO", ""),
    (1008, "C08", "ENTREGUE", "2026-10-28"),
]
salvar_csv("pedidos.csv",
           ["id_pedido", "id_cliente", "status", "previsao_entrega"], pedidos)

# ------------------------------------------------------------------
# 6. Frases rotuladas por intenção (treino do classificador do chatbot)
# ------------------------------------------------------------------
frases = {
    "saudacao": [
        "oi", "olá, tudo bem?", "bom dia", "boa tarde, preciso de ajuda",
        "e aí", "boa noite", "oi, alguém aí?", "olá, quero atendimento",
        "oi, bom dia!", "olá", "boa tarde", "oi, tudo certo?",
    ],
    "recomendar": [
        "me indica um mouse", "quero uma sugestão de presente",
        "qual teclado vocês recomendam",
        "procuro um headset para home office",
        "me recomenda algo para jogar", "o que combina com meu monitor",
        "quero melhorar meu computador", "sugere um produto até 300 reais",
        "qual produto você indica para mim", "me sugere um presente gamer",
        "recomenda uma webcam boa", "o que vocês indicam para escritório",
    ],
    "status_pedido": [
        "onde está meu pedido", "meu pedido 1002 já saiu?",
        "quero rastrear minha compra", "qual a previsão de entrega do pedido",
        "status do pedido 1006", "minha encomenda não chegou",
        "já enviaram meu pedido?", "acompanhar entrega",
        "meu pedido está atrasado", "quando chega meu pedido",
        "rastrear pedido 1003", "situação da minha entrega",
    ],
    "troca_devolucao": [
        "quero trocar um produto", "como faço para devolver",
        "o mouse veio com defeito", "preciso devolver o teclado",
        "posso trocar por outro modelo", "produto chegou quebrado",
        "quero meu dinheiro de volta", "política de troca",
        "quero fazer uma devolução",
        "o produto veio com defeito, quero trocar", "como trocar um item",
        "devolver produto",
    ],
    "horario": [
        "que horas vocês atendem", "qual o horário de atendimento",
        "vocês abrem sábado?", "até que horas funciona o atendimento",
        "atendem domingo?", "horário da loja",
        "o atendimento funciona à noite?", "quando posso falar com vocês",
        "qual o horário do suporte", "vocês atendem feriado?",
        "horário de funcionamento", "abre que horas",
    ],
    "falar_humano": [
        "quero falar com um atendente", "me passa para uma pessoa",
        "atendente humano por favor", "não quero falar com robô",
        "chama alguém de verdade", "preciso de um humano",
        "transferir para atendente", "falar com o suporte humano",
        "quero uma pessoa real", "me transfere para um atendente",
        "falar com humano", "tem algum atendente aí?",
    ],
    "despedida": [
        "tchau", "obrigado, era só isso", "valeu", "até mais",
        "pode encerrar",
        "obrigada pela ajuda", "falou", "encerrar atendimento",
        "tchau, obrigado", "era só isso mesmo", "até logo", "valeu, tchau",
    ],
}
linhas_frases = [[frase, intencao]
                 for intencao, lista in frases.items() for frase in lista]
salvar_csv("intencoes.csv", ["frase", "intencao"], linhas_frases)

# ------------------------------------------------------------------
# 7. Base de conhecimento (políticas usadas pelo assistente / RAG)
# ------------------------------------------------------------------
base = [
    ("troca",
     "Trocas e devoluções podem ser solicitadas em até 7 dias após o "
     "recebimento. O produto deve estar na embalagem original. Produtos com "
     "defeito têm 30 dias para troca."),
    ("entrega",
     "O prazo de entrega aparece no acompanhamento do pedido. Capitais "
     "recebem em até 5 dias úteis e demais cidades em até 10 dias úteis "
     "após a confirmação do pagamento."),
    ("pagamento",
     "Aceitamos cartão de crédito em até 10 vezes sem juros, boleto e Pix. "
     "Pedidos pagos com Pix são confirmados em poucos minutos."),
    ("garantia",
     "Todos os produtos têm garantia legal de 90 dias. Alguns fabricantes "
     "oferecem garantia estendida de 12 meses, informada na página do "
     "produto."),
    ("privacidade",
     "Os dados pessoais são usados apenas para processar pedidos e, com "
     "consentimento, personalizar recomendações. O cliente pode pedir acesso"
     " ou exclusão dos dados a qualquer momento."),
    ("atendimento",
     "O atendimento humano funciona de segunda a sexta, das 9h às 18h, e aos"
     " sábados das 9h às 13h. O assistente virtual funciona 24 horas."),
]
salvar_csv("base_conhecimento.csv", ["tema", "texto"], base)

# ------------------------------------------------------------------
# 8. Teste A/B (dois algoritmos de recomendação em produção por 14 dias)
#    A = recomendação por popularidade | B = recomendação híbrida
# ------------------------------------------------------------------
ab = []
for dia in range(1, 15):
    sessoes_a = 170 + (dia * 7) % 23
    sessoes_b = 168 + (dia * 11) % 25
    conv_a = 6 + (dia * 5) % 4
    conv_b = 8 + (dia * 3) % 5
    ab.append([dia, "A", sessoes_a, round(sessoes_a * 0.11), conv_a])
    ab.append([dia, "B", sessoes_b, round(sessoes_b * 0.15), conv_b])
salvar_csv("ab_teste.csv",
           ["dia", "grupo", "sessoes", "cliques", "conversoes"], ab)

# ------------------------------------------------------------------
# 9. Log diário do assistente virtual (monitoramento — Aula 17)
#    Na 2ª semana surge um assunto novo (Pix parcelado) que o bot
#    não conhece.
# ------------------------------------------------------------------
log = []
for dia in range(1, 15):
    conversas = 120 + (dia * 13) % 30
    taxa_fallback = 0.06 + (0.09 if dia > 7 else 0) + ((dia % 3) * 0.01)
    fallback = round(conversas * taxa_fallback)
    transferidas = round(conversas * 0.08) + (dia > 7) * 6
    resolvidas = conversas - fallback - transferidas
    nota = round(4.5 - (0.5 if dia > 7 else 0) - (dia % 2) * 0.1, 1)
    log.append([f"2026-10-{dia:02d}", conversas, resolvidas, transferidas,
                fallback, nota])
salvar_csv("log_atendimento.csv",
           ["data", "conversas", "resolvidas", "transferidas", "fallback",
            "nota_media"], log)

# ------------------------------------------------------------------
# 10. Feedback das recomendações exibidas (ajuste contínuo — Aula 17)
# ------------------------------------------------------------------
feedback = []
categorias = ["Periféricos", "Áudio", "Armazenamento", "Acessórios"]
for semana in (1, 2):
    for c, categoria in enumerate(categorias):
        exibidas = 200
        if semana == 1:
            cliques = [30, 12, 22, 16][c]
        else:
            cliques = [18, 34, 20, 15][c]   # interesse por Áudio cresceu
        feedback.append([semana, categoria, exibidas, cliques])
salvar_csv("feedback_recomendacoes.csv",
           ["semana", "categoria", "exibidas", "cliques"], feedback)

print("\nBase da LojaTech criada com sucesso na pasta dados/")
