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

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPCP550')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')
## Begin User Import -----------------------------------------------------------
# MODULES-----------------------------------------------------------------------
## IP
import extr_matrix_XTPIICrossPointSeries_v1_1_1_1 as ModuleXTP
import chri_vp_D13HDHS_D13WUHS_v1_0_2_0           as ModuleChristie
import extr_sm_SMP_111_v1_1_0_0                   as ModuleSMP111
import smsg_display_LHxxQMFPLGCKR_Series_v1_0_0_0 as ModuleSamsung
import biam_dsp_TesiraSeries_v1_5_20_0            as ModuleTesira
import sony_camera_BRC_H800_X1000_v1_0_0_0        as ModulePTZ
import csco_vtc_SX_Series_CE81_v1_2_0_1           as ModuleCisco

##
# MODULE TO DEVICE INSTANCES ---------------------------------------------------
# Video Server
XTP   = ModuleXTP.EthernetClass('192.168.0.10', 23, Model='XTP II CrossPoint 3200')
# Projectors
ProjA = ModuleChristie.EthernetClass('192.168.0.19', 3002, Model='D13WU-HS')
ProjB = ModuleChristie.EthernetClass('192.168.0.18', 3002, Model='D13WU-HS')
# Recorders
RecA  = ModuleSMP111.EthernetClass('192.168.0.13', 23, Model='SMP 111')
RecB  = ModuleSMP111.EthernetClass('192.168.0.14', 23, Model='SMP 111')
# Displays
LCD1  = ModuleSamsung.EthernetClass('192.168.0.26', 1515, Model='LH55QMFPLGC/KR')
LCD2  = ModuleSamsung.EthernetClass('192.168.0.27', 1515, Model='LH55QMFPLGC/KR')
LCD3  = ModuleSamsung.EthernetClass('192.168.0.28', 1515, Model='LH55QMFPLGC/KR')
LCD4  = ModuleSamsung.EthernetClass('192.168.0.29', 1515, Model='LH55QMFPLGC/KR')
LCDP1 = ModuleSamsung.EthernetClass('192.168.0.30', 1515, Model='LH55QMFPLGC/KR')
LCDP2 = ModuleSamsung.EthernetClass('192.168.0.31', 1515, Model='LH55QMFPLGC/KR')
LCDL1 = ModuleSamsung.EthernetClass('192.168.0.32', 1515, Model='LH55QMFPLGC/KR')
LCDL2 = ModuleSamsung.EthernetClass('192.168.0.33', 1515, Model='LH55QMFPLGC/KR')
# Audio Server
Tesira = ModuleTesira.EthernetClass('192.168.0.38', 23, Model='Tesira SERVER-IO')
# Cameras
PTZ1 = ModulePTZ.EthernetClass('192.168.0.20', 52381, ServicePort=52381, Model='BRC-H800') ##UDP
# Videoconference Códec´s
Cisco1 = ModuleCisco.EthernetClass('192.168.0.60', 23, Model='SX20 CE8.1.X')
Cisco2 = ModuleCisco.EthernetClass('192.168.0.61', 23, Model='SX20 CE8.1.X')

# DEVICES INTERFACES -----------------------------------------------------------
#
# 12v Power Interface
SWPowerPort1 = SWPowerInterface(IPCP, 'SPI1')
SWPowerPort2 = SWPowerInterface(IPCP, 'SPI2')
SWPowerPort3 = SWPowerInterface(IPCP, 'SPI3')
SWPowerPort4 = SWPowerInterface(IPCP, 'SPI4')
#
# Relay
AScreenUp = RelayInterface(IPCP, 'RLY3')
AScreenDw = RelayInterface(IPCP, 'RLY4')
AElevatUp = RelayInterface(IPCP, 'RLY7')
AElevatDw = RelayInterface(IPCP, 'RLY8')
A2ScreenUp = RelayInterface(IPCP, 'RLY1')
A2ScreenDw = RelayInterface(IPCP, 'RLY2')
A2ElevatUp = RelayInterface(IPCP, 'RLY5')
A2ElevatDw = RelayInterface(IPCP, 'RLY6')
##
## End User Import -------------------------------------------------------------

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
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
ABtnAudio   = Button(TLP1, 14)
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

