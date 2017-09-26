## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin User Import -----------------------------------------------------------
import extr_matrix_XTPIICrossPointSeries_v1_1_1_1 as DeviceA
Matrix = DeviceA.EthernetClass('192.168.0.10', 23, Model='XTP II CrossPoint 3200')

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPCP550')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
# TouchPanel A -----------------------------------------------------------------
## Index
ABtnIndex = Button(TLP1, 1)
## Full Main - Lateral Bar
ABtnRoom    = Button(TLP1, 10)
ABtnSwitch  = Button(TLP1, 11)
ABtnDisplay = Button(TLP1, 12)
ABtnVC      = Button(TLP1, 13)
ABtnAudio   = Button(TLP1, 14)
ABtnREC     = Button(TLP1, 15)
ABtnVoIP    = Button(TLP1, 16)
ABtnInfo    = Button(TLP1, 17)
ABtnPower   = Button(TLP1, 18)
## Full Main - Up Bar
ALblMain    = Label(TLP1, 20)
ABtnRoom1   = Button(TLP1, 21)
ABtnRoom2   = Button(TLP1, 22)
## Full Switching---------------------------------------------
## Outputs
## XTP Out Slot 1
AOut1  = Button(TLP1, 101) ##Room1 Projector
AOut2  = Button(TLP1, 102) ##Room1 LCD Confidence
AOut3  = Button(TLP1, 103) ##Room1 LCD Podium
## XTP Out Slot 2
AOut5  = Button(TLP1, 105) ##Room2 Projector
AOut6  = Button(TLP1, 106) ##Room2 LCD Confidence
AOut7  = Button(TLP1, 107) ##Room2 LCD Podium
## XTP Out Slot 3
AOut9  = Button(TLP1, 109) ##Core Tricaster 1 - Input 1
AOut10 = Button(TLP1, 110) ##Core Tricaster 1 - Input 2
AOut11 = Button(TLP1, 111) ##Core Tricaster 1 - Input 3
AOut12 = Button(TLP1, 112) ##Core Tricaster 1 - Input 4
## XTP Out Slot 4
AOut13 = Button(TLP1, 113) ##Core Tricaster 2 - Input 1
AOut14 = Button(TLP1, 114) ##Core Tricaster 2 - Input 2
AOut15 = Button(TLP1, 115) ##Core Tricaster 2 - Input 3
AOut16 = Button(TLP1, 116) ##Core Tricaster 2 - Input 4
## XTP Out Slot 5
AOut17 = Button(TLP1, 117) ##Core Cisco 1 - Input Camera
AOut18 = Button(TLP1, 118) ##Core Cisco 1 - Input Graphics
AOut19 = Button(TLP1, 119) ##Core Cisco 2 - Input Camera
AOut20 = Button(TLP1, 120) ##Core Cisco 2 - Input Graphics
## XTP Out Slot 6
AOut21 = Button(TLP1, 121) ##Core Recorder 1
AOut22 = Button(TLP1, 122) ##Core Recorder 2
## Inputs
## XTP Slot 1
AInput1    = Button(TLP1, 201) ##Room1 PC Left
AInput2    = Button(TLP1, 202) ##Room1 PC Right
AInput3    = Button(TLP1, 203) ##Room1 PC Stage
AInput4    = Button(TLP1, 204) ##Room1 PC Right
## XTP Slot 2
AInput5    = Button(TLP1, 205) ##Room2 PC Left
AInput6    = Button(TLP1, 206) ##Room2 PC Right
AInput7    = Button(TLP1, 207) ##Room2 PC Stage
AInput8    = Button(TLP1, 208) ##Room2 PC Back
## XTP Slot 3
AInput9    = Button(TLP1, 209) ##Room1 PTZ1
AInput10   = Button(TLP1, 210) ##Room1 PTZ2
AInput11   = Button(TLP1, 211) ##Room2 PTZ1
AInput12   = Button(TLP1, 212) ##Room2 PTZ2
## XTP Slot 4
AInput13   = Button(TLP1, 213) ##Room1 PC Cabin
AInput14   = Button(TLP1, 214) ##Room2 PC Cabin
##...
##...
## XTP Slot 5
AInput17   = Button(TLP1, 215) ##Core Cisco 1 Out
AInput18   = Button(TLP1, 216) ##Core Cisco 2 Out
AInput19   = Button(TLP1, 217) ##Core ShareLink 1
AInput20   = Button(TLP1, 218) ##Core ShareLink 2
## XTP Slot 6
AInput21   = Button(TLP1, 219) ##Core Tricaster 1 - Out 1
AInput22   = Button(TLP1, 220) ##Core Tricaster 2 - Out 1

