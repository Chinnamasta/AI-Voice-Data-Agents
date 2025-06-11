# AI-Voice-Data-Agents

**Projetos de Agentes e LLM Interativo**
Este repositório contém dois projetos Python distintos, mas complementares, que exploram as capacidades de Grandes Modelos de Linguagem (LLMs) para interações de voz e análise de dados.

Estrutura do Repositório
/seu_repositorio
├── .env.example
├── df_agent.py
├── talking_llm.py
└── README.md

**TalkingLLM: Seu Assistente de Voz Interativo**
Este projeto implementa um assistente de voz que utiliza modelos de linguagem para transcrever áudio, processar a entrada e gerar respostas faladas. É ideal para criar interfaces de conversação ativadas por voz.

1) Funcionalidades
  - Ativação por Hotkey: Inicia/para a gravação de áudio com uma combinação de teclas (Ctrl+Alt+H).
  - Gravação de Áudio: Captura sua voz através do microfone.
  - Transcrições Poderosas: Utiliza o modelo Whisper (OpenAI) para converter áudio em texto.
  - Geração de Respostas Inteligentes: Envia o texto transcrito para um Large Language Model (LLM) via LangChain/OpenAI para gerar respostas contextuais.
  - Conversão de Texto em Voz (TTS): Transforma a resposta do LLM em áudio usando a API OpenAI TTS, reproduzindo-a para o usuário.

2) Como Rodar
  - Configuração do Ambiente:
      Certifique-se de ter Python 3.8+ instalado.
  - Crie um ambiente virtual (altamente recomendado):
      Bash
      python -m venv .venv
      .\.venv\Scripts\activate
      source ./.venv/bin/activate
  - Instalação das Dependências:
      Bash
      pip install -r requirements.txt
  - Configuração da Chave da API OpenAI:
      Crie um arquivo chamado .env na raiz do seu projeto (onde talking_llm.py está).
      Adicione sua chave da API da OpenAI a este arquivo:
      OPENAI_API_KEY="sua_chave_api_da_openai_aqui"
  - Executar o Aplicativo:
      Bash
      python talking_llm.py
  - Interação:
      Pressione Ctrl+Alt+H para começar a gravar.
      Fale sua pergunta ou comando.
      Pressione Ctrl+Alt+H novamente para parar a gravação. O sistema transcreverá, processará e responderá.
      Pressione Ctrl+C no terminal para sair do programa.

**Agente Pandas DataFrame: Análise de Dados com LLM**
Este projeto demonstra como usar um LLM (via LangChain) para interagir e analisar dados contidos em um Pandas DataFrame usando linguagem natural. Ele é perfeito para explorar e obter insights de conjuntos de dados sem a necessidade de escrever código Python complexo diretamente.

1) Funcionalidades
  - Interpretação de Linguagem Natural: Transforma perguntas em português sobre seu DataFrame em operações de análise de dados.
  - Integração com Pandas: Utiliza o poder do Pandas para manipulação e análise de dados.
  - Agente Inteligente: O agente é capaz de inferir quais operações do Pandas são necessárias para responder à sua pergunta.
  - Saída Verbosa: Mostra os passos que o agente está tomando para chegar à resposta, incluindo o código Python gerado e executado.

2) Como Rodar
  - Configuração do Ambiente:
      Certifique-se de ter Python 3.8+ instalado.
      Use o mesmo ambiente virtual do projeto anterior, se desejar, ou crie um novo.
      Bash
      python -m venv .venv
      .\.venv\Scripts\activate   # No Windows
      source ./.venv/bin/activate # No macOS/Linux
  - Instalação das Dependências:
      Bash
      pip install -r requirements.txt
  - Configuração da Chave da API OpenAI:
      Certifique-se de que o arquivo .env com OPENAI_API_KEY esteja configurado conforme descrito na seção do TalkingLLM.
  - Preparação do Conjunto de Dados:
      Certifique-se de que o arquivo csv esteja na mesma pasta que df_agent.py. Este é o DataFrame que o agente irá analisar.
  - Executar o Aplicativo:
      Bash
      python df_agent.py

3) Interação:
    O script executará a pergunta definida no código (agent.invoke("Quantas linhas há no conjunto de dados?")) e mostrará a     resposta gerada pelo LLM, juntamente com os passos internos do agente.
  Você pode modificar a string dentro de agent.invoke() para fazer outras perguntas ao seu DataFrame.
