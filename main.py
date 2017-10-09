"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Colegio de México (COLMEX)
 Project    | Alfonso Reyes Auditorium
 Version    | 0.1 --------------------------------------------------------- """

## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface, \
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface, \
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
import collections
#
print(Version())
# CONTROLLERS ------------------------------------------------------------------
IPCP = ProcessorDevice('IPCP550')
# USER INTERFACES --------------------------------------------------------------
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')
# MODULES-----------------------------------------------------------------------
## IP
import extr_matrix_XTPIICrossPointSeries_v1_1_1_1 as ModuleXTP
import chri_vp_D13HDHS_D13WUHS_v1_0_2_0           as ModuleChristie
import extr_sm_SMP_111_v1_1_0_0                   as ModuleSMP111
import smsg_display_LHxxQMFPLGCKR_Series_v1_0_0_0 as ModuleSamsung
import biam_dsp_TesiraSeries_v1_5_20_0            as ModuleTesira
import csco_vtc_SX_Series_CE82_v1_1_0_2           as ModuleCisco

##
# MODULE TO DEVICE INSTANCES ---------------------------------------------------
# Video Server
XTP = ModuleXTP.EthernetClass('172.16.241.5', 23, Model='XTP II CrossPoint 3200')
XTP.devicePassword = 'SWExtronXTP'
#
# Projectors
ProjA = ModuleChristie.EthernetClass('172.16.240.201', 3002, Model='D13WU-HS')
ProjB = ModuleChristie.EthernetClass('172.16.240.200', 3002, Model='D13WU-HS')
#
# Recorders
RecA = ModuleSMP111.EthernetClass('172.16.241.6', 23, Model='SMP 111')
RecA.devicePassword = 'R3cSala1'
#
RecB = ModuleSMP111.EthernetClass('172.16.241.7', 23, Model='SMP 111')
RecB.devicePassword = 'R3cSala2'
#
# Displays
Monitor1 = IRInterface(IPCP, 'IRS1', 'Samsung.eir')
Monitor2 = IRInterface(IPCP, 'IRS2', 'Samsung.eir')
LCDCab1 = ModuleSamsung.EthernetClass('172.16.241.24', 1515, Model='LH55QMFPLGC/KR')
LCDCab2 = ModuleSamsung.EthernetClass('172.16.241.25', 1515, Model='LH55QMFPLGC/KR')
LCDCab3 = ModuleSamsung.EthernetClass('172.16.241.26', 1515, Model='LH55QMFPLGC/KR')
LCDCab4 = ModuleSamsung.EthernetClass('172.16.241.27', 1515, Model='LH55QMFPLGC/KR')
LCDPod1 = ModuleSamsung.EthernetClass('172.16.241.28', 1515, Model='LH55QMFPLGC/KR')
LCDPod2 = ModuleSamsung.EthernetClass('172.16.241.29', 1515, Model='LH55QMFPLGC/KR')
LCDLob1 = ModuleSamsung.EthernetClass('172.16.241.30', 1515, Model='LH55QMFPLGC/KR')
LCDLob2 = ModuleSamsung.EthernetClass('172.16.241.31', 1515, Model='LH55QMFPLGC/KR')
#
# Audio Server
Tesira = ModuleTesira.EthernetClass('172.16.241.100', 23, Model='Tesira SERVER-IO')
#
# Videoconference Códecs
Cisco1 = ModuleCisco.EthernetClass('172.16.240.87', 23, Model='SX20 CE8.2.X')
Cisco1.deviceUsername ='admin'
Cisco1.devicePassword = 'auditc0lm3xS1'
#
Cisco2 = ModuleCisco.EthernetClass('172.16.240.88', 23, Model='SX20 CE8.2.X')
Cisco2.deviceUsername = 'admin'
Cisco2.devicePassword = 'auditc0lm3xS2'
#
# DEVICES INTERFACES -----------------------------------------------------------
#
# 12v Power Interface
SWPowerPort1 = SWPowerInterface(IPCP, 'SPI1')
SWPowerPort2 = SWPowerInterface(IPCP, 'SPI2')
SWPowerPort3 = SWPowerInterface(IPCP, 'SPI3')
SWPowerPort4 = SWPowerInterface(IPCP, 'SPI4')
#
# Relay
AScreenUp  = RelayInterface(IPCP, 'RLY3')
AScreenDw  = RelayInterface(IPCP, 'RLY4')
AElevatUp  = RelayInterface(IPCP, 'RLY7')
AElevatDw  = RelayInterface(IPCP, 'RLY8')
A2ScreenUp = RelayInterface(IPCP, 'RLY1')
A2ScreenDw = RelayInterface(IPCP, 'RLY2')
A2ElevatUp = RelayInterface(IPCP, 'RLY5')
A2ElevatDw = RelayInterface(IPCP, 'RLY6')
##
# BUTTONS DEFINITION -----------------------------------------------------------
# TouchPanel A -----------------------------------------------------------------
# Mode Index -------------------------------------------------------------------
ABtnIndex = Button(TLP1, 1)

# Mode Room --------------------------------------------------------------------
ARoomSplit = Button(TLP1, 240)
ARoomMixed = Button(TLP1, 241)

# Mode Main --------------------------------------------------------------------
# Mode Main - Lateral Bar
ABtnRoom    = Button(TLP1, 10)
ABtnSwitch  = Button(TLP1, 11)
ABtnDisplay = Button(TLP1, 12)
ABtnVC      = Button(TLP1, 13)
ABtnREC     = Button(TLP1, 15)
ABtnVoIP    = Button(TLP1, 16)
ABtnInfo    = Button(TLP1, 17)
ABtnPower   = Button(TLP1, 18)

# Mode Main - Up Bar
ALblMain    = Label(TLP1, 20)
ABtnRoom2   = Button(TLP1, 21)
ABtnRoom1   = Button(TLP1, 22)

# Mode Switching ---------------------------------------------------------------
# Outputs ----------------------------------------------------------------------
# XTP Out Slot 1
AOut1  = Button(TLP1, 101) ##Room1 Projector
AOut2  = Button(TLP1, 102) ##Room1 LCD Confidence
AOut3  = Button(TLP1, 103) ##Room1 LCD Podium

# XTP Out Slot 2
AOut5  = Button(TLP1, 105) ##Room2 Projector
AOut6  = Button(TLP1, 106) ##Room2 LCD Confidence
AOut7  = Button(TLP1, 107) ##Room2 LCD Podium

# XTP Out Slot 3
AOut9  = Button(TLP1, 109) ##Core Tricaster 1 - Input 1
AOut10 = Button(TLP1, 110) ##Core Tricaster 1 - Input 2
AOut11 = Button(TLP1, 111) ##Core Tricaster 1 - Input 3
AOut12 = Button(TLP1, 112) ##Core Tricaster 1 - Input 4

# XTP Out Slot 4
AOut13 = Button(TLP1, 113) ##Core Tricaster 2 - Input 1
AOut14 = Button(TLP1, 114) ##Core Tricaster 2 - Input 2
AOut15 = Button(TLP1, 115) ##Core Tricaster 2 - Input 3
AOut16 = Button(TLP1, 116) ##Core Tricaster 2 - Input 4

# XTP Out Slot 5
AOut17 = Button(TLP1, 117) ##Core Cisco 1 - Input Camera
AOut18 = Button(TLP1, 118) ##Core Cisco 1 - Input Graphics
AOut19 = Button(TLP1, 119) ##Core Cisco 2 - Input Camera
AOut20 = Button(TLP1, 120) ##Core Cisco 2 - Input Graphics

# XTP Out Slot 6
AOut21 = Button(TLP1, 121) ##Core Recorder 1
AOut22 = Button(TLP1, 122) ##Core Recorder 2

# Inputs -----------------------------------------------------------------------
# XTP Slot 1
AInput1    = Button(TLP1, 201) ##Room1 PC Left
AInput2    = Button(TLP1, 202) ##Room1 PC Right
AInput3    = Button(TLP1, 203) ##Room1 PC Stage
AInput4    = Button(TLP1, 204) ##Room1 PC Right

# XTP Slot 2
AInput5    = Button(TLP1, 205) ##Room2 PC Left
AInput6    = Button(TLP1, 206) ##Room2 PC Right
AInput7    = Button(TLP1, 207) ##Room2 PC Stage
AInput8    = Button(TLP1, 208) ##Room2 PC Back

# XTP Slot 3
AInput9    = Button(TLP1, 209) ##Room1 PTZ1
AInput10   = Button(TLP1, 210) ##Room1 PTZ2
AInput11   = Button(TLP1, 211) ##Room2 PTZ1
AInput12   = Button(TLP1, 212) ##Room2 PTZ2

# XTP Slot 4
AInput13   = Button(TLP1, 213) ##Room1 PC Cabin
AInput14   = Button(TLP1, 214) ##Room2 PC Cabin
##...
##...

# XTP Slot 5
AInput17   = Button(TLP1, 215) ##Core Cisco 1 Out
AInput18   = Button(TLP1, 216) ##Core Cisco 2 Out
AInput19   = Button(TLP1, 217) ##Core ShareLink 1
AInput20   = Button(TLP1, 218) ##Core ShareLink 2

# XTP Slot 6
AInput21   = Button(TLP1, 219) ##Core Tricaster 1 - Out 1
AInput22   = Button(TLP1, 220) ##Core Tricaster 2 - Out 1
# Input Signal Status

# XTP Slot 1
ASignal1    = Button(TLP1, 130) ##Room1 PC Left
ASignal2    = Button(TLP1, 131) ##Room1 PC Right
ASignal3    = Button(TLP1, 132) ##Room1 PC Stage
ASignal4    = Button(TLP1, 133) ##Room1 PC Right

# XTP Slot 2
ASignal5    = Button(TLP1, 134) ##Room2 PC Left
ASignal6    = Button(TLP1, 135) ##Room2 PC Right
ASignal7    = Button(TLP1, 136) ##Room2 PC Stage
ASignal8    = Button(TLP1, 137) ##Room2 PC Back

# XTP Slot 3
ASignal9    = Button(TLP1, 138) ##Room1 PTZ1
ASignal10   = Button(TLP1, 139) ##Room1 PTZ2
ASignal11   = Button(TLP1, 140) ##Room2 PTZ1
ASignal12   = Button(TLP1, 141) ##Room2 PTZ2

# XTP Slot 4
ASignal13   = Button(TLP1, 142) ##Room1 PC Cabin
ASignal14   = Button(TLP1, 143) ##Room2 PC Cabin
##...
##...

# XTP Slot 5
ASignal17   = Button(TLP1, 144) ##Core Cisco 1 Out
ASignal18   = Button(TLP1, 145) ##Core Cisco 2 Out
ASignal19   = Button(TLP1, 146) ##Core ShareLink 1
ASignal20   = Button(TLP1, 147) ##Core ShareLink 2

# XTP Slot 6
ASignal21   = Button(TLP1, 148) ##Core Tricaster 1 - Out 1
ASignal22   = Button(TLP1, 149) ##Core Tricaster 2 - Out 1

# Mode Display -----------------------------------------------------------------
# Room 1 - Projection
AProjAPwr   = Button(TLP1, 30)
AScUp       = Button(TLP1, 31)
AScDw       = Button(TLP1, 32)
AElUp       = Button(TLP1, 33)
AElDw       = Button(TLP1, 34)

# Room 1 - LCD
ALCDCab1    = Button(TLP1, 42)
ALCDCab2    = Button(TLP1, 41)
ALCDCab3    = Button(TLP1, 40)
ALCDLobby   = Button(TLP1, 43)
ALCDPodium1 = Button(TLP1, 48)

# Room 2 - Projection
AProjBPwr   = Button(TLP1, 35)
A2ScUp      = Button(TLP1, 36)
A2ScDw      = Button(TLP1, 37)
A2ElUp      = Button(TLP1, 38)
A2ElDw      = Button(TLP1, 39)

# Room 2 - LCD
A2LCDCab1   = Button(TLP1, 46)
A2LCDCab2   = Button(TLP1, 45)
A2LCDCab3   = Button(TLP1, 44)
A2LCDLobby  = Button(TLP1, 47)
ALCDPodium2 = Button(TLP1, 49)

# Mode Recording ---------------------------------------------------------------
# Recorder A - Record
Astop      = Button(TLP1, 60)
Arecord    = Button(TLP1, 61)
Apause     = Button(TLP1, 62)
Atime      = Label(TLP1, 63)

# Recorder A - Info
ARecSource  = Label(TLP1, 64)
ARecDestine = Label(TLP1, 65)
ARecResolut = Label(TLP1, 66)
ARecMode    = Label(TLP1, 67)
ARecDisk    = Label(TLP1, 68)
ARecHDCP    = Label(TLP1, 69)

# Recorder B - Record
A2stop      = Button(TLP1, 70)
A2record    = Button(TLP1, 71)
A2pause     = Button(TLP1, 72)
A2time      = Label(TLP1, 73)

# Recorder B - Info
A2RecSource  = Label(TLP1, 74)
A2RecDestine = Label(TLP1, 75)
A2RecResolut = Label(TLP1, 76)
A2RecMode    = Label(TLP1, 77)
A2RecDisk    = Label(TLP1, 78)
A2RecHDCP    = Label(TLP1, 79)

# Mode VC ----------------------------------------------------------------------
# Cisco 1 ---------------------
ADial0      = Button(TLP1, 2130)
ADial1      = Button(TLP1, 2131)
ADial2      = Button(TLP1, 2132)
ADial3      = Button(TLP1, 2133)
ADial4      = Button(TLP1, 2134)
ADial5      = Button(TLP1, 2135)
ADial6      = Button(TLP1, 2136)
ADial7      = Button(TLP1, 2137)
ADial8      = Button(TLP1, 2138)
ADial9      = Button(TLP1, 2139)
ADialDot    = Button(TLP1, 2140)
ADialHash   = Button(TLP1, 2141)
ADialDelete = Button(TLP1, 2144, repeatTime=0.1)
# Dialer

# Call
ADTMF       = Button(TLP1, 2142)
ACall       = Button(TLP1, 2143)

# Answer
AAnswer1    = Button(TLP1, 400)
ADiscard1   = Button(TLP1, 401)

# Content
AContentOn  = Button(TLP1, 2145)
AContentOff = Button(TLP1, 2146)

# Label
AVCDial     = Label(TLP1, 2147)
AVCRemote   = Label(TLP1, 2148)

# Cisco 2 -----------------------
A2Dial0      = Button(TLP1, 2100)
A2Dial1      = Button(TLP1, 2101)
A2Dial2      = Button(TLP1, 2102)
A2Dial3      = Button(TLP1, 2103)
A2Dial4      = Button(TLP1, 2104)
A2Dial5      = Button(TLP1, 2105)
A2Dial6      = Button(TLP1, 2106)
A2Dial7      = Button(TLP1, 2107)
A2Dial8      = Button(TLP1, 2108)
A2Dial9      = Button(TLP1, 2109)
A2DialDot    = Button(TLP1, 2110)
A2DialHash   = Button(TLP1, 2111)
A2DialDelete = Button(TLP1, 2114, repeatTime=0.1)
# Dialer

# Call
A2DTMF       = Button(TLP1, 2112)
A2Call       = Button(TLP1, 2113)

# Answer
AAnswer2    = Button(TLP1, 402)
ADiscard2   = Button(TLP1, 403)

# Content
A2ContentOn  = Button(TLP1, 2115)
A2ContentOff = Button(TLP1, 2116)

# Label
A2VCDial     = Label(TLP1, 2117)
A2VCRemote   = Label(TLP1, 2118)

# Mode Status ------------------------------------------------------------------
AInfoXTP     = Button(TLP1, 300)

AInfoTesira  = Button(TLP1, 301)

AInfoProjA   = Button(TLP1, 302)
AInfo2ProjA  = Label(TLP1, 303)
AInfo3ProjA  = Label(TLP1, 304)

AInfoProjB   = Button(TLP1, 305)
AInfo2ProjB  = Label(TLP1, 306)
AInfo3ProjB  = Label(TLP1, 307)

AInfoLCDCab1 = Button(TLP1, 308)
AInfoLCDCab2 = Button(TLP1, 309)
AInfoLCDCab3 = Button(TLP1, 310)
AInfoLCDCab4 = Button(TLP1, 311)

AInfoCisco   = Button(TLP1, 312)
AInfo2Cisco  = Button(TLP1, 313)

AInfoCisco2   = Button(TLP1, 315)
AInfo2Cisco2  = Button(TLP1, 316)

AInfoRecA     = Button(TLP1, 318)
AInfo2RecA    = Button(TLP1, 319)
AInfoRecB     = Button(TLP1, 320)
AInfo2RecB    = Button(TLP1, 321)

AInfoLCDLob1  = Button(TLP1, 322)
AInfoLCDLob2  = Button(TLP1, 323)

AInfoLCDPod1  = Button(TLP1, 324)
AInfoLCDPod2  = Button(TLP1, 325)

APython       = Label(TLP1, 326)


# Mode PowerOff ------------------------------------------------------------------
ABtnPowerAB   = Button(TLP1, 420)
ABtnPowerA    = Button(TLP1, 421)
ABtnPowerB    = Button(TLP1, 422)




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

# BUTTON GROUPING --------------------------------------------------------------
# Mode Index
Index = [ABtnIndex, BBtnIndex]

# Mode Room
ModeRoom = [ARoomSplit, ARoomMixed]
#
GroupRoom = MESet(ModeRoom)

# Mode Main
Main  = [ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC, ABtnREC,
         ABtnVoIP, ABtnInfo, ABtnPower,
         BBtnRoom, BBtnSwitch, BBtnDisplay, BBtnVC, BBtnAudio, BBtnREC,
         BBtnVoIP, BBtnInfo, BBtnPower]
#
GroupMainA = MESet([ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC,
                    ABtnREC,ABtnVoIP, ABtnInfo, ABtnPower])

# Mode Video Switching
Outputs = [AOut1, AOut2, AOut3, AOut5, AOut6,AOut7, AOut9, AOut10, AOut11,
           AOut12, AOut13, AOut14, AOut15, AOut16, AOut17, AOut18, AOut19,
           AOut20, AOut21, AOut22]
#
Inputs = [AInput1, AInput2, AInput3, AInput4, AInput5, AInput6, AInput7, 
          AInput8, AInput9, AInput10, AInput11, AInput12, AInput13,
          AInput14, AInput17, AInput18, AInput19, AInput20, AInput21, 
          AInput22]
#
GroupInputs = MESet(Inputs)
GroupOutputs = MESet(Outputs)

# Mode Projection
ProjeccionA = [AProjAPwr, AScUp, AScDw, AElUp, AElDw, ALCDCab1, ALCDCab2,
               ALCDCab3, ALCDLobby, ALCDPodium1]
ProjeccionB = [AProjBPwr, A2ScUp, A2ScDw, A2ElUp, A2ElDw, A2LCDCab1, A2LCDCab2,
               A2LCDCab3, A2LCDLobby, ALCDPodium2]
#
GroupScreenA = MESet([AScUp, AScDw])
GroupElevatA = MESet([AElUp, AElDw])
#
GroupScreen2A = MESet([A2ScUp, A2ScDw])
GroupElevat2A = MESet([A2ElUp, A2ElDw])

# Mode Recording
Rec = [Arecord, Astop, Apause, A2record, A2stop, A2pause]
#
GroupRecA = MESet([Arecord, Astop, Apause])
GroupRecB = MESet([A2record, A2stop, A2pause])

# Mode Videoconference
VCDial = [ADial0, ADial1, ADial2, ADial3, ADial4, ADial5, ADial6, ADial7, ADial8, ADial9, ADialDot, ADialHash, ADialDelete]
VCButtons = [ACall, ADTMF, AContentOn, AContentOff, AAnswer1, ADiscard1]
GroupContentA = MESet([AContentOn, AContentOff])
#
VC2Dial = [A2Dial0, A2Dial1, A2Dial2, A2Dial3, A2Dial4, A2Dial5, A2Dial6, A2Dial7, A2Dial8, A2Dial9, A2DialDot, A2DialHash, A2DialDelete]
VC2Buttons = [A2Call, A2DTMF, A2ContentOn, A2ContentOff, AAnswer2, ADiscard2]
GroupContentB = MESet([A2ContentOn, A2ContentOff])

# Mode PowerOff
GroupPower = [ABtnPowerA, ABtnPowerB, ABtnPowerAB]

# Button State List
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------

# INITIALIZE FUNCTION ----------------------------------------------------------
def Initialize():
    """This is the last function that loads when starting the system"""
    ## Open Sockets
    ## IP
    XTP.Connect(timeout = 5)
    Tesira.Connect(timeout = 5)
    #
    ProjA.Connect(timeout = 5)
    ProjB.Connect(timeout = 5)
    #
    RecA.Connect(timeout = 5)
    RecB.Connect(timeout = 5)
    #
    LCDCab1.Connect(timeout = 5)
    LCDCab2.Connect(timeout = 5)
    LCDCab3.Connect(timeout = 5)
    LCDCab4.Connect(timeout = 5)
    LCDLob1.Connect(timeout = 5)
    LCDLob2.Connect(timeout = 5)
    LCDPod1.Connect(timeout = 5)
    LCDPod2.Connect(timeout = 5)
    #
    Cisco1.Connect(timeout = 5)
    Cisco2.Connect(timeout = 5)
    
    ## XTP Matrix Data Init
    global output
    global input
    output = ''
    input = ''

    ## Cisco1 Dial PAGE
    global dialerVC  ## To access the Dial String variable in all program
    dialerVC = ''    ## Clean the Dial String Variable
    AVCDial.SetText('')

    ## Cisco1 Dial PAGE
    global dialerVC2  ## To access the Dial String variable in all program
    dialerVC2 = ''    ## Clean the Dial String Variable
    A2VCDial.SetText('')

    ##12v Interface (This brings power to all Relays)
    SWPowerPort1.SetState('On')
    SWPowerPort2.SetState('On')
    SWPowerPort3.SetState('On')
    SWPowerPort4.SetState('On')

    ## Audio Routing (XTP HDMI Matrix to Tesira Server I/O)
    ## XTP Input Slot 1
    XTP.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'9', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'10', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'11', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'12', 'Tie Type':'Audio'})
    ## XTP Input Slot 2
    XTP.Set('MatrixTieCommand', None, {'Input':'5', 'Output':'13', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'6', 'Output':'14', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'7', 'Output':'15', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'8', 'Output':'16', 'Tie Type':'Audio'})
    ## XTP Input Slot 3
    XTP.Set('MatrixTieCommand', None, {'Input':'13', 'Output':'17', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'14', 'Output':'18', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'19', 'Output':'19', 'Tie Type':'Audio'})
    XTP.Set('MatrixTieCommand', None, {'Input':'20', 'Output':'20', 'Tie Type':'Audio'})

    ## Notify to console
    print('System Initialize')
    APython.SetText(Version())
    pass

# RECONEX / QUERY LIST ---------------------------------------------------------
# This is a rotate list of Update Commands per Device
XTP_QUERY_LIST = [
    ('InputSignal',{'Input':'1'}),
    ('InputSignal',{'Input':'2'}),
    ('InputSignal',{'Input':'3'}),
    ('InputSignal',{'Input':'4'}),
    ('InputSignal',{'Input':'5'}),
    ('InputSignal',{'Input':'6'}),
    ('InputSignal',{'Input':'7'}),
    ('InputSignal',{'Input':'8'}),
    ('InputSignal',{'Input':'9'}),
    ('InputSignal',{'Input':'10'}),
    ('InputSignal',{'Input':'11'}),
    ('InputSignal',{'Input':'12'}),
    ('InputSignal',{'Input':'13'}),
    ('InputSignal',{'Input':'14'}),
    #('InputSignal',{'Input':'15'}),
    #('InputSignal',{'Input':'16'}),
    ('InputSignal',{'Input':'17'}),
    ('InputSignal',{'Input':'18'}),
    ('InputSignal',{'Input':'19'}),
    ('InputSignal',{'Input':'20'}),
    ('InputSignal',{'Input':'21'}),
    ('InputSignal',{'Input':'22'}),
    #('InputSignal',{'Input':'23'}),
    #('InputSignal',{'Input':'24'}),
]
XTP_Queue = collections.deque(XTP_QUERY_LIST)

TESIRA_QUERY_LIST = [
    ('LogicState', {'Instance Tag':'Room', 'Channel':'1'}),
]
Tesira_Queue = collections.deque(TESIRA_QUERY_LIST)

PROJECTOR_A_QUERY_LIST = [
    ('Power', None),
    ('Input', None),
]
Projector_A_Queue = collections.deque(PROJECTOR_A_QUERY_LIST)

PROJECTOR_B_QUERY_LIST = [
    ('Power', None),
    ('Input', None),
]
Projector_B_Queue = collections.deque(PROJECTOR_B_QUERY_LIST)

CISCO1_QUERY_LIST = [
    ('Presentation', {'Instance':'1'}),
    ('CallStatus', {'Call':'1'}),
    ('DisplayName', {'Call':'1'}),
    ('RemoteNumber', {'Call':'1'}),
]
Cisco1_Queue = collections.deque(CISCO1_QUERY_LIST)

CISCO2_QUERY_LIST = [
    ('Presentation', {'Instance':'1'}),
    ('CallStatus', {'Call':'1'}),
    ('DisplayName', {'Call':'1'}),
    ('RemoteNumber', {'Call':'1'}),
]
Cisco2_Queue = collections.deque(CISCO2_QUERY_LIST)

RECA_QUERY_LIST = [
    ('Record', None),
    ('RecordDestination', None),
    ('RecordingMode', None),
    ('HDCPStatus', None),
    ('VideoResolution', {'Stream':'Record'}),
    ('RemainingFreeDiskSpace',{'Drive':'Primary'}),
    ('CurrentRecordingDuration', None),
]
RecA_Queue = collections.deque(RECA_QUERY_LIST)

RECB_QUERY_LIST = [
    ('Record', None),
    ('RecordDestination', None),
    ('RecordingMode', None),
    ('HDCPStatus', None),
    ('VideoResolution', {'Stream':'Record'}),
    ('RemainingFreeDiskSpace',{'Drive':'Primary'}),
    ('CurrentRecordingDuration', None),
]
RecB_Queue = collections.deque(RECB_QUERY_LIST)

LCDCab1_QUERY_LIST = [
    ('Power', None),
]
LCDCab1_Queue = collections.deque(LCDCab1_QUERY_LIST)

LCDCab2_QUERY_LIST = [
    ('Power', None),
]
LCDCab2_Queue = collections.deque(LCDCab2_QUERY_LIST)

LCDCab3_QUERY_LIST = [
    ('Power', None),
]
LCDCab3_Queue = collections.deque(LCDCab3_QUERY_LIST)

LCDCab4_QUERY_LIST = [
    ('Power', None),
]
LCDCab4_Queue = collections.deque(LCDCab4_QUERY_LIST)

LCDLob1_QUERY_LIST = [
    ('Power', None),
]
LCDLob1_Queue = collections.deque(LCDLob1_QUERY_LIST)

LCDLob2_QUERY_LIST = [
    ('Power', None),
]
LCDLob2_Queue = collections.deque(LCDLob2_QUERY_LIST)

LCDPod1_QUERY_LIST = [
    ('Power', None),
]
LCDPod1_Queue = collections.deque(LCDPod1_QUERY_LIST)

LCDPod2_QUERY_LIST = [
    ('Power', None),
]
LCDPod2_Queue = collections.deque(LCDPod2_QUERY_LIST)

# RECONEX / QUERY RECALL ------------------------------------------------------
# This is a recursive function to send Query Command to Device certain time
def QueryXTP():
    """This send Query commands to device every 03.s"""
    #
    XTP.Update(*XTP_Queue[0])
    XTP_Queue.rotate(-1)
    XTP_PollingWait.Restart()
    #
XTP_PollingWait = Wait(1, QueryXTP)

def QueryTesira():
    """This send Query commands to device every 03.s"""
    #
    Tesira.Update(*Tesira_Queue[0])
    Tesira_Queue.rotate(-1)
    Tesira_PollingWait.Restart()
    #
Tesira_PollingWait = Wait(5, QueryTesira)

def QueryProjectorA():
    """This send Query commands to device every 03.s"""
    #
    ProjA.Update(*Projector_A_Queue[0])
    Projector_A_Queue.rotate(-1)
    Projector_A_PollingWait.Restart()
    #
Projector_A_PollingWait = Wait(5, QueryProjectorA)

def QueryProjectorB():
    """This send Query commands to device every 03.s"""
    #
    ProjB.Update(*Projector_B_Queue[0])
    Projector_B_Queue.rotate(-1)
    Projector_B_PollingWait.Restart()
    #
Projector_B_PollingWait = Wait(5, QueryProjectorB)

def QueryCisco1():
    """This send Query commands to device every 01.s"""
    #
    Cisco1.Update(*Cisco1_Queue[0])
    Cisco1_Queue.rotate(-1)
    Cisco1_PollingWait.Restart()
    #
Cisco1_PollingWait = Wait(1, QueryCisco1)

def QueryCisco2():
    """This send Query commands to device every 01.s"""
    #
    Cisco2.Update(*Cisco2_Queue[0])
    Cisco2_Queue.rotate(-1)
    Cisco2_PollingWait.Restart()
    #
Cisco2_PollingWait = Wait(1, QueryCisco2)

def QueryRecA():
    """This send Query commands to device every 01.s"""
    #
    RecA.Update(*RecA_Queue[0])
    RecA_Queue.rotate(-1)
    RecA_PollingWait.Restart()
    #
RecA_PollingWait = Wait(1, QueryRecA)

def QueryRecB():
    """This send Query commands to device every 01.s"""
    #
    RecB.Update(*RecB_Queue[0])
    RecB_Queue.rotate(-1)
    RecB_PollingWait.Restart()
    #
RecB_PollingWait = Wait(1, QueryRecB)

def QueryLCDCab1():
    """This send Query commands to device every 01.s"""
    #
    LCDCab1.Update(*LCDCab1_Queue[0])
    LCDCab1_Queue.rotate(-1)
    LCDCab1_PollingWait.Restart()
    #
LCDCab1_PollingWait = Wait(5, QueryLCDCab1)

def QueryLCDCab2():
    """This send Query commands to device every 02.s"""
    #
    LCDCab2.Update(*LCDCab2_Queue[0])
    LCDCab2_Queue.rotate(-1)
    LCDCab2_PollingWait.Restart()
    #
LCDCab2_PollingWait = Wait(5, QueryLCDCab2)

def QueryLCDCab3():
    """This send Query commands to device every 03.s"""
    #
    LCDCab3.Update(*LCDCab3_Queue[0])
    LCDCab3_Queue.rotate(-1)
    LCDCab3_PollingWait.Restart()
    #
LCDCab3_PollingWait = Wait(5, QueryLCDCab3)

def QueryLCDCab4():
    """This send Query commands to device every 03.s"""
    #
    LCDCab4.Update(*LCDCab4_Queue[0])
    LCDCab4_Queue.rotate(-1)
    LCDCab4_PollingWait.Restart()
    #
LCDCab4_PollingWait = Wait(5, QueryLCDCab4)

def QueryLCDLob1():
    """This send Query commands to device every 03.s"""
    #
    LCDLob1.Update(*LCDLob1_Queue[0])
    LCDLob1_Queue.rotate(-1)
    LCDLob1_PollingWait.Restart()
    #
LCDLob1_PollingWait = Wait(5, QueryLCDLob1)

def QueryLCDLob2():
    """This send Query commands to device every 03.s"""
    #
    LCDLob2.Update(*LCDLob2_Queue[0])
    LCDLob2_Queue.rotate(-1)
    LCDLob2_PollingWait.Restart()
    #
LCDLob2_PollingWait = Wait(5, QueryLCDLob2)

def QueryLCDPod1():
    """This send Query commands to device every 03.s"""
    #
    LCDPod1.Update(*LCDPod1_Queue[0])
    LCDPod1_Queue.rotate(-1)
    LCDPod1_PollingWait.Restart()
    #
LCDPod1_PollingWait = Wait(5, QueryLCDPod1)

def QueryLCDPod2():
    """This send Query commands to device every 03.s"""
    #
    LCDPod2.Update(*LCDPod2_Queue[0])
    LCDPod2_Queue.rotate(-1)
    LCDPod2_PollingWait.Restart()
    #
LCDPod2_PollingWait = Wait(5, QueryLCDPod2)

# RECONEX / TCP CONNECTIONS HANDLING ------------------------------------------
# This Try to connect automatically a Device
def AttemptConnectXTP():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect XTP')
    result = XTP.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitXTP.Restart()
    pass
reconnectWaitXTP = Wait(15, AttemptConnectXTP)

def AttemptConnectTesira():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Tesira Server')
    result = Tesira.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitTesira.Restart()
    pass
reconnectWaitTesira = Wait(15, AttemptConnectTesira)

def AttemptConnectProjectorA():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector A')
    result = ProjA.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitProjectorA.Restart()
    pass
reconnectWaitProjectorA = Wait(15, AttemptConnectProjectorA)

def AttemptConnectProjectorB():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector B')
    result = ProjB.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitProjectorB.Restart()
    pass
reconnectWaitProjectorB = Wait(15, AttemptConnectProjectorB)

def AttemptConnectCisco1():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Cisco 1')
    result = Cisco1.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitCisco1.Restart()
    pass
reconnectWaitCisco1 = Wait(15, AttemptConnectCisco1)

def AttemptConnectCisco2():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Cisco 2')
    result = Cisco2.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitCisco2.Restart()
    pass
reconnectWaitCisco2 = Wait(15, AttemptConnectCisco2)

def AttemptConnectRecA():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Recorder A')
    result = RecA.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitRecA.Restart()
    pass
reconnectWaitRecA = Wait(15, AttemptConnectRecA)

def AttemptConnectRecB():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Recorder B')
    result = RecB.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitRecB.Restart()
    pass
reconnectWaitRecB = Wait(15, AttemptConnectRecB)

def AttemptConnectLCDCab1():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD 1')
    result = LCDCab1.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab1.Restart()
    pass
reconnectWaitLCDCab1 = Wait(15, AttemptConnectLCDCab1)

def AttemptConnectLCDCab2():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD 2')
    result = LCDCab2.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab2.Restart()
    pass
reconnectWaitLCDCab2 = Wait(15, AttemptConnectLCDCab2)

def AttemptConnectLCDCab3():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD 3')
    result = LCDCab3.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab3.Restart()
    pass
reconnectWaitLCDCab3 = Wait(15, AttemptConnectLCDCab3)

def AttemptConnectLCDCab4():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD 4')
    result = LCDCab4.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab4.Restart()
    pass
reconnectWaitLCDCab4 = Wait(15, AttemptConnectLCDCab4)

def AttemptConnectLCDLob1():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD Lob1')
    result = LCDLob1.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDLob1.Restart()
    pass
reconnectWaitLCDLob1 = Wait(15, AttemptConnectLCDLob1)

def AttemptConnectLCDLob2():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD Lob2')
    result = LCDLob2.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDLob2.Restart()
    pass
reconnectWaitLCDLob2 = Wait(15, AttemptConnectLCDLob2)

def AttemptConnectLCDPod1():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD Pod1')
    result = LCDPod1.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDPod1.Restart()
    pass
reconnectWaitLCDPod1 = Wait(15, AttemptConnectLCDPod1)

def AttemptConnectLCDPod2():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect LCD Pod2')
    result = LCDPod2.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDPod2.Restart()
    pass
reconnectWaitLCDPod2 = Wait(15, AttemptConnectLCDPod2)

# RECONEX / TCP CONNECTIONS HANDLING ------------------------------------------
# This Functions parse the Incoming Data of every Device
def ReceiveXTP(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module XTP: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            XTP.Disconnect()
            reconnectWaitXTP.Restart()
            AInfoXTP.SetState(0)
        else:
            AInfoXTP.SetState(1)
    #
    elif command == 'InputSignal':
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
        #
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
        #
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
        #
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
        #
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
        #
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
        #print('--- Parsing Matrix: (Out ' +  qualifier['Output'] + ' In ' + value + ' ' + qualifier['Tie Type'] + ')')
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
    pass

def ReceiveTesira(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Tesira: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            Tesira.Disconnect()
            reconnectWaitTesira.Restart()
            AInfoTesira.SetState(0)
        else:
            AInfoTesira.SetState(1)
    #
    elif command == 'LogicState':
        if qualifier['Instance Tag'] == 'Room' and qualifier['Channel'] == '1':
            if value == 'True':
                Room_Data['Mixed'] = True
                #Tesira.Set('PresetRecall', '1')
                GroupRoom.SetCurrent(ARoomMixed)
            else:
                Room_Data['Mixed'] = False
                #Tesira.Set('PresetRecall', '2')
                GroupRoom.SetCurrent(ARoomSplit)
    pass

def ReceiveProjectorA(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Projector A: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            ProjA.Disconnect()
            reconnectWaitProjectorA.Restart()
            AInfoProjA.SetState(0)
        else:
            AInfoProjA.SetState(1)
    #
    elif command == 'Power':
        AInfo2ProjA.SetText('Power ' + value)
        print('--- Parsing Projector A: (Power ' +  value + ' )')
        if value == 'On':
            AProjAPwr.SetState(1)
            Room1ElevatorDown()
            Room1ScreenDown()
        else:
            AProjAPwr.SetState(0)
            Room1ElevatorUp()
            Room1ScreenUp()
    #
    elif command == 'Input':
        AInfo3ProjA.SetText(value)
        print('--- Parsing Projector A: (Input ' +  value + ' )')
    pass

def ReceiveProjectorB(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Projector B: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            ProjB.Disconnect()
            reconnectWaitProjectorB.Restart()
            AInfoProjB.SetState(0)
        else:
            AInfoProjB.SetState(1)
    #
    elif command == 'Power':
        AInfo2ProjB.SetText('Power ' + value)
        print('--- Parsing Projector B: (Power ' +  value + ' )')
        if value == 'On':
            AProjBPwr.SetState(1)
            Room2ElevatorDown()
            Room2ScreenDown()
        else:
            AProjBPwr.SetState(0)
            Room2ElevatorUp()
            Room2ScreenUp()
    #
    elif command == 'Input':
        AInfo3ProjB.SetText(value)
        print('--- Parsing Projector B: (Input ' +  value + ' )')
    pass

def ReceiveCisco1(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Cisco1: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            Cisco1.Disconnect()
            reconnectWaitCisco1.Restart()
            AInfoCisco.SetState(0)
        else:
            AInfoCisco.SetState(1)
    #
    elif command == 'Presentation':
        print('--- Parsing Cisco 1: (Presentation ' +  value + ' )')
        if value == '2':
            GroupContentA.SetCurrent(AContentOn)
        elif value == 'Stop':
            GroupContentA.SetCurrent(AContentOff)
    #
    elif command == 'CallStatus':
        print('--- Parsing Cisco 2: (CallStatus ' +  value + ' )')
        AInfo2Cisco.SetText(value)
        #
        if value == 'Ringing':
            TLP1.ShowPopup('Cisco1.Call')
        else:
            TLP1.HidePopup('Cisco1.Call')
        #
        if value == 'Idle' or value == 'Disconnecting':
            ACall.SetState(0)
            ACall.SetText('Llamar')
        #
        elif value == 'Connected' or value == 'Connecting':
            ACall.SetState(1)
            ACall.SetText('Colgar')
    #
    elif command == 'DisplayName':
        print('--- Parsing Cisco 1: (DisplayName ' +  value + ' )')
        AVCRemote.SetText(value)
    #
    elif command == 'RemoteNumber':
        print('--- Parsing Cisco 1: (RemoteNumber ' +  value + ' )')
    pass

def ReceiveCisco2(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Cisco2: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            Cisco2.Disconnect()
            reconnectWaitCisco2.Restart()
            AInfoCisco2.SetState(0)
        else:
            AInfoCisco2.SetState(1)
    #
    elif command == 'Presentation':
        print('--- Parsing Cisco 2: (Presentation ' +  value + ' )')
        if value == '2':
            GroupContentB.SetCurrent(A2ContentOn)
        elif value == 'Stop':
            GroupContentB.SetCurrent(A2ContentOff)
    #
    elif command == 'CallStatus':
        AInfo2Cisco2.SetText(value)
        print('--- Parsing Cisco 2: (CallStatus ' +  value + ' )')
        #
        if value == 'Ringing':
            TLP1.ShowPopup('Cisco2.Call')
        else:
            TLP1.HidePopup('Cisco2.Call')
        #
        if value == 'Idle' or value == 'Disconnecting':
            A2Call.SetState(0)
            A2Call.SetText('Llamar')
        #
        elif value == 'Connected' or value == 'Connecting':
            A2Call.SetState(1)
            A2Call.SetText('Colgar')
    #
    elif command == 'DisplayName':
        print('--- Parsing Cisco 2: (DisplayName ' +  value + ' )')
        A2VCRemote.SetText(value)
    #
    elif command == 'RemoteNumber':
        print('--- Parsing Cisco 2: (RemoteNumber ' +  value + ' )')
    pass

def ReceiveRecA(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Rec A: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            RecA.Disconnect()
            reconnectWaitRecA.Restart()
            AInfoRecA.SetState(0)
        else:
            AInfoRecA.SetState(1)
    #
    elif command == 'Record':
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
        AInfo2RecA.SetText(value)
        if value == 'Start':
            GroupRecA.SetCurrent(Arecord)
        elif value == 'Pause':
            GroupRecA.SetCurrent(Apause)
        elif value == 'Stop':
            GroupRecA.SetCurrent(Astop)
    #
    elif command == 'RecordDestination':
        ARecDestine.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'RecordingMode':
        ARecMode.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'VideoResolution':
        ARecResolut.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'HDCPStatus':
        ARecHDCP.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'RemainingFreeDiskSpace':
        if qualifier['Drive'] == 'Primary':
            value = int(value / 1024)
            ARecDisk.SetText('Disk Free: ' + str(value) + 'GB')
            #print('--- Parsing Recorder A: ' + command + ' ' + str(value))
    #
    elif command == 'CurrentRecordingDuration':
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
        Atime.SetText(value)
    pass

def ReceiveRecB(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module Rec B: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            RecB.Disconnect()
            reconnectWaitRecB.Restart()
            AInfoRecB.SetState(0)
        else:
            AInfoRecB.SetState(1)
    #
    elif command == 'Record':
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
        AInfo2RecB.SetText(value)
        if value == 'Start':
            GroupRecB.SetCurrent(A2record)
        elif value == 'Pause':
            GroupRecB.SetCurrent(A2pause)
        elif value == 'Stop':
            GroupRecB.SetCurrent(A2stop)
    #
    elif command == 'RecordDestination':
        A2RecDestine.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'RecordingMode':
        A2RecMode.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'VideoResolution':
        A2RecResolut.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'HDCPStatus':
        A2RecHDCP.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'RemainingFreeDiskSpace':
        if qualifier['Drive'] == 'Primary':
            value = int(value / 1024)
            A2RecDisk.SetText('Disk Free: ' + str(value) + 'GB')
            #print('--- Parsing Recorder B: ' + command + ' ' + str(value))
    #
    elif command == 'CurrentRecordingDuration':
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
        A2time.SetText(value)
    pass

def ReceiveLCDCab1(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Cab1: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDCab1.Disconnect()
            reconnectWaitLCDCab1.Restart()
            AInfoLCDCab1.SetState(0)
        else:
            AInfoLCDCab1.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab1: (Power ' +  value + ' )')
        if value == 'On':
            A2LCDCab2.SetState(1)
        else:
            A2LCDCab2.SetState(0)
    pass

def ReceiveLCDCab2(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Cab2: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDCab2.Disconnect()
            reconnectWaitLCDCab2.Restart()
            AInfoLCDCab2.SetState(0)
        else:
            AInfoLCDCab2.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab2: (Power ' +  value + ' )')
        if value == 'On':
            A2LCDCab3.SetState(1)
        else:
            A2LCDCab3.SetState(0)
    pass

def ReceiveLCDCab3(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Cab3: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDCab3.Disconnect()
            reconnectWaitLCDCab3.Restart()
            AInfoLCDCab3.SetState(0)
        else:
            AInfoLCDCab3.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab3: (Power ' +  value + ' )')
        if value == 'On':
            ALCDCab1.SetState(1)
        else:
            ALCDCab1.SetState(0)
    pass

def ReceiveLCDCab4(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Cab4: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDCab4.Disconnect()
            reconnectWaitLCDCab4.Restart()
            AInfoLCDCab4.SetState(0)
        else:
            AInfoLCDCab4.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab4: (Power ' +  value + ' )')
        if value == 'On':
            ALCDCab2.SetState(1)
        else:
            ALCDCab2.SetState(0)
    pass

def ReceiveLCDLob1(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Lob1: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDLob1.Disconnect()
            reconnectWaitLCDLob1.Restart()
            AInfoLCDLob1.SetState(0)
        else:
            AInfoLCDLob1.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Lob1: (Power ' +  value + ' )')
        if value == 'On':
            ALCDLobby.SetState(1)
        else:
            ALCDLobby.SetState(0)
    pass

def ReceiveLCDLob2(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Lob2: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDLob2.Disconnect()
            reconnectWaitLCDLob2.Restart()
            AInfoLCDLob2.SetState(0)
        else:
            AInfoLCDLob2.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Lob2: (Power ' +  value + ' )')
        if value == 'On':
            A2LCDLobby.SetState(1)
        else:
            A2LCDLobby.SetState(0)
    pass

def ReceiveLCDPod1(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Pod1: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDPod1.Disconnect()
            reconnectWaitLCDPod1.Restart()
            AInfoLCDPod1.SetState(0)
        else:
            AInfoLCDPod1.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Pod1: (Power ' +  value + ' )')
        if value == 'On':
            ALCDPodium1.SetState(1)
        else:
            ALCDPodium1.SetState(0)
    pass

def ReceiveLCDPod2(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module LCD Pod2: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            LCDPod2.Disconnect()
            reconnectWaitLCDPod2.Restart()
            AInfoLCDPod2.SetState(0)
        else:
            AInfoLCDPod2.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Pod2: (Power ' +  value + ' )')
        if value == 'On':
            ALCDPodium2.SetState(1)
        else:
            ALCDPodium2.SetState(0)
    pass

# RECONEX / SUBSCRIPTIONS ------------------------------------------
# This Commands make a real data mach from Device to Processor
def SubscribeXTP():
    XTP.SubscribeStatus('ConnectionStatus', None, ReceiveXTP)
    ##
    XTP.SubscribeStatus('InputSignal', {'Input':'1'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'2'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'3'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'4'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'5'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'6'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'7'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'8'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'9'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'10'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'11'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'12'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'13'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'14'}, ReceiveXTP)
    #XTP.SubscribeStatus('InputSignal', {'Input':'15'}, ReceiveXTP)
    #XTP.SubscribeStatus('InputSignal', {'Input':'16'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'17'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'18'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'19'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'20'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'21'}, ReceiveXTP)
    XTP.SubscribeStatus('InputSignal', {'Input':'22'}, ReceiveXTP)
    #XTP.SubscribeStatus('InputSignal', {'Input':'23'}, ReceiveXTP)
    #XTP.SubscribeStatus('InputSignal', {'Input':'24'}, ReceiveXTP)
    ##
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'}, ReceiveXTP)
    #XTP.SubscribeStatus('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'5', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'6', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'7', 'Tie Type':'Video'}, ReceiveXTP)
    #XTP.SubscribeStatus('OutputTieStatus', {'Output':'8', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'9', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'10', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'11', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'12', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'13', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'14', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'15', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'16', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'17', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'18', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'19', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'20', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'21', 'Tie Type':'Video'}, ReceiveXTP)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'22', 'Tie Type':'Video'}, ReceiveXTP)
    #XTP.SubscribeStatus('OutputTieStatus', {'Output':'23', 'Tie Type':'Video'}, ReceiveXTP)
    #XTP.SubscribeStatus('OutputTieStatus', {'Output':'24', 'Tie Type':'Video'}, ReceiveXTP)
    pass
SubscribeXTP()
#
def SubscribeTesira():
    Tesira.SubscribeStatus('ConnectionStatus', None, ReceiveTesira)
    Tesira.SubscribeStatus('LogicState', {'Instance Tag':'Room', 'Channel':'1'}, ReceiveTesira)
    pass
SubscribeTesira()
#
def SubscribeProjectorA():
    ProjA.SubscribeStatus('ConnectionStatus', None, ReceiveProjectorA)
    ProjA.SubscribeStatus('Power', None, ReceiveProjectorA)
    ProjA.SubscribeStatus('Input', None, ReceiveProjectorA)
    pass
SubscribeProjectorA()
#
def SubscribeProjectorB():
    ProjB.SubscribeStatus('ConnectionStatus', None, ReceiveProjectorB)
    ProjB.SubscribeStatus('Power', None, ReceiveProjectorB)
    ProjB.SubscribeStatus('Input', None, ReceiveProjectorB)
    pass
SubscribeProjectorB()
#
def SubscribeCisco1():
    Cisco1.SubscribeStatus('ConnectionStatus', None, ReceiveCisco1)
    Cisco1.SubscribeStatus('Presentation', {'Instance':'1'}, ReceiveCisco1)
    Cisco1.SubscribeStatus('PresentationMode', None, ReceiveCisco1)
    Cisco1.SubscribeStatus('CallStatus', {'Call':'1'}, ReceiveCisco1)
    Cisco1.SubscribeStatus('CallStatusType', {'Call':'1'}, ReceiveCisco1)
    Cisco1.SubscribeStatus('DisplayName', {'Call':'1'}, ReceiveCisco1)
    Cisco1.SubscribeStatus('IPAddress', None, ReceiveCisco1)
    Cisco1.SubscribeStatus('RemoteNumber', {'Call':'1'}, ReceiveCisco1)
    pass
SubscribeCisco1()
#
def SubscribeCisco2():
    Cisco2.SubscribeStatus('ConnectionStatus', None, ReceiveCisco2)
    Cisco2.SubscribeStatus('Presentation', {'Instance':'1'}, ReceiveCisco2)
    Cisco2.SubscribeStatus('PresentationMode', None, ReceiveCisco2)
    Cisco2.SubscribeStatus('CallStatus', {'Call':'1'}, ReceiveCisco2)
    Cisco2.SubscribeStatus('CallStatusType', {'Call':'1'}, ReceiveCisco2)
    Cisco2.SubscribeStatus('DisplayName', {'Call':'1'}, ReceiveCisco2)
    Cisco2.SubscribeStatus('IPAddress', None, ReceiveCisco2)
    Cisco2.SubscribeStatus('RemoteNumber', {'Call':'1'}, ReceiveCisco2)
    pass
SubscribeCisco2()
#
def SubscribeRecA():
    RecA.SubscribeStatus('ConnectionStatus', None, ReceiveRecA)
    RecA.SubscribeStatus('Record', None, ReceiveRecA)
    RecA.SubscribeStatus('RecordDestination', None, ReceiveRecA)
    RecA.SubscribeStatus('RecordingMode', None, ReceiveRecA)
    RecA.SubscribeStatus('HDCPStatus', None, ReceiveRecA)
    RecA.SubscribeStatus('VideoResolution', {'Stream':'Record'}, ReceiveRecA)
    RecA.SubscribeStatus('RemainingFreeDiskSpace',{'Drive':'Primary'}, ReceiveRecA)
    RecA.SubscribeStatus('CurrentRecordingDuration', None, ReceiveRecA)
    pass
SubscribeRecA()
#
def SubscribeRecB():
    RecB.SubscribeStatus('ConnectionStatus', None, ReceiveRecB)
    RecB.SubscribeStatus('Record', None, ReceiveRecB)
    RecB.SubscribeStatus('RecordDestination', None, ReceiveRecB)
    RecB.SubscribeStatus('RecordingMode', None, ReceiveRecB)
    RecB.SubscribeStatus('HDCPStatus', None, ReceiveRecB)
    RecB.SubscribeStatus('VideoResolution', {'Stream':'Record'}, ReceiveRecB)
    RecB.SubscribeStatus('RemainingFreeDiskSpace',{'Drive':'Primary'}, ReceiveRecB)
    RecB.SubscribeStatus('CurrentRecordingDuration', None, ReceiveRecB)
    pass
SubscribeRecB()
#
def SubscribeLCD1():
    LCDCab1.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab1)
    LCDCab1.SubscribeStatus('Power', None, ReceiveLCDCab1)
    pass
SubscribeLCD1()
#
def SubscribeLCD2():
    LCDCab2.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab2)
    LCDCab2.SubscribeStatus('Power', None, ReceiveLCDCab2)
    pass
SubscribeLCD2()
#
def SubscribeLCD3():
    LCDCab3.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab3)
    LCDCab3.SubscribeStatus('Power', None, ReceiveLCDCab3)
    pass
SubscribeLCD3()
#
def SubscribeLCD4():
    LCDCab4.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab4)
    LCDCab4.SubscribeStatus('Power', None, ReceiveLCDCab4)
    pass
SubscribeLCD4()
#
def SubscribeLob1():
    LCDLob1.SubscribeStatus('ConnectionStatus', None, ReceiveLCDLob1)
    LCDLob1.SubscribeStatus('Power', None, ReceiveLCDLob1)
    pass
SubscribeLob1()
#
def SubscribeLob2():
    LCDLob2.SubscribeStatus('ConnectionStatus', None, ReceiveLCDLob2)
    LCDLob2.SubscribeStatus('Power', None, ReceiveLCDLob2)
    pass
SubscribeLob2()
#
def SubscribePod1():
    LCDPod1.SubscribeStatus('ConnectionStatus', None, ReceiveLCDPod1)
    LCDPod1.SubscribeStatus('Power', None, ReceiveLCDPod1)
    pass
SubscribePod1()
#
def SubscribePod2():
    LCDPod2.SubscribeStatus('ConnectionStatus', None, ReceiveLCDPod2)
    LCDPod2.SubscribeStatus('Power', None, ReceiveLCDPod2)
    pass
SubscribePod2()

# RECONEX / SOCKET ------------------------------------------
# This reports a physical connection socket of every Device
@event(XTP, 'Disconnected')
@event(XTP, 'Connected')
def XTP_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectMatrix"""
    if state == 'Connected':
        AInfoXTP.SetState(1)
        reconnectWaitXTP.Cancel()
    else:
        AInfoXTP.SetState(0)
        print('Socket Disconnected: Matrix')
    pass

