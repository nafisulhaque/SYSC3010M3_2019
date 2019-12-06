# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time



textport = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = ('localhost', port)
s.bind(server_address)

while True:

    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)

    buf, address = s.recvfrom(port)
    if not len(buf):
        break
    print("\n")
    print(type(buf))        #checking the type of the buf
    print(list(buf))        #checking the list value of the buf to use later
    print("\n")
    
    command = int(buf.decode("utf-8"));

    #now we are going to check if the wanted numbers which are sent from the app meets the command numbers
    if(list(buf)[0] >= 49 & list(buf)[0] <= 54):

 
        
        if(command == 1):      
            lights = True
            print("ok... turning lights on")
            
        elif(command == 2):     
            lights = False
            print("ok... turning lights off")

        elif(command == 3):                        
            print("ok... here is the temperature")
            
        elif(command == 4):                        
            print("ok... here is the humidty")
            
        elif(command == 5):   
            blinds = True
            print("ok... opening blinds")

        elif(command == 6):     
            blinds = False
            print("ok... closing blinds")
            
        else:
            ("Hmm... something seems wrong")
    else:
        print("Opsie.... wrong value/character entered")            
     
    print ("Message Received: %s" %buf)         

s.shutdown(1)
