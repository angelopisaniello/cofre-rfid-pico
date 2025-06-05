# Bibliotecas:
from machine import ADC, Pin 	# ADC =, IOs
import time 	# Temporizacao
import utime 	# Temporizacao
from machine import RTC # Real Time Clock
from machine import I2C 	# I2C
from mfrc522 import MFRC522 # RFID
from ssd1306 import SSD1306_I2C # Display OLED
#---------------------------------------------------------------------------------------------

# Variaveis globais:
WIDTH =128 
HEIGHT= 64
ST = 250 # Tempo de atualizacao em ms
usuarios = { 111111111: "Angelo", 1587063440:"Daniel", 2307218261: "Danilo"} # Dicionarios para os usuarios
gavetas = { "Angelo" : 1, "Daniel": 2, "Danilo": 3} # Dicionario para as gavetas
teclas = [
    ['1', '3', 'A', '2'],
    ['4', '6', 'B', '5'],
    ['7', '9', 'C', '8'],
    ['*', '#', 'D', '0']
] # Teclas
SENHA = "123456" # Senha mestre do cofre
#---------------------------------------------------------------------------------------------

# Mapeamento de Hardware:
#Entradas:
fototransistores = [ ADC(Pin(26)), ADC(Pin(27)), ADC(Pin(28))] # Fototransistores
reader = MFRC522(spi_id = 0, sck = 6, miso = 4, mosi = 7, cs = 5, rst = 3) # Leitor RFID
linhas = [Pin(i, Pin.OUT) for i in (15, 16, 17, 18)]# Linhas do teclado
colunas = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in (19, 20, 21, 22)] # Colunas do teclado
#Saidas:
decoder = [machine.Pin(10, machine.Pin.OUT), machine.Pin(11, machine.Pin.OUT)] # Decoder
solenoide = [ machine.Pin(14, machine.Pin.OUT), machine.Pin(13, machine.Pin.OUT), machine.Pin(12, machine.Pin.OUT)] # Solenoides
buzzer = machine.Pin(2, machine.Pin.OUT) # Buzzer
i2c=I2C(0,scl=Pin(9),sda=Pin(8),freq=200000) # Display OLED
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c) # Display OLED
#Led_on_board = machine.Pin(25, machine.Pin.OUT) # Led ON Board
gLed = machine.Pin(0, machine.Pin.OUT) # LED verde
rLed = machine.Pin(1, machine.Pin.OUT) # LED vermelho
rtc = RTC() # rtc
#---------------------------------------------------------------------------------------------

# Funcoes:
#def blink(timer): # Alterar estado do LED
 #   led.toggle()
# Funcao para retornar o TimeStamp formatado:
def TimeStamp_to_str( ref ): 
    aux = str(ref[0]) + "-" # AAAA-
    for i in range(1, 6):
        if  ref[i] < 10 : # Menos de dois digitos
            aux += '0'
        aux += str(ref[i]) + "-"*(i<2) + " "*(i==2) + ":"*(i>2 and i < 5) # XX
    return aux ## AAAA-MM-DD HH:MM:SS

#Funcao para retornar o LOG formatado
def LOG_to_str( ts, us, gv): 
    lg = '\n' + TimeStamp_to_str(ts) + ";" + str(us) + ";" + str(gv)
    return lg

#Funcao auxiliar para testar os solenoides
def Testa_solenoides():
    while(1):
        for i in range(3):
            solenoide[i].on()
        time.sleep(4)
        for i in range(3):
            solenoide[i].off()
        time.sleep(4)

# Funcao para tocar a buzzer por um numero de repeticoes
def Campainha( T, n):
    for i in range(n):
        buzzer.on() # Aciona
        time.sleep_ms(int(T/2))
        buzzer.off() # Desliga
        time.sleep_ms( int(T/2))
        
#Funcao para controlar os leds ligados no decoder:
def Decodifica( l ):
    decoder[0].value( l &  1)
    decoder[1].value( l >> 1)

#Funcao para retornar a tecla pressionada (ou se nenhuma foi pressionada
def Tecla():
    for i, linha in enumerate(linhas):
        linha.high()  # Ativa linha atual
        for j, coluna in enumerate(colunas):
            if coluna.value() == 1:
                linha.low()
                return teclas[i][j]
        linha.low()
    return -1

#Funcao para cronometar abertura da gaveta
def Cronometrar_abertura(gav, us ):
    for i in range(4):
        oled.fill(0) # Cor de fundo preta
        print(4-i)
        oled.text("Bem vindo,", 0, 18)
        oled.text(us, 0, 30)
        oled.text("Abrindo " + str(gav) + "...", 0, 45)
        oled.text("Tempo: " + str(4-i), 30, 55)
        oled.show()
        Campainha(100, 1)
        time.sleep(0.9)
        oled.fill(0) # Cor de fundo preta
    print(0)
    oled.text("Bem vindo,", 0, 18)
    oled.text(us, 0, 30)
    oled.text("Abrindo " + str(gav) + "...", 0, 45)
    oled.text("Tempo: 0", 30, 55)
    oled.show()
    
