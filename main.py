"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en TecnologÃ­a S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Colegio de MÃ©xico (COLMEX)
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
import re

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
import csco_vtc_SX_Series_CE82_v1_1_0_2           as ModuleCisco

##
# MODULE TO DEVICE INSTANCES ---------------------------------------------------
# Video Server
XTP   = ModuleXTP.EthernetClass('172.16.241.5', 23, Model='XTP II CrossPoint 3200')
XTP.devicePassword = 'SWExtronXTP'

# Projectors
ProjA = ModuleChristie.EthernetClass('172.16.240.201', 3002, Model='D13WU-HS')
ProjB = ModuleChristie.EthernetClass('172.16.240.200', 3002, Model='D13WU-HS')

# Recorders
RecA  = ModuleSMP111.EthernetClass('172.16.241.6', 23, Model='SMP 111')
RecA.devicePassword = 'R3cSala1'

RecB  = ModuleSMP111.EthernetClass('172.16.241.7', 23, Model='SMP 111')
RecB.devicePassword = 'R3cSala2'

# Displays
LCDCab1 = ModuleSamsung.EthernetClass('172.16.241.24', 1515, Model='LH55QMFPLGC/KR')
LCDCab2 = ModuleSamsung.EthernetClass('172.16.241.25', 1515, Model='LH55QMFPLGC/KR')
LCDCab3 = ModuleSamsung.EthernetClass('172.16.241.26', 1515, Model='LH55QMFPLGC/KR')
LCDCab4 = ModuleSamsung.EthernetClass('172.16.241.27', 1515, Model='LH55QMFPLGC/KR')
LCDPod1 = ModuleSamsung.EthernetClass('172.16.241.28', 1515, Model='LH55QMFPLGC/KR')
LCDPod2 = ModuleSamsung.EthernetClass('172.16.241.29', 1515, Model='LH55QMFPLGC/KR')
LCDLob1 = ModuleSamsung.EthernetClass('172.16.241.30', 1515, Model='LH55QMFPLGC/KR')
LCDLob2 = ModuleSamsung.EthernetClass('172.16.241.31', 1515, Model='LH55QMFPLGC/KR')

# Audio Server
Tesira = ModuleTesira.EthernetClass('172.16.241.100', 23, Model='Tesira SERVER-IO')

# Cameras
PTZ1 = ModulePTZ.EthernetClass('172.16.240.15', 52381, ServicePort=52381, Model='BRC-H800') ##UDP

# Videoconference Códecs
Cisco1 = ModuleCisco.EthernetClass('172.16.240.87', 23, Model='SX20 CE8.2.X')
Cisco1.deviceUsername = 'admin'
Cisco1.devicePassword = 'auditc0lm3xS1'

Cisco2 = ModuleCisco.EthernetClass('172.16.240.88', 23, Model='SX20 CE8.2.X')
Cisco2.deviceUsername = 'admin'
Cisco2.devicePassword = 'auditc0lm3xS2'

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
AInfo2Cisco  = Button(TLP1, 314)



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

# Answer
AAnswer1    = Button(TLP1, 400)
ADiscard1   = Button(TLP1, 401)

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