# Mode Status ------------------------------------------------------------------
# Projector A
ALANProjA    = Label(TLP1, 2512)
AInfoProjA   = Label(TLP1, 2513)

# Projector B
ALANProjB    = Label(TLP1, 2500)
AInfoProjB   = Label(TLP1, 2501)

# Recorder A
ALANRecA     = Label(TLP1, 2515)
AinfoRecA    = Label(TLP1, 2516)

# Recorder B
ALANRecB     = Label(TLP1, 2503)
AinfoRecB    = Label(TLP1, 2504)

# Displays A
ALCDInfoPod1 = Label(TLP1, 2520)
ALCDInfoCab3 = Label(TLP1, 2521)
ALCDInfoCab4 = Label(TLP1, 2522)
ALCDInfoLob1 = Label(TLP1, 2523)

# Displays B
ALCDInfoPod2 = Label(TLP1, 2508)
ALCDInfoCab1 = Label(TLP1, 2509)
ALCDInfoCab2 = Label(TLP1, 2510)
ALCDInfoLob2 = Label(TLP1, 2511)

# XTP II 3200
ALANXtp      = Label(TLP1, 2524)

# Mode Audio VoIP ----------------------------------------------------------------------
# Line 1 ---------------------
AViDial0      = Button(TLP1, 2030)
AViDial1      = Button(TLP1, 2031)
AViDial2      = Button(TLP1, 2032)
AViDial3      = Button(TLP1, 2033)
AViDial4      = Button(TLP1, 2034)
AViDial5      = Button(TLP1, 2035)
AViDial6      = Button(TLP1, 2036)
AViDial7      = Button(TLP1, 2037)
AViDial8      = Button(TLP1, 2038)
AViDial9      = Button(TLP1, 2039)
AViDialDot    = Button(TLP1, 2040)
AViDialHash   = Button(TLP1, 2041)
AViDialDelete = Button(TLP1, 2044, repeatTime=0.1)
# Dialer

# Call
AViHangup     = Button(TLP1, 2042)
AViCall       = Button(TLP1, 2043)

# Call Options
AViRedial  = Button(TLP1, 2045)
AViDTMF = Button(TLP1, 2046)

# Label
AViDial     = Label(TLP1, 2047)
AViRemote   = Label(TLP1, 2048)

# Mode Audio VoIP ----------------------------------------------------------------------
# Line 2 ---------------------
AVi2Dial0      = Button(TLP1, 2000)
AVi2Dial1      = Button(TLP1, 2001)
AVi2Dial2      = Button(TLP1, 2002)
AVi2Dial3      = Button(TLP1, 2003)
AVi2Dial4      = Button(TLP1, 2004)
AVi2Dial5      = Button(TLP1, 2005)
AVi2Dial6      = Button(TLP1, 2006)
AVi2Dial7      = Button(TLP1, 2007)
AVi2Dial8      = Button(TLP1, 2008)
AVi2Dial9      = Button(TLP1, 2009)
AVi2DialDot    = Button(TLP1, 2010)
AVi2DialHash   = Button(TLP1, 2011)
AVi2DialDelete = Button(TLP1, 2014, repeatTime=0.1)
# Dialer

# Call
AVi2Hangup     = Button(TLP1, 2012)
AVi2Call       = Button(TLP1, 2013)

# Call Options
AVi2Redial  = Button(TLP1, 2015)
AVi2DTMF = Button(TLP1, 2016)

# Label
AVi2Dial     = Label(TLP1, 2017)
AVi2Remote   = Label(TLP1, 2018)


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
AHangup     = Button(TLP1, 2142)
ACall       = Button(TLP1, 2143)

# Content
AContentOn  = Button(TLP1, 2145)
AContentOff = Button(TLP1, 2146)

# Label
AVCDial     = Label(TLP1, 2147)
AVCRemote   = Label(TLP1, 2148)

# Cisco 2 ---------------------
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
A2Hangup     = Button(TLP1, 2112)
A2Call       = Button(TLP1, 2113)

# Content
A2ContentOn  = Button(TLP1, 2115)
A2ContentOff = Button(TLP1, 2116)