@event(Tesira, 'Disconnected')
@event(Tesira, 'Connected')
def Tesira_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoTesira.SetState(1)
        reconnectWaitTesira.Cancel()
    else:
        AInfoTesira.SetState(0)
        print('Socket Disconnected: Tesira')
    pass

@event(ProjA, 'Disconnected')
@event(ProjA, 'Connected')
def ProjA_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoProjA.SetState(1)
        reconnectWaitProjectorA.Cancel()
    else:
        AInfoProjA.SetState(0)
        print('Socket Disconnected: Projector A')
    pass

@event(ProjB, 'Disconnected')
@event(ProjB, 'Connected')
def ProjB_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoProjB.SetState(1)
        reconnectWaitProjectorB.Cancel()
    else:
        AInfoProjB.SetState(0)
        print('Socket Disconnected: Projector B')
    pass

@event(Cisco1, 'Disconnected')
@event(Cisco1, 'Connected')
def Cisco1_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoCisco.SetState(1)
        reconnectWaitCisco1.Cancel()
    else:
        print('Socket Disconnected: Cisco1')
        AInfoCisco.SetState(0)
    pass

@event(Cisco2, 'Disconnected')
@event(Cisco2, 'Connected')
def Cisco2_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoCisco2.SetState(1)
        reconnectWaitCisco2.Cancel()
    else:
        print('Socket Disconnected: Cisco2')
        AInfoCisco2.SetState(0)
    pass