# Answer
AAnswer2    = Button(TLP1, 402)
ADiscard2   = Button(TLP1, 403)

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
VCButtons = [ACall, AHangup, AContentOn, AContentOff, AAnswer1, ADiscard1]
GroupContentA = MESet([AContentOn, AContentOff])
#
VC2Dial = [A2Dial0, A2Dial1, A2Dial2, A2Dial3, A2Dial4, A2Dial5, A2Dial6, A2Dial7, A2Dial8, A2Dial9, A2DialDot, A2DialHash, A2DialDelete]
VC2Buttons = [A2Call, A2Hangup, A2ContentOn, A2ContentOff, AAnswer2, ADiscard2]
GroupContentB = MESet([A2ContentOn, A2ContentOff])

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
    ProjA.Connect(timeout = 5)
    ProjB.Connect(timeout = 5)
    """RecA.Connect()
    RecB.Connect()"""
    LCDCab1.Connect(timeout = 5)
    LCDCab2.Connect(timeout = 5)
    LCDCab3.Connect(timeout = 5)
    LCDCab4.Connect(timeout = 5)
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
    ('InputSignal',{'Input':'15'}),
    ('InputSignal',{'Input':'16'}),
    ('InputSignal',{'Input':'17'}),
    ('InputSignal',{'Input':'18'}),
    ('InputSignal',{'Input':'19'}),
    ('InputSignal',{'Input':'20'}),
    ('InputSignal',{'Input':'21'}),
    ('InputSignal',{'Input':'22'}),
    ('InputSignal',{'Input':'23'}),
    ('InputSignal',{'Input':'24'}),
    ('InputSignal',{'Input':'25'}),
    ('InputSignal',{'Input':'26'}),
    ('InputSignal',{'Input':'27'}),
    ('InputSignal',{'Input':'28'}),
    ('InputSignal',{'Input':'29'}),
    ('InputSignal',{'Input':'30'}),
    ('InputSignal',{'Input':'31'}),
    ('InputSignal',{'Input':'32'}),
]
XTP_Queue = collections.deque(XTP_QUERY_LIST)

TESIRA_QUERY_LIST = [
    ('LastDialed', {'Instance Tag':'Dialer', 'Line':'1'}),
    """('VoIPCallStatus', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'}),
    ('VoIPCallerID', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'}),
    ('VoIPLineInUse', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'}),"""
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
    ('PresentationMode', None),
    ('CallStatus', {'Call':'1'}),
    ('CallStatusType', {'Call':'1'}),
    ('DisplayName', {'Call':'1'}),
    ('IPAddress', None),
    ('RemoteNumber', {'Call':'1'}),
]
Cisco1_Queue = collections.deque(CISCO1_QUERY_LIST)

CISCO2_QUERY_LIST = [
    ('Presentation', {'Instance':'1'}),
    ('PresentationMode', None),
    ('CallStatus', {'Call':'1'}),
    ('CallStatusType', {'Call':'1'}),
    ('DisplayName', {'Call':'1'}),
    ('IPAddress', None),
    ('RemoteNumber', {'Call':'1'}),
]
Cisco2_Queue = collections.deque(CISCO2_QUERY_LIST)

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

# RECONEX / QUERY RECALL ------------------------------------------------------
# This is a recursive function to send Query Command to Device certain time
def QueryXTP():
    """This send Query commands to device every 03.s"""
    #
    XTP.Update(*XTP_Queue[0])
    XTP_Queue.rotate(-1)
    XTP_PollingWait.Restart()
    #
XTP_PollingWait = Wait(0.3, QueryXTP)

def QueryTesira():
    """This send Query commands to device every 03.s"""
    #
    Tesira.Update(*Tesira_Queue[0])
    Tesira_Queue.rotate(-1)
    Tesira_PollingWait.Restart()
    #
Tesira_PollingWait = Wait(0.3, QueryTesira)

def QueryProjectorA():
    """This send Query commands to device every 03.s"""
    #
    ProjA.Update(*Projector_A_Queue[0])
    Projector_A_Queue.rotate(-1)
    Projector_A_PollingWait.Restart()
    #
Projector_A_PollingWait = Wait(0.3, QueryProjectorA)

def QueryProjectorB():
    """This send Query commands to device every 03.s"""
    #
    ProjB.Update(*Projector_B_Queue[0])
    Projector_B_Queue.rotate(-1)
    Projector_B_PollingWait.Restart()
    #
Projector_B_PollingWait = Wait(0.3, QueryProjectorB)

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

def QueryLCDCab1():
    """This send Query commands to device every 01.s"""
    #
    LCDCab1.Update(*LCDCab1_Queue[0])
    LCDCab1_Queue.rotate(-1)
    LCDCab1_PollingWait.Restart()
    #
LCDCab1_PollingWait = Wait(1, QueryLCDCab1)

def QueryLCDCab2():
    """This send Query commands to device every 02.s"""
    #
    LCDCab2.Update(*LCDCab2_Queue[0])
    LCDCab2_Queue.rotate(-1)
    LCDCab2_PollingWait.Restart()
    #
