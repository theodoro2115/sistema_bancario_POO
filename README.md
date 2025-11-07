# Sistema Bancário Orientado a Objetos (POO)

Este projeto é uma refatoração de um sistema bancário simples, implementado em Python, com o objetivo de aplicar os conceitos de **Programação Orientada a Objetos (POO)**. A versão anterior utilizava dicionários para armazenar clientes e contas, e esta nova versão adota classes e objetos, seguindo um modelo de classes UML.

## 🚀 Funcionalidades

O sistema simula as operações básicas de um banco:

*   **Novo Usuário (`nu`)**: Cria um novo cliente (Pessoa Física) com CPF único.
*   **Nova Conta (`nc`)**: Cria uma nova conta corrente e a associa a um cliente existente.
*   **Depósito (`d`)**: Realiza um depósito na conta, aceitando apenas valores positivos.
*   **Saque (`s`)**: Realiza um saque, respeitando o limite de valor por saque (R$ 500,00) e o limite diário de 3 saques.
*   **Extrato (`e`)**: Exibe o histórico de transações e o saldo atual da conta.
*   **Listar Contas (`lc`)**: Lista todas as contas criadas no sistema.

## 📐 Modelo de Classes (UML)

O projeto é estruturado em classes que representam as entidades do sistema bancário:

| Classe | Descrição | Herança |
| :--- | :--- | :--- |
| **`Cliente`** | Classe base para clientes. Gerencia a lista de contas e a realização de transações. | - |
| **`PessoaFisica`** | Representa um cliente pessoa física. Armazena CPF, nome e data de nascimento. | `Cliente` |
| **`Conta`** | Classe base para contas bancárias. Gerencia saldo, número, agência e histórico. | - |
| **`ContaCorrente`** | Representa uma conta corrente. Implementa limite de cheque especial e limite de saques diários. | `Conta` |
| **`Historico`** | Registra todas as transações realizadas na conta. | - |
| **`Transacao`** | Classe base para transações. Garante que o valor seja acessível via `@property`. | - |
| **`Deposito`** | Transação de depósito. | `Transacao` |
| **`Saque`** | Transação de saque. Implementa a lógica de registro na conta. | `Transacao` |

## 🛠️ Como Executar

O projeto é um script Python simples e não requer a instalação de bibliotecas externas além das nativas.

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd sistema-bancario-poo
    ```

2.  **Execute o script principal:**
    ```bash
    python3 main.py
    ```

3.  **Utilize o menu interativo** para realizar as operações.

## 📝 Exemplo de Uso

Ao executar o script, o menu será exibido:

```
================ MENU ================
[d]	Depositar
[s]	Sacar
[e]	Extrato
[nc]	Nova conta
[lc]	Listar contas
[nu]	Novo usuário
[q]	Sair
=> 
```

Para testar o sistema, siga os passos:

1.  **Criar Novo Usuário** (`nu`)
2.  **Criar Nova Conta** (`nc`)
3.  **Depositar** (`d`)
4.  **Sacar** (`s`)
5.  **Extrato** (`e`)


