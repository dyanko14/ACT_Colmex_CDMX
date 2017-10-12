"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Colegio de México (COLMEX)
 Project    | Alfonso Reyes Auditorium
 Version    | 0.5 --------------------------------------------------------- """

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

# MODULE TO DEVICE INSTANCES ---------------------------------------------------
# Video Server
XTP = ModuleXTP.EthernetClass('172.16.241.5', 23, Model='XTP II CrossPoint 3200')
XTP.devicePassword = 'SWExtronXTP'
#
# Audio Server
Tesira = ModuleTesira.EthernetClass('172.16.241.100', 23, Model='Tesira SERVER-IO')
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
ABtnREC     = Button(TLP1, 14)
ABtnInfo    = Button(TLP1, 15)
ABtnPower   = Button(TLP1, 16)

# Mode Main - Up Bar
ALblMain = Label(TLP1, 20)
ABtnRoom2 = Button(TLP1, 21)
ABtnRoom1 = Button(TLP1, 22)

# Mode Switching ---------------------------------------------------------------
# Outputs ----------------------------------------------------------------------
# XTP Out Slot 1
ABtnOut1 = Button(TLP1, 101) ##Room1 Projector
ABtnOut2 = Button(TLP1, 102) ##Room1 LCD Confidence
ABtnOut3 = Button(TLP1, 103) ##Room1 LCD Podium
# XTP Out Slot 2
ABtnOut5 = Button(TLP1, 105) ##Room2 Projector
ABtnOut6 = Button(TLP1, 106) ##Room2 LCD Confidence
ABtnOut7 = Button(TLP1, 107) ##Room2 LCD Podium
# XTP Out Slot 3
ABtnOut9 = Button(TLP1, 109) ##Core Tricaster 1 - Input 1
ABtnOut10 = Button(TLP1, 110) ##Core Tricaster 1 - Input 2
ABtnOut11 = Button(TLP1, 111) ##Core Tricaster 1 - Input 3
ABtnOut12 = Button(TLP1, 112) ##Core Tricaster 1 - Input 4
# XTP Out Slot 4
ABtnOut13 = Button(TLP1, 113) ##Core Tricaster 2 - Input 1
ABtnOut14 = Button(TLP1, 114) ##Core Tricaster 2 - Input 2
ABtnOut15 = Button(TLP1, 115) ##Core Tricaster 2 - Input 3
ABtnOut16 = Button(TLP1, 116) ##Core Tricaster 2 - Input 4
# XTP Out Slot 5
ABtnOut17 = Button(TLP1, 117) ##Core Cisco 1 - Input Camera
ABtnOut18 = Button(TLP1, 118) ##Core Cisco 1 - Input Graphics
ABtnOut19 = Button(TLP1, 119) ##Core Cisco 2 - Input Camera
ABtnOut20 = Button(TLP1, 120) ##Core Cisco 2 - Input Graphics
# XTP Out Slot 6
ABtnOut21 = Button(TLP1, 121) ##Core Recorder 1
ABtnOut22 = Button(TLP1, 122) ##Core Recorder 2

# Inputs -----------------------------------------------------------------------
# XTP Slot 1
ABtnInput1 = Button(TLP1, 201) ##Room1 PC Left
ABtnInput2 = Button(TLP1, 202) ##Room1 PC Right
ABtnInput3 = Button(TLP1, 203) ##Room1 PC Stage
ABtnInput4 = Button(TLP1, 204) ##Room1 PC Right
# XTP Slot 2
ABtnInput5 = Button(TLP1, 205) ##Room2 PC Left
ABtnInput6 = Button(TLP1, 206) ##Room2 PC Right
ABtnInput7 = Button(TLP1, 207) ##Room2 PC Stage
ABtnInput8 = Button(TLP1, 208) ##Room2 PC Back
# XTP Slot 3
ABtnInput9 = Button(TLP1, 209) ##Room1 PTZ1
ABtnInput10 = Button(TLP1, 210) ##Room1 PTZ2
ABtnInput11 = Button(TLP1, 211) ##Room2 PTZ1
ABtnInput12 = Button(TLP1, 212) ##Room2 PTZ2
# XTP Slot 4
ABtnInput13 = Button(TLP1, 213) ##Room1 PC Cabin
ABtnInput14 = Button(TLP1, 214) ##Room2 PC Cabin
##...
##...
# XTP Slot 5
ABtnInput17 = Button(TLP1, 217) ##Core Cisco 1 Out
ABtnInput18 = Button(TLP1, 218) ##Core Cisco 2 Out
ABtnInput19 = Button(TLP1, 219) ##Core ShareLink 1
ABtnInput20 = Button(TLP1, 220) ##Core ShareLink 2
# XTP Slot 6
ABtnInput21 = Button(TLP1, 221) ##Core Tricaster 1 - Out 1
ABtnInput22 = Button(TLP1, 222) ##Core Tricaster 2 - Out 1
# Input Signal Status
# XTP Slot 1
ABtnSignal1 = Button(TLP1, 130) ##Room1 PC Left
ABtnSignal2 = Button(TLP1, 131) ##Room1 PC Right
ABtnSignal3 = Button(TLP1, 132) ##Room1 PC Stage
ABtnSignal4 = Button(TLP1, 133) ##Room1 PC Right
# XTP Slot 2
ABtnSignal5 = Button(TLP1, 134) ##Room2 PC Left
ABtnSignal6 = Button(TLP1, 135) ##Room2 PC Right
ABtnSignal7 = Button(TLP1, 136) ##Room2 PC Stage
ABtnSignal8 = Button(TLP1, 137) ##Room2 PC Back
# XTP Slot 3
ABtnSignal9 = Button(TLP1, 138) ##Room1 PTZ1
ABtnSignal10 = Button(TLP1, 139) ##Room1 PTZ2
ABtnSignal11 = Button(TLP1, 140) ##Room2 PTZ1
ABtnSignal12 = Button(TLP1, 141) ##Room2 PTZ2
# XTP Slot 4
ABtnSignal13 = Button(TLP1, 142) ##Room1 PC Cabin
ABtnSignal14 = Button(TLP1, 143) ##Room2 PC Cabin
##...
##...
# XTP Slot 5
ABtnSignal17 = Button(TLP1, 144) ##Core Cisco 1 Out
ABtnSignal18 = Button(TLP1, 145) ##Core Cisco 2 Out
ABtnSignal19 = Button(TLP1, 146) ##Core ShareLink 1
ABtnSignal20 = Button(TLP1, 147) ##Core ShareLink 2
# XTP Slot 6
ABtnSignal21 = Button(TLP1, 148) ##Core Tricaster 1 - Out 1
ABtnSignal22 = Button(TLP1, 149) ##Core Tricaster 2 - Out 1

# Mode Display -----------------------------------------------------------------
# Room 1 - Projection
ABtnPwrProjA    = Button(TLP1, 30)
ABtnScreenAUp   = Button(TLP1, 31)
ABtnScreenADown = Button(TLP1, 32)
ABtnElevAUp     = Button(TLP1, 33)
ABtnElevADown   = Button(TLP1, 34)

# Room 1 - LCD
ALCDCab1    = Button(TLP1, 42)
ALCDCab2    = Button(TLP1, 41)
ALCDCab3    = Button(TLP1, 40)
ALCDLobby   = Button(TLP1, 43)
ALCDPodium1 = Button(TLP1, 48)

# Room 2 - Projection
ABtnPwrProjB    = Button(TLP1, 35)
ABtnScreenBUp   = Button(TLP1, 36)
ABtnScreenBDown = Button(TLP1, 37)
ABtnElevBUp     = Button(TLP1, 38)
ABtnElevBDown   = Button(TLP1, 39)

# Room 2 - LCD
A2LCDCab1   = Button(TLP1, 46)
A2LCDCab2   = Button(TLP1, 45)
A2LCDCab3   = Button(TLP1, 44)
A2LCDLobby  = Button(TLP1, 47)
ALCDPodium2 = Button(TLP1, 49)

# Mode Recording ---------------------------------------------------------------
# Recorder A - Record
ABtnRecAStop   = Button(TLP1, 60)
ABtnRecARecord = Button(TLP1, 61)
ABtnRecAPause  = Button(TLP1, 62)
ALblRecATime   = Label(TLP1, 63)

# Recorder A - Info
ALblRecA1 = Label(TLP1, 64)
ALblRecA2 = Label(TLP1, 65)
ALblRecA3 = Label(TLP1, 66)
ALblRecA4 = Label(TLP1, 67)
ALblRecA5 = Label(TLP1, 68)
ALblRecA6 = Label(TLP1, 69)


# Recorder B - Record
ABtnRecBStop   = Button(TLP1, 70)
ABtnRecBRecord = Button(TLP1, 71)
ABtnRecBPause  = Button(TLP1, 72)
ALblRecBTime   = Label(TLP1, 73)

# Recorder B - Info
ALblRecB1  = Label(TLP1, 74)
ALblRecB2 = Label(TLP1, 75)
ALblRecB3 = Label(TLP1, 76)
ALblRecB4    = Label(TLP1, 77)
ALblRecB5    = Label(TLP1, 78)
ALblRecB6    = Label(TLP1, 79)

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
# Call
ABtnVC1DTMF = Button(TLP1, 2142)
ABtnVC1Call = Button(TLP1, 2143)
# Answer
ABtnVC1Answer = Button(TLP1, 400)
ABtnVC1Reject = Button(TLP1, 401)
# Content
ABtnVC1ContenOn  = Button(TLP1, 2145)
ABtnVC1ContenOff = Button(TLP1, 2146)
# Label
ALblVC1Dial     = Label(TLP1, 2147)
ALblVC1Remote   = Label(TLP1, 2148)

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
# Call
ABtnVC2DTMF = Button(TLP1, 2112)
ABtnVC2Call = Button(TLP1, 2113)
# Answer
ABtnVC2Answer = Button(TLP1, 402)
ABtnVC2Reject = Button(TLP1, 403)
# Content
ABtnVC2ContenOn  = Button(TLP1, 2115)
ABtnVC2ContenOff = Button(TLP1, 2116)
# Label
ALblVC2Dial   = Label(TLP1, 2117)
ALblVC2Remote = Label(TLP1, 2118)

# Mode Status ------------------------------------------------------------------
# Room 1
ALblLanProjA   = Button(TLP1, 302)
ALblinfo1ProjA = Label(TLP1, 303)
ALblinfo2ProjA = Label(TLP1, 304)
#
ABtnLanLCDCab3 = Button(TLP1, 310)
ABtnLanLCDCab4 = Button(TLP1, 311)
ABtnLanLCDLob1 = Button(TLP1, 322)
ABtnLanLCDPod1 = Button(TLP1, 324)
# Room 2
ALblLanProjB   = Button(TLP1, 305)
ALblinfo1ProjB = Label(TLP1, 306)
ALblinfo2ProjB = Label(TLP1, 307)
#
ABtnLanLCDCab1 = Button(TLP1, 308)
ABtnLanLCDCab2 = Button(TLP1, 309)
ABtnLanLCDLob2 = Button(TLP1, 323)
ABtnLanLCDPod2 = Button(TLP1, 325)
# Core
ABtnLanXTP    = Button(TLP1, 300)
#
ABtnLanTesira = Button(TLP1, 301)
#
ABtnLanVC1    = Button(TLP1, 312)
ALblinfo1VC1  = Label(TLP1, 313)
#
ABtnLanVC2    = Button(TLP1, 315)
ALblinfo1VC2  = Label(TLP1, 316)
#
ABtnLanRecA   = Button(TLP1, 318)
ALblinfo1RecA = Label(TLP1, 319)
#
ABtnLanRecB   = Button(TLP1, 320)
ALblinfo1RecB = Label(TLP1, 321)
# Build
ALblPython    = Label(TLP1, 326)

# Mode PowerOff ------------------------------------------------------------------
ABtnPowerAB   = Button(TLP1, 420, holdTime=1, repeatTime=1,)
ABtnPowerA    = Button(TLP1, 421, holdTime=1, repeatTime=1,)
ABtnPowerB    = Button(TLP1, 422, holdTime=1, repeatTime=1,)
ALblPowerAB   = Label(TLP1, 430)
ALblPowerA    = Label(TLP1, 431)
ALblPowerB    = Label(TLP1, 432)

# TouchPanel B -----------------------------------------------------------------
# Mode Index -------------------------------------------------------------------
BBtnIndex = Button(TLP2, 1)

# Mode Room --------------------------------------------------------------------
BRoomSplit = Button(TLP2, 240)
BRoomMixed = Button(TLP2, 241)

# Mode Main --------------------------------------------------------------------
# Mode Main - Lateral Bar
BBtnRoom    = Button(TLP2, 10)
BBtnSwitch  = Button(TLP2, 11)
BBtnDisplay = Button(TLP2, 12)
BBtnVC      = Button(TLP2, 13)
BBtnREC     = Button(TLP2, 14)
BBtnInfo    = Button(TLP2, 15)
BBtnPower   = Button(TLP2, 16)

# Mode Main - Up Bar
BLblMain    = Label(TLP2, 20)
BBtnRoom2   = Button(TLP2, 21)
BBtnRoom1   = Button(TLP2, 22)

# Mode Switching ---------------------------------------------------------------
# Outputs ----------------------------------------------------------------------
# XTP Out Slot 1
BBtnOut1  = Button(TLP2, 101) ##Room1 Projector
BBtnOut2  = Button(TLP2, 102) ##Room1 LCD Confidence
BBtnOut3  = Button(TLP2, 103) ##Room1 LCD Podium
# XTP Out Slot 2
BBtnOut5  = Button(TLP2, 105) ##Room2 Projector
BBtnOut6  = Button(TLP2, 106) ##Room2 LCD Confidence
BBtnOut7  = Button(TLP2, 107) ##Room2 LCD Podium
# XTP Out Slot 3
BBtnOut9  = Button(TLP2, 109) ##Core Tricaster 1 - Input 1
BBtnOut10 = Button(TLP2, 110) ##Core Tricaster 1 - Input 2
BBtnOut11 = Button(TLP2, 111) ##Core Tricaster 1 - Input 3
BBtnOut12 = Button(TLP2, 112) ##Core Tricaster 1 - Input 4
# XTP Out Slot 4
BBtnOut13 = Button(TLP2, 113) ##Core Tricaster 2 - Input 1
BBtnOut14 = Button(TLP2, 114) ##Core Tricaster 2 - Input 2
BBtnOut15 = Button(TLP2, 115) ##Core Tricaster 2 - Input 3
BBtnOut16 = Button(TLP2, 116) ##Core Tricaster 2 - Input 4
# XTP Out Slot 5
BBtnOut17 = Button(TLP2, 117) ##Core Cisco 1 - Input Camera
BBtnOut18 = Button(TLP2, 118) ##Core Cisco 1 - Input Graphics
BBtnOut19 = Button(TLP2, 119) ##Core Cisco 2 - Input Camera
BBtnOut20 = Button(TLP2, 120) ##Core Cisco 2 - Input Graphics
# XTP Out Slot 6
BBtnOut21 = Button(TLP2, 121) ##Core Recorder 1
BBtnOut22 = Button(TLP2, 122) ##Core Recorder 2

# Inputs -----------------------------------------------------------------------
# XTP Slot 1
BBtnInput1  = Button(TLP2, 201) ##Room1 PC Left
BBtnInput2  = Button(TLP2, 202) ##Room1 PC Right
BBtnInput3  = Button(TLP2, 203) ##Room1 PC Stage
BBtnInput4  = Button(TLP2, 204) ##Room1 PC Right
# XTP Slot 2
BBtnInput5  = Button(TLP2, 205) ##Room2 PC Left
BBtnInput6  = Button(TLP2, 206) ##Room2 PC Right
BBtnInput7  = Button(TLP2, 207) ##Room2 PC Stage
BBtnInput8  = Button(TLP2, 208) ##Room2 PC Back
# XTP Slot 3
BBtnInput9  = Button(TLP2, 209) ##Room1 PTZ1
BBtnInput10 = Button(TLP2, 210) ##Room1 PTZ2
BBtnInput11 = Button(TLP2, 211) ##Room2 PTZ1
BBtnInput12 = Button(TLP2, 212) ##Room2 PTZ2
# XTP Slot 4
BBtnInput13 = Button(TLP2, 213) ##Room1 PC Cabin
BBtnInput14 = Button(TLP2, 214) ##Room2 PC Cabin
##...
##...
# XTP Slot 5
BBtnInput17 = Button(TLP2, 217) ##Core Cisco 1 Out
BBtnInput18 = Button(TLP2, 218) ##Core Cisco 2 Out
BBtnInput19 = Button(TLP2, 219) ##Core ShareLink 1
BBtnInput20 = Button(TLP2, 220) ##Core ShareLink 2
# XTP Slot 6
BBtnInput21 = Button(TLP2, 221) ##Core Tricaster 1 - Out 1
BBtnInput22 = Button(TLP2, 222) ##Core Tricaster 2 - Out 1
# Input Signal Status
# XTP Slot 1
BBtnSignal1 = Button(TLP2, 130) ##Room1 PC Left
BBtnSignal2 = Button(TLP2, 131) ##Room1 PC Right
BBtnSignal3 = Button(TLP2, 132) ##Room1 PC Stage
BBtnSignal4 = Button(TLP2, 133) ##Room1 PC Right
# XTP Slot 2
BBtnSignal5 = Button(TLP2, 134) ##Room2 PC Left
BBtnSignal6 = Button(TLP2, 135) ##Room2 PC Right
BBtnSignal7 = Button(TLP2, 136) ##Room2 PC Stage
BBtnSignal8 = Button(TLP2, 137) ##Room2 PC Back
# XTP Slot 3
BBtnSignal9 = Button(TLP2, 138) ##Room1 PTZ1
BBtnSignal10 = Button(TLP2, 139) ##Room1 PTZ2
BBtnSignal11 = Button(TLP2, 140) ##Room2 PTZ1
BBtnSignal12 = Button(TLP2, 141) ##Room2 PTZ2
# XTP Slot 4
BBtnSignal13 = Button(TLP2, 142) ##Room1 PC Cabin
BBtnSignal14 = Button(TLP2, 143) ##Room2 PC Cabin
##...
##...
# XTP Slot 5
BBtnSignal17 = Button(TLP2, 144) ##Core Cisco 1 Out
BBtnSignal18 = Button(TLP2, 145) ##Core Cisco 2 Out
BBtnSignal19 = Button(TLP2, 146) ##Core ShareLink 1
BBtnSignal20 = Button(TLP2, 147) ##Core ShareLink 2
# XTP Slot 6
BBtnSignal21 = Button(TLP2, 148) ##Core Tricaster 1 - Out 1
BBtnSignal22 = Button(TLP2, 149) ##Core Tricaster 2 - Out 1

# Mode Display -----------------------------------------------------------------
# Room 1 - Projection
BBtnPwrProjA    = Button(TLP2, 30)
BBtnScreenAUp   = Button(TLP2, 31)
BBtnScreenADown = Button(TLP2, 32)
BBtnElevAUp     = Button(TLP2, 33)
BBtnElevADown   = Button(TLP2, 34)

# Room 1 - LCD
BLCDCab1    = Button(TLP2, 42)
BLCDCab2    = Button(TLP2, 41)
BLCDCab3    = Button(TLP2, 40)
BLCDLobby   = Button(TLP2, 43)
BLCDPodium1 = Button(TLP2, 48)

# Room 2 - Projection
BBtnPwrProjB    = Button(TLP2, 35)
BBtnScreenBUp   = Button(TLP2, 36)
BBtnScreenBDown = Button(TLP2, 37)
BBtnElevBUp     = Button(TLP2, 38)
BBtnElevBDown   = Button(TLP2, 39)

# Room 2 - LCD
B2LCDCab1   = Button(TLP2, 46)
B2LCDCab2   = Button(TLP2, 45)
B2LCDCab3   = Button(TLP2, 44)
B2LCDLobby  = Button(TLP2, 47)
BLCDPodium2 = Button(TLP2, 49)

# Mode Recording ---------------------------------------------------------------
# Recorder A - Record
BBtnRecAStop   = Button(TLP2, 60)
BBtnRecARecord = Button(TLP2, 61)
BBtnRecAPause  = Button(TLP2, 62)
BLblRecATime   = Label(TLP2, 63)

# Recorder A - Info
BLblRecA1 = Label(TLP2, 64)
BLblRecA2 = Label(TLP2, 65)
BLblRecA3 = Label(TLP2, 66)
BLblRecA4 = Label(TLP2, 67)
BLblRecA5 = Label(TLP2, 68)
BLblRecA6 = Label(TLP2, 69)

# Recorder B - Record
BBtnRecBStop   = Button(TLP2, 70)
BBtnRecBRecord = Button(TLP2, 71)
BBtnRecBPause  = Button(TLP2, 72)
BLblRecBTime   = Label(TLP2, 73)

# Recorder B - Info
BLblRecB1 = Label(TLP2, 74)
BLblRecB2 = Label(TLP2, 75)
BLblRecB3 = Label(TLP2, 76)
BLblRecB4 = Label(TLP2, 77)
BLblRecB5 = Label(TLP2, 78)
BLblRecB6 = Label(TLP2, 79)

# Mode VC ----------------------------------------------------------------------
# Cisco 1 ---------------------
BDial0      = Button(TLP2, 2130)
BDial1      = Button(TLP2, 2131)
BDial2      = Button(TLP2, 2132)
BDial3      = Button(TLP2, 2133)
BDial4      = Button(TLP2, 2134)
BDial5      = Button(TLP2, 2135)
BDial6      = Button(TLP2, 2136)
BDial7      = Button(TLP2, 2137)
BDial8      = Button(TLP2, 2138)
BDial9      = Button(TLP2, 2139)
BDialDot    = Button(TLP2, 2140)
BDialHash   = Button(TLP2, 2141)
BDialDelete = Button(TLP2, 2144, repeatTime=0.1)
# Call
BBtnVC1DTMF = Button(TLP2, 2142)
BBtnVC1Call = Button(TLP2, 2143)
# Answer
BBtnVC1Answer = Button(TLP2, 400)
BBtnVC1Reject = Button(TLP2, 401)
# Content
BBtnVC1ContenOn  = Button(TLP2, 2145)
BBtnVC1ContenOff = Button(TLP2, 2146)
# Label
BLblVC1Dial     = Label(TLP2, 2147)
BLblVC1Remote   = Label(TLP2, 2148)

# Cisco 2 -----------------------
B2Dial0      = Button(TLP2, 2100)
B2Dial1      = Button(TLP2, 2101)
B2Dial2      = Button(TLP2, 2102)
B2Dial3      = Button(TLP2, 2103)
B2Dial4      = Button(TLP2, 2104)
B2Dial5      = Button(TLP2, 2105)
B2Dial6      = Button(TLP2, 2106)
B2Dial7      = Button(TLP2, 2107)
B2Dial8      = Button(TLP2, 2108)
B2Dial9      = Button(TLP2, 2109)
B2DialDot    = Button(TLP2, 2110)
B2DialHash   = Button(TLP2, 2111)
B2DialDelete = Button(TLP2, 2114, repeatTime=0.1)
# Call
BBtnVC2DTMF = Button(TLP2, 2112)
BBtnVC2Call = Button(TLP2, 2113)
# Answer
BBtnVC2Answer = Button(TLP2, 402)
BBtnVC2Reject = Button(TLP2, 403)
# Content
BBtnVC2ContenOn  = Button(TLP2, 2115)
BBtnVC2ContenOff = Button(TLP2, 2116)
# Label
BLblVC2Dial   = Label(TLP2, 2117)
BLblVC2Remote = Label(TLP2, 2118)

# Mode Status ------------------------------------------------------------------
# Room 1
BLblLanProjA   = Button(TLP2, 302)
BLblinfo1ProjA = Label(TLP2, 303)
BLblinfo2ProjA = Label(TLP2, 304)
#
BBtnLanLCDCab3 = Button(TLP2, 310)
BBtnLanLCDCab4 = Button(TLP2, 311)
BBtnLanLCDLob1 = Button(TLP2, 322)
BBtnLanLCDPod1 = Button(TLP2, 324)
# Room 2
BLblLanProjB   = Button(TLP2, 305)
BLblinfo1ProjB = Label(TLP2, 306)
BLblinfo2ProjB = Label(TLP2, 307)
#
BBtnLanLCDCab1 = Button(TLP2, 308)
BBtnLanLCDCab2 = Button(TLP2, 309)
BBtnLanLCDLob2 = Button(TLP2, 323)
BBtnLanLCDPod2 = Button(TLP2, 325)
# Core
BBtnLanXTP    = Button(TLP2, 300)
#
BBtnLanTesira = Button(TLP2, 301)
#
BBtnLanVC1    = Button(TLP2, 312)
BLblinfo1VC1  = Label(TLP2, 313)
#
BBtnLanVC2    = Button(TLP2, 315)
BLblinfo1VC2  = Label(TLP2, 316)
#
BBtnLanRecA   = Button(TLP2, 318)
BLblinfo1RecA = Label(TLP2, 319)
#
BBtnLanRecB   = Button(TLP2, 320)
BLblinfo1RecB = Label(TLP2, 321)
# Build
BLblPython    = Label(TLP2, 326)

# Mode PowerOff ------------------------------------------------------------------
BBtnPowerAB   = Button(TLP2, 420, repeatTime=1, holdTime=3)
BBtnPowerA    = Button(TLP2, 421, repeatTime=1, holdTime=3)
BBtnPowerB    = Button(TLP2, 422, repeatTime=1, holdTime=3)
BLblPowerAB   = Label(TLP2, 430)
BLblPowerA    = Label(TLP2, 431)
BLblPowerB    = Label(TLP2, 432)

# BUTTON GROUPING --------------------------------------------------------------
# Mode Index
GroupModeIndex = [ABtnIndex, BBtnIndex]

# Mode Room
ModeRoom = [ARoomSplit, ARoomMixed, BRoomSplit, BRoomMixed]
#
GroupRoomA = MESet([ARoomSplit, ARoomMixed])
GroupRoomB = MESet([BRoomSplit, BRoomMixed])
GroupModeRoom = MESet(ModeRoom)

# Mode Main
ModeMain  = [ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC, ABtnREC, ABtnInfo, ABtnPower,
             BBtnRoom, BBtnSwitch, BBtnDisplay, BBtnVC, BBtnREC, BBtnInfo, BBtnPower]
#
GroupMainA = MESet([ABtnRoom, ABtnSwitch, ABtnDisplay, ABtnVC, ABtnREC, ABtnInfo, ABtnPower])
GroupMainB = MESet([BBtnRoom, BBtnSwitch, BBtnDisplay, BBtnVC, BBtnREC, BBtnInfo, BBtnPower])

# Mode Video Switching
OutputsA = [ABtnOut1, ABtnOut2, ABtnOut3, ABtnOut5, ABtnOut6,ABtnOut7, ABtnOut9, ABtnOut10, ABtnOut11,
            ABtnOut12, ABtnOut13, ABtnOut14, ABtnOut15, ABtnOut16, ABtnOut17, ABtnOut18, ABtnOut19,
            ABtnOut20, ABtnOut21, ABtnOut22]

OutputsB = [BBtnOut1, BBtnOut2, BBtnOut3, BBtnOut5, BBtnOut6,BBtnOut7, BBtnOut9, BBtnOut10, BBtnOut11,
            BBtnOut12, BBtnOut13, BBtnOut14, BBtnOut15, BBtnOut16, BBtnOut17, BBtnOut18, BBtnOut19,
            BBtnOut20, BBtnOut21, BBtnOut22]
#
InputsA = [ABtnInput1, ABtnInput2, ABtnInput3, ABtnInput4, ABtnInput5, ABtnInput6, ABtnInput7, 
           ABtnInput8, ABtnInput9, ABtnInput10, ABtnInput11, ABtnInput12, ABtnInput13,
           ABtnInput14, ABtnInput17, ABtnInput18, ABtnInput19, ABtnInput20, ABtnInput21, 
           ABtnInput22]

InputsB = [BBtnInput1, BBtnInput2, BBtnInput3, BBtnInput4, BBtnInput5, BBtnInput6, BBtnInput7, 
           BBtnInput8, BBtnInput9, BBtnInput10, BBtnInput11, BBtnInput12, BBtnInput13,
           BBtnInput14, BBtnInput17, BBtnInput18, BBtnInput19, BBtnInput20, BBtnInput21, 
           BBtnInput22]
#
GroupInputsA = MESet(InputsA)
GroupInputsB = MESet(InputsB)

GroupOutputsA = MESet(OutputsA)
GroupOutputsB = MESet(OutputsB)

# Mode Projection
ProjeccionA = [ABtnPwrProjA, ABtnScreenAUp, ABtnScreenADown, ABtnElevAUp, ABtnElevADown, ALCDCab1, ALCDCab2,
               ALCDCab3, ALCDLobby, ALCDPodium1,
               BBtnPwrProjA, BBtnScreenAUp, BBtnScreenADown, BBtnElevAUp, BBtnElevADown, BLCDCab1, BLCDCab2,
               BLCDCab3, BLCDLobby, BLCDPodium1]

ProjeccionB = [ABtnPwrProjB, ABtnScreenBUp, ABtnScreenBDown, ABtnElevBUp, ABtnElevBDown, A2LCDCab1, A2LCDCab2,
               A2LCDCab3, A2LCDLobby, ALCDPodium2,
               BBtnPwrProjB, BBtnScreenBUp, BBtnScreenBDown, BBtnElevBUp, BBtnElevBDown, B2LCDCab1, B2LCDCab2,
               B2LCDCab3, B2LCDLobby, BLCDPodium2]
#
GroupScreenA = MESet([ABtnScreenAUp, ABtnScreenADown])
GroupElevatA = MESet([ABtnElevAUp, ABtnElevADown])
#
GroupScreen2A = MESet([ABtnScreenBUp, ABtnScreenBDown])
GroupElevat2A = MESet([ABtnElevBUp, ABtnElevBDown])

# Mode Recording
GroupModeRec = [ABtnRecARecord, ABtnRecAStop, ABtnRecAPause, ABtnRecBRecord, ABtnRecBStop, ABtnRecBPause,
                BBtnRecARecord, BBtnRecAStop, BBtnRecAPause, BBtnRecBRecord, BBtnRecBStop, BBtnRecBPause]
#
GroupRecA1 = MESet([ABtnRecARecord, ABtnRecAStop, ABtnRecAPause])
GroupRecA2 = MESet([BBtnRecARecord, BBtnRecAStop, BBtnRecAPause])

GroupRecB1 = MESet([ABtnRecBRecord, ABtnRecBStop, ABtnRecBPause])
GroupRecB2 = MESet([BBtnRecBRecord, BBtnRecBStop, BBtnRecBPause])

# Mode Videoconference
VCDial = [ADial0, ADial1, ADial2, ADial3, ADial4, ADial5, ADial6, ADial7, ADial8, ADial9, ADialDot, ADialHash, ADialDelete,
          BDial0, BDial1, BDial2, BDial3, BDial4, BDial5, BDial6, BDial7, BDial8, BDial9, BDialDot, BDialHash, BDialDelete,]

VCButtons = [ABtnVC1Call, ABtnVC1DTMF, ABtnVC1ContenOn, ABtnVC1ContenOff, ABtnVC1Answer, ABtnVC1Reject,
             BBtnVC1Call, BBtnVC1DTMF, BBtnVC1ContenOn, BBtnVC1ContenOff, BBtnVC1Answer, BBtnVC1Reject]

GroupContentA1 = MESet([ABtnVC1ContenOn, ABtnVC1ContenOff])
GroupContentA2 = MESet([BBtnVC1ContenOn, BBtnVC1ContenOff])
#
VC2Dial = [A2Dial0, A2Dial1, A2Dial2, A2Dial3, A2Dial4, A2Dial5, A2Dial6, A2Dial7, A2Dial8, A2Dial9, A2DialDot, A2DialHash, A2DialDelete,
           B2Dial0, B2Dial1, B2Dial2, B2Dial3, B2Dial4, B2Dial5, B2Dial6, B2Dial7, B2Dial8, B2Dial9, B2DialDot, B2DialHash, B2DialDelete]

VC2Buttons = [ABtnVC2Call, ABtnVC2DTMF, ABtnVC2ContenOn, ABtnVC2ContenOff, ABtnVC2Answer, ABtnVC2Reject,
              BBtnVC2Call, BBtnVC2DTMF, BBtnVC2ContenOn, BBtnVC2ContenOff, BBtnVC2Answer, BBtnVC2Reject]

GroupContentB1 = MESet([ABtnVC2ContenOn, ABtnVC2ContenOff])
GroupContentB2 = MESet([BBtnVC2ContenOn, BBtnVC2ContenOff])

# Mode PowerOff
GroupPower = [ABtnPowerA, ABtnPowerB, ABtnPowerAB, BBtnPowerA, BBtnPowerB, BBtnPowerAB]

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
 
    ## PowerCounter Data Init
    global PowerCounterAB
    global PowerCounterA
    global PowerCounterB
    PowerCounterAB = 4
    PowerCounterA = 4
    PowerCounterB = 4

    ## Cisco1 Dial PAGE
    global dialerVC  ## To access the Dial String variable in all program
    dialerVC = ''    ## Clean the Dial String Variable
    ALblVC1Dial.SetText('')

    ## Cisco1 Dial PAGE
    global dialerVC2  ## To access the Dial String variable in all program
    dialerVC2 = ''    ## Clean the Dial String Variable
    ALblVC2Dial.SetText('')

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
    ALblPython.SetText('Extron API ' + Version())
    BLblPython.SetText('Extron API ' + Version())
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
            ABtnLanXTP.SetState(0)
            BBtnLanXTP.SetState(0)
        else:
            ABtnLanXTP.SetState(1)
            BBtnLanXTP.SetState(1)
    #
    elif command == 'InputSignal':
        # XTP Slot 1-------------------
        if qualifier['Input'] == '1':
            if value == 'Active':
                ABtnSignal1.SetState(1)
                BBtnSignal1.SetState(1)
            else:
                ABtnSignal1.SetState(0)
                BBtnSignal1.SetState(0)
        #
        elif qualifier['Input'] == '2':
            if value == 'Active':
                ABtnSignal2.SetState(1)
                BBtnSignal2.SetState(1)
            else:
                ABtnSignal2.SetState(0)
                BBtnSignal2.SetState(0)
        #
        if qualifier['Input'] == '3':
            if value == 'Active':
                ABtnSignal3.SetState(1)
                BBtnSignal3.SetState(1)
            else:
                ABtnSignal3.SetState(0)
                BBtnSignal3.SetState(0)
        #
        elif qualifier['Input'] == '4':
            if value == 'Active':
                ABtnSignal4.SetState(1)
                BBtnSignal4.SetState(1)
            else:
                ABtnSignal4.SetState(0)
                BBtnSignal4.SetState(0)
        #
        # XTP Slot 2--------------------
        if qualifier['Input'] == '5':
            if value == 'Active':
                ABtnSignal5.SetState(1)
                BBtnSignal5.SetState(1)
            else:
                ABtnSignal5.SetState(0)
                BBtnSignal5.SetState(0)
        #
        elif qualifier['Input'] == '6':
            if value == 'Active':
                ABtnSignal6.SetState(1)
                BBtnSignal6.SetState(1)
            else:
                ABtnSignal6.SetState(0)
                BBtnSignal6.SetState(0)
        #
        if qualifier['Input'] == '7':
            if value == 'Active':
                ABtnSignal7.SetState(1)
                BBtnSignal7.SetState(1)
            else:
                ABtnSignal7.SetState(0)
                BBtnSignal7.SetState(0)
        #
        elif qualifier['Input'] == '8':
            if value == 'Active':
                ABtnSignal8.SetState(1)
                BBtnSignal8.SetState(1)
            else:
                ABtnSignal8.SetState(0)
                BBtnSignal8.SetState(0)
        #
        # XTP Slot 3--------------------
        elif qualifier['Input'] == '9':
            if value == 'Active':
                ABtnSignal9.SetState(1)
                BBtnSignal9.SetState(1)
            else:
                ABtnSignal9.SetState(0)
                BBtnSignal9.SetState(0)
        #
        elif qualifier['Input'] == '10':
            if value == 'Active':
                ABtnSignal10.SetState(1)
                BBtnSignal10.SetState(1)
            else:
                ABtnSignal10.SetState(0)
                BBtnSignal10.SetState(0)
        #
        elif qualifier['Input'] == '11':
            if value == 'Active':
                ABtnSignal11.SetState(1)
                BBtnSignal11.SetState(1)
            else:
                ABtnSignal11.SetState(0)
                BBtnSignal11.SetState(0)
        #
        elif qualifier['Input'] == '12':
            if value == 'Active':
                ABtnSignal12.SetState(1)
                BBtnSignal12.SetState(1)
            else:
                ABtnSignal12.SetState(0)
                BBtnSignal12.SetState(0)
        #
        # XTP Slot 4--------------------
        elif qualifier['Input'] == '13':
            if value == 'Active':
                ABtnSignal13.SetState(1)
                BBtnSignal13.SetState(1)
            else:
                ABtnSignal13.SetState(0)
                BBtnSignal13.SetState(0)
        #
        elif qualifier['Input'] == '14':
            if value == 'Active':
                ABtnSignal14.SetState(1)
                BBtnSignal14.SetState(1)
            else:
                ABtnSignal14.SetState(0)
                BBtnSignal14.SetState(0)
        #
        # XTP Slot 5---------------------
        elif qualifier['Input'] == '17':
            if value == 'Active':
                ABtnSignal17.SetState(1)
                BBtnSignal17.SetState(1)
            else:
                ABtnSignal17.SetState(0)
                BBtnSignal17.SetState(0)
        #
        elif qualifier['Input'] == '18':
            if value == 'Active':
                ABtnSignal18.SetState(1)
                BBtnSignal18.SetState(1)
            else:
                ABtnSignal18.SetState(0)
                BBtnSignal18.SetState(0)
        #
        elif qualifier['Input'] == '19':
            if value == 'Active':
                ABtnSignal19.SetState(1)
                BBtnSignal19.SetState(1)
            else:
                ABtnSignal19.SetState(0)
                BBtnSignal19.SetState(0)
        #       
        elif qualifier['Input'] == '20':
            if value == 'Active':
                ABtnSignal20.SetState(1)
                BBtnSignal20.SetState(1)
            else:
                ABtnSignal20.SetState(0)
                BBtnSignal20.SetState(0)
        #
        # XTP Slot 6--------------------
        elif qualifier['Input'] == '21':
            if value == 'Active':
                ABtnSignal21.SetState(1)
                BBtnSignal21.SetState(1)
            else:
                ABtnSignal21.SetState(0)
                BBtnSignal21.SetState(0)
        #
        elif qualifier['Input'] == '22':
            if value == 'Active':
                ABtnSignal22.SetState(1)
                BBtnSignal22.SetState(1)
            else:
                ABtnSignal22.SetState(0)
                BBtnSignal22.SetState(0)
    #
    elif command == 'OutputTieStatus':
        if qualifier['Output'] == '21': #Recorder A (Extron SMP 111)
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    ALblRecA1.SetText('S1: PC Left')
                    BLblRecA1.SetText('S1: PC Left')
                elif value == '2':
                    ALblRecA1.SetText('S1: PC Right')
                    BLblRecA1.SetText('S1: PC Right')
                elif value == '3':
                    ALblRecA1.SetText('S1: PC Stage')
                    BLblRecA1.SetText('S1: PC Stage')
                elif value == '4':
                    ALblRecA1.SetText('S1: PC Back')
                    BLblRecA1.SetText('S1: PC Back')
                elif value == '5':
                    ALblRecA1.SetText('S2: PC Left')
                    BLblRecA1.SetText('S2: PC Left')
                elif value == '6':
                    ALblRecA1.SetText('S2: PC Right')
                    BLblRecA1.SetText('S2: PC Right')
                elif value == '7':
                    ALblRecA1.SetText('S2: PC Stage')
                    BLblRecA1.SetText('S2: PC Stage')
                elif value == '8':
                    ALblRecA1.SetText('S2: PC Back')
                    BLblRecA1.SetText('S2: PC Back')
                elif value == '9':
                    ALblRecA1.SetText('S1: PTZ Front')
                    BLblRecA1.SetText('S1: PTZ Front')
                elif value == '10':
                    ALblRecA1.SetText('S1: PTZ Back')
                    BLblRecA1.SetText('S1: PTZ Back')
                elif value == '11':
                    ALblRecA1.SetText('S2: PTZ Front')
                    BLblRecA1.SetText('S2: PTZ Front')
                elif value == '12':
                    ALblRecA1.SetText('S2: PTZ Back')
                    BLblRecA1.SetText('S2: PTZ Back')
                elif value == '13':
                    ALblRecA1.SetText('PC Cabina A')
                    BLblRecA1.SetText('PC Cabina A')
                elif value == '14':
                    ALblRecA1.SetText('PC Cabina B')
                    BLblRecA1.SetText('PC Cabina B')
                elif value == '17':
                    ALblRecA1.SetText('Cisco A')
                    BLblRecA1.SetText('Cisco A')
                elif value == '18':
                    ALblRecA1.SetText('Cisco B')
                    BLblRecA1.SetText('Cisco B')
                elif value == '19':
                    ALblRecA1.SetText('ShareLink A')
                    BLblRecA1.SetText('ShareLink A')
                elif value == '20':
                    ALblRecA1.SetText('ShareLink B')
                    BLblRecA1.SetText('ShareLink B')
                elif value == '21':
                    ALblRecA1.SetText('Tricaster A')
                    BLblRecA1.SetText('Tricaster A')
                elif value == '22':
                    ALblRecA1.SetText('Tricaster B')
                    BLblRecA1.SetText('Tricaster B')
        #
        elif qualifier['Output'] == '22': #Recorder B (Extron SMP 111)
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    ALblRecB1.SetText('S1: PC Left')
                    BLblRecB1.SetText('S1: PC Left')
                elif value == '2':
                    ALblRecB1.SetText('S1: PC Right')
                    BLblRecB1.SetText('S1: PC Right')
                elif value == '3':
                    ALblRecB1.SetText('S1: PC Stage')
                    BLblRecB1.SetText('S1: PC Stage')
                elif value == '4':
                    ALblRecB1.SetText('S1: PC Back')
                    BLblRecB1.SetText('S1: PC Back')
                elif value == '5':
                    ALblRecB1.SetText('S2: PC Left')
                    BLblRecB1.SetText('S2: PC Left')
                elif value == '6':
                    ALblRecB1.SetText('S2: PC Right')
                    BLblRecB1.SetText('S2: PC Right')
                elif value == '7':
                    ALblRecB1.SetText('S2: PC Stage')
                    BLblRecB1.SetText('S2: PC Stage')
                elif value == '8':
                    ALblRecB1.SetText('S2: PC Back')
                    BLblRecB1.SetText('S2: PC Back')
                elif value == '9':
                    ALblRecB1.SetText('S1: PTZ Front')
                    BLblRecB1.SetText('S1: PTZ Front')
                elif value == '10':
                    ALblRecB1.SetText('S1: PTZ Back')
                    BLblRecB1.SetText('S1: PTZ Back')
                elif value == '11':
                    ALblRecB1.SetText('S2: PTZ Front')
                    BLblRecB1.SetText('S2: PTZ Front')
                elif value == '12':
                    ALblRecB1.SetText('S2: PTZ Back')
                    BLblRecB1.SetText('S2: PTZ Back')
                elif value == '13':
                    ALblRecB1.SetText('PC Cabina A')
                    BLblRecB1.SetText('PC Cabina A')
                elif value == '14':
                    ALblRecB1.SetText('PC Cabina B')
                    BLblRecB1.SetText('PC Cabina B')
                elif value == '17':
                    ALblRecB1.SetText('Cisco A')
                    BLblRecB1.SetText('Cisco A')
                elif value == '18':
                    ALblRecB1.SetText('Cisco B')
                    BLblRecB1.SetText('Cisco B')
                elif value == '19':
                    ALblRecB1.SetText('ShareLink A')
                    BLblRecB1.SetText('ShareLink A')
                elif value == '20':
                    ALblRecB1.SetText('ShareLink B')
                    BLblRecB1.SetText('ShareLink B')
                elif value == '21':
                    ALblRecB1.SetText('Tricaster A')
                    BLblRecB1.SetText('Tricaster A')
                elif value == '22':
                    ALblRecB1.SetText('Tricaster B')
                    BLblRecB1.SetText('Tricaster B')
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
            ABtnLanTesira.SetState(0)
            BBtnLanTesira.SetState(0)
        else:
            ABtnLanTesira.SetState(1)
            BBtnLanTesira.SetState(1)
    #
    elif command == 'LogicState':
        if qualifier['Instance Tag'] == 'Room' and qualifier['Channel'] == '1':
            if value == 'True':
                Room_Data['Mixed'] = True
                Tesira.Set('PresetRecall', '1')
                GroupRoomA.SetCurrent(ARoomMixed)
                GroupRoomB.SetCurrent(BRoomMixed)
            else:
                Room_Data['Mixed'] = False
                Tesira.Set('PresetRecall', '2')
                GroupRoomA.SetCurrent(ARoomSplit)
                GroupRoomB.SetCurrent(BRoomSplit)
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
            ALblLanProjA.SetState(0)
            BLblLanProjA.SetState(0)
        else:
            ALblLanProjA.SetState(1)
            BLblLanProjA.SetState(1)
    #
    elif command == 'Power':
        ALblinfo1ProjA.SetText('Power ' + value)
        BLblinfo1ProjA.SetText('Power ' + value)
        print('--- Parsing Projector A: (Power ' +  value + ' )')
        if value == 'On':
            ABtnPwrProjA.SetState(1)
            BBtnPwrProjA.SetState(1)
            #Room1ElevatorDown()
            #Room1ScreenDown()
        else:
            ABtnPwrProjA.SetState(0)
            BBtnPwrProjA.SetState(0)
            #Room1ElevatorUp()
            #Room1ScreenUp()
    #
    elif command == 'Input':
        ALblinfo2ProjA.SetText(value)
        BLblinfo2ProjA.SetText(value)
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
            ALblLanProjB.SetState(0)
            BLblLanProjB.SetState(0)
        else:
            ALblLanProjB.SetState(1)
            BLblLanProjB.SetState(1)
    #
    elif command == 'Power':
        ALblinfo1ProjB.SetText('Power ' + value)
        BLblinfo1ProjB.SetText('Power ' + value)
        print('--- Parsing Projector B: (Power ' +  value + ' )')
        if value == 'On':
            ABtnPwrProjB.SetState(1)
            BBtnPwrProjB.SetState(1)
            #Room2ElevatorDown()
            #Room2ScreenDown()
        else:
            ABtnPwrProjB.SetState(0)
            BBtnPwrProjB.SetState(0)
            #Room2ElevatorUp()
            #Room2ScreenUp()
    #
    elif command == 'Input':
        ALblinfo2ProjB.SetText(value)
        BLblinfo2ProjB.SetText(value)
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
            ABtnLanVC1.SetState(0)
            BBtnLanVC1.SetState(0)
        else:
            ABtnLanVC1.SetState(1)
            BBtnLanVC1.SetState(1)
    #
    elif command == 'Presentation':
        print('--- Parsing Cisco 1: (Presentation ' +  value + ' )')
        if value == '2':
            GroupContentA1.SetCurrent(ABtnVC1ContenOn)
            GroupContentA2.SetCurrent(BBtnVC1ContenOn)
        elif value == 'Stop':
            GroupContentA1.SetCurrent(ABtnVC1ContenOff)
            GroupContentA1.SetCurrent(BBtnVC1ContenOff)
    #
    elif command == 'CallStatus':
        print('--- Parsing Cisco 2: (CallStatus ' +  value + ' )')
        ALblinfo1VC1.SetText(value)
        BLblinfo1VC1.SetText(value)
        #
        if value == 'Ringing':
            if Room_Data['Mixed'] == True:
                TLP1.ShowPopup('Cisco1.Call')
                TLP2.ShowPopup('Cisco1.Call')
            else:
                TLP1.ShowPopup('Cisco1.Call')
        else:
            if Room_Data['Mixed'] == True:
                TLP1.HidePopup('Cisco1.Call')
                TLP2.HidePopup('Cisco1.Call')
            else:
                TLP1.HidePopup('Cisco1.Call')
        #
        if value == 'Idle' or value == 'Disconnecting':
            ABtnVC1Call.SetState(0)
            BBtnVC1Call.SetState(0)
            ABtnVC1Call.SetText('Llamar')
            BBtnVC1Call.SetText('Llamar')
        #
        elif value == 'Connected' or value == 'Connecting':
            ABtnVC1Call.SetState(1)
            BBtnVC1Call.SetState(1)
            ABtnVC1Call.SetText('Colgar')
            BBtnVC1Call.SetText('Colgar')
    #
    elif command == 'DisplayName':
        print('--- Parsing Cisco 1: (DisplayName ' +  value + ' )')
        ALblVC1Remote.SetText(value)
        BLblVC1Remote.SetText(value)
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
            ABtnLanVC2.SetState(0)
            BBtnLanVC2.SetState(0)
        else:
            ABtnLanVC2.SetState(1)
            BBtnLanVC2.SetState(1)
    #
    elif command == 'Presentation':
        print('--- Parsing Cisco 2: (Presentation ' +  value + ' )')
        if value == '2':
            GroupContentB1.SetCurrent(ABtnVC2ContenOn)
            GroupContentB2.SetCurrent(BBtnVC2ContenOn)
        elif value == 'Stop':
            GroupContentB1.SetCurrent(ABtnVC2ContenOff)
            GroupContentB2.SetCurrent(BBtnVC2ContenOff)
    #
    elif command == 'CallStatus':
        ALblinfo1VC2.SetText(value)
        BLblinfo1VC2.SetText(value)
        print('--- Parsing Cisco 2: (CallStatus ' +  value + ' )')
        #
        if value == 'Ringing':
            if Room_Data['Mixed'] == True:
                TLP1.ShowPopup('Cisco2.Call')
                TLP2.ShowPopup('Cisco2.Call')
            else:
                TLP2.ShowPopup('Cisco2.Call')
        else:
            if Room_Data['Mixed'] == True:
                TLP1.HidePopup('Cisco2.Call')
                TLP2.HidePopup('Cisco2.Call')
            else:
                TLP2.HidePopup('Cisco2.Call')
        #
        if value == 'Idle' or value == 'Disconnecting':
            ABtnVC2Call.SetState(0)
            BBtnVC2Call.SetState(0)
            ABtnVC2Call.SetText('Llamar')
            BBtnVC2Call.SetText('Llamar')
        #
        elif value == 'Connected' or value == 'Connecting':
            ABtnVC2Call.SetState(1)
            BBtnVC2Call.SetState(1)
            ABtnVC2Call.SetText('Colgar')
            BBtnVC2Call.SetText('Colgar')
    #
    elif command == 'DisplayName':
        print('--- Parsing Cisco 2: (DisplayName ' +  value + ' )')
        ALblVC2Remote.SetText(value)
        BLblVC2Remote.SetText(value)
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
            ABtnLanRecA.SetState(0)
            BBtnLanRecA.SetState(0)
        else:
            ABtnLanRecA.SetState(1)
            BBtnLanRecA.SetState(1)
    #
    elif command == 'Record':
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
        ALblinfo1RecA.SetText(value)
        BLblinfo1RecA.SetText(value)
        if value == 'Start':
            GroupRecA1.SetCurrent(ABtnRecARecord)
            GroupRecA2.SetCurrent(BBtnRecARecord)
        elif value == 'Pause':
            GroupRecA1.SetCurrent(ABtnRecAPause)
            GroupRecA2.SetCurrent(BBtnRecAPause)
        elif value == 'Stop':
            GroupRecA1.SetCurrent(ABtnRecAStop)
            GroupRecA2.SetCurrent(BBtnRecAStop)
            
    #
    elif command == 'RecordDestination':
        ALblRecA2.SetText(value)
        BLblRecA2.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'RecordingMode':
        ALblRecA4.SetText(value)
        BLblRecA4.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'VideoResolution':
        ALblRecA3.SetText(value)
        BLblRecA3.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'HDCPStatus':
        ALblRecA6.SetText(value)
        BLblRecA6.SetText(value)
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
    #
    elif command == 'RemainingFreeDiskSpace':
        if qualifier['Drive'] == 'Primary':
            value = int(value / 1024)
            ALblRecA5.SetText('Disk Free: ' + str(value) + 'GB')
            BLblRecA5.SetText('Disk Free: ' + str(value) + 'GB')
            #print('--- Parsing Recorder A: ' + command + ' ' + str(value))
    #
    elif command == 'CurrentRecordingDuration':
        #print('--- Parsing Recorder A: ' + command + ' ' + value)
        ALblRecATime.SetText(value)
        BLblRecATime.SetText(value)
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
            ABtnLanRecB.SetState(0)
            BBtnLanRecB.SetState(0)
        else:
            ABtnLanRecB.SetState(1)
            BBtnLanRecB.SetState(1)
    #
    elif command == 'Record':
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
        ALblinfo1RecB.SetText(value)
        BLblinfo1RecB.SetText(value)
        if value == 'Start':
            GroupRecB1.SetCurrent(ABtnRecBRecord)
            GroupRecB2.SetCurrent(BBtnRecBRecord)
        elif value == 'Pause':
            GroupRecB1.SetCurrent(ABtnRecBPause)
            GroupRecB2.SetCurrent(BBtnRecBPause)
        elif value == 'Stop':
            GroupRecB1.SetCurrent(ABtnRecBStop)
            GroupRecB2.SetCurrent(BBtnRecBStop)
    #
    elif command == 'RecordDestination':
        ALblRecB2.SetText(value)
        BLblRecB2.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'RecordingMode':
        ALblRecB4.SetText(value)
        BLblRecB4.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'VideoResolution':
        ALblRecB3.SetText(value)
        BLblRecB3.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'HDCPStatus':
        ALblRecB6.SetText(value)
        BLblRecB6.SetText(value)
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
    #
    elif command == 'RemainingFreeDiskSpace':
        if qualifier['Drive'] == 'Primary':
            value = int(value / 1024)
            ALblRecB5.SetText('Disk Free: ' + str(value) + 'GB')
            BLblRecB5.SetText('Disk Free: ' + str(value) + 'GB')
            #print('--- Parsing Recorder B: ' + command + ' ' + str(value))
    #
    elif command == 'CurrentRecordingDuration':
        #print('--- Parsing Recorder B: ' + command + ' ' + value)
        ALblRecBTime.SetText(value)
        BLblRecBTime.SetText(value)
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
            ABtnLanLCDCab1.SetState(0)
            BBtnLanLCDCab1.SetState(0)
        else:
            ABtnLanLCDCab1.SetState(1)
            BBtnLanLCDCab1.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab1: (Power ' +  value + ' )')
        if value == 'On':
            A2LCDCab2.SetState(1)
            B2LCDCab2.SetState(1)
        else:
            A2LCDCab2.SetState(0)
            B2LCDCab2.SetState(0)
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
            ABtnLanLCDCab2.SetState(0)
            BBtnLanLCDCab2.SetState(0)
        else:
            ABtnLanLCDCab2.SetState(1)
            BBtnLanLCDCab2.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab2: (Power ' +  value + ' )')
        if value == 'On':
            A2LCDCab3.SetState(1)
            B2LCDCab3.SetState(1)
        else:
            A2LCDCab3.SetState(0)
            B2LCDCab3.SetState(0)
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
            ABtnLanLCDCab3.SetState(0)
            BBtnLanLCDCab3.SetState(0)
        else:
            ABtnLanLCDCab3.SetState(1)
            BBtnLanLCDCab3.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab3: (Power ' +  value + ' )')
        if value == 'On':
            ALCDCab1.SetState(1)
            BLCDCab1.SetState(1)
        else:
            ALCDCab1.SetState(0)
            BLCDCab1.SetState(0)
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
            ABtnLanLCDCab4.SetState(0)
            BBtnLanLCDCab4.SetState(0)
        else:
            ABtnLanLCDCab4.SetState(1)
            BBtnLanLCDCab4.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Cab4: (Power ' +  value + ' )')
        if value == 'On':
            ALCDCab2.SetState(1)
            BLCDCab2.SetState(1)
        else:
            ALCDCab2.SetState(0)
            BLCDCab2.SetState(0)
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
            ABtnLanLCDLob1.SetState(0)
            BBtnLanLCDLob1.SetState(0)
        else:
            ABtnLanLCDLob1.SetState(1)
            BBtnLanLCDLob1.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Lob1: (Power ' +  value + ' )')
        if value == 'On':
            ALCDLobby.SetState(1)
            BLCDLobby.SetState(1)
        else:
            ALCDLobby.SetState(0)
            BLCDLobby.SetState(0)
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
            ABtnLanLCDLob2.SetState(0)
            BBtnLanLCDLob2.SetState(0)
        else:
            ABtnLanLCDLob2.SetState(1)
            BBtnLanLCDLob2.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Lob2: (Power ' +  value + ' )')
        if value == 'On':
            A2LCDLobby.SetState(1)
            B2LCDLobby.SetState(1)
        else:
            A2LCDLobby.SetState(0)
            B2LCDLobby.SetState(0)
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
            ABtnLanLCDPod1.SetState(0)
            BBtnLanLCDPod1.SetState(0)
        else:
            ABtnLanLCDPod1.SetState(1)
            BBtnLanLCDPod1.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Pod1: (Power ' +  value + ' )')
        if value == 'On':
            ALCDPodium1.SetState(1)
            BLCDPodium1.SetState(1)
        else:
            ALCDPodium1.SetState(0)
            BLCDPodium1.SetState(0)
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
            ABtnLanLCDPod2.SetState(0)
            BBtnLanLCDPod2.SetState(0)
        else:
            ABtnLanLCDPod2.SetState(1)
            BBtnLanLCDPod2.SetState(1)
    #
    elif command == 'Power':
        print('--- Parsing LCD Pod2: (Power ' +  value + ' )')
        if value == 'On':
            ALCDPodium2.SetState(1)
            BLCDPodium2.SetState(1)
        else:
            ALCDPodium2.SetState(0)
            BLCDPodium2.SetState(0)
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
    Cisco1.SubscribeStatus('CallStatus', {'Call':'1'}, ReceiveCisco1)
    Cisco1.SubscribeStatus('DisplayName', {'Call':'1'}, ReceiveCisco1)
    Cisco1.SubscribeStatus('RemoteNumber', {'Call':'1'}, ReceiveCisco1)
    pass
SubscribeCisco1()
#
def SubscribeCisco2():
    Cisco2.SubscribeStatus('ConnectionStatus', None, ReceiveCisco2)
    Cisco2.SubscribeStatus('Presentation', {'Instance':'1'}, ReceiveCisco2)
    Cisco2.SubscribeStatus('CallStatus', {'Call':'1'}, ReceiveCisco2)
    Cisco2.SubscribeStatus('DisplayName', {'Call':'1'}, ReceiveCisco2)
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
        ABtnLanXTP.SetState(1)
        reconnectWaitXTP.Cancel()
    else:
        ABtnLanXTP.SetState(0)
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
        ABtnLanTesira.SetState(1)
        BBtnLanTesira.SetState(1)
        reconnectWaitTesira.Cancel()
    else:
        ABtnLanTesira.SetState(0)
        BBtnLanTesira.SetState(0)
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
        ALblLanProjA.SetState(1)
        reconnectWaitProjectorA.Cancel()
    else:
        ALblLanProjA.SetState(0)
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
        ALblLanProjB.SetState(1)
        reconnectWaitProjectorB.Cancel()
    else:
        ALblLanProjB.SetState(0)
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
        ABtnLanVC1.SetState(1)
        reconnectWaitCisco1.Cancel()
    else:
        print('Socket Disconnected: Cisco1')
        ABtnLanVC1.SetState(0)
    pass

@event(Cisco2, 'Disconnected')
@event(Cisco2, 'Connected')
def Cisco2_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        ABtnLanVC2.SetState(1)
        reconnectWaitCisco2.Cancel()
    else:
        print('Socket Disconnected: Cisco2')
        ABtnLanVC2.SetState(0)
    pass

@event(RecA, 'Disconnected')
@event(RecA, 'Connected')
def RecA_PhysicalConex(interface, state):
    """If the TCP Connection has been established physically, stop attempting
       reconnects. This can be triggered by the initial TCP connect attempt in
       the Initialize function or from the connection attemps from
       AttemptConnectProjector"""
    if state == 'Connected':
        ABtnLanRecA.SetState(1)
        reconnectWaitRecA.Cancel()
    else:
        ABtnLanRecA.SetState(0)
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
        ABtnLanRecB.SetState(1)
        reconnectWaitRecB.Cancel()
    else:
        ABtnLanRecB.SetState(0)
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
        ABtnLanLCDCab1.SetState(1)
        reconnectWaitLCDCab1.Cancel()
    else:
        ABtnLanLCDCab1.SetState(0)
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
        ABtnLanLCDCab2.SetState(1)
        reconnectWaitLCDCab2.Cancel()
    else:
        ABtnLanLCDCab2.SetState(0)
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
        ABtnLanLCDCab3.SetState(1)
        reconnectWaitLCDCab3.Cancel()
    else:
        ABtnLanLCDCab3.SetState(0)
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
        ABtnLanLCDCab4.SetState(1)
        reconnectWaitLCDCab4.Cancel()
    else:
        ABtnLanLCDCab4.SetState(0)
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
        ABtnLanLCDLob1.SetState(1)
        reconnectWaitLCDLob1.Cancel()
    else:
        ABtnLanLCDLob1.SetState(0)
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
        ABtnLanLCDLob2.SetState(1)
        reconnectWaitLCDLob2.Cancel()
    else:
        ABtnLanLCDLob2.SetState(0)
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
        ABtnLanLCDPod1.SetState(1)
        reconnectWaitLCDPod1.Cancel()
    else:
        ABtnLanLCDPod1.SetState(0)
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
        ABtnLanLCDPod2.SetState(1)
        reconnectWaitLCDPod2.Cancel()
    else:
        ABtnLanLCDPod2.SetState(0)
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
@event(GroupModeIndex, ButtonEventList)
def Index(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if state == 'Pressed':
        button.SetState(1)
        #
        if Room_Data['Mixed'] == True:
            TLP1.ShowPage('Main')
            TLP2.ShowPage('Main')
            print("Touch: {0}".format("Index"))
        else:
            if button.Host.DeviceAlias == 'TouchPanelA':
                TLP1.ShowPage('Main')
                print("Touch 1: {0}".format("Index"))
            else:
                TLP2.ShowPage('Main')
                print("Touch 2: {0}".format("Index"))
    else:
        button.SetState(0)
    pass

def FunctionMixRoom():
    """This prepare the room to be used in mode Mixed"""
    ## Store the data in dictionary
    Tesira.Set('LogicState', 'True', {'Instance Tag':'Room', 'Channel':'1'})
    Room_Data['Mixed'] = True
    Tesira.Set('PresetRecall', '1')
    ## Activate button feedback
    ABtnRoom1.SetState(1)
    ABtnRoom2.SetState(1)
    BBtnRoom1.SetState(1)
    BBtnRoom2.SetState(1)
    GroupRoomA.SetCurrent(ARoomMixed)
    GroupRoomB.SetCurrent(BRoomMixed)
    # TouchPanel Actions
    TLP1.ShowPopup('Room')
    TLP2.ShowPopup('Room')
    GroupMainA.SetCurrent(ABtnRoom)
    GroupMainB.SetCurrent(BBtnRoom)
    ALblMain.SetText('Configuración de Sala')
    BLblMain.SetText('Configuración de Sala')
    ## Notify to console
    print("Room Mixed")
    pass

def FunctionSplitRoom():
    ## Store the data in dictionary
    Tesira.Set('LogicState', 'False', {'Instance Tag':'Room', 'Channel':'1'})
    Room_Data['Mixed'] = False
    Tesira.Set('PresetRecall', '2')
    ## Activate button feedback
    ABtnRoom1.SetState(1)
    ABtnRoom2.SetState(0)
    BBtnRoom1.SetState(0)
    BBtnRoom2.SetState(1)
    GroupRoomA.SetCurrent(ARoomSplit)
    GroupRoomB.SetCurrent(BRoomSplit)
    # TouchPanel Actions
    TLP1.ShowPopup('Room')
    TLP2.ShowPopup('Room')
    GroupMainA.SetCurrent(ABtnRoom)
    GroupMainB.SetCurrent(BBtnRoom)
    ALblMain.SetText('Configuración de Sala')
    BLblMain.SetText('Configuración de Sala')
    ## Notify to console
    print("Room Split")
    pass

# ACTIONS - ROOM CONFIGURATION MODE --------------------------------------------
## Room Page
@event(ModeRoom, 'Pressed')
def Room(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    # Validate the Active TouchPanel
    if button.ID == 241:
        FunctionMixRoom()
    else:
        FunctionSplitRoom()
    pass

# ACTIONS - MAIN OPERATION MODE ------------------------------------------------
@event(ModeMain, 'Pressed')
def FullMain(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    # Validate the Active TouchPanel
    if button.Host.DeviceAlias == 'TouchPanelA':
        Panel = TLP1
        Label = ALblMain
        Group = GroupMainA
        PanelID = 'Touch 1'
    else:
        Panel = TLP2
        Label = BLblMain
        Group = GroupMainB
        PanelID = 'Touch 2'
    
    # Validate the Active Room Configuration
    if Room_Data['Mixed'] == True:
        #
        TLP1.HideAllPopups()
        TLP2.HideAllPopups()
        #
        # Validate Buttons Actions
        if button.ID == 10: #Room
            print(PanelID + ": {0}".format("Mode Room"))
            #
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')
            GroupMainA.SetCurrent(ABtnRoom)
            GroupMainB.SetCurrent(BBtnRoom)
            ALblMain.SetText('Configuración de Sala')
            BLblMain.SetText('Configuración de Sala')
        #
        elif button.ID == 11: #Switching
            print(PanelID + ": {0}".format("Mode Switching"))
            #
            TLP1.ShowPopup('Full.Inputs')
            TLP2.ShowPopup('Full.Inputs')
            TLP1.ShowPopup('Full.Outputs')
            TLP2.ShowPopup('Full.Outputs')
            GroupMainA.SetCurrent(ABtnSwitch)
            GroupMainB.SetCurrent(BBtnSwitch)
            ALblMain.SetText('Switcheo de Videos')
            BLblMain.SetText('Switcheo de Videos')
        #
        elif button.ID == 12: #Displays
            print(PanelID + ": {0}".format("Mode Display"))
            #
            TLP1.ShowPopup('Full.Displays')
            TLP2.ShowPopup('Full.Displays')
            GroupMainA.SetCurrent(ABtnDisplay)
            GroupMainB.SetCurrent(BBtnDisplay)
            ALblMain.SetText('Control de Display')
            BLblMain.SetText('Control de Display')
        #
        elif button.ID == 13: #Videoconference
            print(PanelID + ": {0}".format("Mode VC"))
            Cisco1.Set('Standby', 'Deactivate')
            Cisco2.Set('Standby', 'Deactivate')
            #
            TLP1.ShowPopup('Full.VC')
            TLP2.ShowPopup('Full.VC')
            GroupMainA.SetCurrent(ABtnVC)
            GroupMainB.SetCurrent(BBtnVC)
            ALblMain.SetText('Control de Videoconferencia')
            BLblMain.SetText('Control de Videoconferencia')
        #
        elif button.ID == 14: #Recorder
            print(PanelID + ": {0}".format("Mode REC"))
            #
            TLP1.ShowPopup('Full.Rec')
            TLP2.ShowPopup('Full.Rec')
            GroupMainA.SetCurrent(ABtnREC)
            GroupMainB.SetCurrent(BBtnREC)
            ALblMain.SetText('Control de Grabación')
            BLblMain.SetText('Control de Grabación')
        #
        elif button.ID == 15: #Info
            print(PanelID + ": {0}".format("Mode Info"))
            #
            TLP1.ShowPopup('Full.Info')
            TLP2.ShowPopup('Full.Info')
            GroupMainA.SetCurrent(ABtnInfo)
            GroupMainB.SetCurrent(BBtnInfo)
            ALblMain.SetText('Información de Dispositivos')
            BLblMain.SetText('Información de Dispositivos')
        #
        elif button.ID == 16: #PowerOff
            print(PanelID + ": {0}".format("Mode PowerOff"))
            #
            TLP1.ShowPopup('Full.Power')
            TLP2.ShowPopup('Full.Power')
            GroupMainA.SetCurrent(ABtnPower)
            GroupMainB.SetCurrent(BBtnPower)
            ALblMain.SetText('Apagado General')
            BLblMain.SetText('Apagado General')
        #
    else: # SPLIT ROOM
        #
        Group.SetCurrent(button)
        Panel.HideAllPopups()
        #
        # Validate Buttons Actions
        if button.ID == 10: #Room
            print(PanelID + ": {0}".format("Mode Room"))
            #
            Panel.HideAllPopups()
            Panel.ShowPopup('Room')
            Label.SetText('Configuración de Sala')
        #
        elif button.ID == 11: #Switching
            print(PanelID + ": {0}".format("Mode Switching"))
            Label.SetText('Switcheo de Videos')
            #
            if Panel == TLP1:
                Panel.ShowPopup('Split.OutputsA')
                Panel.ShowPopup('Full.Inputs')
            else:
                Panel.ShowPopup('Split.OutputsB')
                Panel.ShowPopup('Full.Inputs')
        #
        elif button.ID == 12: #Displays
            print(PanelID + ": {0}".format("Mode Display"))
            Label.SetText('Control de Displays')            
            #
            if Panel == TLP1:
                Panel.ShowPopup('Split.DisplaysA')
            else:
                Panel.ShowPopup('Split.DisplaysB')
        #
        elif button.ID == 13: #Videoconference
            print(PanelID + ": {0}".format("Mode VC"))
            Cisco1.Set('Standby', 'Deactivate')
            Cisco2.Set('Standby', 'Deactivate')
            Label.SetText('Control de Videoconferencia')
            #
            if Panel == TLP1:
                Panel.ShowPopup('Split.Cisco1')
            else:
                Panel.ShowPopup('Split.Cisco2')
        #
        elif button.ID == 14: #Recorder
            print(PanelID + ": {0}".format("Mode VC"))
            Label.SetText('Control de Grabación')
            #
            if Panel == TLP1:
                Panel.ShowPopup('Split.RecA')
            else:
                Panel.ShowPopup('Split.RecB')
        #
        elif button.ID == 15: #Info
            print(PanelID + ": {0}".format("Mode Info"))
            Label.SetText('Información de Dispositivos')
            Panel.ShowPopup('Full.Info')
        #
        elif button.ID == 16: #PowerOff
            print(PanelID + ": {0}".format("Mode PowerOff"))
            Label.SetText('Apagado General')
            #
            if Panel == TLP1:
                Panel.ShowPopup('Split.PowerA')
            else:
                Panel.ShowPopup('Split.PowerB')
    pass

# ACTIONS - MATRIX TIE INFO FUNCTIONS ------------------------------------------
def FunctionActiveTie(output, touch):
    '''This retrieve the real Output-Input Video Relation when the user push the Display button'''
    activeTie = XTP.ReadStatus('OutputTieStatus', {'Output':output, 'Tie Type':'Video'})
    ##
    if touch == 'TLP1':
        if activeTie == '0':
            GroupInputsA.SetCurrent(None)
        elif activeTie == '1':
            GroupInputsA.SetCurrent(ABtnInput1)
        elif activeTie == '2':
            GroupInputsA.SetCurrent(ABtnInput2)
        elif activeTie == '3':
            GroupInputsA.SetCurrent(ABtnInput3)
        elif activeTie == '4':
            GroupInputsA.SetCurrent(ABtnInput4)
        ##
        elif activeTie == '5':
            GroupInputsA.SetCurrent(ABtnInput5)
        elif activeTie == '6':
            GroupInputsA.SetCurrent(ABtnInput6)
        elif activeTie == '7':
            GroupInputsA.SetCurrent(ABtnInput7)
        elif activeTie == '8':
            GroupInputsA.SetCurrent(ABtnInput8)
        ##
        elif activeTie == '9':
            GroupInputsA.SetCurrent(ABtnInput9)
        elif activeTie == '10':
            GroupInputsA.SetCurrent(ABtnInput10)
        elif activeTie == '11':
            GroupInputsA.SetCurrent(ABtnInput11)
        elif activeTie == '12':
            GroupInputsA.SetCurrent(ABtnInput12)
        ##
        elif activeTie == '13':
            GroupInputsA.SetCurrent(ABtnInput13)
        elif activeTie == '14':
            GroupInputsA.SetCurrent(ABtnInput14)
        ##
        elif activeTie == '17':
            GroupInputsA.SetCurrent(ABtnInput17)
        elif activeTie == '18':
            GroupInputsA.SetCurrent(ABtnInput18)
        elif activeTie == '19':
            GroupInputsA.SetCurrent(ABtnInput19)
        elif activeTie == '20':
            GroupInputsA.SetCurrent(ABtnInput20)
        ##
        elif activeTie == '21':
            GroupInputsA.SetCurrent(ABtnInput21)
        elif activeTie == '22':
            GroupInputsA.SetCurrent(ABtnInput22)
    else:
        if activeTie == '0':
            GroupInputsB.SetCurrent(None)
        elif activeTie == '1':
            GroupInputsB.SetCurrent(BBtnInput1)
        elif activeTie == '2':
            GroupInputsB.SetCurrent(BBtnInput2)
        elif activeTie == '3':
            GroupInputsB.SetCurrent(BBtnInput3)
        elif activeTie == '4':
            GroupInputsB.SetCurrent(BBtnInput4)
        ##
        elif activeTie == '5':
            GroupInputsB.SetCurrent(BBtnInput5)
        elif activeTie == '6':
            GroupInputsB.SetCurrent(BBtnInput6)
        elif activeTie == '7':
            GroupInputsB.SetCurrent(BBtnInput7)
        elif activeTie == '8':
            GroupInputsB.SetCurrent(BBtnInput8)
        ##
        elif activeTie == '9':
            GroupInputsB.SetCurrent(BBtnInput9)
        elif activeTie == '10':
            GroupInputsB.SetCurrent(BBtnInput10)
        elif activeTie == '11':
            GroupInputsB.SetCurrent(BBtnInput11)
        elif activeTie == '12':
            GroupInputsB.SetCurrent(BBtnInput12)
        ##
        elif activeTie == '13':
            GroupInputsB.SetCurrent(BBtnInput13)
        elif activeTie == '14':
            GroupInputsB.SetCurrent(BBtnInput14)
        ##
        elif activeTie == '17':
            GroupInputsB.SetCurrent(BBtnInput17)
        elif activeTie == '18':
            GroupInputsB.SetCurrent(BBtnInput18)
        elif activeTie == '19':
            GroupInputsB.SetCurrent(BBtnInput19)
        elif activeTie == '20':
            GroupInputsB.SetCurrent(BBtnInput20)
        ##
        elif activeTie == '21':
            GroupInputsB.SetCurrent(BBtnInput21)
        elif activeTie == '22':
            GroupInputsB.SetCurrent(BBtnInput22)
    pass

# ACTIONS - SWITCHING VIDEO OUTPUTS MODE ---------------------------------------
@event(OutputsA + OutputsB, 'Pressed')
def OutsSwitching(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    ## Data Init
    global output
    global touch
    ## Mutually Exclusive
    if button.Host.DeviceAlias == 'TouchPanelA':
        touch = 'TLP1'
        GroupOutputsA.SetCurrent(button)
    else:
        touch = 'TLP2'
        GroupOutputsB.SetCurrent(button)

    # XTP Slot 1-----------------------------------------------------
    if button.ID == 101:
        output = '1'
        print("Touch: {0}".format("Out Room 1: Projector"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 102:
        output = '2'
        print("Touch: {0}".format("Out Room 1: LCD Podium"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 103:
        output = '3'
        print("Touch: {0}".format("Out Room 1: LCD Lobby"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    
    #XTP Slot 2-----------------------------------------------------
    elif button.ID == 105:
        output = '5'
        print("Touch 1: {0}".format("Out Room 2: Projector"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 106:
        output = '6'
        print("Touch 1: {0}".format("Out Room 2: LCD Podium"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 107:
        output = '7'
        print("Touch 1: {0}".format("Out Room 2: LCD Lobby"))
        ##Recall Function
        FunctionActiveTie(output, touch)

    #XTP Slot 3-----------------------------------------------------
    elif button.ID == 109:
        output = '9'
        print("Touch 1: {0}".format("Out Room 1: Tricaster In 1"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 110:
        output = '10'
        print("Touch 1: {0}".format("Out Room 1: Tricaster In 2"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 111:
        output = '11'
        print("Touch 1: {0}".format("Out Room 1: Tricaster In 3"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 112:
        output = '12'
        print("Touch 1: {0}".format("Out Room 1: Tricaster In 4"))
        ##Recall Function
        FunctionActiveTie(output, touch)

    #XTP Slot 4-----------------------------------------------------
    elif button.ID == 113:
        output = '13'
        print("Touch 1: {0}".format("Out Room 2: Tricaster In 1"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 114:
        output = '14'
        print("Touch 1: {0}".format("Out Room 2: Tricaster In 2"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 115:
        output = '15'
        print("Touch 1: {0}".format("Out Room 2: Tricaster In 3"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 116:
        output = '16'
        print("Touch 1: {0}".format("Out Room 2: Tricaster In 4"))
        ##Recall Function
        FunctionActiveTie(output, touch)
        
    #XTP Slot 5------------------------------------------------------
    elif button.ID == 117:
        output = '17'
        print("Touch 1: {0}".format("Out Room 1: Cisco Camera"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 118:
        output = '18'
        print("Touch 1: {0}".format("Out Room 1: Cisco Graphics"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 119:
        output = '19'
        print("Touch 1: {0}".format("Out Room 2: Cisco Camera"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 120:
        output = '20'
        print("Touch 1: {0}".format("Out Room 2: Cisco Graphics"))
        ##Recall Function
        FunctionActiveTie(output, touch)

    #XTP Slot 6------------------------------------------------------
    elif button.ID == 121:
        output = '21'
        print("Touch 1: {0}".format("Out Room 1: Recorder"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    #
    elif button.ID == 122:
        output = '22'
        print("Touch 1: {0}".format("Out Room 2: Recorder"))
        ##Recall Function
        FunctionActiveTie(output, touch)
    pass

# ACTIONS - SWITCHING VIDEO INPUTS MODE ----------------------------------------
@event(InputsA + InputsB, 'Pressed')
def InSwitching(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    ## Data Init
    global output
    print(button.ID)
    ## Mutually Exclusive
    if button.Host.DeviceAlias == 'TouchPanelA':
        GroupInputsA.SetCurrent(button)
    else:
        GroupInputsB.SetCurrent(button)

    ## Button Functions
    # XTP Slot 1-----------------------------------------------------
    if button.ID == 201:
        input = '1'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: Placa Left"))
    #
    elif button.ID == 202:
        input = '2'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: Placa Right"))
    #
    elif button.ID == 203:
        input = '3'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: Placa Stage"))
    #
    elif button.ID == 204:
        input = '4'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: Placa Back"))

    # XTP Slot 2-----------------------------------------------------
    elif button.ID == 205:
        input = '5'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: Placa Left"))
    #
    elif button.ID == 206:
        input = '6'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: Placa Right"))
    #
    elif button.ID == 207:
        input = '7'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: Placa Stage"))
    #
    elif button.ID == 208:
        input = '8'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: Placa Back"))
        
    # XTP Slot 3-----------------------------------------------------
    elif button.ID == 209:
        input = '9'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: PTZ Frontal"))
    #
    elif button.ID == 210:
        input = '10'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: PTZ Back"))
    #
    elif button.ID == 211:
        input = '11'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: PTZ Frontal"))
    #
    elif button.ID == 212:
        input = '12'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: PTZ Back"))
        
    # XTP Slot 4-----------------------------------------------------
    elif button.ID == 213:
        input = '13'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 1: PC Cabina"))
    #
    elif button.ID == 214:
        input = '14'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Room 2: PC Cabina"))
        
    # XTP Slot 5-----------------------------------------------------
    elif button.ID == 217:
        input = '17'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Core: Cisco 1 Out"))
    #
    elif button.ID == 218:
        input = '18'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Core: Cisco 2 Out"))
    #
    elif button.ID == 219:
        input = '19'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Core: ShareLink 1"))
    #
    elif button.ID == 220:
        input = '20'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Core: ShareLink 2"))
        
    # XTP Slot 6-----------------------------------------------------
    elif button.ID == 221:
        input = '21'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Core: Tricaster 1 Out"))
    #
    elif button.ID == 222:
        input = '22'
        XTP.Set('MatrixTieCommand', None, {'Input':input, 'Output':output, 'Tie Type':'Video'})
        print("Touch: {0}".format("In Core: Tricaster 2 Out"))
    pass

# ACTIONS - RELAYS FUNCTIONS ---------------------------------------------------
def Room1ScreenUp():
    """Control of Relays"""
    AScreenDw.SetState('Open')
    #AScreenUp.SetState('Close')
    AScreenUp.Pulse(2)
    pass

def Room1ScreenDown():
    """Control of Relays"""
    AScreenUp.SetState('Open')
    #AScreenDw.SetState('Close')
    AScreenDw.Pulse(2)
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
    A2ScreenUp.Pulse(2)
    pass

def Room2ScreenDown():
    """Control of Relays"""
    A2ScreenUp.SetState('Open')
    #A2ScreenDw.SetState('Close')
    A2ScreenDw.Pulse(2)
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
    if button.ID == 30: #Projector A
        if ProjA.ReadStatus('Power',None) == 'On':
            print("Touch: {0}".format("Proyector 1: PowerOff"))
            ABtnPwrProjA.SetState(0)
            BBtnPwrProjA.SetState(0)
            ProjA.Set('Power','Off')
            Room1ElevatorUp()
            Room1ScreenUp()
        else:
            print("Touch: {0}".format("Proyector 1: PowerOn"))
            ABtnPwrProjA.SetState(1)
            BBtnPwrProjA.SetState(1)
            ProjA.Set('Power','On')
            Room1ElevatorDown()
            Room1ScreenDown()
    #
    elif button.ID == 31: #Screen A - Up
        GroupScreenA.SetCurrent(ABtnScreenAUp)
        Room1ScreenUp()
        print("Touch: {0}".format("Screen 1: Up"))
    #
    elif button.ID == 32: #Screen A - Down
        GroupScreenA.SetCurrent(ABtnScreenADown)
        Room1ScreenDown()
        print("Touch: {0}".format("Screen 1: Down"))
    #
    elif button.ID == 33: #Elevator A - Up
        GroupElevatA.SetCurrent(ABtnElevAUp)
        Room1ElevatorUp()
        print("Touch: {0}".format("Elevator 1: Up"))
    #
    elif button.ID == 34: #Elevator A - Down
        GroupElevatA.SetCurrent(ABtnElevADown)
        Room1ElevatorDown()
        print("Touch: {0}".format("Elevator 1: Down"))
    #
    elif button.ID == 42: #LCD 3 - Cabina
        if LCDCab3.ReadStatus('Power', None) == 'On':
            ALCDCab1.SetState(0)
            BLCDCab1.SetState(0)
            LCDCab3.Set('Power','Off')
            print("Touch: {0}".format("LCD 3 Power Off"))
        else:
            ALCDCab1.SetState(1)
            BLCDCab1.SetState(1)
            LCDCab3.Set('Power','On')
            print("Touch: {0}".format("LCD 3 Power On"))
    #
    elif button.ID == 41: #LCD 4 - Cabina
        if LCDCab4.ReadStatus('Power', None) == 'On':
            ALCDCab2.SetState(0)
            BLCDCab2.SetState(0)
            LCDCab4.Set('Power','Off')
            print("Touch: {0}".format("LCD 4 Power Off"))
        else:
            ALCDCab2.SetState(1)
            BLCDCab2.SetState(1)
            LCDCab4.Set('Power','On')
            print("Touch: {0}".format("LCD Cab4 Power On"))
    #
    elif button.ID == 43: #LCD 1 - Lobby
        if LCDLob1.ReadStatus('Power', None) == 'On':
            ALCDLobby.SetState(0)
            BLCDLobby.SetState(0)
            LCDLob1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD Lob1 Power Off"))
        else:
            ALCDLobby.SetState(1)
            BLCDLobby.SetState(1)
            LCDLob1.Set('Power','On')
            print("Touch: {0}".format("LCD Lob1 Power On"))
    #
    elif button.ID == 48: #LCD 1 - Podium
        if LCDPod1.ReadStatus('Power', None) == 'On':
            ALCDPodium1.SetState(0)
            BLCDPodium1.SetState(0)
            LCDPod1.Set('Power','Off')
            print("Touch: {0}".format("LCD P1 Power Off"))
        else:
            ALCDPodium1.SetState(1)
            BLCDPodium1.SetState(1)
            LCDPod1.Set('Power','On')
            print("Touch 1: {0}".format("LCD P1 Power On"))
    #
    elif button.ID == 40: #Monitor IR - Cabina
        Monitor1.PlayContinuous('POWER')
        Monitor1.Stop()
        print("Touch: {0}".format("Monitor Cab1 Power IR"))
    pass

# ACTIONS - DISPLAYS B MODE ----------------------------------------------------
@event(ProjeccionB, 'Pressed')
def ButtonObjectPressed(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    if button.ID == 35: #Projector B
        if ProjB.ReadStatus('Power',None) == 'On':
            print("Touch 1: {0}".format("Proyector 2: PowerOff"))
            ABtnPwrProjB.SetState(0)
            BBtnPwrProjB.SetState(0)
            ProjB.Set('Power','Off')
            Room2ElevatorUp()
            Room2ScreenUp()
        else:
            print("Touch 1: {0}".format("Proyector 2: PowerOn"))
            ABtnPwrProjB.SetState(1)
            BBtnPwrProjB.SetState(1)
            ProjB.Set('Power','On')
            Room2ElevatorDown()
            Room2ScreenDown()
    #
    elif button.ID == 36: #Screen B - Up
        GroupScreen2A.SetCurrent(ABtnScreenBUp)
        Room2ScreenUp()
        print("Touch 1: {0}".format("Screen 2: Up"))
    #
    elif button.ID == 37: #Screen B - Down
        GroupScreen2A.SetCurrent(ABtnScreenBDown)
        Room2ScreenDown()
        print("Touch 1: {0}".format("Screen 2: Down"))
    #
    elif button.ID == 38: #Elevator B - Up
        GroupElevat2A.SetCurrent(ABtnElevBUp)
        Room2ElevatorUp()
        print("Touch 1: {0}".format("Elevator 2: Up"))
    #
    elif button.ID == 39: #Elevator B - Down
        GroupElevat2A.SetCurrent(ABtnElevBDown)
        Room2ElevatorDown()
        print("Touch 1: {0}".format("Elevator 2: Down"))
    #
    elif button.ID == 45: #LCD 1 - Cabin
        if LCDCab1.ReadStatus('Power', None) == 'On':
            A2LCDCab2.SetState(0)
            B2LCDCab2.SetState(0)
            LCDCab1.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 1 Power Off"))
        else:
            A2LCDCab2.SetState(1)
            B2LCDCab2.SetState(1)
            LCDCab1.Set('Power','On')
            print("Touch 1: {0}".format("LCD 1 Power On"))
    #
    elif button.ID == 44: #LCD 2 - Cabin
        if LCDCab2.ReadStatus('Power', None) == 'On':
            A2LCDCab3.SetState(0)
            B2LCDCab3.SetState(0)
            LCDCab2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD 2 Power Off"))
        else:
            A2LCDCab3.SetState(1)
            B2LCDCab3.SetState(1)
            LCDCab2.Set('Power','On')
            print("Touch 1: {0}".format("LCD 2 Power On"))
    #
    elif button.ID == 47: #LCD 2 - Lobby
        if LCDLob2.ReadStatus('Power', None) == 'On':
            A2LCDLobby.SetState(0)
            B2LCDLobby.SetState(0)
            LCDLob2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD L2 Power Off"))
        else:
            A2LCDLobby.SetState(1)
            B2LCDLobby.SetState(1)
            LCDLob2.Set('Power','On')
            print("Touch 1: {0}".format("LCD L2 Power On"))
    #
    elif button.ID == 49: #LCD 2 - Podium
        if LCDPod2.ReadStatus('Power', None) == 'On':
            ALCDPodium2.SetState(0)
            BLCDPodium2.SetState(0)
            LCDPod2.Set('Power','Off')
            print("Touch 1: {0}".format("LCD P2 Power Off"))
        else:
            ALCDPodium2.SetState(1)
            BLCDPodium2.SetState(1)
            LCDPod2.Set('Power','On')
            print("Touch 1: {0}".format("LCD P2 Power On"))
    #
    elif button.ID == 46: #Monitor IR - Cabin 2
        Monitor2.PlayContinuous('POWER')
        Monitor2.Stop()
        print("Touch 1: {0}".format("Monitor Cab2 Power IR"))
    pass

# ACTIONS - RECORDING MODE -----------------------------------------------------
@event(GroupModeRec, 'Pressed')
def ButtonObjectPressed(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    print(button.ID)
    if button.ID == 61: #Rec
        RecA.Set('Record','Start')
        print("Touch: {0}".format("SMP11-A: Rec"))
    #
    elif button.ID == 60: #Stop
        RecA.Set('Record','Stop')
        print("Touch: {0}".format("SMP11-A: Stop"))
    #
    elif button.ID == 62: #Pause
        RecA.Set('Record','Pause')
        print("Touch: {0}".format("SMP11-A: Pause"))
    #
    elif button.ID == 71: #Rec
        RecB.Set('Record','Start')
        print("Touch: {0}".format("SMP11-B: Rec"))
    #
    elif button.ID == 70: #Stop
        RecB.Set('Record','Stop')
        print("Touch: {0}".format("SMP11-B: Stop"))
    #
    elif button.ID == 72: #Pause
        RecB.Set('Record','Pause')
        print("Touch: {0}".format("SMP11-B: Pause"))
    pass

# ACTIONS - CISCO 1 MODE -----------------------------------------------------
## This function add or remove data from the panel Dial Number
def PrintDialerVC1(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVC

    if btn_name == 'Delete':           #If the user push 'Delete' button
        dialerVC = dialerVC[:-1]       #Remove the last char of the string
        Cisco1_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        ALblVC1Dial.SetText(dialerVC)      #Send the string to GUI Label
        BLblVC1Dial.SetText(dialerVC)
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
            ALblVC1Dial.SetText(dialerVC)  #Send the string to GUI Label
            BLblVC1Dial.SetText(dialerVC)
    pass

## This function is called when the user press a Dial Button
@event(VCDial, ButtonEventList)
def vc_dial_events(button, state):
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
    if button.ID == 2143:
        if Cisco1.ReadStatus('CallStatus', {'Call':'1'}) == 'Connected':
            Cisco1.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
            ALblVC1Dial.SetText('')
            BLblVC1Dial.SetText('')
            dialerVC = ''
            print("Touch: {0}".format("Cisco1: Hangup"))
        else:
            Cisco1.Set('Hook', 'Dial', {'Number':Cisco1_Data['Dial'], 'Protocol':'H323'})
            print("Touch: {0}".format("Cisco1: Call"))
    #
    elif button.ID == 2142:
        if Cisco1_Data['DTMF'] == False:
            Cisco1_Data['DTMF'] = True
            ADialDot.SetText('*')
            BDialDot.SetText('*')
            ABtnVC1DTMF.SetState(1)
            BBtnVC1DTMF.SetState(1)
            print("Touch 1: {0}".format("Cisco1: DTMF On"))
        else:
            Cisco1_Data['DTMF'] = False
            ADialDot.SetText('?')
            BDialDot.SetText('?')
            ABtnVC1DTMF.SetState(0)
            BBtnVC1DTMF.SetState(0)
            print("Touch 1: {0}".format("Cisco1: DTMF Off"))
    #
    elif button.ID == 2145:
        GroupContentA1.SetCurrent(ABtnVC1ContenOn)
        GroupContentA2.SetCurrent(BBtnVC1ContenOn)
        Cisco1.Set('Presentation', '2', {'Instance': '1'})
        print("Touch: {0}".format("Cisco1: Content On"))
    #
    elif button.ID == 2146:
        GroupContentA1.SetCurrent(ABtnVC1ContenOff)
        GroupContentA2.SetCurrent(BBtnVC1ContenOff)
        Cisco1.Set('Presentation', 'Stop', {'Instance': '1'})
        print("Touch: {0}".format("Cisco1: Content Off"))
    #
    elif button.ID == 400:
        TLP1.HidePopup('Cisco1.Call')
        TLP2.HidePopup('Cisco1.Call')
        Cisco1.Set('Hook', 'Accept', {'Number':'','Protocol': 'H323'})
        print("Touch: {0}".format("Cisco1: Answer"))
    #
    elif button.ID == 401:
        TLP1.HidePopup('Cisco1.Call')
        TLP2.HidePopup('Cisco1.Call')
        Cisco1.Set('Hook', 'Reject', {'Number':'','Protocol': 'H323'})
        print("Touch: {0}".format("Cisco1: Reject"))
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
        ALblVC2Dial.SetText(dialerVC2)  #Send the string to GUI Label
        BLblVC2Dial.SetText(dialerVC2)
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
            ALblVC2Dial.SetText(dialerVC2)  #Send the string to GUI Label
            BLblVC2Dial.SetText(dialerVC2)
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
    if button.ID == 2113:
        if Cisco2.ReadStatus('CallStatus', {'Call':'1'}) == 'Connected':
            Cisco2.Set('Hook', 'Disconnect 1', {'Number':'','Protocol': 'H323'})
            ALblVC2Dial.SetText('')
            BLblVC2Dial.SetText('')
            dialerVC2 = ''
            print("Touch 1: {0}".format("Cisco2: Hangup"))
        else:
            Cisco2.Set('Hook', 'Dial', {'Number':Cisco2_Data['Dial'], 'Protocol':'H323'})
            print("Touch 1: {0}".format("Cisco2: Call"))
    #
    elif button.ID == 2112:
        if Cisco2_Data['DTMF'] == False:
            Cisco2_Data['DTMF'] = True
            A2DialDot.SetText('*')
            B2DialDot.SetText('*')
            ABtnVC2DTMF.SetState(1)
            BBtnVC2DTMF.SetState(1)
            print("Touch: {0}".format("Cisco2: DTMF On"))
        else:
            Cisco2_Data['DTMF'] = False
            A2DialDot.SetText('?')
            B2DialDot.SetText('?')
            ABtnVC2DTMF.SetState(0)
            BBtnVC2DTMF.SetState(0)
            print("Touch: {0}".format("Cisco2: DTMF Off"))
    #
    elif button.ID == 2115:
        GroupContentB1.SetCurrent(ABtnVC2ContenOn)
        GroupContentB2.SetCurrent(BBtnVC2ContenOn)
        Cisco2.Set('Presentation', '2', {'Instance': '1'})
        print("Touch: {0}".format("Cisco2: Content On"))
    #
    elif button.ID == 2116:
        GroupContentB1.SetCurrent(ABtnVC2ContenOff)
        GroupContentB2.SetCurrent(BBtnVC2ContenOff)
        Cisco2.Set('Presentation', 'Stop', {'Instance': '1'})
        print("Touch: {0}".format("Cisco2: Content Off"))
    #
    elif button.ID == 402:
        TLP1.HidePopup('Cisco2.Call')
        Cisco2.Set('Hook', 'Accept', {'Number':'','Protocol': 'H323'})
        print("Touch: {0}".format("Cisco2: Answer"))
    #
    elif button.ID == 403:
        TLP1.HidePopup('Cisco2.Call')
        Cisco2.Set('Hook', 'Reject', {'Number':'','Protocol': 'H323'})
        print("Touch: {0}".format("Cisco2: Reject"))
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
    ALblVC1Dial.SetText('')
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
    ALblVC2Dial.SetText('')
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
    ALblVC1Dial.SetText('')
    ALblVC2Dial.SetText('')
    dialerVC = ''
    dialerVC2 = ''
    # VC Standby
    Cisco1.Set('Standby', 'Activate')
    Cisco2.Set('Standby', 'Activate')
    # TouchPanel Actions
    TLP1.ShowPage('Index')
    TLP2.ShowPage('Index')
    pass

@event(GroupPower, ButtonEventList)
def PowerOff_Mode(button, state):
    """Are actions that occur with user interaction with TouchPanel"""
    #
    global PowerCounterAB
    global PowerCounterA
    global PowerCounterB
    #
    if button.ID == 420:
        if state == 'Pressed':
            PowerCounterAB = 3
            ALblPowerAB.SetText(str(PowerCounterAB))
            BLblPowerAB.SetText(str(PowerCounterAB))
        #
        elif state == 'Repeated':
            PowerCounterAB -= 1
            ALblPowerAB.SetText(str(PowerCounterAB))
            BLblPowerAB.SetText(str(PowerCounterAB))
            if PowerCounterAB == 0:
                #PowerOffRoomAB()
                TLP1.ShowPage('Index')
                TLP2.ShowPage('Index')
                print("Touch: {0}".format("PowerOff: Sala A-B"))
        #
        elif state == 'Released' or state == 'Tapped':
            PowerCounterAB = 0
            ALblPowerAB.SetText('..')
            BLblPowerAB.SetText('..')
    #
    elif button.ID == 421:
        if state == 'Pressed':
            PowerCounterA = 3
            ALblPowerA.SetText(str(PowerCounterA))
            BLblPowerA.SetText(str(PowerCounterA))
        #
        elif state == 'Repeated':
            PowerCounterA -= 1
            ALblPowerA.SetText(str(PowerCounterA))
            BLblPowerA.SetText(str(PowerCounterA))
            if PowerCounterA == 0:
                #PowerOffRoomA()
                TLP1.ShowPage('Index')
                print("Touch: {0}".format("PowerOff: Sala 1"))
        #
        elif state == 'Released' or state == 'Tapped':
            PowerCounterA = 0
            ALblPowerA.SetText('..')
            BLblPowerA.SetText('..')
    #
    elif button.ID == 422:
        if state == 'Pressed':
            PowerCounterB = 3
            ALblPowerB.SetText(str(PowerCounterB))
            BLblPowerB.SetText(str(PowerCounterB))
        #
        elif state == 'Repeated':
            PowerCounterB -= 1
            ALblPowerB.SetText(str(PowerCounterB))
            BLblPowerB.SetText(str(PowerCounterB))
            if PowerCounterB == 0:
                #PowerOffRoomB()
                TLP2.ShowPage('Index')
                print("Touch: {0}".format("PowerOff: Sala 2"))
        #
        elif state == 'Released' or state == 'Tapped':
            PowerCounterB = 0
            ALblPowerB.SetText('..')
            BLblPowerB.SetText('..')
    pass

## End Events Definitions-------------------------------------------------------
Initialize()