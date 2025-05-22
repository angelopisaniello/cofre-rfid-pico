# Sistema de Gavetas Inteligentes com Abertura por RFID

> Satatus: Developing ⚠️

## Descrição Geral
Este projeto foi desenvolvido como parte da disciplina **EEN251 - Microcontroladores e Sistemas Embarcados** do Instituto Mauá de Tecnologia.

## 👨‍💻 Integrantes da Equipe

| Nome                     | RA           |
|--------------------------|--------------|
| Angelo Pisaniello Junior | 12.95003-3   |
| Danilo Di Fábio Bueno    | 22.00028-3   |
| Daniel F. Soares         | 22.01298-2   |


## Descrição do Projeto

O projeto consiste em um sistema embarcado para controle de três gavetas inteligentes com abertura por **RFID**, desenvolvido com o microcontrolador **Raspberry Pi Pico**. As gavetas possuem **solenóides** para travamento/abertura, e o sistema inclui ainda:

- **Teclado matricial** para comandos locais;
- **Display OLED** para exibição de mensagens;
- **LEDs e buzzer** para sinalização visual e sonora;
- **Sensores ópticos** para detecção de estado (aberta/fechada) das gavetas.

Este projeto tem aplicação potencial em **cofres de hotel**, **estações públicas de recarga de celular** ou **armários inteligentes**.

---

## 📋 Requisitos do Sistema

| ID     | Requisito                                                                                         | Tipo         |
|--------|---------------------------------------------------------------------------------------------------|--------------|
| SR-01  | Ser composto por módulos prontos e de fácil acesso                                                | Obrigatório  |
| SR-02  | Controlar a abertura de 3 gavetas de forma independente por meio de autenticação RFID             | Obrigatório  |
| SR-03  | Travar e destravar as gavetas utilizando solenoides de 12V                                        | Obrigatório  |
| SR-04  | Detectar o estado (aberta/fechada) de cada gaveta utilizando sensores ópticos                     | Obrigatório  |
| SR-05  | Fornecer feedback visual através de LEDs indicadores                                              | Obrigatório  |
| SR-06  | Fornecer feedback sonoro através de buzzer                                                        | Obrigatório  |
| SR-07  | Permitir comandos e interação local por meio de teclado matricial                                 | Obrigatório  |
| SR-08  | Exibir informações no display OLED (status, mensagens de operação)                                | Obrigatório  |
| SR-09  | Possuir sistema de proteção elétrica adequado (diodos flyback, MOSFETs para acionamento)          | Obrigatório  |
| SR-10  | Ser alimentado por fonte de 12V com corrente suficiente para acionar os 3 solenoides              | Obrigatório  |
| SR-11  | Ser montado em uma estrutura mecânica adequada (gaveteiro e caixa segura para o mecanismo)        | Obrigatório  |
| SR-12  | Garantir a segurança contra sobreaquecimento dos solenoides com controle de tempo de acionamento  | Obrigatório  |
| SR-13  | Permitir futuras expansões, como comunicação com sistema externo (Wi-Fi, Bluetooth)               | Desejável    |
| SR-14  | Implementar modo de bloqueio total, caso tentativas de abertura não autorizadas sejam detectadas  | Desejável    |


## 📝 Lista de Componentes

> Satatus: Developing ⚠️
>
| Descrição do Produto                    | Quantidade | Valor Total |
|-----------------------------------------|------------|-------------|
| Raspberry Pi Picpo (Zero)               |     01     | R$ 159,90   |
| Mini Solenoide 12 (V)                   |     03     | R$ 129,28   |
| Kit RFID Mfrc522 - 13,56 (MHz)          |     01     | R$ 12,82    |
| Tag RFID - Chaveiro (13,56Mhz)          |     02     | R$ 3,60     |
| Teclado Matricial de Membrana 16 Teclas |     01     | R$ 6,17     |
| Display oLED 0.96 I2C Branco            |     01     | R$ 21,75    |
| Buzzer Passivo 5V                       |     01     | R$ 1,69     |
| Kit Receptor e Emissor IR 5mm           |     03     | R$ 8,55     |
| LED 5mm Verde                           |     01     | R$ 0,24     |
| Transistor   ?????                      |     01     | R$          |
| Resistor     ?????                      |     01     | R$          |
| Placa padrão ?????                      |     01     | R$          |
|                                         |      Total | R$ 344,00   |


## Diagrama de Blocos
![image alt](https://github.com/angelopisaniello/cofre-rfid-pico/blob/c4062b0324a2e89cb6f8d55536021832ba76cf56/PROJETO_V5.png)

## Esquema Elétrico

> Satatus: Developing ⚠️

## 🛠️ Projeto Mecânico das Gavetas

O projeto das peças mecânicas foi desenvolvido utilizando o software **Autodesk Fusion 360**, versão **2601.1.37 x86_64**, com plano **Estudante**. O ambiente de modelagem foi realizado no **Windows 11 Pro 24H2**.

As peças foram concebidas visando **facilidade de fabricação e montagem**, sendo idealizadas para **impressão 3D** utilizando o material **PLA (Ácido Polilático)**.

### 🎯 Motivos para a escolha do PLA:
- Excelente **custo-benefício**.
- **Facilidade de impressão**, mesmo em impressoras 3D domésticas.
- **Boa resistência mecânica** e **rigidez**, adequada para a estrutura das gavetas.
- Material **biodegradável** e com baixo impacto ambiental.
- **Acabamento estético** superior, com superfície lisa e sem necessidade de pós-processamento complexo.

### 🖥️ Por que o Autodesk Fusion 360?
- Ferramenta **profissional e amplamente utilizada** na indústria.
- Permite integração completa entre **modelagem 3D**, **simulações** e **geração de arquivos para impressão (STL)**.
- Licença gratuita para **uso educacional**, ideal para o desenvolvimento acadêmico.
- Ambiente intuitivo, com recursos de **parametrização** e **colaboração em nuvem**.

![image alt](https://github.com/angelopisaniello/cofre-rfid-pico/blob/main/Folha_de_desenho_v2.png)

> Satatus: Developing ⚠️

## Vídeo Explicativo

> Satatus: Developing ⚠️

## Conclusão

> Satatus: Developing ⚠️