#Funcao para abrir uma gaveta
def Abrir_gaveta( gav, us):
    oled.fill(0) # Cor de fundo preta
    oled.text("Bem vindo,", 0, 18)
    oled.text(us, 0, 30)
    Campainha(200, 3)
    oled.text("Abrindo " + str(gav) + "...", 0, 45)
    oled.show()
    solenoide[gav - 1].on() # Retrai o solenoide
    gLed.on() # Liga o LED de sinalizacao verde
    Cronometrar_abertura( gav, us ) # Mostra o cronometro
    solenoide[gav-1].off() # Desliga o solenoide
    print("Gaveta " + str(gav) + " aberta")
    time.sleep(0.5) # Aguarda 0.5s
    ocr = 0 # Numero de ocorrencias
    buz = 0 # Auxiliar para buzzer
    flag = time.ticks_ms() # Reseta a flag (cronometro)
    oled.fill(0) # Cor de fundo preta
    oled.text("Feche a gaveta", 0, 20)
    oled.show()
    Acende_gaveta( gav ) #
    time.sleep(5)
    while ocr < 3:
        valor = fototransistores[gav-1].read_u16() # Conversao AD
        print("adc = " + str(valor)) # Apenas depuracao
        if (valor< 60000 and gav == 3) or (valor < 62000 and gav == 2) or (valor < 63000 and gav == 1) or Tecla() == '*': # Gaveta esta fechada
            ocr = ocr + 1 # Incrementa o numero de ocorrencias
        else:
            ocr = 0 # Zera o numero de ocorrencias
        if time.ticks_diff(time.ticks_ms(), flag) > 60000: # Gaveta a mais de 60 segundos aberta
            buzzer.value( buz < 3)
            buz = (buz + 1) % 6
        time.sleep_ms(20) # Aguarda 20 ms
    gLed.off() # Desliga o LED de sinalizacao verde                
    Acende_gaveta( -1 ) # Apaga os LEDs            
    
def Menu_principal():
    oled.fill(0) # Cor de fundo preta
    oled.text("Cofre 1.0", 30, 5)
    oled.text("Aproxime a TAG", 8, 20)
    oled.show()
    
def Menu_mestre(): # Menu de gerenciamente
    oled.fill(0) # Cor de fundo preta
    oled.text("Gerenciamento", 25, 5)
    oled.text("1 - Abrir gaveta 1", 0, 15)
    oled.text("2 - Abrir gaveta 2", 0, 25)
    oled.text("3 - Abrir gaveta 3", 0, 35)
    oled.text("4 - Retroceder", 0, 45)
    oled.show()
    
def Acende_gaveta( gav ):
    if( gav == 3):
        Decodifica(1)
    elif gav == 2:
         Decodifica(2)           
    elif gav == 1:
        Decodifica(0)
    else:
        Decodifica(3)
#---------------------------------------------------------------------------------------------
    
# Configuracoes Iniciais (Setup):    
#timer.init(freq=2.5, mode=machine.Timer.PERIODIC, callback=blink)

print("Configuracoes Termidas")
print("Entrando na Rotina Principal...")
time.sleep_ms(250) # Aguarda 250 ms
#rtc.datetime((2024, 4, 30, 4, 16, 26, 30, 0)) # Configura o horario
gLed.off() # Desliga o LED de sinalizacao verde   
rLed.off() # Desliga o LED de sinalizacao verde
buzzer.off() # Desliga o buzzer
Decodifica(3) # Leds desligados
for i in range(3): # 3 solenoides
    solenoide[i].off() # Desliga os solenoides
oled.fill(0) # Cor de fundo preta
oled.text("Cofre 1.0", 30, 5)
oled.show()
#---------------------------------------------------------------------------------------------
while 1:
    solenoide[3 - 1].on()
    time.sleep(4)
    solenoide[3 - 1].off()
    time.sleep(4)
# Rotina Principal (Loop):
# teste = 0
# while 1:
#     print(Tecla())
#     time.sleep_ms(100) # Aguarda