# Label
A2VCDial     = Label(TLP1, 2117)
A2VCRemote   = Label(TLP1, 2118)


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
Main  = [ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC, ABtnAudio, ABtnREC,
         ABtnVoIP, ABtnInfo, ABtnPower,
         BBtnRoom, BBtnSwitch, BBtnDisplay, BBtnVC, BBtnAudio, BBtnREC,
         BBtnVoIP, BBtnInfo, BBtnPower]
#
GroupMainA = MESet([ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC, ABtnAudio,
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

# Mode Audio VoIP
VoIPDial = [AViDial0, AViDial1, AViDial2, AViDial3, AViDial4, AViDial5, AViDial6, AViDial7, AViDial8, AViDial9, AViDialDot, AViDialHash, AViDialDelete]
VoIPButtons = [AViCall, AViHangup, AViRedial, AViDTMF]
#
VoIP2Dial = [AVi2Dial0, AVi2Dial1, AVi2Dial2, AVi2Dial3, AVi2Dial4, AVi2Dial5, AVi2Dial6, AVi2Dial7, AVi2Dial8, AVi2Dial9, AVi2DialDot, AVi2DialHash, AVi2DialDelete]
VoIP2Buttons = [AVi2Call, AVi2Hangup, AVi2Redial, AVi2DTMF]

# Mode Videoconference
VCDial = [ADial0, ADial1, ADial2, ADial3, ADial4, ADial5, ADial6, ADial7, ADial8, ADial9, ADialDot, ADialHash, ADialDelete]
VCButtons = [ACall, AHangup, AContentOn, AContentOff]
#
VC2Dial = [A2Dial0, A2Dial1, A2Dial2, A2Dial3, A2Dial4, A2Dial5, A2Dial6, A2Dial7, A2Dial8, A2Dial9, A2DialDot, A2DialHash, A2DialDelete]
VC2Buttons = [A2Call, A2Hangup, A2ContentOn, A2ContentOff]

# Button State List
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------

def Initialize():
    """This is the last function that loads when starting the system"""
    ## Open Sockets
    ## IP
    XTP.Connect()
    ##ProjA.Connect()
    ##ProjB.Connect()
    RecA.Connect(timeout=5)
    ##RecB.Connect()
    ##LCD1.Connect()
    ##LCD2.Connect()
    ##LCD3.Connect()
    ##LCD4.Connect()
    ##LCDL1.Connect()
    ##LCDL2.Connect()
    ##LCDP1.Connect()
    ##LCDP2.Connect()
    ##Tesira.Connect()
    ##PTZ1.Connect()
    ##Cisco1.Connect()
    ##Cisco2.Connect()

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

    ## Audio VoIP1 Dial PAGE
    global dialerVoIP  ## To access the Dial String variable in all program
    dialerVoIP = ''    ## Clean the Dial String Variable
    AViDial.SetText('')

    ## Audio VoIP2 Dial PAGE
    global dialerVoIP2  ## To access the Dial String variable in all program
    dialerVoIP2 = ''    ## Clean the Dial String Variable
    AVi2Dial.SetText('')

    ##12v Interface (This brings power to all Relays)
    SWPowerPort1.SetState('On')
    SWPowerPort2.SetState('On')
    SWPowerPort3.SetState('On')
    SWPowerPort4.SetState('On')
    pass

# SUBSCRIBE FUNCTIONS ----------------------------------------------------------
def subscribe_matrix():
    """This send Subscribe Commands to Device"""
    ## Socket Status
    XTP.SubscribeStatus('ConnectionStatus', None, XTP_parsing)
    ## Input Signal Status
    XTP.SubscribeStatus('InputSignal', {'Input':'1'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'2'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'3'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'4'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'5'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'6'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'7'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'8'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'9'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'10'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'11'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'12'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'13'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'14'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'15'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'16'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'17'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'18'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'19'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'20'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'21'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'22'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'23'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'24'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'25'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'26'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'27'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'28'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'29'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'30'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'31'}, XTP_parsing)
    XTP.SubscribeStatus('InputSignal', {'Input':'32'}, XTP_parsing)
    ## Output Signal Status
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'5', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'6', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'7', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'8', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'9', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'10', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'11', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'12', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'13', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'14', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'15', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'16', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'17', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'18', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'19', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'20', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'21', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'22', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'23', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'24', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'25', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'26', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'27', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'28', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'29', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'30', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'31', 'Tie Type':'Video'}, XTP_parsing)
    XTP.SubscribeStatus('OutputTieStatus', {'Output':'32', 'Tie Type':'Video'}, XTP_parsing)
    pass



