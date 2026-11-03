# UC10 — Chatbot RAG persistente + Groq + MySQL

## Funcionalidades
- Upload PDF (texto extraível), TXT, CSV e XLSX
- Embeddings multilíngues locais e indexação permanente no ChromaDB (`dados_locais/chroma`)
- Busca semântica com indicação de arquivo e página/aba/linhas
- Histórico de conversas salvo automaticamente no SQLite (`dados_locais/historico.sqlite3`)
- Consultas MySQL pré-definidas e somente SELECT: visão geral, receita mensal, pedidos por status
- Exportação do histórico em JSON e resultado SQL em CSV

## Instalação no Windows / VS Code

1. Crie um ambiente virtual na pasta do projeto (opcional, recomendado):

   ```powershell
   c:\python313\python.exe -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e preencha com **uma nova chave** Groq e com as credenciais do MySQL. **Nunca compartilhe `.env`.**
4. Se necessário, crie usuário MySQL de leitura por meio do arquivo `criar_usuario_mysql.sql`.
5. Verifique que o banco indicado por `MYSQL_DATABASE` realmente existe e que `pedidos` contém `criado_em` (DATE/DATETIME), `status` e `valor_total` (NUMERIC).
6. Execute:

   ```powershell
   python -m streamlit run app.py
   ```

7. Acesse `http://localhost:8501`.

## Teste de uso
1. Modo **Documentos (RAG)**: anexe um PDF/TXT/CSV/XLSX e clique **Indexar arquivos**.
2. Pergunte algo relacionado ao conteúdo. Veja os trechos em **Trechos encontrados na base RAG**.
3. Reinicie o Streamlit: os trechos continuam no ChromaDB e as conversas no SQLite.
4. Modo **MySQL Loja Tech**: escolha ano, status e relatório; clique **Consultar banco**; depois pergunte sobre o resultado.
5. Modo **Ambos**: combine um contexto documental com o último relatório SQL.

## Segurança e limitações
- Não conectamos a IA diretamente à execução de comandos SQL: ela recebe o **resultado** de SELECTs previamente definidos.
- Crie o usuário `lojatech_leitura` com privilégio SELECT apenas na tabela necessária.
- `SET SESSION TRANSACTION READ ONLY` é defesa complementar; o privilégio SELECT é a proteção principal.
- O app foi desenhado para uso **local e didático**, não para implantação pública sem autenticação e isolamento por usuário.
- As bases vetoriais e conversas são compartilhadas por usuários que tenham acesso à mesma instância do app. Não armazene informações confidenciais sem controles adicionais.
- PDF escaneado sem camada de texto exige OCR; esta versão não executa OCR.
- A busca semântica não garante respostas corretas; confirme os dados citados.
- Planilhas são indexadas para busca textual, **não** para cálculos completos. Para totais use consultas SQL ou rotinas Pandas.
- O primeiro carregamento de embeddings pode baixar o modelo pela internet.
- A indexação limita-se a 2.000 trechos, e arquivos enormes podem consumir muita memória.
- O arquivo SQL usa `lojatech1` como padrão. Ajuste caso seu banco se chame `lojatech`.