@event(RecA, 'Disconnected')
@event(RecA, 'Connected')
def RecA_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoRecA.SetState(1)
        reconnectWaitRecA.Cancel()
    else:
        AInfoRecA.SetState(0)
        print('Socket Disconnected: Rec A')
    pass

@event(RecB, 'Disconnected')
@event(RecB, 'Connected')
def RecB_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoRecB.SetState(1)
        reconnectWaitRecB.Cancel()
    else:
        AInfoRecB.SetState(0)
        print('Socket Disconnected: Rec A')
    pass

@event(LCDCab1, 'Disconnected')
@event(LCDCab1, 'Connected')
def LCDCab1_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDCab1.SetState(1)
        reconnectWaitLCDCab1.Cancel()
    else:
        AInfoLCDCab1.SetState(0)
        print('Socket Disconnected: LCD Cab1')
    pass

@event(LCDCab2, 'Disconnected')
@event(LCDCab2, 'Connected')
def LCDCab2_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDCab2.SetState(1)
        reconnectWaitLCDCab2.Cancel()
    else:
        AInfoLCDCab2.SetState(0)
        print('Socket Disconnected: LCD Cab2')
    pass

@event(LCDCab3, 'Disconnected')
@event(LCDCab3, 'Connected')
def LCDCab3_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDCab3.SetState(1)
        reconnectWaitLCDCab3.Cancel()
    else:
        AInfoLCDCab3.SetState(0)
        print('Socket Disconnected: LCD Cab3')
    pass