## Input Signal Status
## XTP Slot 1
ASignal1    = Button(TLP1, 130) ##Room1 PC Left
ASignal2    = Button(TLP1, 131) ##Room1 PC Right
ASignal3    = Button(TLP1, 132) ##Room1 PC Stage
ASignal4    = Button(TLP1, 133) ##Room1 PC Right
## XTP Slot 2
ASignal5    = Button(TLP1, 134) ##Room2 PC Left
ASignal6    = Button(TLP1, 135) ##Room2 PC Right
ASignal7    = Button(TLP1, 136) ##Room2 PC Stage
ASignal8    = Button(TLP1, 137) ##Room2 PC Back
## XTP Slot 3
ASignal9    = Button(TLP1, 138) ##Room1 PTZ1
ASignal10   = Button(TLP1, 139) ##Room1 PTZ2
ASignal11   = Button(TLP1, 140) ##Room2 PTZ1
ASignal12   = Button(TLP1, 141) ##Room2 PTZ2
## XTP Slot 4
ASignal13   = Button(TLP1, 142) ##Room1 PC Cabin
ASignal14   = Button(TLP1, 143) ##Room2 PC Cabin
##...
##...
## XTP Slot 5
ASignal17   = Button(TLP1, 144) ##Core Cisco 1 Out
ASignal18   = Button(TLP1, 145) ##Core Cisco 2 Out
ASignal19   = Button(TLP1, 146) ##Core ShareLink 1
ASignal20   = Button(TLP1, 147) ##Core ShareLink 2
## XTP Slot 6
ASignal21   = Button(TLP1, 148) ##Core Tricaster 1 - Out 1
ASignal22   = Button(TLP1, 149) ##Core Tricaster 2 - Out 1


# TouchPanel B -----------------------------------------------------------------
## Index
BBtnIndex = Button(TLP2, 1)
## Full Main - Lateral Bar
BBtnRoom    = Button(TLP2, 10)
BBtnSwitch  = Button(TLP2, 11)
BBtnDisplay = Button(TLP2, 12)
BBtnVC      = Button(TLP2, 13)
BBtnAudio   = Button(TLP2, 14)
BBtnREC     = Button(TLP2, 15)
BBtnVoIP    = Button(TLP2, 16)
BBtnInfo    = Button(TLP2, 17)
BBtnPower   = Button(TLP2, 18)
## Full Main - Up Bar
BLblMain    = Label(TLP2, 20)
BBtnRoom1   = Button(TLP2, 21)
BBtnRoom2   = Button(TLP2, 22)


Index = [ABtnIndex, BBtnIndex]

Main  = [ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC, ABtnAudio, ABtnREC, ABtnVoIP, ABtnInfo, ABtnPower,
         BBtnRoom, BBtnSwitch, BBtnDisplay, BBtnVC, BBtnAudio, BBtnREC, BBtnVoIP, BBtnInfo, BBtnPower]

Outputs = [AOut1, AOut2, AOut3, AOut5, AOut6, AOut7, AOut9, AOut10, AOut11, AOut12,
           AOut13, AOut14, AOut15, AOut16, AOut17, AOut18, AOut19, AOut20, AOut21, AOut22]      
GroupOutputs = MESet(Outputs)

Inputs = [AInput1, AInput2, AInput3, AInput4, AInput5, AInput6, AInput7, AInput8,
          AInput9, AInput10, AInput11, AInput12, AInput13, AInput14, AInput17,
          AInput18, AInput19, AInput20, AInput21, AInput22]
GroupInputs = MESet(Inputs)
## End Communication Interface Definition --------------------------------------

def Initialize():
    """This is the last function that loads when starting the system """
    ## Open Sockets
    ## IP
    Matrix.Connect()
    
    ## Data Init
    global output
    global input
    output = ''
    input = ''

    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------