LCDCab2_PollingWait = Wait(1, QueryLCDCab2)

def QueryLCDCab3():
    """This send Query commands to device every 03.s"""
    #
    LCDCab3.Update(*LCDCab3_Queue[0])
    LCDCab3_Queue.rotate(-1)
    LCDCab3_PollingWait.Restart()
    #
LCDCab3_PollingWait = Wait(1, QueryLCDCab3)

def QueryLCDCab4():
    """This send Query commands to device every 03.s"""
    #
    LCDCab4.Update(*LCDCab4_Queue[0])
    LCDCab4_Queue.rotate(-1)
    LCDCab4_PollingWait.Restart()
    #
LCDCab4_PollingWait = Wait(1, QueryLCDCab4)

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
    print('Attempting to connect Projector B')
    result = Cisco1.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitCisco1.Restart()
    pass
reconnectWaitCisco1 = Wait(15, AttemptConnectCisco1)

def AttemptConnectCisco2():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector B')
    result = Cisco2.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitCisco2.Restart()
    pass
reconnectWaitCisco2 = Wait(15, AttemptConnectCisco2)

def AttemptConnectLCDCab1():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector B')
    result = LCDCab1.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab1.Restart()
    pass
reconnectWaitLCDCab1 = Wait(15, AttemptConnectLCDCab1)

def AttemptConnectLCDCab2():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector B')
    result = LCDCab2.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab2.Restart()
    pass
reconnectWaitLCDCab2 = Wait(15, AttemptConnectLCDCab2)

def AttemptConnectLCDCab3():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector B')
    result = LCDCab3.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab3.Restart()
    pass
reconnectWaitLCDCab3 = Wait(15, AttemptConnectLCDCab3)

def AttemptConnectLCDCab4():
    """Attempt to create a TCP connection to the LCD
       IF it fails, retry in 15 seconds
    """
    print('Attempting to connect Projector B')
    result = LCDCab4.Connect(timeout=5)
    if result != 'Connected':
        reconnectWaitLCDCab4.Restart()
    pass
reconnectWaitLCDCab4 = Wait(15, AttemptConnectLCDCab4)

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

def ReceiveTesira(command, value, qualifier):
    """If the module´s ConnectionStatus becomes Disconnected, then many
       consecutive Updates have failed to receive a response from the device.
       Attempt to re-stablish the TCP connection to the device by calling
       Disconnect on the module instance and restarting reconnectWait
    """
    print(qualifier)
    print(value)

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
        else:
            AProjAPwr.SetState(0)
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
        else:
            AProjBPwr.SetState(0)
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
        AInfo2Cisco.SetText(value)
        print('--- Parsing Cisco 1: (Presentation ' +  value + ' )')
        if value == '2':
            GroupContentA.SetCurrent(AContentOn)
        elif value == 'Stop':
            GroupContentA.SetCurrent(AContentOff)
    #
    elif command == 'PresentationMode':
        print('--- Parsing Cisco 1: (PresentationMode ' +  value + ' )')
    #
    elif command == 'CallStatus':
        print('--- Parsing Cisco 1: (CallStatus ' +  value + ' )')
        if value == 'Ringing':
            TLP1.ShowPopup('Cisco1.Call')
        else:
            TLP1.HidePopup('Cisco1.Call')
    #
    elif command == 'CallStatusType':
        print('--- Parsing Cisco 1: (CallStatusType ' +  value + ' )')
    #
    elif command == 'DisplayName':
        print('--- Parsing Cisco 1: (DisplayName ' +  value + ' )')
        AVCRemote.SetText(value)
    #
    elif command == 'IPAddress':
        print('--- Parsing Cisco 1: (IPAddress ' +  value + ' )')
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
            AInfoCisco.SetState(0)
        else:
            AInfoCisco.SetState(1)
    #
    elif command == 'Presentation':
        AInfo2Cisco.SetText(value)
        print('--- Parsing Cisco 2: (Presentation ' +  value + ' )')
        if value == '2':
            GroupContentB.SetCurrent(A2ContentOn)
        elif value == 'Stop':
            GroupContentB.SetCurrent(A2ContentOff)
    #
    elif command == 'PresentationMode':
        print('--- Parsing Cisco 2: (PresentationMode ' +  value + ' )')
    #
    elif command == 'CallStatus':
        print('--- Parsing Cisco 2: (CallStatus ' +  value + ' )')
        if value == 'Ringing':
            TLP1.ShowPopup('Cisco2.Call')
        else:
            TLP1.HidePopup('Cisco2.Call')
    #
    elif command == 'CallStatusType':
        print('--- Parsing Cisco 2: (CallStatusType ' +  value + ' )')
    #
    elif command == 'DisplayName':
        print('--- Parsing Cisco 2: (DisplayName ' +  value + ' )')
        A2VCRemote.SetText(value)
    #
    elif command == 'IPAddress':
        print('--- Parsing Cisco 2: (IPAddress ' +  value + ' )')
    #
    elif command == 'RemoteNumber':
        print('--- Parsing Cisco 2: (RemoteNumber ' +  value + ' )')
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

