Integrantes do grupo responsáveis pelo desenvolvimento:

Lucas Iraha Saraiva - lucasiraha@unisantos.br

Lorenzo Galvão Costa - lgcosta@unisantos.br

Pedro Messias Rosa - pedro.messias@unisantos.br

Descrição do Projeto

Este projeto é uma simulação prática de um sistema de gestão hospitalar desenvolvido em Python. A ideia foi aplicar conceitos de Programação Orientada a Objetos (POO) para recriar a jornada completa de um paciente dentro de uma unidade de saúde.

O sistema foi desenhado de forma modular: ele separa a interface com o usuário da lógica "pesada" do código. Na prática, o software permite que um Secretário registre os pacientes e que um Enfermeiro realize a triagem automática, onde sinais vitais são simulados e o nível de urgência é definido.

O grande diferencial do projeto é o algoritmo de Fila Inteligente. Em vez de atender puramente por ordem de chegada, o sistema cruza duas informações cruciais: a gravidade dos sintomas (carregados de um banco de dados externo) e o tempo que a pessoa já está aguardando. Isso garante uma gestão mais justa e eficiente, priorizando quem realmente precisa, o que demonstra a aplicação prática de estruturas de dados e lógica de priorização em um cenário realista.

Informações de configurações e como executar o software:

Para rodar o software corretamente, você precisa garantir que o ambiente Python e a estrutura de arquivos estejam configurados da seguinte maneira:

Pré-requisitos Ter o Python 3.x instalado no seu computador. Não há necessidade de instalar bibliotecas externas (o projeto usa apenas bibliotecas padrão como abc, enum, datetime, random, csv e os).

Estrutura de Arquivos Você deve colocar os seguintes três arquivos na mesma pasta: main.py: O arquivo principal que contém o menu e inicia o programa. sistema_hospitalar.py: O módulo que contém as classes e a lógica do sistema. sintomas.csv: Um arquivo de banco de dados necessário para o funcionamento da triagem. Nota: O código tenta carregar este arquivo e avisa se ele não for encontrado. Como este arquivo não foi fornecido no seu upload, você deve criá-lo.

Criando o arquivo sintomas.csv (Necessário) Crie um arquivo de texto, nomeie-o como sintomas.csv e cole o seguinte conteúdo dentro dele (baseado na estrutura que o código sistema_hospitalar.py espera ): Snippet de código sintoma,urgencia,descricao Dor no peito,CRITICO,Dor intensa no centro do peito irradiando para o braço Falta de ar,ALTO,Dificuldade respiratória severa Febre alta,MEDIO,Temperatura corporal acima de 39 graus Dor de cabeca,BAIXO,Cefaleia leve a moderada Corte profundo,ALTO,Ferimento com sangramento ativo Gripe,BAIXO,Sintomas virais comuns e coriza Parada cardiaca,CRITICO,Ausência de batimentos cardíacos Fratura exposta,ALTO,Osso visível através da pele

Como Executar Abra o seu terminal (CMD, PowerShell ou Terminal do VS Code), navegue até a pasta onde os arquivos estão salvos e execute o seguinte comando:

Bash python main.py O sistema abrirá o menu interativo onde você poderá navegar digitando as opções numéricas (1 a 5). O que esperar ao executar: O sistema carregará os sintomas do CSV. Você poderá registrar um paciente (Opção 1), onde o sistema pedirá Nome, CPF, Idade, Sexo e o Sintoma (que pode ser escolhido da lista carregada).