def subscribe_matrix():
    """This send Subscribe Commands to Device """
    ## Socket Status
    Matrix.SubscribeStatus('ConnectionStatus', None, matrix_parsing)
    ## Input Signal Status
    Matrix.SubscribeStatus('InputSignal', {'Input':'1'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'2'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'3'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'4'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'5'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'6'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'7'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'8'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'9'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'10'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'11'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'12'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'13'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'14'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'15'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'16'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'17'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'18'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'19'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'20'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'21'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'22'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'23'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'24'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'25'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'26'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'27'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'28'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'29'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'30'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'31'}, matrix_parsing)
    Matrix.SubscribeStatus('InputSignal', {'Input':'32'}, matrix_parsing)
    ## Output Signal Status
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'5', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'6', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'7', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'8', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'9', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'10', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'11', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'12', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'13', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'14', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'15', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'16', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'17', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'18', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'19', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'20', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'21', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'22', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'23', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'24', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'25', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'26', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'27', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'28', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'29', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'30', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'31', 'Tie Type':'Video'}, matrix_parsing)
    Matrix.SubscribeStatus('OutputTieStatus', {'Output':'32', 'Tie Type':'Video'}, matrix_parsing)
    pass

## UPDATE FUNCTIONS ------------------------------------------------------------
def update_matrix():
    """This send Update Commands to Device"""
    Matrix.Update('InputSignal',{'Input':'1'})
    Matrix.Update('InputSignal',{'Input':'2'})
    Matrix.Update('InputSignal',{'Input':'3'})
    Matrix.Update('InputSignal',{'Input':'4'})
    Matrix.Update('InputSignal',{'Input':'5'})
    Matrix.Update('InputSignal',{'Input':'6'})
    Matrix.Update('InputSignal',{'Input':'7'})
    Matrix.Update('InputSignal',{'Input':'8'})
    Matrix.Update('InputSignal',{'Input':'9'})
    Matrix.Update('InputSignal',{'Input':'10'})
    Matrix.Update('InputSignal',{'Input':'11'})
    Matrix.Update('InputSignal',{'Input':'12'})
    Matrix.Update('InputSignal',{'Input':'13'})
    Matrix.Update('InputSignal',{'Input':'14'})
    Matrix.Update('InputSignal',{'Input':'15'})
    Matrix.Update('InputSignal',{'Input':'16'})
    Matrix.Update('InputSignal',{'Input':'17'})
    Matrix.Update('InputSignal',{'Input':'18'})
    Matrix.Update('InputSignal',{'Input':'19'})
    Matrix.Update('InputSignal',{'Input':'20'})
    Matrix.Update('InputSignal',{'Input':'21'})
    Matrix.Update('InputSignal',{'Input':'22'})
    Matrix.Update('InputSignal',{'Input':'23'})
    Matrix.Update('InputSignal',{'Input':'24'})
    Matrix.Update('InputSignal',{'Input':'25'})
    Matrix.Update('InputSignal',{'Input':'27'})
    Matrix.Update('InputSignal',{'Input':'28'})
    Matrix.Update('InputSignal',{'Input':'29'})
    Matrix.Update('InputSignal',{'Input':'30'})
    Matrix.Update('InputSignal',{'Input':'31'})
    Matrix.Update('InputSignal',{'Input':'32'})
    pass

