# Bibliotecas:
from machine import Pin 	# IOs
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
usuarios = { 111111111: "Angelo", 1587063440:"Daniel", 992307218261: "Danilo"} # Dicionarios para os usuarios
gavetas = { "Angelo" : 1, "Daniel": 2, "Danilo": 3} # Dicionario para as gavetas
#---------------------------------------------------------------------------------------------

# Mapeamento de Hardware:
Led_on_board = machine.Pin(25, machine.Pin.OUT) # Led ON Board
buzzer = machine.Pin(2, machine.Pin.OUT) # Buzzer
gLed = machine.Pin(0, machine.Pin.OUT) # LED verde
rLed = machine.Pin(1, machine.Pin.OUT) # LED vermelho
solenoide = [ machine.Pin(12, machine.Pin.OUT), machine.Pin(13, machine.Pin.OUT), machine.Pin(14, machine.Pin.OUT)] # Solenoides
reader = MFRC522(spi_id = 0, sck = 6, miso = 4, mosi = 7, cs = 5, rst = 5) # Leitor RFID
rtc = RTC() # rtc
i2c=I2C(0,scl=Pin(9),sda=Pin(8),freq=200000) # Display OLED
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c) # Display OLED
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
        
#---------------------------------------------------------------------------------------------
    
# Configuracoes Iniciais (Setup):    
#timer.init(freq=2.5, mode=machine.Timer.PERIODIC, callback=blink)

print("Configuracoes Termidas")
print("Entrando na Rotina Principal...")
time.sleep_ms(250) # Aguarda 250 ms
#rtc.datetime((2024, 4, 30, 4, 16, 26, 30, 0)) # Configura o horario
gLed.off() # Desliga o LED de sinalizacao verde   
rLed.off() # Desliga o LED de sinalizacao verde   
for i in range(3): # 3 solenoides
    solenoide[i].off() # Desliga os solenoides
oled.fill(0) # Cor de fundo preta
oled.text("Cofre 1.0", 30, 5)
oled.show()
#---------------------------------------------------------------------------------------------

# Rotina Principal (Loop):

while 1:
    oled.fill(0) # Cor de fundo preta
    oled.text("Cofre 1.0", 30, 5)
    oled.show()
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
                oled.text("Bem vindo,", 0, 18)
                oled.text(usuario, 0, 30)
                Campainha(200, 3)
                oled.text("Abrindo " + str(gaveta) + "...", 0, 45)
                oled.show()
                print(log)
                print("Usario Identificado: " + usuario) # Informa o usuario
                print("Abrindo gaveta " + str(gaveta) + "...") # Informa a gaveta correspondente
                solenoide[gaveta-1].on() # Liga o solenoide
                gLed.on() # Liga o LED de sinalizacao verde
                for i in range(4):
                    oled.fill(0) # Cor de fundo preta
                    print(4-i)
                    oled.text("Bem vindo,", 0, 18)
                    oled.text(usuario, 0, 30)
                    oled.text("Abrindo " + str(gaveta) + "...", 0, 45)
                    oled.text("Tempo: " + str(4-i), 30, 55)
                    oled.show()
                    time.sleep(1)
                oled.fill(0) # Cor de fundo preta
                print(0)
                oled.text("Bem vindo,", 0, 18)
                oled.text(usuario, 0, 30)
                oled.text("Abrindo " + str(gaveta) + "...", 0, 45)
                oled.text("Tempo: 0", 30, 55)
                oled.show()
                #Campainha(400, 10)
                #time.sleep(4) # Solenoide ligado por 4s
                solenoide[gaveta-1].off() # Desliga o solenoide
                gLed.off() # Desliga o LED de sinalizacao verde                
                print("Gaveta " + str(gaveta) + " aberta")
                time.sleep(1) # Aguarda 1s
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
    #Led_on_board.on() # Liga o LED
    #time.sleep_ms(ST) # Aguarda 100 ms
    #Led_on_board.off() # Desliga o LED
    time.sleep_ms(ST) # Aguarda 