# UPDATE FUNCTIONS -------------------------------------------------------------
def update_matrix():
    """This send Update Commands to Device"""
    XTP.Update('InputSignal',{'Input':'1'})
    XTP.Update('InputSignal',{'Input':'2'})
    XTP.Update('InputSignal',{'Input':'3'})
    XTP.Update('InputSignal',{'Input':'4'})
    XTP.Update('InputSignal',{'Input':'5'})
    XTP.Update('InputSignal',{'Input':'6'})
    XTP.Update('InputSignal',{'Input':'7'})
    XTP.Update('InputSignal',{'Input':'8'})
    XTP.Update('InputSignal',{'Input':'9'})
    XTP.Update('InputSignal',{'Input':'10'})
    XTP.Update('InputSignal',{'Input':'11'})
    XTP.Update('InputSignal',{'Input':'12'})
    XTP.Update('InputSignal',{'Input':'13'})
    XTP.Update('InputSignal',{'Input':'14'})
    XTP.Update('InputSignal',{'Input':'15'})
    XTP.Update('InputSignal',{'Input':'16'})
    XTP.Update('InputSignal',{'Input':'17'})
    XTP.Update('InputSignal',{'Input':'18'})
    XTP.Update('InputSignal',{'Input':'19'})
    XTP.Update('InputSignal',{'Input':'20'})
    XTP.Update('InputSignal',{'Input':'21'})
    XTP.Update('InputSignal',{'Input':'22'})
    XTP.Update('InputSignal',{'Input':'23'})
    XTP.Update('InputSignal',{'Input':'24'})
    XTP.Update('InputSignal',{'Input':'25'})
    XTP.Update('InputSignal',{'Input':'27'})
    XTP.Update('InputSignal',{'Input':'28'})
    XTP.Update('InputSignal',{'Input':'29'})
    XTP.Update('InputSignal',{'Input':'30'})
    XTP.Update('InputSignal',{'Input':'31'})
    XTP.Update('InputSignal',{'Input':'32'})
    pass

# Module and Physical Handle Connections ---------------------------------------

# RECONEX / QUERY LIST ---------------------------------------------------------
SMP111_A_QUERY_LIST = [
    ('Record', None),
    ('RecordDestination', None),
    ('RecordingMode', None),
    ('VideoResolution', {'Stream':'Record'}),
    ('HDCPStatus', None),
    ('RemainingFreeDiskSpace',{'Drive':'Primary'}),
    ('RemainingFreeDiskSpace',{'Drive':'Secondary'}),
    ('CurrentRecordingDuration', None),
]
#
SMP111_A_Queue = collections.deque(SMP111_A_QUERY_LIST)

# RECONEX / QUERY RECALL ------------------------------------------------------
def QuerySMP111_A():
    """This send Query commands to device every 03.s"""
    RecA.Update(*SMP111_A_Queue[0])
    SMP111_A_Queue.rotate(-1)
    SMP111_A_PollingWait.Restart()

SMP111_A_PollingWait = Wait(0.5, QuerySMP111_A)

# RECONEX / TCP CONNECTIONS HANDLING ------------------------------------------
def AttemptConnectSMP111_A():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect the SMP111.A')
    result = RecA.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitSMP111_A.Restart()

reconnectWaitSMP111_A = Wait(15, AttemptConnectSMP111_A)