## DATA PARSING FUNCTIONS ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function activate feedback
## Each function works with the subscription methods of the Python modules
def matrix_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device"""
    if command == 'ConnectionStatus':
        print('Matrix Module Conex status: {}'.format(value))
        #
        if value == 'Connected':
            Matrix_Data['ConexModule'] = True
            #BTN['LANMatrix'].SetState(1)
        else:
            Matrix_Data['ConexModule'] = False
            #BTN['LANMatrix'].SetState(0)
            ## Disconnect the IP Socket
            Matrix.Disconnect()
    
    elif command == 'InputSignal':
        if value == 'Active':
            print('Input ' + qualifier['Input'] + ' ...')
        else:
            print('Input ' + qualifier['Input'] + ': Ok')

        # XTP Slot 1-------------------
        if qualifier['Input'] == '1':
            if value == 'Active':
                ASignal1.SetState(1)
            else:
                ASignal1.SetState(0)
        #
        elif qualifier['Input'] == '2':
            if value == 'Active':
                ASignal2.SetState(1)
            else:
                ASignal2.SetState(0)
        #
        if qualifier['Input'] == '3':
            if value == 'Active':
                ASignal3.SetState(1)
            else:
                ASignal3.SetState(0)
        #
        elif qualifier['Input'] == '4':
            if value == 'Active':
                ASignal4.SetState(1)
            else:
                ASignal4.SetState(0)
        
        # XTP Slot 2--------------------
        if qualifier['Input'] == '5':
            if value == 'Active':
                ASignal5.SetState(1)
            else:
                ASignal5.SetState(0)
        #
        elif qualifier['Input'] == '6':
            if value == 'Active':
                ASignal6.SetState(1)
            else:
                ASignal6.SetState(0)
        #
        if qualifier['Input'] == '7':
            if value == 'Active':
                ASignal7.SetState(1)
            else:
                ASignal7.SetState(0)
        #
        elif qualifier['Input'] == '8':
            if value == 'Active':
                ASignal8.SetState(1)
            else:
                ASignal8.SetState(0)
        
        # XTP Slot 3--------------------
        elif qualifier['Input'] == '9':
            if value == 'Active':
                ASignal9.SetState(1)
            else:
                ASignal9.SetState(0)
        #
        elif qualifier['Input'] == '10':
            if value == 'Active':
                ASignal10.SetState(1)
            else:
                ASignal10.SetState(0)
        #
        elif qualifier['Input'] == '11':
            if value == 'Active':
                ASignal11.SetState(1)
            else:
                ASignal11.SetState(0)
        #
        elif qualifier['Input'] == '12':
            if value == 'Active':
                ASignal12.SetState(1)
            else:
                ASignal12.SetState(0)
        
        # XTP Slot 4--------------------
        elif qualifier['Input'] == '13':
            if value == 'Active':
                ASignal13.SetState(1)
            else:
                ASignal13.SetState(0)
        #
        elif qualifier['Input'] == '14':
            if value == 'Active':
                ASignal14.SetState(1)
            else:
                ASignal14.SetState(0)
        
        # XTP Slot 5---------------------
        elif qualifier['Input'] == '17':
            if value == 'Active':
                ASignal17.SetState(1)
            else:
                ASignal17.SetState(0)
        #
        elif qualifier['Input'] == '18':
            if value == 'Active':
                ASignal18.SetState(1)
            else:
                ASignal18.SetState(0)
        #
        elif qualifier['Input'] == '19':
            if value == 'Active':
                ASignal19.SetState(1)
            else:
                ASignal19.SetState(0)
        #       
        elif qualifier['Input'] == '20':
            if value == 'Active':
                ASignal20.SetState(1)
            else:
                ASignal20.SetState(0)

        # XTP Slot 6--------------------
        elif qualifier['Input'] == '21':
            if value == 'Active':
                ASignal21.SetState(1)
            else:
                ASignal21.SetState(0)
        #
        elif qualifier['Input'] == '22':
            if value == 'Active':
                ASignal22.SetState(1)
            else:
                ASignal22.SetState(0)

    elif command == 'OutputTieStatus':
            if value == '1':
                GroupInputs.SetCurrent(AInput1)
            elif value == '2':
                GroupInputs.SetCurrent(AInput2)
            elif value == '3':
                GroupInputs.SetCurrent(AInput3)
            elif value == '4':
                GroupInputs.SetCurrent(AInput4)
            elif value == '5':
                GroupInputs.SetCurrent(AInput5)
            elif value == '6':
                GroupInputs.SetCurrent(AInput6)
            elif value == '7':
                GroupInputs.SetCurrent(AInput7)
            elif value == '8':
                GroupInputs.SetCurrent(AInput8)
            elif value == '9':
                GroupInputs.SetCurrent(AInput9)
            elif value == '10':
                GroupInputs.SetCurrent(AInput10)
            elif value == '11':
                GroupInputs.SetCurrent(AInput11)
            elif value == '12':
                GroupInputs.SetCurrent(AInput12)
            elif value == '13':
                GroupInputs.SetCurrent(AInput13)
            elif value == '14':
                GroupInputs.SetCurrent(AInput14)
            elif value == '17':
                GroupInputs.SetCurrent(AInput17)
            elif value == '18':
                GroupInputs.SetCurrent(AInput18)
            elif value == '19':
                GroupInputs.SetCurrent(AInput19)
            elif value == '20':
                GroupInputs.SetCurrent(AInput20)
            elif value == '21':
                GroupInputs.SetCurrent(AInput21)
            elif value == '22':
                GroupInputs.SetCurrent(AInput22)

            print(qualifier)
            print(value)

    pass

## EVENT FUNCTIONS ----------------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send a Connect()
## CAUTION: If you never make a Connect(), the Module never work with Subscriptions
@event(Matrix, 'Connected')
@event(Matrix, 'Disconnected')
def matrix_conex_event(interface, state):
    """MATRIX CONNECT() STATUS """
    print('Matrix Conex Event: ' + state)
    if state == 'Connected':
        Matrix_Data['ConexEvent'] = True
        ## Send & Query Information
        subscribe_matrix()
        update_matrix()
    elif state == 'Disconnected':
        Matrix_Data['ConexEvent'] = False
        trying_matrix()
    pass

## RECURSIVE FUNCTIONS ------------------------------------------------------------
## Help´s when the device was Off in the first Connect() method when the code starts
def trying_matrix():
    """Try to make a Connect() to device"""
    if Matrix_Data['ConexEvent'] == False:
        print('Tryng to make a Connect() in Matrix')
        Matrix.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_matrix = Wait(5, trying_matrix)

## RECURSIVE LOOP FUNCTIONS -----------------------------------------------------------
## This not affect any device
## This return True / False when no response is received from Module
## If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
## Generate 'Connected' / 'Disconnected'

def update_loop_matrix():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    Update('InputSignal',{'Input':'1'})
    loop_update_Restart()
loop_update_matrix = Wait(12, update_loop_matrix)

## DATA DICTIONARIES -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## IP
Matrix_Data = {
    'ConexModule': None,
    'ConexEvent' : None,
}

## Event Definitions -----------------------------------------------------------
## Index Page
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']


@event(Index, ButtonEventList)
def Index(button, state):
    if state == 'Pressed':
        if button.Host.DeviceAlias == 'TouchPanelA':
            TLP1.ShowPage('Main')
            print("Touch 1: {0}".format("Index"))
        else:
            TLP2.ShowPage('Main')
            print("Touch 2: {0}".format("Index"))
    pass

@event(Main, ButtonEventList)
def FullMain(button, state):
    if state == 'Pressed':
        if button.Host.DeviceAlias == 'TouchPanelA':
            TLP1.HideAllPopups()
            if button is ABtnRoom:
                TLP1.ShowPopup('Room')
                print("Touch 1: {0}".format("Mode Room"))
            #
            elif button is ABtnSwitch:
                TLP1.ShowPopup('Full.Outputs')
                TLP1.ShowPopup('Full.Inputs')
                print("Touch 1: {0}".format("Mode Switching"))
            #
            elif button is ABtnDisplay:
                TLP1.ShowPopup('Full.Displays')
                print("Touch 1: {0}".format("Mode Display"))
            #
            elif button is ABtnVC:
                TLP1.ShowPopup('Full.VC')
                print("Touch 1: {0}".format("Mode VideoConferencia"))
            #
            elif button is ABtnAudio:
                print("Touch 1: {0}".format("Mode Audio"))
            #
            elif button is ABtnREC:
                TLP1.ShowPopup('Full.Rec')
                print("Touch 1: {0}".format("Mode REC"))
            #
            elif button is ABtnVoIP:
                TLP1.ShowPopup('Full.VoIP')
                print("Touch 1: {0}".format("Mode VoIP"))
            #
            elif button is ABtnInfo:
                TLP1.ShowPopup('Full.Info')
                print("Touch 1: {0}".format("Mode Info"))
            #
            elif button is ABtnPower:
                print("Touch 1: {0}".format("Mode PowerAll"))
        elif button.Host.DeviceAlias == 'TouchPanelB':
            TLP2.HideAllPopups()
            if button is BBtnRoom:
                TLP2.ShowPopup('Room')
                print("Touch 2: {0}".format("Mode Room"))
            #
            elif button is BBtnSwitch:
                TLP2.ShowPopup('Full.Outputs')
                print("Touch 2: {0}".format("Mode Switching"))
            #
            elif button is BBtnDisplay:
                TLP2.ShowPopup('Full.Displays')
                print("Touch 2: {0}".format("Mode Display"))
            #
            elif button is BBtnVC:
                TLP2.ShowPopup('Full.VC')
                print("Touch 2: {0}".format("Mode VideoConferencia"))
            #
            elif button is BBtnAudio:
                print("Touch 2: {0}".format("Mode Audio"))
            #
            elif button is BBtnREC:
                TLP2.ShowPopup('Full.Rec')
                print("Touch 2: {0}".format("Mode REC"))
            #
            elif button is BBtnVoIP:
                TLP2.ShowPopup('Full.VoIP')
                print("Touch 2: {0}".format("Mode VoIP"))
            #
            elif button is BBtnInfo:
                TLP2.ShowPopup('Full.Info')
                print("Touch 2: {0}".format("Mode Info"))
            #
            elif button is BBtnPower:
                print("Touch 2: {0}".format("Mode PowerAll"))
    pass

def FunctionActiveTie(output):
    '''This retrieve the real Output-Input Video Relation when the user push the Display button'''
    activeTie = Matrix.ReadStatus('OutputTieStatus', {'Output':output, 'Tie Type':'Video'})
    GroupInputs.SetCurrent(None)
    ##
    if activeTie == '1':
        GroupInputs.SetCurrent(AInput1)
    elif activeTie == '2':
        GroupInputs.SetCurrent(AInput2)
    elif activeTie == '3':
        GroupInputs.SetCurrent(AInput3)
    elif activeTie == '4':
        GroupInputs.SetCurrent(AInput4)
    ##
    elif activeTie == '5':
        GroupInputs.SetCurrent(AInput5)
    elif activeTie == '6':
        GroupInputs.SetCurrent(AInput6)
    elif activeTie == '7':
        GroupInputs.SetCurrent(AInput7)
    elif activeTie == '8':
        GroupInputs.SetCurrent(AInput8)
    ##
    elif activeTie == '9':
        GroupInputs.SetCurrent(AInput9)
    elif activeTie == '10':
        GroupInputs.SetCurrent(AInput10)
    elif activeTie == '11':
        GroupInputs.SetCurrent(AInput11)
    elif activeTie == '12':
        GroupInputs.SetCurrent(AInput12)
    ##
    elif activeTie == '13':
        GroupInputs.SetCurrent(AInput13)
    elif activeTie == '14':
        GroupInputs.SetCurrent(AInput14)
    ##
    elif activeTie == '17':
        GroupInputs.SetCurrent(AInput17)
    elif activeTie == '18':
        GroupInputs.SetCurrent(AInput18)
    elif activeTie == '19':
        GroupInputs.SetCurrent(AInput19)
    elif activeTie == '20':
        GroupInputs.SetCurrent(AInput20)
    ##
    elif activeTie == '21':
        GroupInputs.SetCurrent(AInput21)
    elif activeTie == '22':
        GroupInputs.SetCurrent(AInput22)
    pass

@event(Outputs, ButtonEventList)
def OutsSwitching(button, state):
    ## Mutually Exclusive
    GroupOutputs.SetCurrent(button)
    global output
    
    ## Button Functions
    if state == 'Pressed':
        if button.Host.DeviceAlias == 'TouchPanelA':
            # XTP Slot 1-----------------------------------------------------
            if button is AOut1:
                output = '1'
                print("Touch 1: {0}".format("Out Room 1: Projector"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut2:
                output = '2'
                print("Touch 1: {0}".format("Out Room 1: LCD Podium"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut3:
                output = '3'
                print("Touch 1: {0}".format("Out Room 1: LCD Lobby"))
                ##Recall Function
                FunctionActiveTie(output)
            
            #XTP Slot 2-----------------------------------------------------
            elif button is AOut5:
                output = '5'
                print("Touch 1: {0}".format("Out Room 2: Projector"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut6:
                output = '6'
                print("Touch 1: {0}".format("Out Room 2: LCD Podium"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut7:
                output = '7'
                print("Touch 1: {0}".format("Out Room 2: LCD Lobby"))
                ##Recall Function
                FunctionActiveTie(output)

            #XTP Slot 3-----------------------------------------------------
            elif button is AOut9:
                output = '9'
                print("Touch 1: {0}".format("Out Room 1: Tricaster In 1"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut10:
                output = '10'
                print("Touch 1: {0}".format("Out Room 1: Tricaster In 2"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut11:
                output = '11'
                print("Touch 1: {0}".format("Out Room 1: Tricaster In 3"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut12:
                output = '12'
                print("Touch 1: {0}".format("Out Room 1: Tricaster In 4"))
                ##Recall Function
                FunctionActiveTie(output)

            #XTP Slot 4-----------------------------------------------------
            elif button is AOut13:
                output = '13'
                print("Touch 1: {0}".format("Out Room 2: Tricaster In 1"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut14:
                output = '14'
                print("Touch 1: {0}".format("Out Room 2: Tricaster In 2"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut15:
                output = '15'
                print("Touch 1: {0}".format("Out Room 2: Tricaster In 3"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut16:
                output = '16'
                print("Touch 1: {0}".format("Out Room 2: Tricaster In 4"))
                ##Recall Function
                FunctionActiveTie(output)
                
            #XTP Slot 5------------------------------------------------------
            elif button is AOut17:
                output = '17'
                print("Touch 1: {0}".format("Out Room 1: Cisco Camera"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut18:
                output = '18'
                print("Touch 1: {0}".format("Out Room 1: Cisco Graphics"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut19:
                output = '19'
                print("Touch 1: {0}".format("Out Room 2: Cisco Camera"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut20:
                output = '20'
                print("Touch 1: {0}".format("Out Room 2: Cisco Graphics"))
                ##Recall Function
                FunctionActiveTie(output)

            #XTP Slot 6------------------------------------------------------
            elif button is AOut21:
                output = '21'
                print("Touch 1: {0}".format("Out Room 1: Recorder"))
                ##Recall Function
                FunctionActiveTie(output)
            #
            elif button is AOut22:
                output = '22'
                print("Touch 1: {0}".format("Out Room 2: Recorder"))
                ##Recall Function
                FunctionActiveTie(output)

    #print('Active Output:' + output)
    pass

@event(Inputs, ButtonEventList)
def InSwitching(button, state):
    ## Data Init
    global output
    global input
    
    ## Button Functions
    if state == 'Pressed':
        if button.Host.DeviceAlias == 'TouchPanelA':
            # XTP Slot 1-----------------------------------------------------
            if button is AInput1:
                input = '1'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: Placa Left"))
            #
            elif button is AInput2:
                input = '2'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: Placa Right"))
            #
            elif button is AInput3:
                input = '3'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: Placa Stage"))
            #
            elif button is AInput4:
                input = '4'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: Placa Back"))

            # XTP Slot 2-----------------------------------------------------
            elif button is AInput5:
                input = '5'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: Placa Left"))
            #
            elif button is AInput6:
                input = '6'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: Placa Right"))
            #
            elif button is AInput7:
                input = '7'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: Placa Stage"))
            #
            elif button is AInput8:
                input = '8'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: Placa Back"))
                
            # XTP Slot 3-----------------------------------------------------
            elif button is AInput9:
                input = '9'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: PTZ Frontal"))
            #
            elif button is AInput10:
                input = '10'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: PTZ Back"))
            #
            elif button is AInput11:
                input = '11'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: PTZ Frontal"))
            #
            elif button is AInput12:
                input = '12'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: PTZ Back"))
                
            # XTP Slot 4-----------------------------------------------------
            elif button is AInput13:
                input = '13'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 1: PC Cabina"))
            #
            elif button is AInput14:
                input = '14'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Room 2: PC Cabina"))
                
            # XTP Slot 5-----------------------------------------------------
            elif button is AInput17:
                input = '17'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Core: Cisco 1 Out"))
            #
            elif button is AInput18:
                input = '18'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Core: Cisco 2 Out"))
            #
            elif button is AInput19:
                input = '19'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Core: ShareLink 1"))
            #
            elif button is AInput20:
                input = '20'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Core: ShareLink 2"))
                
            # XTP Slot 6-----------------------------------------------------
            elif button is AInput21:
                input = '21'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Core: Tricaster 1 Out"))
            #
            elif button is AInput22:
                input = '22'
                Matrix.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
                print("Touch 1: {0}".format("In Core: Tricaster 2 Out"))

    #print('Active Input:' + input)
    pass

## End Events Definitions-------------------------------------------------------

Initialize()