@event(LCDCab4, 'Disconnected')
@event(LCDCab4, 'Connected')
def LCDCab4_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDCab4.SetState(1)
        reconnectWaitLCDCab4.Cancel()
    else:
        AInfoLCDCab4.SetState(0)
        print('Socket Disconnected: LCD Cab4')
    pass

@event(LCDLob1, 'Disconnected')
@event(LCDLob1, 'Connected')
def LCDLob1_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDLob1.SetState(1)
        reconnectWaitLCDLob1.Cancel()
    else:
        AInfoLCDLob1.SetState(0)
        print('Socket Disconnected: LCD Lob1')
    pass

@event(LCDLob2, 'Disconnected')
@event(LCDLob2, 'Connected')
def LCDLob2_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDLob2.SetState(1)
        reconnectWaitLCDLob2.Cancel()
    else:
        AInfoLCDLob2.SetState(0)
        print('Socket Disconnected: LCD Lob2')
    pass
@event(LCDPod1, 'Disconnected')
@event(LCDPod1, 'Connected')
def LCDPod1_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDPod1.SetState(1)
        reconnectWaitLCDPod1.Cancel()
    else:
        AInfoLCDPod1.SetState(0)
        print('Socket Disconnected: LCD Pod1')
    pass

@event(LCDPod2, 'Disconnected')
@event(LCDPod2, 'Connected')
def LCDPod2_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        AInfoLCDPod2.SetState(1)
        reconnectWaitLCDPod2.Cancel()
    else:
        AInfoLCDPod2.SetState(0)
        print('Socket Disconnected: LCD Pod2')
    pass