def ReceiveSMP111_A(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    if command == 'ConnectionStatus':
        print('Module SMP111.A: ' + value)
        #
        if value == 'Disconnected':
            ## Recall the Re-Connection Routines
            RecA.Disconnect()
            reconnectWaitSMP111_A.Restart()
        else:
            ALCDInfoCab1.SetText('Online')
    #
    elif command == 'Record':
        print('--- Parsing Recorder A: ' + command + ' ' + value)
        AinfoRecA.SetText(value)
        if value == 'Start':
            GroupRecA.SetCurrent(Arecord)
        elif value == 'Pause':
            GroupRecA.SetCurrent(Apause)
        elif value == 'Stop':
            GroupRecA.SetCurrent(Astop)
    #
    elif command == 'RecordDestination':
        ARecDestine.SetText(value)
        print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'RecordingMode':
        ARecMode.SetText(value)
        print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'VideoResolution':
        ARecResolut.SetText(value)
        print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'HDCPStatus':
        ARecHDCP.SetText(value)
        print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'RemainingFreeDiskSpace':
        if qualifier['Drive'] == 'Primary':
            value = int(value / 1024)
            ARecDisk.SetText('Disk Free: ' + str(value) + 'GB')
            print('--- Parsing Recorder A: ' + command + ' ' + str(value))
    #
    elif command == 'CurrentRecordingDuration':
        print('--- Parsing Recorder A: ' + command + ' ' + value)
        Atime.SetText(value)
    pass

RecA.SubscribeStatus('ConnectionStatus', None, ReceiveSMP111_A)
RecA.SubscribeStatus('Record', None, ReceiveSMP111_A)
RecA.SubscribeStatus('RecordDestination', None, ReceiveSMP111_A)
RecA.SubscribeStatus('RecordingMode', None, ReceiveSMP111_A)
RecA.SubscribeStatus('HDCPStatus', None, ReceiveSMP111_A)
RecA.SubscribeStatus('VideoResolution', {'Stream':'Record'}, ReceiveSMP111_A)
RecA.SubscribeStatus('RemainingFreeDiskSpace',{'Drive':'Primary'}, ReceiveSMP111_A)
RecA.SubscribeStatus('RemainingFreeDiskSpace',{'Drive':'Secondary'}, ReceiveSMP111_A)
RecA.SubscribeStatus('CurrentRecordingDuration', None, ReceiveSMP111_A)


@event(RecA, 'Disconnected')
@event(RecA, 'Connected')
def SMP111_A_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectMatrix"""
    if state == 'Connected':
        reconnectWaitSMP111_A.Cancel()
    else:
        print('XD')
    pass





# DATA PARSING FUNCTIONS -------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function activate feedback
## Each function works with the subscription methods of the Python modules
def XTP_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device"""
    if command == 'ConnectionStatus':
        print('> Module: ' + value + " | XTP II 3200")
        #
        if value == 'Connected':
            Matrix_Data['ConexModule'] = True
            ALANXtp.SetText('Online')
        else:
            Matrix_Data['ConexModule'] = False
            ALANXtp.SetText('Fail')
            ## Disconnect the IP Socket
            XTP.Disconnect()
    
    elif command == 'InputSignal':
        if value == 'Active':
            print('--- Parsing Matrix: (Input ' + qualifier['Input'] + ' Ok)' )
        else:
            print('--- Parsing Matrix: (Input ' + qualifier['Input'] + ' ...)')
        #
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
        print('--- Parsing Matrix: (Out ' +  qualifier['Output'] + ' In ' + value + ' ' + qualifier['Tie Type'] + ')')
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



# EVENT FUNCTIONS --------------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send a Connect()
## CAUTION: If you never make a Connect(), the Module never work with Subscriptions
@event(XTP, 'Connected')
@event(XTP, 'Disconnected')
def matrix_conex_event(interface, state):
    """This reports the physical connection status of the device"""
    #
    print('> Socket: ' + state + " | XTP II 3200")
    #
    if state == 'Connected':
        Matrix_Data['ConexEvent'] = True
        ALANXtp.SetText('Online')
        ## Send & Query Information
        subscribe_matrix()
        update_matrix()
    else:
        Matrix_Data['ConexEvent'] = False
        ALANXtp.SetText('Fail')
        trying_matrix()
    pass


# RECURSIVE FUNCTIONS ----------------------------------------------------------
## Help´s when the device was Off in the first Connect() method when the code starts
def trying_matrix():
    """Try to make a Connect() to device"""
    if Matrix_Data['ConexEvent'] == False:
        print('Tryng to make a Connect() in Matrix')
        XTP.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_matrix = Wait(5, trying_matrix)


# RECURSIVE LOOP FUNCTIONS -----------------------------------------------------
## This not affect any device
## This return True / False when no response is received from Module
## If in 5 times the data is not reported (connectionCounter = 5) from Update Command
## Generate 'Connected' / 'Disconnected'
def update_loop_matrix():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    XTP.Update('InputSignal',{'Input':'1'})
    loop_update_matrix.Restart()
loop_update_matrix = Wait(12, update_loop_matrix)







# DATA DICTIONARIES ------------------------------------------------------------
## Each dictionary store the real time information of room devices
## Room
Room_Data = {
    'Mixed' : None
}
## IP
Matrix_Data = {
    'ConexModule': None,
    'ConexEvent' : None,
}

VoIP1_Data = {
    'Dial' : None,
    'DTMF' : False,
}

VoIP2_Data = {
    'Dial' : None,
    'DTMF' : False,
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

def FunctionOpenRoom():
    """This prepare the room to be used in mode Mixed"""
    ## Store the data in dictionary
    Room_Data['Mixed'] = False
    ## Activate button feedback
    ABtnRoom1.SetState(1)
    ABtnRoom2.SetState(0)
    ## Touchpanel actions
    TLP1.ShowPage('Main')
    ## Notify to console
    print("Touch 1: {0}".format("Room Split"))
    pass

def FunctionCloseRoom():
    ## Store the data in dictionary
    Room_Data['Mixed'] = True
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
            FunctionOpenRoom()
        else:
            FunctionCloseRoom()
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
            ALblMain.SetText('Control de Videoconferencia')
            print("Touch 1: {0}".format("Mode VideoConferencia"))
        #
        elif button is ABtnAudio:
            ## Audio Routing
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
            ##
            ALblMain.SetText('Control de Sala')
            print("Touch 1: {0}".format("Mode Audio"))
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
        elif button is ABtnVoIP:
            TLP1.ShowPopup('Full.VoIP')
            ALblMain.SetText('Control de VoIP')
            print("Touch 1: {0}".format("Mode VoIP"))
        #
        elif button is ABtnInfo:
            TLP1.ShowPopup('Full.Info')
            ALblMain.SetText('Información de Dispositivos')
            print("Touch 1: {0}".format("Mode Info"))
        #
        elif button is ABtnPower:
            ALblMain.SetText('Apagar Sistema')
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

# ACTIONS - MATRIX TIE INFO FUNCTIONS ------------------------------------------
def FunctionActiveTie(output):
    '''This retrieve the real Output-Input Video Relation when the user push the Display button'''
    activeTie = XTP.ReadStatus('OutputTieStatus', {'Output':output, 'Tie Type':'Video'})
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
    AScreenUp.SetState('Close')
    pass

def Room1ScreenDown():
    """Control of Relays"""
    AScreenUp.SetState('Open')
    AScreenDw.SetState('Close')
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
    A2ScreenUp.SetState('Close')
    pass

def Room2ScreenDown():
    """Control of Relays"""
    A2ScreenUp.SetState('Open')
    A2ScreenDw.SetState('Close')
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
            ProjA.Set('Power','Off')
        else:
            print("Touch 1: {0}".format("Proyector 1: PowerOn"))
            ProjA.Set('Power','On')
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
        if LCD3.ReadStatus('Power', None) == 'On':
            LCD3.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 3 Power Off"))
        else:
            LCD3.Set('Power','On')
            print("Touch 1: {0}".format("LCD 3 Power On"))
    #
    elif button is ALCDCab2:
        if LCD4.ReadStatus('Power', None) == 'On':
            LCD4.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 4 Power Off"))
        else:
            LCD4.Set('Power','On')
            print("Touch 1: {0}".format("LCD 4 Power On"))
    #
    elif button is ALCDLobby:
        if LCDL1.ReadStatus('Power', None) == 'On':
            LCDL1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD L1 Power Off"))
        else:
            LCDL1.Set('Power','On')
            print("Touch 1: {0}".format("LCD L1 Power On"))
    #
    elif button is ALCDPodium1:
        if LCDP1.ReadStatus('Power', None) == 'On':
            LCDP1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD P1 Power Off"))
        else:
            LCDP1.Set('Power','On')
            print("Touch 1: {0}".format("LCD P1 Power On"))
    pass

# ACTIONS - DISPLAYS B MODE ----------------------------------------------------
@event(ProjeccionB, 'Pressed')
def ButtonObjectPressed(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is AProjBPwr:
        if ProjB.ReadStatus('Power',None) == 'On':
            print("Touch 1: {0}".format("Proyector 2: PowerOff"))
            ProjB.Set('Power','Off')
        else:
            print("Touch 1: {0}".format("Proyector 2: PowerOn"))
            ProjB.Set('Power','On')
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
        if LCD1.ReadStatus('Power', None) == 'On':
            LCD1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 1 Power Off"))
        else:
            LCD1.Set('Power','On')
            print("Touch 1: {0}".format("LCD 1 Power On"))
    #
    elif button is A2LCDCab3:
        if LCD2.ReadStatus('Power', None) == 'On':
            LCD2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 2 Power Off"))
        else:
            LCD2.Set('Power','On')
            print("Touch 1: {0}".format("LCD 2 Power On"))
    #
    elif button is A2LCDLobby:
        if LCDL2.ReadStatus('Power', None) == 'On':
            LCDL2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD L2 Power Off"))
        else:
            LCDL2.Set('Power','On')
            print("Touch 1: {0}".format("LCD L2 Power On"))
    #
    elif button is ALCDPodium2:
        if LCDP2.ReadStatus('Power', None) == 'On':
            LCDP2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD P2 Power Off"))
        else:
            LCDP2.Set('Power','On')
            print("Touch 1: {0}".format("LCD P2 Power On"))
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

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def PrintDialerVC1(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVC

    if btn_name == 'Delete':         #If the user push 'Delete' button
        dialerVC = dialerVC[:-1]     #Remove the last char of the string
        Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        AVCDial.SetText(dialerVC)  #Send the string to GUI Label

    else:                            #If the user push a [*#0-9] button
        number = str(btn_name[4])    #Extract the valid character of BTN name
        dialerVC += number           #Append the last char to the string
        Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        AVCDial.SetText(dialerVC)  #Send the string to GUI Label
    pass

@event(VCDial, ButtonEventList)
def vi_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VoIP Dial Buttons pressed come in button variable
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
        Cisco1.Set('Hook', 'Dial', {'Number':Cisco1_Data['Dial'], 'Protocol':'H323'})
        print("Touch 1: {0}".format("Cisco1: Call"))
    #
    elif button is AHangup:
        Cisco1.Set('Hook', 'Disconnect 1', {'Number':Cisco1_Data['Dial'], 'Protocol':'H323'})
        AVCDial.SetText('')
        print("Touch 1: {0}".format("Cisco1: Hangup"))
    #
    elif button is AContentOn:
        Cisco1.Set('Presentation', '1')
        print("Touch 1: {0}".format("Cisco1: Content On"))
    #
    elif button is AContentOff:
        Cisco1.Set('Presentation', 'Stop')
        print("Touch 1: {0}".format("Cisco1: Content Off"))
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
        dialerVC2 += number           #Append the last char to the string
        Cisco2_Data['Dial'] = dialerVC2 #Asign the string to the data dictionary
        A2VCDial.SetText(dialerVC2)  #Send the string to GUI Label
    pass

@event(VC2Dial, ButtonEventList)
def VC2_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VoIP Dial Buttons pressed come in button variable
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
        Cisco2.Set('Hook', 'Dial', {'Number':Cisco2_Data['Dial'], 'Protocol':'H323'})
        print("Touch 1: {0}".format("Cisco2: Call"))
    #
    elif button is A2Hangup:
        Cisco2.Set('Hook', 'Disconnect 1', {'Number':Cisco2_Data['Dial'], 'Protocol':'H323'})
        A2VCDial.SetText('')
        print("Touch 1: {0}".format("Cisco2: Hangup"))
    #
    elif button is A2ContentOn:
        Cisco2.Set('Presentation', '1')
        print("Touch 1: {0}".format("Cisco2: Content On"))
    #
    elif button is A2ContentOff:
        Cisco2.Set('Presentation', 'Stop')
        print("Touch 1: {0}".format("Cisco2: Content Off"))
    pass

# ACTIONS - AUDIO VOIP LINE 1 MODE ------------------------------------------------

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def PrintDialerVoIP1(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVoIP

    if btn_name == 'Delete':             #If the user push 'Delete' button
        dialerVoIP = dialerVoIP[:-1]     #Remove the last char of the string
        VoIP1_Data['Dial'] = dialerVoIP  #Asign the string to the data dictionary
        AViDial.SetText(dialerVoIP)      #Send the string to GUI Label

    else:                                   #If the user push a [*#0-9] button
        if VoIP1_Data['DTMF'] == False:
            number = str(btn_name[4])       #Extract the valid character of BTN name
            dialerVoIP += number            #Append the last char to the string
            VoIP1_Data['Dial'] = dialerVoIP #Asign the string to the data dictionary
            AViDial.SetText(dialerVoIP)     #Send the string to GUI Label
        else:
            Tesira.Set('DTMF', number, {'Instance Tag':'Dialer', 'Line':'1'})
    pass

@event(VoIPDial, ButtonEventList)
def VoIP1_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VoIP Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Touch: VoIP L1 %s' % (button.Name))
        PrintDialerVoIP1(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(VoIPButtons, 'Pressed')
def VC_Mode(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is AViCall:
        Tesira.Set('VoIPHook', 'Dial', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1', 'Number':VoIP1_Data['Dial']})
        print("Touch 1: {0}".format("VoIP L1: Call"))
    #
    elif button is AViHangup:
        Tesira.Set('VoIPHook', 'End', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'})
        AViDial.SetText('')
        print("Touch 1: {0}".format("VoIP L1: Hangup"))
    #
    elif button is AViRedial:
        Tesira.Set('VoIPHook', 'Redial', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'})
        print("Touch 1: {0}".format("VoIP L1: Redial"))
    #
    elif button is AViDTMF:
        if VoIP1_Data['DTMF'] == False:
            VoIP1_Data['DTMF'] = True
            AViDTMF.SetState(1)
            print("Touch 1: {0}".format("VoIP L1: DTMF On"))
        else:
            VoIP1_Data['DTMF'] = False
            AViDTMF.SetState(0)
            print("Touch 1: {0}".format("VoIP L1: DTMF Off"))
    pass

# ACTIONS - AUDIO VOIP LINE 2 MODE ------------------------------------------------

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def PrintDialerVoIP2(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVoIP2

    if btn_name == 'Delete':             #If the user push 'Delete' button
        dialerVoIP2 = dialerVoIP2[:-1]     #Remove the last char of the string
        VoIP2_Data['Dial'] = dialerVoIP2  #Asign the string to the data dictionary
        AVi2Dial.SetText(dialerVoIP2)      #Send the string to GUI Label

    else:                                   #If the user push a [*#0-9] button
        if VoIP2_Data['DTMF'] == False:
            number = str(btn_name[4])       #Extract the valid character of BTN name
            dialerVoIP2 += number            #Append the last char to the string
            VoIP2_Data['Dial'] = dialerVoIP2 #Asign the string to the data dictionary
            AVi2Dial.SetText(dialerVoIP2)     #Send the string to GUI Label
        else:
            Tesira.Set('DTMF', number, {'Instance Tag':'Dialer', 'Line':'2'})
    pass

@event(VoIP2Dial, ButtonEventList)
def VoIP2_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VoIP Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Touch: VoIP L2 %s' % (button.Name))
        PrintDialerVoIP2(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(VoIP2Buttons, 'Pressed')
def VoIP2_Mode(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button is AVi2Call:
        Tesira.Set('VoIPHook', 'Dial', {'Instance Tag':'Dialer', 'Line':'2', 'Call Appearance':'1', 'Number':VoIP1_Data['Dial']})
        print("Touch 1: {0}".format("VoIP L2: Call"))
    #
    elif button is AVi2Hangup:
        Tesira.Set('VoIPHook', 'End', {'Instance Tag':'Dialer', 'Line':'2', 'Call Appearance':'1'})
        AViDial.SetText('')
        print("Touch 1: {0}".format("VoIP L2: Hangup"))
    #
    elif button is AVi2Redial:
        Tesira.Set('VoIPHook', 'Redial', {'Instance Tag':'Dialer', 'Line':'2', 'Call Appearance':'1'})
        print("Touch 1: {0}".format("VoIP L2: Redial"))
    #
    elif button is AVi2DTMF:
        if VoIP2_Data['DTMF'] == False:
            VoIP2_Data['DTMF'] = True
            AVi2DTMF.SetState(1)
            print("Touch 1: {0}".format("VoIP L2: DTMF On"))
        else:
            VoIP2_Data['DTMF'] = False
            AVi2DTMF.SetState(0)
            print("Touch 1: {0}".format("VoIP L2: DTMF Off"))
    pass


## End Events Definitions-------------------------------------------------------

Initialize()