# while 1:
#     solenoide[0].on()
#     Decodifica(1)
#     time.sleep_ms(3500) # Aguarda
#     Decodifica(0)
#     solenoide[0].off();
#     time.sleep_ms(5000) # Aguarda
teste = 0
Acende_gaveta( -1 )
# # while True:
# #     # Testa leitura dos ADCs
# #     for i in range(3):
# #         print(f"ADC {i}: {fototransistores[i].read_u16()}")
# #     time.sleep(0.5)
# while 1:
#     #Decodifica(0/)
#     fototransistores[0] = ADC(Pin(28))
#     print( fototransistores[0].read_u16())
#     time.sleep(0.2)
# 
# while 1:
#     Decodifica(teste)
#     teste = (teste + 1) % 4
#     print(teste)
#     print( fototransistores[teste-1].read_u16())
#     time.sleep_ms(3000) # Aguarda
flag = time.ticks_ms() # Seta a flag (cronometro)
while 1:
    Menu_principal()
    if ( Tecla() != '*'): # * nao pressionado
        flag = time.ticks_ms() # Reseta a flag (cronometro)
    print(time.ticks_diff(time.ticks_ms(), flag))    
    if ( time.ticks_diff(time.ticks_ms(), flag) >= 10000): # Pressionou por mais de 10 segundos:
        Campainha(100, 5)
        print("Aguarde...")
        oled.fill(0) # Cor de fundo preta
        oled.text("Aguarde...", 30, 25)
        time.sleep_ms(500) # Aguarda
        oled.show()
        while (Tecla() == "*"): # Ainda nao soltou o *
            oled.text("Solte o *", 40, 25)
            time.sleep_ms(50) # Aguarda
        flag = time.ticks_ms() # Flag de inicio da subrotina de menu
        tentativa = 1 # Tentativas
        senha = "" # senha digitada
        while time.ticks_diff(time.ticks_ms(), flag) < 10000 and tentativa <= 3  : # Ate 10 segundos de inatividade ou 3 tentativas
            oled.fill(0) # Cor de fundo preta
            oled.text("Digite a senha:", 10, 20)
            oled.text("*" * len(senha), 32, 40)
            oled.show()
            aux = Tecla() # Le o teclado
            if aux != -1: # Pressionou alguma tecla
                Campainha(300, 1) # Soa
                senha = senha + aux # adiciona a tecla pressionada a senha
                while Tecla() == aux: # Enquanto estiver pressionado
                    time.sleep_ms(50) # Aguarda
                flag = time.ticks_ms() # Reseta a flag (cronometro)   
            print(str(time.ticks_diff(time.ticks_ms(), flag)) + "   " + senha)
            if ( len(senha) == 6):
                if ( senha == SENHA): # Senha correta
                    Campainha(200, 2)
                    flag = time.ticks_ms() # Reseta a flag (cronometro)   
                    aux = -1
                    while time.ticks_diff(time.ticks_ms(), flag) < 10000 and aux != '4': # Ate 10 segundos de inatividade ou opcao por voltar
                        Menu_mestre()
                        aux = Tecla()
                        print("aux = " + str(aux))
                        if( aux != -1 and aux != '4'):
                            while Tecla() == aux: # Enquanto estiver pressionado
                                time.sleep_ms(50) # Aguarda
                            Abrir_gaveta( int(aux), "Mestre" )
                            flag = time.ticks_ms() # Reseta a flag (cronometro)
                        tentativa = 4 # Forca a saida
                        time.sleep_ms(50) # Aguarda
                else: # Senha incorreta
                    Campainha(200, 5)
                    tentativa = tentativa + 1 # nova tentativa
                    senha = ""
                flag = time.ticks_ms() # Reseta a flag 
            time.sleep_ms(50) # Aguarda
    reader.init() # Inicia o leitor
    (stat, tag_type) = reader.request(reader.REQIDL) # Leitura
    if stat == reader.OK: # Se a leitura foi bem sucedida
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+ str(card) )
            if card in usuarios: # Cartao valido
                timeStamp = rtc.datetime() # Horario para o LOG
                usuario = usuarios[card] # Usuario atual
                gaveta = gavetas[usuario]
                log = LOG_to_str(timeStamp, usuario, gaveta) # Obtem a string do LOG
                print(log)
                print("Usario Identificado: " + usuario) # Informa o usuario
                print("Abrindo gaveta " + str(gaveta) + "...") # Informa a gaveta correspondente
                Abrir_gaveta( gaveta, usuario)
            else: # TAG nao encontrada
                rLed.on() #Liga o LED de sinalizacao vermelho     
                buzzer.on() # Aciona
                print("TAG nao encontrada")
                oled.text("TAG invalida", 0, 25)
                oled.text("Tente novamente", 0, 50)
                oled.show()
                time.sleep(1) # Aguarda 1s
                buzzer.off()# Desliga
                rLed.off() # Desliga o LED de sinalizacao vermelho
            flag = time.ticks_ms() # Flag de inicio da subrotina de menu
    time.sleep_ms(100) # Aguarda 

