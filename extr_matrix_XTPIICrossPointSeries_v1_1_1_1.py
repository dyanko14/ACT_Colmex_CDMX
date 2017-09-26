from extronlib.interface import EthernetClientInterface, SerialInterface
from re import compile, search
from extronlib.system import Wait, ProgramLog

class DeviceClass:

    def __init__(self):
        self.Unidirectional = 'False'
        self.connectionCounter = 5

        self.devicePassword = None
        self.Debug = False
        
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Models = {
            'XTP II CrossPoint 6400': self.extr_15_1269_6400,
            'XTP II CrossPoint 1600': self.extr_15_1269_1600,
            'XTP II CrossPoint 3200': self.extr_15_1269_3200,
            }

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AudioMute': {'Parameters': ['Output'], 'Status': {}},
            'EndpointTie': {'Parameters': ['Input', 'Tie Type'], 'Status': {}},
            'ExecutiveMode': {'Status': {}},
            'GlobalAudioMute': {'Status': {}},
            'GlobalVideoMute': {'Status': {}},
            'InputSignal': {'Parameters': ['Input'], 'Status': {}},
            'InputTieStatus': {'Parameters': ['Input', 'Output'], 'Status': {}},
            'MatrixTieCommand': {'Parameters': ['Input', 'Output', 'Tie Type'], 'Status': {}},
            'OutputTieStatus': {'Parameters': ['Output', 'Tie Type'], 'Status': {}},
            'PowerSupplyStatus': {'Parameters': ['Number'], 'Status': {}},
            'PresetRecall': {'Status': {}},
            'PresetSave': {'Status': {}},
            'RefreshMatrix': {'Status': {}},
            'Relay': {'Parameters': ['Output', 'Relay'], 'Status': {}},
            'RelayPulse': {'Parameters': ['Output', 'Relay'], 'Status': {}},
            'TestPattern': {'Status': {}},
            'VideoMute': {'Parameters': ['Output'], 'Status': {}},
            'Volume': {'Parameters': ['Output'], 'Status': {}},
            'XTPInputPower': {'Parameters': ['Input'], 'Status': {}},
            'XTPOutputPower': {'Parameters': ['Output'], 'Status': {}}
        }

        self.OutputStatus = {'Video': ['Initial' for _ in range(0, 64)],
                             'Audio': ['Initial' for _ in range(0, 64)]}
        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'
        self.outputInit = {'Audio': ['0' for _ in range(0, 64)],
                           'Video': ['0' for _ in range(0, 64)]}

        if self.Unidirectional == 'False':
            self.AddMatchString(compile(b'Out(\d{2}) Vol(\d{2})\r\n'), self.__MatchVolume, None)
            self.AddMatchString(compile(b'Frq0+\*([0-1]+)\r\n'), self.__MatchInputSignal, None)
            self.AddMatchString(compile(b'Vmt(\d+)\*([0-1])\r\n'), self.__MatchVideoMute, None)
            self.AddMatchString(compile(b'Exec([0-2])\r\n'), self.__MatchExecutiveMode, None)
            self.AddMatchString(compile(b'Amt(\d+)\*([0-3])\r\n'), self.__MatchAudioMute, None)
            self.AddMatchString(compile(b'Rely(\d+)\*(\d+)\*(1|0)\r\n'), self.__MatchRelay, None)
            self.AddMatchString(compile(b'Vmt[0-1]\r\n'), self.__MatchGlobalMute, None)
            self.AddMatchString(compile(b'Amt[0-3]\r\n'), self.__MatchGlobalMute, None)
            self.AddMatchString(compile(b'Mut([0-7]+)\r\n'), self.__MatchMute, None)
            self.AddMatchString(compile(b'Etie([0-9]{2})\*([1-3])\*([1-3])\r\n'), self.__MatchEndpointTie, None)
            self.AddMatchString(compile(b'Qik\r\n'), self.__MatchQik, None)
            self.AddMatchString(compile(b'PrstR\d+\r\n'), self.__MatchQik, None)
            self.AddMatchString(compile(b'(Out(\d+) )?In(\d+) (All|RGB|Vid|Aud)\r\n'), self.__MatchOutputTieStatus, None)
            self.AddMatchString(compile(b'Vgp00 Out(\d{2})\*([0-9 -]*)Vid\r\n'), self.__MatchAllMatrixTie, 'Video')
            self.AddMatchString(compile(b'Vgp00 Out(\d{2})\*([0-9 -]*)Aud\r\n'), self.__MatchAllMatrixTie, 'Audio')

            self.AddMatchString(compile(b'Sts00\*(?P<voltage>[0-9]{1,2}\.[0-9]{2}( )){3,5}(?P<temperature>\+?[0-9]{3}\.[0-9]{2}( ))(?P<rpm>[0-9]{5}( )){2,7}(?P<power>[01]{2,4})\r\n'), self.__MatchPowerSupplyStatus, None)
            self.AddMatchString(compile(b'Tst([01]\d)\r\n'), self.__MatchTestPattern, None)
            self.AddMatchString(compile(b'PoecI00\*(?P<power>[01]{0,32})\r\n'), self.__MatchXTPInputPower, 'Polled')
            self.AddMatchString(compile(b'PoecI(?P<input>[0-9]{2})\*(?P<power>0|1)\*(?P<amount>00|13)\*(?P<status>[0-4])\r\n'), self.__MatchXTPInputPower, 'Unsolicited')
            self.AddMatchString(compile(b'PoecO00\*(?P<power>[01]{0,32})\r\n'), self.__MatchXTPOutputPower, 'Polled')
            self.AddMatchString(compile(b'PoecO(?P<output>[0-9]{2})\*(?P<power>0|1)\*(?P<amount>00|13)\*(?P<status>[0-4])\r\n'), self.__MatchXTPOutputPower, 'Unsolicited')

            self.AddMatchString(compile(b'E(\d+)\r\n'), self.__MatchErrors, None)
            self.AddMatchString(compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)

            if 'Serial' not in self.ConnectionType:
                self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
                self.AddMatchString(compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
                self.AddMatchString(compile(b'Login User\r\n'), self.__MatchLoginUser, None)

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 2:
            print('Log in failed. Please supply proper Admin password')
        else:
            if self.devicePassword is not None:
                self.Send(self.devicePassword + '\r\n')
            else:
                self.MissingCredentialsLog('Password')
        self.Authenticated = 'None'        

    def __MatchLoginAdmin(self, match, tag):
        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):
        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print('Logged in as User. May have limited functionality.')

    def __MatchVerboseMode(self, match, qualifier):
        self.VerboseDisabled = False
        self.UpdateAllMatrixTie(None, None)
        self.OnConnected()

    def __MatchGlobalMute(self, match, tag):
        self.UpdateMute(None, None)

    def UpdateMute(self, value, qualifier):
        self.Send('wvm\r')

    def __MatchMute(self, match, tag):
        stat = match.group(1).decode()
        output = 1
        for i in stat:
            if i == '0':
                self.WriteStatus('AudioMute', 'Off', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'Off', {'Output': str(output)})
            elif i == '1':
                self.WriteStatus('AudioMute', 'Off', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'On', {'Output': str(output)})
            elif i == '2':
                self.WriteStatus('AudioMute', 'Digital', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'Off', {'Output': str(output)})
            elif i == '3':
                self.WriteStatus('AudioMute', 'Digital', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'On', {'Output': str(output)})
            elif i == '4':
                self.WriteStatus('AudioMute', 'Analog', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'Off', {'Output': str(output)})
            elif i == '5':
                self.WriteStatus('AudioMute', 'Analog', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'On', {'Output': str(output)})
            elif i == '6':
                self.WriteStatus('AudioMute', 'On', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'Off', {'Output': str(output)})
            elif i == '7':
                self.WriteStatus('AudioMute', 'On', {'Output': str(output)})
                self.WriteStatus('VideoMute', 'On', {'Output': str(output)})
            output += 1

    def __MatchQik(self, match, tag):
        self.UpdateAllMatrixTie(None, None)

    def UpdateAllMatrixTie(self, value, qualifier):
        if self.OutputSize == 16:
            self.Send('w0*1*2vc\r')
            self.Send('w0*1*1vc\r')
        elif self.OutputSize == 32:
            self.Send('w0*1*2vc\r')
            self.Send('w0*1*1vc\r')
            self.Send('w0*17*1vc\r')
            self.Send('w0*17*2vc\r')
        elif self.OutputSize == 64:
            self.Send('w0*1*2vc\r')
            self.Send('w0*1*1vc\r')
            self.Send('w0*17*1vc\r')
            self.Send('w0*17*2vc\r')
            self.Send('w0*33*1vc\r')
            self.Send('w0*33*2vc\r')
            self.Send('w0*49*1vc\r')
            self.Send('w0*49*2vc\r')

    def __MatchAllTie(self, match, tag):
        typeDic = {
            b'All': 'Audio/Video',
            b'RGB': 'Video',
            b'Vid': 'Video',
            b'Aud': 'Audio',
        }

        input_ = str(int(match.group(3)))
        type_ = typeDic[match.group(4)]
        output = 1

        while output <= self.OutputSize:
            if 'Audio' in type_:
                self.__SetMatrixStatus(str(int(output)), input_, 'Audio')
            if 'Video' in type_:
                self.__SetMatrixStatus(str(int(output)), input_, 'Video')
            output += 1
            
    def __MatchAllMatrixTie(self, match, tag):
        output = int(match.group(1))
        inputList = match.group(2).decode().split()
        opTag = 'Video' if tag == 'Audio' else 'Audio' 
        
        for value in inputList:
            if value == '--':
                value = '0'
            else:
                value = str(int(value))
            
            if str(output) not in self.outputInit[tag]:
                if value == '0':
                    self.WriteStatus('OutputTieStatus', '0', {'Output': str(output), 'Tie Type': tag})
                    self.WriteStatus('OutputTieStatus', '0', {'Output': str(output), 'Tie Type': 'Audio/Video'})
                for inp in range(1, self.InputSize+1):
                    inputStr = str(inp)
                    if value == '0':
                        if self.outputInit[tag][int(inputStr)-1] == value and self.outputInit[opTag][int(inputStr)-1] == value:
                            self.WriteStatus('InputTieStatus', 'Untied', {'Input': inputStr, 'Output': str(output)})
                    elif inputStr != value and self.outputInit[opTag][output-1] == '0':
                        self.WriteStatus('InputTieStatus', 'Untied', {'Input': inputStr, 'Output': str(output)})   
                self.outputInit[tag][output-1] = str(output)

            self.__SetMatrixStatus(str(output), value, tag)
            output += 1

    def __SetMatrixStatus(self, output, newInput, tag):
        oldInput = self.OutputStatus[tag][int(output)-1]
        opTag = 'Audio' if tag == 'Video' else 'Video'
        if oldInput != newInput:
            self.WriteStatus('OutputTieStatus', newInput, {'Output': output, 'Tie Type': tag})
            opInVal = self.ReadStatus('OutputTieStatus', {'Output': output, 'Tie Type': opTag})
            prevInputTieStatus = self.ReadStatus('InputTieStatus', {'Input': oldInput, 'Output': output})
            if prevInputTieStatus == 'Audio/Video':
                self.WriteStatus('InputTieStatus', opTag, {'Input': oldInput, 'Output': output})
            else:
                self.WriteStatus('InputTieStatus', 'Untied', {'Input': oldInput, 'Output': output})

            if opInVal == newInput:
                self.WriteStatus('OutputTieStatus', newInput, {'Output': output, 'Tie Type': 'Audio/Video'})
                self.WriteStatus('InputTieStatus', 'Audio/Video', {'Input': newInput, 'Output': output})
            else:
                self.WriteStatus('OutputTieStatus', '0', {'Output': output, 'Tie Type': 'Audio/Video'})
                self.WriteStatus('InputTieStatus', tag, {'Input': newInput, 'Output': output})

            self.OutputStatus[tag][int(output)-1] = newInput

    def SetAudioMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0',
            'On': '3',
            'Analog': '2',
            'Digital': '1',
        }
        channel = int(qualifier['Output'])
        if channel < 1 or channel > self.OutputSize:
            print('Invalid Command for SetAudioMute')
        else:
            self.__SetHelper('AudioMute', '{0}*{1}z'.format(channel, AudioMuteState[value]), value, qualifier)

    def UpdateAudioMute(self, value, qualifier):
        channel = int(qualifier['Output'])
        if channel < 1 or channel > self.OutputSize:
            print('Invalid Command for UpdateAudioMute')
        else:
            self.__UpdateHelper('AudioMute', '{0}z'.format(channel), value, qualifier)

    def __MatchAudioMute(self, match, qualifier):
        AudioMuteName={
            b'0': 'Off',
            b'3': 'On',
            b'2': 'Analog',
            b'1': 'Digital',
        }
        self.WriteStatus('AudioMute', AudioMuteName[match.group(2)], {'Output': str(int(match.group(1)))})

    def SetEndpointTie(self, value, qualifier):

        EndpointStates = {
            'Analog Input 1': '1',
            'HDMI Input 2': '2',
            'HDMI Input 3': '3'
        }

        TieTypeStates = {
            'Audio': '2',
            'Video': '1',
            'Audio/Video': '3'
        }

        input_ = qualifier['Input']
        endpoint = EndpointStates[value]
        tie_type = TieTypeStates[qualifier['Tie Type']]

        if 1 <= int(input_) <= self.InputSize:
            EndpointTieCmdString = '\x1B{0}*{1}*{2}ETIE\r'.format(input_, endpoint, tie_type)
            self.__SetHelper('EndpointTie', EndpointTieCmdString, value, qualifier)
        else:
            print('Invalid Command for SetEndpointTie')

    def UpdateEndpointTie(self, value, qualifier):

        input_ = qualifier['Input']
        if 1 <= int(input_) <= self.InputSize:
            EndpointTieStatusCmdString = '\x1B{0}ETIE\r'.format(input_)
            self.__UpdateHelper('EndpointTie', EndpointTieStatusCmdString, value, qualifier)
        else:
            print('Invalid Command for UpdateEndpointTie')

    def __MatchEndpointTie(self, match, qualifier):
        
        ValueStateValues = {
            '1': 'Analog Input 1',
            '2': 'HDMI Input 2',
            '3': 'HDMI Input 3'
        }

        input_res = str(int(match.group(1).decode()))
        audio_tie = ValueStateValues[match.group(3).decode()]
        video_tie = ValueStateValues[match.group(2).decode()]
        if audio_tie == video_tie:
            self.WriteStatus('EndpointTie', audio_tie, {'Input': input_res, 'Tie Type': 'Audio/Video'})
        else:
            self.WriteStatus('EndpointTie', 'None', {'Input': input_res, 'Tie Type': 'Audio/Video'})
        self.WriteStatus('EndpointTie', audio_tie, {'Input': input_res, 'Tie Type': 'Audio'})
        self.WriteStatus('EndpointTie', video_tie, {'Input': input_res, 'Tie Type': 'Video'})

    def SetExecutiveMode(self, value, qualifier):
        ExecutiveModeState = {
            'Mode 1': '1',
            'Mode 2': '2',
            'Off': '0'
        }
        self.__SetHelper('ExecutiveMode', '\x1B{0}EXEC\r'.format(ExecutiveModeState[value]), value, qualifier)

    def UpdateExecutiveMode(self, value, qualifier):
        self.__UpdateHelper('ExecutiveMode', '\x1BEXEC\r', value, qualifier)

    def __MatchExecutiveMode(self, match, qualifier):
        ExecutiveModeName = {
            b'1': 'Mode 1',
            b'2': 'Mode 2',
            b'0': 'Off',
        }
        self.WriteStatus('ExecutiveMode', ExecutiveModeName[match.group(1)], None)

    def SetGlobalAudioMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0',
            'On': '3',
            'Analog': '2',
            'Digital': '1',
        }
        self.__SetHelper('GlobalAudioMute', '{0}*z'.format(AudioMuteState[value]), value, qualifier)

    def SetGlobalVideoMute(self, value, qualifier):
        VideoMuteState = {
            'Off': '0',
            'On': '1',
        }
        self.__SetHelper('GlobalVideoMute', '{0}*b'.format(VideoMuteState[value]), value, qualifier)

    def UpdateInputSignal(self, value, qualifier):

        if 1 <= int(qualifier['Input']) <= self.InputSize:
            self.__UpdateHelper('InputSignal', '0LS', value, qualifier)
        else:
            print('Invalid Command for UpdateInputSignal')

    def __MatchInputSignal(self, match, qualifier):
        InputSignalStatus = {
            '1': 'Active',
            '0': 'Inactive',
            }
        signal = match.group(1).decode()
        inputNumber = 1
        for input_ in signal:
            self.WriteStatus('InputSignal', InputSignalStatus[input_], {'Input': str(inputNumber)})
            inputNumber += 1

    def SetMatrixTieCommand(self, value, qualifier):
        TieTypeValues = {
            'Audio': '\x24',
            'Video': '\x26',
            'Audio/Video': '\x21'
        }
        
        input_ = int(qualifier['Input'])
        output = int(qualifier['Output'])
        tieType = qualifier['Tie Type']
        outrange = ['All']
        for i in range(1, self.OutputSize+1):
            outrange.append(i)

        if output not in outrange:
            print('Invalid Command for SetMatrixTieCommand')
        elif input_ < 0 or input_ > self.InputSize:
            print('Invalid Command for SetMatrixTieCommand')
        else:
            output = '' if output == 'All' else output
            self.__SetHelper('MatrixTieCommand', '{0}*{1}{2}'.format(input_, output, TieTypeValues[tieType]), input_, qualifier)

    def __MatchOutputTieStatus(self, match, qualifier):
        if match.group(1):
            TieTypeStates = {
                'Aud': 'Audio',  
                'Vid': 'Video', 
                'RGB': 'Video', 
                'All': 'Audio/Video',
            }
            output, input_ = str(int(match.group(2))), str(int(match.group(3)))
            tieType = TieTypeStates[match.group(4).decode()]
            if 'Audio' in tieType:
                if output not in self.outputInit['Audio']:
                    if input_ == '0':
                        self.WriteStatus('OutputTieStatus', '0', {'Output': output, 'Tie Type':'Audio'})
                    for inp in range(1, self.InputSize+1):
                        inputStr = str(inp)
                        if inputStr != input_ or input_ == '0':
                            self.WriteStatus('InputTieStatus', 'Untied', {'Input':inputStr, 'Output':output})
                    self.outputInit['Audio'].append(output)
                self.__SetMatrixStatus(output, input_, 'Audio')
            if 'Video' in tieType:
                if output not in self.outputInit['Video']:
                    if input_ == '0':
                        self.WriteStatus('OutputTieStatus', '0', {'Output':output, 'Tie Type':'Video'})
                    for inp in range(1, self.InputSize+1):
                        inputStr = str(inp)
                        if inputStr != input_ or input_ == '0':
                            self.WriteStatus('InputTieStatus', 'Untied', {'Input':inputStr, 'Output':output})
                    self.outputInit['Video'].append(output)
                self.__SetMatrixStatus(output, input_, 'Video')
        else:
            self.__MatchAllTie(match, None)

    def UpdatePowerSupplyStatus(self, value, qualifier):
        PowerSupplyStatusCmdString = 'S\r'
        self.__UpdateHelper('PowerSupplyStatus', PowerSupplyStatusCmdString, value, qualifier)
        
    def __MatchPowerSupplyStatus(self, match, tag):
        ValueStateValues = {
            '1': 'Installed/Normal',
            '0': 'Not Installed/Failed'
        }
        max_ = len(match.group('power').decode())
        if max_ in [2, 4]:
            for number in range(0, 4):        
                qualifier = {'Number': str(number+1)}
                if number < max_:
                    value = ValueStateValues[match.group('power').decode()[number]]
                else:
                    value = 'Not Installed/Failed'
                self.WriteStatus('PowerSupplyStatus', value, qualifier)

    def SetPresetRecall(self, value, qualifier):
        value = int(value)
        if 0 < value < 33:   
            self.__SetHelper('PresetRecall', '\x1BR{0}PRST\r'.format(value), value, qualifier)
        else:
            print('Invalid Command for SetPresetRecall')

    def SetPresetSave(self, value, qualifier):
        value = int(value)
        if 0 < value < 33:   
            self.__SetHelper('PresetSave', '\x1BS{0}PRST\r'.format(value), value, qualifier)
        else:
            print('Invalid Command for SetPresetSave')
            
    def SetRefreshMatrix(self, value, qualifier):
        valueStates = {
            '1 - 16':    'w0*1*2vc\rw0*1*1vc\r',
            '17 - 32':   'w0*17*1vc\rw0*17*2vc\r',
            '33 - 48':   'w0*33*1vc\rw0*33*2vc\r',
            '49 - 64':   'w0*49*1vc\rw0*49*2vc\r',
        }

        if value == 'All' and self.OutputSize == 16:
            command = 'w0*1*2vc\rw0*1*1vc\r'
        elif value == 'All' and self.OutputSize == 32:
            command = 'w0*1*2vc\rw0*1*1vc\rw0*17*1vc\rw0*17*2vc\r'
        elif value == 'All' and self.OutputSize == 64:
            command = 'w0*1*2vc\rw0*1*1vc\rw0*17*1vc\rw0*17*2vc\rw0*33*1vc\rw0*33*2vc\rw0*49*1vc\rw0*49*2vc\r'
        else:
            command = valueStates[value]

        self.__SetHelper('RefreshMatrix', command, value, qualifier)

    def SetRelay(self, value, qualifier):
        RelayState = {
            'Close': '1',
            'Open': '0',
            }

        output = int(qualifier['Output'])
        relay = int(qualifier['Relay'])

        if output < 1 or output > self.OutputSize:
            print('Invalid Command for SetRelay')
        elif relay < 1 or relay > 2:
            print('Invalid Command for SetRelay')
        else:
            if value in ['Close', 'Open']:
                self.__SetHelper('Relay', 'w{0}*{1}*{2}rely\r'.format(output, relay, RelayState[value]), value, qualifier)

    def UpdateRelay(self, value, qualifier):
        output = int(qualifier['Output'])
        relay = int(qualifier['Relay'])

        if output < 1 or output > self.OutputSize:
            print('Invalid Command for UpdateRelay')
        elif relay < 1 or relay > 2:
            print('Invalid Command for UpdateRelay')
        else:
            self.__UpdateHelper('Relay', 'w{0}*{1}rely\r'.format(output, relay), value, qualifier)

    def __MatchRelay(self, match, qualifier):
        RelayState = {
            b'1': 'Close',
            b'0': 'Open',
        }

        output = int(match.group(1))
        relay = int(match.group(2))
        self.WriteStatus('Relay', RelayState[match.group(3)], {'Output':str(output), 'Relay': str(relay)})

    def SetRelayPulse(self, value, qualifier):


        output = int(qualifier['Output'])
        relay = int(qualifier['Relay'])

        if 1 <= output <= self.OutputSize and 1 <= relay <= 2 and 0.016 <= value <= 1048.56:
            pulseTime = int(value/0.016)
            self.__SetHelper('RelayPulse', 'w{0}*{1}*3*{2}rely\r'.format(output, relay, pulseTime), value, qualifier)
        else:
            print('Invalid Command for SetRelayPulse')


    def SetTestPattern(self, value, qualifier):
        ValueStateValues = {
            'Black Screen, No Audio (720p @ 50 Hz)':    '2',
            'Black Screen, No Audio (720p @ 60 Hz)':    '4',
            'Black Screen, No Audio (1080p @ 60 Hz)':   '6',
            'Black Screen, Audio (720p @ 50 Hz)':       '8',
            'Black Screen, Audio (720p @ 60 Hz)':       '10',
            'Black Screen, Audio (1080p @ 60 Hz)':      '12',
            'Color Bars, No Audio (720p @ 50 Hz)':      '1',
            'Color Bars, No Audio (720p @ 60 Hz)':      '3',
            'Color Bars, No Audio (1080p @ 60 Hz)':     '5',
            'Color Bars, Audio (720p @ 50 Hz)':         '7',
            'Color Bars, Audio (720p @ 60 Hz)':         '9',
            'Color Bars, Audio (1080p @ 60 Hz)':        '11',
            'Off':                                     '0'
        }

        TestPatternCmdString = '\x1B{0}TEST\r'.format(ValueStateValues[value])
        self.__SetHelper('TestPattern', TestPatternCmdString, value, qualifier)

    def UpdateTestPattern(self, value, qualifier):
        TestPatternCmdString = '\x1BTEST\r'
        self.__UpdateHelper('TestPattern', TestPatternCmdString, value, qualifier)

    def __MatchTestPattern(self, match, tag):
        ValueStateValues = {
            '02': 'Black Screen, No Audio (720p @ 50 Hz)',
            '04': 'Black Screen, No Audio (720p @ 60 Hz)',
            '06': 'Black Screen, No Audio (1080p @ 60 Hz)',
            '08': 'Black Screen, Audio (720p @ 50 Hz)',
            '10': 'Black Screen, Audio (720p @ 60 Hz)',
            '12': 'Black Screen, Audio (1080p @ 60 Hz)',
            '01': 'Color Bars, No Audio (720p @ 50 Hz)',
            '03': 'Color Bars, No Audio (720p @ 60 Hz)',
            '05': 'Color Bars, No Audio (1080p @ 60 Hz)',
            '07': 'Color Bars, Audio (720p @ 50 Hz)',
            '09': 'Color Bars, Audio (720p @ 60 Hz)',
            '11': 'Color Bars, Audio (1080p @ 60 Hz)',
            '00': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('TestPattern', value, None)

    def SetVideoMute(self, value, qualifier):
        VideoMuteState={
            'Off': '0',
            'On':  '1',
        }
        channel = int(qualifier['Output'])
        if 1 <= channel <= self.OutputSize:
            self.__SetHelper('VideoMute', '{0}*{1}b'.format(channel, VideoMuteState[value]), value, qualifier)
        else:
            print('Invalid Command for SetVideoMute')

    def UpdateVideoMute(self, value, qualifier):
        channel = int(qualifier['Output'])
        if 1 <= channel <= self.OutputSize:
            self.__UpdateHelper('VideoMute', '{0}b'.format(channel), value, qualifier)
        else:
            print('Invalid Command for UpdateVideoMute')

    def __MatchVideoMute(self, match, qualifier):
        VideoMuteName = {
            b'0': 'Off',
            b'1': 'On',
        }
        self.WriteStatus('VideoMute', VideoMuteName[match.group(2)], {'Output': str(int(match.group(1)))})

    def SetVolume(self, value, qualifier):
        channel = int(qualifier['Output'])
        if channel < 1 or channel > self.OutputSize:
            print('Invalid Command for SetVolume')
        elif value < 0 or value > 64:
            print('Invalid Command for SetVolume') 
        else:
            self.__SetHelper('Volume', '{0}*{1}v'.format(channel, value), value, qualifier)

    def UpdateVolume(self, value, qualifier):
        channel = int(qualifier['Output'])
        if channel < 1 or channel > self.OutputSize:
            print('Invalid Command for UpdateVolume')
        else:
            self.__UpdateHelper('Volume', '{0}v'.format(channel), value, qualifier)

    def __MatchVolume(self, match, qualifier):
        self.WriteStatus('Volume', int(match.group(2)), {'Output': str(int(match.group(1)))})

    def SetXTPInputPower(self, value, qualifier):
        
        ValueStateValues = {
            'On':  '1',
            'Off': '0'
        }
        
        input_ = qualifier['Input']
        if 1 <= int(input_) <= self.InputSize:
            XTPInputPowerCmdString = 'wI{0}*{1}POEC\r'.format(input_, ValueStateValues[value])
            self.__SetHelper('XTPInputPower', XTPInputPowerCmdString, value, qualifier)
        else:
            print('Invalid Command for SetXTPInputPower')

    def UpdateXTPInputPower(self, value, qualifier):
        input_ = qualifier['Input']
        
        if 1 <= int(input_) <= self.InputSize:
            XTPInputPowerCmdString = 'wIPOEC\r'
            self.__UpdateHelper('XTPInputPower', XTPInputPowerCmdString, value, qualifier)
        else:
            print('Device Is Busy for UpdateXTPInputPower')

    def __MatchXTPInputPower(self, match, tag):
        ValueStateValues = {
            '1' : 'On', 
            '0' : 'Off'
        }
        
        if tag == 'Polled':
            input_ = 1
            for value in match.group('power').decode():
                if input_ > self.InputSize:
                    break
                self.WriteStatus('XTPInputPower', ValueStateValues[value], {'Input': str(input_)})
                input_ += 1
        elif tag == 'Unsolicited':
            input_ = match.group('input').decode().lstrip('0')
            if 1 <= int(input_) <= self.InputSize:
                self.WriteStatus('XTPInputPower', ValueStateValues[match.group('power').decode()], {'Input': input_})

    def SetXTPOutputPower(self, value, qualifier):

        ValueStateValues = {
            'On' : '1', 
            'Off' : '0'
        }
        
        output = qualifier['Output']
        
        if 1 <= int(output) <= self.OutputSize:
            XTPOutputPowerCmdString = 'wO{0}*{1}POEC\r'.format(output, ValueStateValues[value])
            self.__SetHelper('XTPOutputPower', XTPOutputPowerCmdString, value, qualifier)
        else:
            print('Invalid Command for SetXTPOutputPower')

    def UpdateXTPOutputPower(self, value, qualifier):
        output = qualifier['Output']
        
        if 1 <= int(output) <= self.OutputSize:
            XTPOutputPowerCmdString = 'wOPOEC\r'
            self.__UpdateHelper('XTPOutputPower', XTPOutputPowerCmdString, value, qualifier)
        else:
            print('Device Is Busy for UpdateXTPOutputPower')    

    def __MatchXTPOutputPower(self, match, tag):
        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }               
        
        if tag == 'Polled':
            output = 1
            for value in match.group('power').decode():
                if output > self.OutputSize:
                    break
                self.WriteStatus('XTPOutputPower', ValueStateValues[value], {'Output': str(output)})
                output += 1
        elif tag == 'Unsolicited':
            output = match.group('output').decode().lstrip('0')
            if 1 <= int(output) <= self.OutputSize:
                self.WriteStatus('XTPOutputPower', ValueStateValues[match.group('power').decode()], {'Output': output})

    def __MatchErrors(self, match, tag):
        DEVICE_ERROR_CODES = {
            '01':  'Invalid input number (too large)',
            '10': 'Invalid command',
            '11': 'Invalid preset number',
            '12': 'Invalid port number',
            '13': 'Invalid value (out of range)',
            '14': 'Command not available for this configuration',
            '17': 'System timed out',
            '22': 'Busy',
            '24': 'Privilege violation',
            '25': 'Device not present',
            '26': 'Maximum number of connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
            '30': 'Hardware failure (followed by a colon [:] and a descriptor number)',
            '31': 'Attempt to break port pass-through when it has not been set',
            '32': 'Incorrect V-chip password'
        }
        value = match.group(1).decode()
        if value in DEVICE_ERROR_CODES:
            print(DEVICE_ERROR_CODES[value])
        else:
            print('Unrecognized error code: ' + match.group(0).decode())

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter += 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()

        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                print('Inappropriate Command ', command)
            else:
                if self.VerboseDisabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        self.Send(commandstring)
                else:
                    self.Send(commandstring)					
        else:
            print('Inappropriate Command ', command)

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        self.OutputStatus['Video'] = ['Initial' for _ in range(0, self.OutputSize)]
        self.OutputStatus['Audio'] = ['Initial' for _ in range(0, self.OutputSize)]
        self.outputInit['Video'] = ['0' for _ in range(0, self.InputSize)]
        self.outputInit['Audio'] = ['0' for _ in range(0, self.InputSize)]

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        if 'Serial' not in self.ConnectionType:
            self.Authenticated = 'Not Needed'
            self.PasswdPromptCount = 0
        self.VerboseDisabled = True
        
    def extr_15_1269_1600(self):
        self.InputSize = 16
        self.OutputSize = 16

    def extr_15_1269_3200(self):
        self.InputSize = 32
        self.OutputSize = 32

    def extr_15_1269_6400(self):
        self.InputSize = 64
        self.OutputSize = 64

    ######################################################    
    # RECOMMENDED not to modify the code below this point
    ######################################################

    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = 'Set%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(value, qualifier)
        else:
            print(command, 'does not support Set.')
     
    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = 'Update%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(None, qualifier)
        else:
            print(command, 'does not support Update.')
            
    def MissingCredentialsLog(self, credential_type):
        if isinstance(self, EthernetClientInterface):
            port_info = 'IP Address: {0}:{1}'.format(self.IPAddress, self.IPPort)
        elif isinstance(self, SerialInterface):
            port_info = 'Host Alias: {0}\r\nPort: {1}'.format(self.Host.DeviceAlias, self.Port)
        else:
            return
        ProgramLog("{0} module received a request from the device for a {1}, "
                   "but device{1} was not provided.\n Please provide a device{1} "
                   "and attempt again.\n Ex: dvInterface.device{1} = '{1}'\n Please "
                   "review the communication sheet.\n {2}"
                   .format(__name__, credential_type, port_info), 'warning')

    def __ReceiveData(self, interface, data):
        # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para':arg}
                

    # Check incoming unsolicited data to see if it matched with device expectancy. 
    def CheckMatchedString(self):
        for regexString in self._compile_list:
            while True:
                result = search(regexString, self._ReceiveBuffer)                
                if result:
                    self._compile_list[regexString]['callback'](result, self._compile_list[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True      

    # This method is to tie a specific command with specific parameter to a call back method
    # when it value is updated. It all setup how often the command to be query, if the command
    # have the update method.
    # interval 0 is for query once, any other integer is used as the query interval.
    # If command doesn't have the update feature then that command is only used for feedback 
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method':{}}
        
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
        
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return
        
            Method['callback'] = callback
            Method['qualifier'] = qualifier    
        else:
            print(command, 'does not exist in the module')
        
    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription :
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)                
                
    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    return None
        try:
            return Status['Live']
        except:
            return None

class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=9600, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()
                

class SerialOverEthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self) 
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()

class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self) 
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()