# RECONEX / SUBSCRIPTIONS ------------------------------------------
# This Commands make a real data mach from Device to Processor
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
XTP.SubscribeStatus('InputSignal', {'Input':'15'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'16'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'17'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'18'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'19'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'20'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'21'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'22'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'23'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'24'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'25'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'26'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'27'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'28'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'29'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'30'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'31'}, ReceiveXTP)
XTP.SubscribeStatus('InputSignal', {'Input':'32'}, ReceiveXTP)
##
XTP.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'5', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'6', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'7', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'8', 'Tie Type':'Video'}, ReceiveXTP)
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
XTP.SubscribeStatus('OutputTieStatus', {'Output':'23', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'24', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'25', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'26', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'27', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'28', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'29', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'30', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'31', 'Tie Type':'Video'}, ReceiveXTP)
XTP.SubscribeStatus('OutputTieStatus', {'Output':'32', 'Tie Type':'Video'}, ReceiveXTP)
#
Tesira.SubscribeStatus('ConnectionStatus', None, ReceiveTesira)
"""Tesira.SubscribeStatus('LastDialed', {'Instance Tag':'Dialer', 'Line':'1'}, ReceiveTesira)
Tesira.SubscribeStatus('VoIPCallStatus', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'}, ReceiveTesira)
Tesira.SubscribeStatus('VoIPCallerID', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'}, ReceiveTesira)
Tesira.SubscribeStatus('VoIPLineInUse', {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'}, ReceiveTesira)"""
#
ProjA.SubscribeStatus('ConnectionStatus', None, ReceiveProjectorA)
ProjA.SubscribeStatus('Power', None, ReceiveProjectorA)
ProjA.SubscribeStatus('Input', None, ReceiveProjectorA)
#
ProjB.SubscribeStatus('ConnectionStatus', None, ReceiveProjectorB)
ProjB.SubscribeStatus('Power', None, ReceiveProjectorB)
ProjB.SubscribeStatus('Input', None, ReceiveProjectorB)
#
Cisco1.SubscribeStatus('ConnectionStatus', None, ReceiveCisco1)
Cisco1.SubscribeStatus('Presentation', {'Instance':'1'}, ReceiveCisco1)
Cisco1.SubscribeStatus('PresentationMode', None, ReceiveCisco1)
Cisco1.SubscribeStatus('CallStatus', {'Call':'1'}, ReceiveCisco1)
Cisco1.SubscribeStatus('CallStatusType', {'Call':'1'}, ReceiveCisco1)
Cisco1.SubscribeStatus('DisplayName', {'Call':'1'}, ReceiveCisco1)
Cisco1.SubscribeStatus('IPAddress', None, ReceiveCisco1)
Cisco1.SubscribeStatus('RemoteNumber', {'Call':'1'}, ReceiveCisco1)
#
Cisco2.SubscribeStatus('ConnectionStatus', None, ReceiveCisco2)
Cisco2.SubscribeStatus('Presentation', {'Instance':'1'}, ReceiveCisco2)
Cisco2.SubscribeStatus('PresentationMode', None, ReceiveCisco2)
Cisco2.SubscribeStatus('CallStatus', {'Call':'1'}, ReceiveCisco2)
Cisco2.SubscribeStatus('CallStatusType', {'Call':'1'}, ReceiveCisco2)
Cisco2.SubscribeStatus('DisplayName', {'Call':'1'}, ReceiveCisco2)
Cisco2.SubscribeStatus('IPAddress', None, ReceiveCisco2)
Cisco2.SubscribeStatus('RemoteNumber', {'Call':'1'}, ReceiveCisco2)
#
LCDCab1.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab1)
LCDCab1.SubscribeStatus('Power', None, ReceiveLCDCab1)
#
LCDCab2.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab2)
LCDCab2.SubscribeStatus('Power', None, ReceiveLCDCab2)
#
LCDCab3.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab3)
LCDCab3.SubscribeStatus('Power', None, ReceiveLCDCab3)
#
LCDCab4.SubscribeStatus('ConnectionStatus', None, ReceiveLCDCab4)
LCDCab4.SubscribeStatus('Power', None, ReceiveLCDCab4)

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
        AInfoCisco.SetState(1)
        reconnectWaitCisco2.Cancel()
    else:
        print('Socket Disconnected: Cisco2')
        AInfoCisco.SetState(0)
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