# DATA DICTIONARIES ------------------------------------------------------------
## Each dictionary store general information
## Room
Room_Data = {
    'Mixed' : None
}
## IP
Cisco1_Data = {
    'DTMF' : False,
    'Dial' : None,
}

Cisco2_Data = {
    'DTMF' : False,
    'Dial' : None,
}

# ACTIONS - INDEX PAGE MODE ----------------------------------------------------
@event(Index, 'Pressed')
def Index(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button.Host.DeviceAlias == 'TouchPanelA':
        TLP1.ShowPage('Main')
        print("Touch 1: {0}".format("Index"))
    else:
        TLP2.ShowPage('Main')
        print("Touch 2: {0}".format("Index"))
    pass

def FunctionMixRoom():
    """This prepare the room to be used in mode Mixed"""
    ## Store the data in dictionary
    Tesira.Set('LogicState', 'False', {'Instance Tag':'Room', 'Channel':'1'})
    Room_Data['Mixed'] = False
    #Tesira.Set('PresetRecall', '1')
    ## Activate button feedback
    ABtnRoom1.SetState(1)
    ABtnRoom2.SetState(0)
    ## Touchpanel actions
    TLP1.ShowPage('Main')
    ## Notify to console
    print("Touch 1: {0}".format("Room Split"))
    pass

def FunctionSplitRoom():
    ## Store the data in dictionary
    Tesira.Set('LogicState', 'True', {'Instance Tag':'Room', 'Channel':'1'})
    Room_Data['Mixed'] = True
    #Tesira.Set('PresetRecall', '2')
    ## Activate button feedback
    ABtnRoom1.SetState(1)
    ABtnRoom2.SetState(1)
    ## Touchpanel actions
    TLP2.ShowPage('Main')
    ## Notify to console
    print("Touch 1: {0}".format("Room Mixed"))
    pass

# ACTIONS - ROOM CONFIGURATION MODE --------------------------------------------
## Room Page
@event(ModeRoom, 'Pressed')
def Index(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    if button.Host.DeviceAlias == 'TouchPanelA':
        #Mutually Exclusive
        GroupRoom.SetCurrent(button)
        #
        if button is ARoomSplit:
            FunctionMixRoom()
        else:
            FunctionSplitRoom()
    pass

# ACTIONS - MAIN OPERATION MODE ------------------------------------------------
@event(Main, 'Pressed')
def FullMain(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button.Host.DeviceAlias == 'TouchPanelA':
        GroupMainA.SetCurrent(button)
        TLP1.HideAllPopups()
        #
        if button is ABtnRoom:
            TLP1.ShowPopup('Room')
            ALblMain.SetText('Configurar Sala')
            print("Touch 1: {0}".format("Mode Room"))
        #
        elif button is ABtnSwitch:
            ALblMain.SetText('Switcheo de Video')
            print("Touch 1: {0}".format("Mode Switching"))
            #
            if GroupRoom.GetCurrent() == ARoomMixed:
                TLP1.ShowPopup('Full.Outputs')
                TLP1.ShowPopup('Full.Inputs')
            else:
                TLP1.ShowPopup('Split.OutputsA')
                TLP1.ShowPopup('Full.Inputs')
        #
        elif button is ABtnDisplay:
            ALblMain.SetText('Control de Display')
            print("Touch 1: {0}".format("Mode Display"))
            #
            if GroupRoom.GetCurrent() == ARoomMixed:
                TLP1.ShowPopup('Full.Displays')
            else:
                TLP1.ShowPopup('Split.DisplaysA')
        #
        elif button is ABtnVC:
            TLP1.ShowPopup('Full.VC')
            Cisco1.Set('Standby', 'Deactivate')
            Cisco2.Set('Standby', 'Deactivate')
            ALblMain.SetText('Control de Videoconferencia')
            print("Touch 1: {0}".format("Mode VideoConferencia"))
        #
        elif button is ABtnREC:
            ALblMain.SetText('Control de Grabación')
            print("Touch 1: {0}".format("Mode REC"))
            #
            if GroupRoom.GetCurrent() == ARoomMixed:
                TLP1.ShowPopup('Full.Rec')
            else:
                TLP1.ShowPopup('Split.RecA')
        #
        elif button is ABtnInfo:
            TLP1.ShowPopup('Full.Info')
            ALblMain.SetText('Información de Dispositivos')
            print("Touch 1: {0}".format("Mode Info"))
        #
        elif button is ABtnPower:
            ALblMain.SetText('Apagar Sistema')
            print("Touch 1: {0}".format("Mode PowerAll"))
            #
            if GroupRoom.GetCurrent() == ARoomMixed:
                TLP1.ShowPopup('Split.PowerAB')
            else:
                TLP1.ShowPopup('Split.PowerA')
    pass

# ACTIONS - MATRIX TIE INFO FUNCTIONS ------------------------------------------
def FunctionActiveTie(output):
    '''This retrieve the real Output-Input Video Relation when the user push the Display button'''
    activeTie = XTP.ReadStatus('OutputTieStatus', {'Output':output, 'Tie Type':'Video'})
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

# ACTIONS - SWITCHING VIDEO OUTPUTS MODE ---------------------------------------
@event(Outputs, 'Pressed')
def OutsSwitching(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    ## Mutually Exclusive
    GroupOutputs.SetCurrent(button)
    global output
    
    ## Button Functions
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
    pass

# ACTIONS - SWITCHING VIDEO INPUTS MODE ----------------------------------------
@event(Inputs, 'Pressed')
def InSwitching(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    ## Data Init
    GroupInputs.SetCurrent(button)
    global output
    global input
    ## Button Functions
    if button.Host.DeviceAlias == 'TouchPanelA':
        # XTP Slot 1-----------------------------------------------------
        if button is AInput1:
            input = '1'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: Placa Left"))
        #
        elif button is AInput2:
            input = '2'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: Placa Right"))
        #
        elif button is AInput3:
            input = '3'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: Placa Stage"))
        #
        elif button is AInput4:
            input = '4'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: Placa Back"))

        # XTP Slot 2-----------------------------------------------------
        elif button is AInput5:
            input = '5'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: Placa Left"))
        #
        elif button is AInput6:
            input = '6'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: Placa Right"))
        #
        elif button is AInput7:
            input = '7'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: Placa Stage"))
        #
        elif button is AInput8:
            input = '8'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: Placa Back"))
            
        # XTP Slot 3-----------------------------------------------------
        elif button is AInput9:
            input = '9'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: PTZ Frontal"))
        #
        elif button is AInput10:
            input = '10'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: PTZ Back"))
        #
        elif button is AInput11:
            input = '11'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: PTZ Frontal"))
        #
        elif button is AInput12:
            input = '12'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: PTZ Back"))
            
        # XTP Slot 4-----------------------------------------------------
        elif button is AInput13:
            input = '13'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 1: PC Cabina"))
        #
        elif button is AInput14:
            input = '14'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Room 2: PC Cabina"))
            
        # XTP Slot 5-----------------------------------------------------
        elif button is AInput17:
            input = '17'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Core: Cisco 1 Out"))
        #
        elif button is AInput18:
            input = '18'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Core: Cisco 2 Out"))
        #
        elif button is AInput19:
            input = '19'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Core: ShareLink 1"))
        #
        elif button is AInput20:
            input = '20'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Core: ShareLink 2"))
            
        # XTP Slot 6-----------------------------------------------------
        elif button is AInput21:
            input = '21'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Core: Tricaster 1 Out"))
        #
        elif button is AInput22:
            input = '22'
            XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
            print("Touch 1: {0}".format("In Core: Tricaster 2 Out"))
    pass

# ACTIONS - RELAYS FUNCTIONS ---------------------------------------------------
def Room1ScreenUp():
    """Control of Relays"""
    AScreenDw.SetState('Open')
    #AScreenUp.SetState('Close')
    AScreenUp.Pulse(20)
    pass

def Room1ScreenDown():
    """Control of Relays"""
    AScreenUp.SetState('Open')
    #AScreenDw.SetState('Close')
    AScreenDw.Pulse(20)
    pass

def Room1ElevatorUp():
    """Control of Relays"""
    AElevatDw.SetState('Open')
    AElevatUp.SetState('Close')
    pass

def Room1ElevatorDown():
    """Control of Relays"""
    AElevatUp.SetState('Open')
    AElevatDw.SetState('Close')
    pass

def Room2ScreenUp():
    """Control of Relays"""
    A2ScreenDw.SetState('Open')
    #A2ScreenUp.SetState('Close')
    A2ScreenUp.Pulse(20)
    pass

def Room2ScreenDown():
    """Control of Relays"""
    A2ScreenUp.SetState('Open')
    #A2ScreenDw.SetState('Close')
    A2ScreenDw.Pulse(20)
    pass

def Room2ElevatorUp():
    """Control of Relays"""
    A2ElevatDw.SetState('Open')
    A2ElevatUp.SetState('Close')
    pass

def Room2ElevatorDown():
    """Control of Relays"""
    A2ElevatUp.SetState('Open')
    A2ElevatDw.SetState('Close')
    pass

# ACTIONS - DISPLAYS A MODE ----------------------------------------------------
@event(ProjeccionA, 'Pressed')
def ButtonObjectPressed(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is AProjAPwr:
        if ProjA.ReadStatus('Power',None) == 'On':
            print("Touch 1: {0}".format("Proyector 1: PowerOff"))
            AProjAPwr.SetState(0)
            ProjA.Set('Power','Off')
            Room1ElevatorUp()
            Room1ScreenUp()
        else:
            print("Touch 1: {0}".format("Proyector 1: PowerOn"))
            AProjAPwr.SetState(1)
            ProjA.Set('Power','On')
            Room1ElevatorDown()
            Room1ScreenDown()
    #
    elif button is AScUp:
        GroupScreenA.SetCurrent(AScUp)
        Room1ScreenUp()
        print("Touch 1: {0}".format("Screen 1: Up"))
    #
    elif button is AScDw:
        GroupScreenA.SetCurrent(AScDw)
        Room1ScreenDown()
        print("Touch 1: {0}".format("Screen 1: Down"))
    #
    elif button is AElUp:
        GroupElevatA.SetCurrent(AElUp)
        Room1ElevatorUp()
        print("Touch 1: {0}".format("Elevator 1: Up"))
    #
    elif button is AElDw:
        GroupElevatA.SetCurrent(AElDw)
        Room1ElevatorDown()
        print("Touch 1: {0}".format("Elevator 1: Down"))
    #
    elif button is ALCDCab1:
        if LCDCab3.ReadStatus('Power', None) == 'On':
            ALCDCab1.SetState(0)
            LCDCab3.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 3 Power Off"))
        else:
            ALCDCab1.SetState(1)
            LCDCab3.Set('Power','On')
            print("Touch 1: {0}".format("LCD 3 Power On"))
    #
    elif button is ALCDCab2:
        if LCDCab4.ReadStatus('Power', None) == 'On':
            ALCDCab2.SetState(0)
            LCDCab4.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 4 Power Off"))
        else:
            ALCDCab2.SetState(1)
            LCDCab4.Set('Power','On')
            print("Touch 1: {0}".format("LCD Cab4 Power On"))
    #
    elif button is ALCDLobby:
        if LCDLob1.ReadStatus('Power', None) == 'On':
            ALCDLobby.SetState(0)
            LCDLob1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD Lob1 Power Off"))
        else:
            ALCDLobby.SetState(1)
            LCDLob1.Set('Power','On')
            print("Touch 1: {0}".format("LCD Lob1 Power On"))
    #
    elif button is ALCDPodium1:
        if LCDPod1.ReadStatus('Power', None) == 'On':
            ALCDPodium1.SetState(0)
            LCDPod1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD P1 Power Off"))
        else:
            ALCDPodium1.SetState(1)
            LCDPod1.Set('Power','On')
            print("Touch 1: {0}".format("LCD P1 Power On"))
    #
    elif button is ALCDCab3:
        Monitor1.PlayContinuous('POWER')
        Monitor1.Stop()
        print("Touch 1: {0}".format("Monitor Cab1 Power IR"))
    pass

# ACTIONS - DISPLAYS B MODE ----------------------------------------------------
@event(ProjeccionB, 'Pressed')
def ButtonObjectPressed(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is AProjBPwr:
        if ProjB.ReadStatus('Power',None) == 'On':
            print("Touch 1: {0}".format("Proyector 2: PowerOff"))
            AProjBPwr.SetState(0)
            ProjB.Set('Power','Off')
            Room2ElevatorUp()
            Room2ScreenUp()
        else:
            print("Touch 1: {0}".format("Proyector 2: PowerOn"))
            AProjBPwr.SetState(1)
            ProjB.Set('Power','On')
            Room2ElevatorDown()
            Room2ScreenDown()
    #
    elif button is A2ScUp:
        GroupScreen2A.SetCurrent(A2ScUp)
        Room2ScreenUp()
        print("Touch 1: {0}".format("Screen 2: Up"))
    #
    elif button is A2ScDw:
        GroupScreen2A.SetCurrent(A2ScDw)
        Room2ScreenDown()
        print("Touch 1: {0}".format("Screen 2: Down"))
    #
    elif button is A2ElUp:
        GroupElevat2A.SetCurrent(A2ElUp)
        Room2ElevatorUp()
        print("Touch 1: {0}".format("Elevator 2: Up"))
    #
    elif button is A2ElDw:
        GroupElevat2A.SetCurrent(A2ElDw)
        Room2ElevatorDown()
        print("Touch 1: {0}".format("Elevator 2: Down"))
    #
    elif button is A2LCDCab2:
        if LCDCab1.ReadStatus('Power', None) == 'On':
            A2LCDCab2.SetState(0)
            LCDCab1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 1 Power Off"))
        else:
            A2LCDCab2.SetState(1)
            LCDCab1.Set('Power','On')
            print("Touch 1: {0}".format("LCD 1 Power On"))
    #
    elif button is A2LCDCab3:
        if LCDCab2.ReadStatus('Power', None) == 'On':
            A2LCDCab3.SetState(0)
            LCDCab2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 2 Power Off"))
        else:
            A2LCDCab3.SetState(1)
            LCDCab2.Set('Power','On')
            print("Touch 1: {0}".format("LCD 2 Power On"))
    #
    elif button is A2LCDLobby:
        if LCDLob2.ReadStatus('Power', None) == 'On':
            A2LCDLobby.SetState(0)
            LCDLob2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD L2 Power Off"))
        else:
            A2LCDLobby.SetState(1)
            LCDLob2.Set('Power','On')
            print("Touch 1: {0}".format("LCD L2 Power On"))
    #
    elif button is ALCDPodium2:
        if LCDPod2.ReadStatus('Power', None) == 'On':
            ALCDPodium2.SetState(0)
            LCDPod2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD P2 Power Off"))
        else:
            ALCDPodium2.SetState(1)
            LCDPod2.Set('Power','On')
            print("Touch 1: {0}".format("LCD P2 Power On"))
    #
    elif button is A2LCDCab1:
        Monitor2.PlayContinuous('POWER')
        Monitor2.Stop()
        print("Touch 1: {0}".format("Monitor Cab2 Power IR"))
    pass

# ACTIONS - RECORDING MODE -----------------------------------------------------
@event(Rec, 'Pressed')
def ButtonObjectPressed(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is Arecord:
        RecA.Set('Record','Start')
        print("Touch 1: {0}".format("SMP11-A: Rec"))
    #
    elif button is Astop:
        RecA.Set('Record','Stop')
        print("Touch 1: {0}".format("SMP11-A: Stop"))
    #
    elif button is Apause:
        RecA.Set('Record','Pause')
        print("Touch 1: {0}".format("SMP11-A: Pause"))
    #
    elif button is A2record:
        RecB.Set('Record','Start')
        print("Touch 1: {0}".format("SMP11-B: Rec"))
    #
    elif button is A2stop:
        RecB.Set('Record','Stop')
        print("Touch 1: {0}".format("SMP11-B: Stop"))
    #
    elif button is A2pause:
        RecB.Set('Record','Pause')
        print("Touch 1: {0}".format("SMP11-B: Pause"))
    pass

# ACTIONS - CISCO 1 MODE -----------------------------------------------------
## This function add or remove data from the panel Dial Number
def PrintDialerVC1(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVC

    if btn_name == 'Delete':           #If the user push 'Delete' button
        dialerVC = dialerVC[:-1]       #Remove the last char of the string
        Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        AVCDial.SetText(dialerVC)      #Send the string to GUI Label
    else:                            #If the user push a [*#0-9] button
        number = str(btn_name[4])    #Extract the valid character of BTN name
        if Cisco1_Data['DTMF'] == True:
            if number == '.':
                Cisco1.Set('DTMF', '*')
            else:
                Cisco1.Set('DTMF', number)
        else:
            dialerVC += number           #Append the last char to the string
            Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
            AVCDial.SetText(dialerVC)  #Send the string to GUI Label
    pass

## This function is called when the user press a Dial Button
@event(VCDial, ButtonEventList)
def vi_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VC Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Touch: VC %s' % (button.Name))
        PrintDialerVC1(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(VCButtons, 'Pressed')
def VC_Mode(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is ACall:
        if Cisco1.ReadStatus('CallStatus', {'Call':'1'}) == 'Connected':
            Cisco1.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
            AVCDial.SetText('')
            dialerVC = ''
            print("Touch 1: {0}".format("Cisco1: Hangup"))
        else:
            Cisco1.Set('Hook', 'Dial', {'Number':Cisco1_Data['Dial'], 'Protocol':'H323'})
            print("Touch 1: {0}".format("Cisco1: Call"))
    #
    elif button is ADTMF:
        if Cisco1_Data['DTMF'] == False:
            Cisco1_Data['DTMF'] = True
            ADialDot.SetText('*')
            ADTMF.SetState(1)
            print("Touch 1: {0}".format("Cisco1: DTMF On"))
        else:
            Cisco1_Data['DTMF'] = False
            ADialDot.SetText('?')
            ADTMF.SetState(0)
            print("Touch 1: {0}".format("Cisco1: DTMF Off"))
    #
    elif button is AContentOn:
        GroupContentA.SetCurrent(AContentOn)
        Cisco1.Set('Presentation', '2', {'Instance': '1'})
        print("Touch 1: {0}".format("Cisco1: Content On"))
    #
    elif button is AContentOff:
        GroupContentA.SetCurrent(AContentOff)
        Cisco1.Set('Presentation', 'Stop', {'Instance': '1'})
        print("Touch 1: {0}".format("Cisco1: Content Off"))
    #
    elif button is AAnswer1:
        TLP1.HidePopup('Cisco1.Call')
        Cisco1.Set('Hook', 'Accept', {'Number':'','Protocol': 'H323'})
        print("Touch 1: {0}".format("Cisco1: Answer"))
    #
    elif button is ADiscard1:
        TLP1.HidePopup('Cisco1.Call')
        Cisco1.Set('Hook', 'Reject', {'Number':'','Protocol': 'H323'})
        print("Touch 1: {0}".format("Cisco1: Reject"))
    pass

# ACTIONS - CISCO 2 MODE -----------------------------------------------------

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def PrintDialerVC2(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVC2

    if btn_name == 'Delete':         #If the user push 'Delete' button
        dialerVC2 = dialerVC2[:-1]     #Remove the last char of the string
        Cisco2_Data['Dial'] = dialerVC2 #Asign the string to the data dictionary
        A2VCDial.SetText(dialerVC2)  #Send the string to GUI Label

    else:                            #If the user push a [*#0-9] button
        number = str(btn_name[4])    #Extract the valid character of BTN name
        if Cisco2_Data['DTMF'] == True:
            if number == '.':
                Cisco2.Set('DTMF', '*')
            else:
                Cisco2.Set('DTMF', number)
        else:
            dialerVC2 += number           #Append the last char to the string
            Cisco2_Data['Dial'] = dialerVC2 #Asign the string to the data dictionary
            A2VCDial.SetText(dialerVC2)  #Send the string to GUI Label
    pass

@event(VC2Dial, ButtonEventList)
def VC2_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VC Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Touch: VC %s' % (button.Name))
        PrintDialerVC2(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(VC2Buttons, 'Pressed')
def VC_Mode(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is A2Call:
        if Cisco2.ReadStatus('CallStatus', {'Call':'1'}) == 'Connected':
            Cisco2.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
            A2VCDial.SetText('')
            dialerVC2 = ''
            print("Touch 1: {0}".format("Cisco2: Hangup"))
        else:
            Cisco2.Set('Hook', 'Dial', {'Number':Cisco2_Data['Dial'], 'Protocol':'H323'})
            print("Touch 1: {0}".format("Cisco2: Call"))
    #
    elif button is A2DTMF:
        if Cisco2_Data['DTMF'] == False:
            Cisco2_Data['DTMF'] = True
            A2DialDot.SetText('*')
            A2DTMF.SetState(1)
            print("Touch 1: {0}".format("Cisco2: DTMF On"))
        else:
            Cisco2_Data['DTMF'] = False
            A2DialDot.SetText('?')
            A2DTMF.SetState(0)
            print("Touch 1: {0}".format("Cisco2: DTMF Off"))
    #
    elif button is A2ContentOn:
        GroupContentB.SetCurrent(A2ContentOn)
        Cisco2.Set('Presentation', '2', {'Instance': '1'})
        print("Touch 1: {0}".format("Cisco2: Content On"))
    #
    elif button is A2ContentOff:
        GroupContentB.SetCurrent(A2ContentOff)
        Cisco2.Set('Presentation', 'Stop', {'Instance': '1'})
        print("Touch 1: {0}".format("Cisco2: Content Off"))
    #
    elif button is AAnswer2:
        TLP1.HidePopup('Cisco2.Call')
        Cisco2.Set('Hook', 'Accept', {'Number':'','Protocol': 'H323'})
        print("Touch 1: {0}".format("Cisco2: Answer"))
    #
    elif button is ADiscard2:
        TLP1.HidePopup('Cisco2.Call')
        Cisco2.Set('Hook', 'Reject', {'Number':'','Protocol': 'H323'})
        print("Touch 1: {0}".format("Cisco2: Reject"))
    pass


# ACTIONS - POWER MODE ---------------------------------------------------------
def PowerOffRoomA():
    """This Shutdown all controllable devices of Room A"""
    # Projection A
    ProjA.Set('Power','Off')
    Room1ElevatorUp()
    Room1ScreenUp()
    # Monitors
    LCDCab3.Set('Power','Off')
    LCDCab4.Set('Power','Off')
    LCDLob1.Set('Power','Off')
    LCDPod1.Set('Power','Off')
    Monitor1.PlayContinuous('POWER')
    Monitor1.Stop()
    # VC Content Off
    Cisco1.Set('Presentation', 'Stop', {'Instance': '1'})
    # Recorder Stop
    RecA.Set('Record','Stop')
    # VC - VoIP Calls Hangup
    Cisco1.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
    AVCDial.SetText('')
    dialerVC = ''
    # VC Standby
    Cisco1.Set('Standby', 'Activate')
    # TouchPanel Actions
    TLP1.ShowPage('Index')
    pass

def PowerOffRoomB():
    """This Shutdown all controllable devices of Room B"""
    # Projection B
    ProjB.Set('Power','Off')
    Room2ElevatorUp()
    Room2ScreenUp()
    # Monitors
    LCDCab1.Set('Power','Off')
    LCDCab2.Set('Power','Off')
    LCDLob2.Set('Power','Off')
    LCDPod2.Set('Power','Off')
    Monitor2.PlayContinuous('POWER')
    Monitor2.Stop()
    # VC Content Off
    Cisco2.Set('Presentation', 'Stop', {'Instance': '1'})
    # Recorder Stop
    RecB.Set('Record','Stop')
    # VC - VoIP Calls Hangup
    Cisco2.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
    A2VCDial.SetText('')
    dialerVC2 = ''
    # VC Standby
    Cisco2.Set('Standby', 'Activate')
    # TouchPanel Actions
    TLP2.ShowPage('Index')
    pass

def PowerOffRoomAB():
    """This Shutdown all controllable devices of Room B"""
    # Projection A
    ProjA.Set('Power','Off')
    ProjB.Set('Power','Off')
    Room1ElevatorUp()
    Room2ElevatorUp()
    Room1ScreenUp()
    Room2ScreenUp()
    # Monitors
    LCDCab3.Set('Power','Off')
    LCDCab4.Set('Power','Off')
    LCDLob1.Set('Power','Off')
    LCDPod1.Set('Power','Off')
    Monitor1.PlayContinuous('POWER')
    Monitor1.Stop()
    #
    LCDCab1.Set('Power','Off')
    LCDCab2.Set('Power','Off')
    LCDLob2.Set('Power','Off')
    LCDPod2.Set('Power','Off')
    Monitor2.PlayContinuous('POWER')
    Monitor2.Stop()
    # VC Content Off
    Cisco1.Set('Presentation', 'Stop', {'Instance': '1'})
    Cisco2.Set('Presentation', 'Stop', {'Instance': '1'})
    # Recorder Stop
    RecA.Set('Record','Stop')
    RecB.Set('Record','Stop')
    # VC - VoIP Calls Hangup
    Cisco1.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
    Cisco2.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
    AVCDial.SetText('')
    A2VCDial.SetText('')
    dialerVC = ''
    dialerVC2 = ''
    # VC Standby
    Cisco1.Set('Standby', 'Activate')
    Cisco2.Set('Standby', 'Activate')
    # TouchPanel Actions
    TLP1.ShowPage('Index')
    TLP2.ShowPage('Index')
    pass

@event(GroupPower, 'Pressed')
def PowerOff_Mode(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is ABtnPowerA:
        PowerOffRoomA()
        print("Touch 1: {0}".format("PowerOff: Sala A"))
    elif button is ABtnPowerB:
        #PowerOffRoomB()
        print("Touch 1: {0}".format("PowerOff: Sala B"))
    elif button is ABtnPowerAB:
        #PowerOffRoomAB()
        print("Touch 1: {0}".format("PowerOff: Sala A-B"))
    pass
## End Events Definitions-------------------------------------------------------

Initialize()