# DATA DICTIONARIES ------------------------------------------------------------
## Each dictionary store general information
## Room
Room_Data = {
    'Mixed' : None
}
## IP
Cisco1_Data = {
    'Dial' : None,
}

Cisco2_Data = {
    'Dial' : None,
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
            ALblMain.SetText('Control de GrabaciÃ³n')
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
            ALblMain.SetText('InformaciÃ³n de Dispositivos')
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
        # Validate Popup -----------------------------------------------
        if button == AOut17 or button == AOut19:
            TLP1.ShowPopup('Full.InputsCam')
        elif button == AOut18 or button == AOut20:
            TLP1.ShowPopup('Full.InputsPC')
        else:
            TLP1.ShowPopup('Full.Inputs')

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
        if LCDCab3.ReadStatus('Power', None) == 'On':
            LCDCab3.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 3 Power Off"))
        else:
            LCDCab3.Set('Power','On')
            print("Touch 1: {0}".format("LCD 3 Power On"))
    #
    elif button is ALCDCab2:
        if LCDCab4.ReadStatus('Power', None) == 'On':
            LCDCab4.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 4 Power Off"))
        else:
            LCDCab4.Set('Power','On')
            print("Touch 1: {0}".format("LCD Cab4 Power On"))
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
        if LCDCab1.ReadStatus('Power', None) == 'On':
            LCDCab1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 1 Power Off"))
        else:
            LCDCab1.Set('Power','On')
            print("Touch 1: {0}".format("LCD 1 Power On"))
    #
    elif button is A2LCDCab3:
        if LCDCab2.ReadStatus('Power', None) == 'On':
            LCDCab2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 2 Power Off"))
        else:
            LCDCab2.Set('Power','On')
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
## This function add or remove data from the panel Dial Number
def PrintDialerVC1(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVC

    if btn_name == 'Delete':           #If the user push 'Delete' button
        dialerVC = dialerVC[:-1]       #Remove the last char of the string
        Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        AVCDial.SetText(dialerVC)      #Send the string to GUI Label

    else:                              #If the user push a [*#0-9] button
        number = str(btn_name[4])      #Extract the valid character of BTN name
        dialerVC += number             #Append the last char to the string
        Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        AVCDial.SetText(dialerVC)      #Send the string to GUI Label
    pass

## This function is called when the user press a Dial Button
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
        if Cisco1.ReadStatus('CallStatus', {'Call':'1'}) == 'Idle':
            pint('XD')
        else:
            Cisco1.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
            AVCDial.SetText('')
            print("Touch 1: {0}".format("Cisco1: Hangup"))
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
        if Cisco2.ReadStatus('CallStatus', {'Call':'1'}) == 'Idle':
            pint('XD')
        else:
            Cisco2.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
            A2VCDial.SetText('')
            print("Touch 1: {0}".format("Cisco2: Hangup"))
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