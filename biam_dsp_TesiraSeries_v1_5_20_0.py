from extronlib.interface import SerialInterface, EthernetClientInterface
from re import compile, findall, search
from extronlib.system import Wait, ProgramLog
import copy


class DeviceClass:

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 5
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {}

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AECEnable': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'AECGain': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'AECPhantomPower': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'AutoAnswer': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'CrosspointLevel': {'Parameters': ['Instance Tag', 'Input', 'Output'], 'Status': {}},
            'CrosspointState': {'Parameters': ['Instance Tag', 'Input', 'Output'], 'Status': {}},
            'DoNotDisturb': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'DTMF': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'FineLevelControl': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'GraphicEqualizerBandGain': {'Parameters': ['Instance Tag', 'Band'], 'Status': {}},
            'InputLevel': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'InputMute': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'VerboseMode': {'Status': {}},
            'LastDialed': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'LogicInputOutput': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'LogicState': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'LevelControl': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'MuteControl': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'NewSpeedDialEntryNameCommand': {'Parameters': ['Instance Tag', 'Line', 'Entry'], 'Status': {}},
            'NewSpeedDialEntryNumberCommand': {'Parameters': ['Instance Tag', 'Line', 'Entry'], 'Status': {}},
            'OutputLevel': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'OutputMute': {'Parameters': ['Instance Tag', 'Channel'], 'Status': {}},
            'PresetRecall': {'Status': {}},
            'PresetRecallName': {'Parameters': ['Name'], 'Status': {}},
            'PresetSave': {'Status': {}},
            'PresetSaveName': {'Parameters': ['Name'], 'Status': {}},
            'RoomCombinerGroup': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerInputLevel': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerInputMute': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerOutputLevel': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerOutputMute': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerSourceLevel': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerSourceMute': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerSourceSelection': {'Parameters': ['Instance Tag', 'Room'], 'Status': {}},
            'RoomCombinerWall': {'Parameters': ['Instance Tag', 'Wall'], 'Status': {}},
            'RouterControl': {'Parameters': ['Instance Tag', 'Output'], 'Status': {}},
            'SignalPresentMeter': {'Parameters': ['Instance Tag', 'Channel', 'Meter Name'], 'Status': {}},
            'SourceSelectorSourceSelection': {'Parameters': ['Instance Tag'], 'Status': {}},
            'SpeedDial': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'SpeedDialEntryName': {'Parameters': ['Instance Tag', 'Line', 'Entry'], 'Status': {}},
            'SpeedDialEntryNumber': {'Parameters': ['Instance Tag', 'Line', 'Entry'], 'Status': {}},
            'TICallerID': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'TICallStatus': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'TIHook': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'TILineInUse': {'Parameters': ['Instance Tag'], 'Status': {}},
            'VoIPCallerID': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'VoIPCallStatus': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'VoIPHook': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'VoIPLineInUse': {'Parameters': ['Instance Tag', 'Line', 'Call Appearance'], 'Status': {}},
            'VoIPReceiveLevel': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'VoIPReceiveMute': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'VoIPTransmitLevel': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}},
            'VoIPTransmitMute': {'Parameters': ['Instance Tag', 'Line'], 'Status': {}}
        }

        self.deviceUsername = 'admin'
        self.devicePassword = None

        self.verboseDisable = True

        self.findDigit = compile('OK \"value\":(-*\d+)\.*\d*')
        self.Subscribe = []
        self.SUBSCRIPTION_RESPONSE_TIME = 100

        self.SigPresMetChnlName = {}

        if self.Unidirectional == 'False':

            if 'Serial' not in self.ConnectionType:
                self.AddMatchString(compile(b'\xFF\xFD\x18\xFF\xFD\x20\xFF\xFD\x23\xFF\xFD\x27\xFF\xFD\$'), self.__FirstString, None)
                self.AddMatchString(compile(b'\xFF\xFB\x03\xFF\xFD\x01\xFF\xFD\x22\xFF\xFD\x1F\xFF\xFB\x05\xFF\xFD\x21'), self.__SecondString, None)
                self.AddMatchString(compile(b'\xFF\xFB\x01\xFF\xFD\x06\xFF\xFD\x00'), self.__ThirdString, None)

            self.AddMatchString(compile(b'login:'), self.__MatchLogin, None)
            self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
            self.AddMatchString(compile(b'Login incorrect'), self.__MatchIncorrectLogin, None)

            self.AddMatchString(compile(b'Welcome to the Tesira Text Protocol Server'), self.__Verbose, None)
            self.AddMatchString(compile(b'SESSION set verbose true'), self.__matchVerbose, None)

            self.AddMatchString(compile(b'-ERR(?P<error>.*)\r\n'), self.__MatchError, None)
            self.UpdateRegex = compile(b'(\+OK|-ERR).+\r\n')

        self.Authenticated = 'Unknown'
        self.LoginAttemptCount = 0

    def __FirstString(self, match, tag):
        self.Send(b'\xFF\xFC\x18\xFF\xFC\x20\xFF\xFC\x23\xFF\xFC\x27\xFF\xFC\x24')

    def __SecondString(self, match, tag):
        self.Send(b'\xFF\xFE\x03\xFF\xFC\x01\xFF\xFC\x22\xFF\xFC\x1F\xFF\xFE\x05\xFF\xFC\x21')

    def __ThirdString(self, match, tag):
        self.Send(b'\xFF\xFE\x01\xFF\xFC\x06\xFF\xFC\x00')

    def __MatchLogin(self, match, tag):
        self.Authenticated = 'Awaiting'
        if self.deviceUsername is not None:
            self.Send(self.deviceUsername + '\r\n')
        else:
            self.MissingCredentialsLog('Username')

    def __MatchPassword(self, match, tag):
        self.Authenticated = 'Awaiting'
        if self.devicePassword is not None:
            self.Send(self.devicePassword + '\r\n')
        else:
            self.MissingCredentialsLog('Password')

    def __MatchIncorrectLogin(self, match, tag):
        self.Authenticated = 'Failed'
        self.LoginAttemptCount += 1
        if self.LoginAttemptCount > 1:
            print('Invalid credentials. Please supply the correct username and password.')

    def __Verbose(self, match, tag):
        self.Authenticated = 'True'
        self.Send('SESSION set verbose true\r')

    def __matchVerbose(self, match, tag):
        self.verboseDisable = False
        self.Authenticated = 'True'

    def SetAECEnable(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 12:
            cmdString = '{0} set aecEnable {1} {2}\n'.format(tag, chnl, state[value])
            self.__SetHelper('AECEnable', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetAECEnable')

    def UpdateAECEnable(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 12:
            res = self.__UpdateHelper('AECEnable', '{0} get aecEnable {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('AECEnable', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('AECEnable', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateAECEnable')
        else:
            print('Invalid Command for UpdateAECEnable')

    def SetAECGain(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 12 and 0 <= value <= 66:
            cmdString = '{0} set gain {1} {2}\n'.format(tag, chnl, value)
            self.__SetHelper('AECGain', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetAECGain')

    def UpdateAECGain(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 12:
            res = self.__UpdateHelper('AECGain', '{0} get gain {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('AECGain', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateAECGain')
        else:
            print('Invalid Command for UpdateAECGain')

    def SetAECPhantomPower(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 12:
            label = '{0}_{1}'.format(tag, 'AECPhantomPower')
            if tag not in self.Commands['AECPhantomPower']['Status']:

                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(\[.+\])\r\n'.format(label).encode()), self.__MatchAECPhantomPower, tag)

            if label not in self.Subscribe:

                self._SetSubscribeHelper('AECPhantomPower', 'phantomPowers', tag, label, qualifier)

            if ' ' in tag:
                tag = '\"' + tag + '\"'

            cmdString = '{0} set phantomPower {1} {2}\n'.format(tag, chnl, state[value])
            self.__SetHelper('AECPhantomPower', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetAECPhantomPower')

    def UpdateAECPhantomPower(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'AECPhantomPower')
            if tag not in self.Commands['AECPhantomPower']['Status']:

                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(\[.+\])\r\n'.format(label).encode()), self.__MatchAECPhantomPower, tag)

            self._UpdateSubscribeHelper('AECPhantomPower', 'phantomPowers', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateAECPhantomPower')

    def __MatchAECPhantomPower(self, match, tag):
        chnl = 1
        allValues = findall('false|true', match.group(1).decode())
        for value in allValues:
            if 'true' in value:
                self.WriteStatus('AECPhantomPower', 'On', {'Instance Tag': tag, 'Channel': str(chnl)})
            elif 'false' in value:
                self.WriteStatus('AECPhantomPower', 'Off', {'Instance Tag': tag, 'Channel': str(chnl)})
            chnl += 1

    def SetAutoAnswer(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            cmdString = '{0} set autoAnswer {1} {2}\n'.format(tag, line, state[value])
            self.__SetHelper('AutoAnswer', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetAutoAnswer')

    def UpdateAutoAnswer(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('AutoAnswer', '{0} get autoAnswer {1}\n'.format(tag, line), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('AutoAnswer', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('AutoAnswer', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateAutoAnswer')
        else:
            print('Invalid Command for UpdateAutoAnswer')

    def SetCrosspointLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        Input = qualifier['Input']
        Output = qualifier['Output']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(Input) <= 48 and 1 <= int(Output) <= 48 and -100 <= value <= 0:
            cmdString = '{0} set crosspointLevel {1} {2} {3}\n'.format(tag, Input, Output, value)
            self.__SetHelper('CrosspointLevel', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetCrosspointLevel')

    def UpdateCrosspointLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        Input = qualifier['Input']
        Output = qualifier['Output']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(Input) <= 48 and 1 <= int(Output) <= 48:
            res = self.__UpdateHelper('CrosspointLevel', '{0} get crosspointLevel {1} {2}\n'.format(tag, Input, Output), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('CrosspointLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateCrosspointLevel')
        else:
            print('Invalid Command for UpdateCrosspointLevel')

    def SetCrosspointState(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }

        tag = qualifier['Instance Tag']
        Input = qualifier['Input']
        Output = qualifier['Output']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(Input) <= 48 and 1 <= int(Output) <= 48:
            cmdString = '{0} set crosspointLevelState {1} {2} {3}\n'.format(tag, Input, Output, state[value])
            self.__SetHelper('CrosspointState', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetCrosspointState')

    def UpdateCrosspointState(self, value, qualifier):

        tag = qualifier['Instance Tag']
        Input = qualifier['Input']
        Output = qualifier['Output']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(Input) <= 48 and 1 <= int(Output) <= 48:
            res = self.__UpdateHelper('CrosspointState', '{0} get crosspointLevelState {1} {2}\n'.format(tag, Input, Output), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('CrosspointState', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('CrosspointState', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateCrosspointState')
        else:
            print('Invalid Command for UpdateCrosspointState')

    def SetDoNotDisturb(self, value, qualifier):

        ValueStateValues = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            DoNotDisturbCmdString = '{0} set dndEnable {1} {2}\n'.format(tag, line, ValueStateValues[value])
            self.__SetHelper('DoNotDisturb', DoNotDisturbCmdString, value, qualifier)
        else:
            print('Invalid Command for SetDoNotDisturb')

    def UpdateDoNotDisturb(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('DoNotDisturb', '{0} get dndEnable {1}\n'.format(tag, line), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('DoNotDisturb', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('DoNotDisturb', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateDoNotDisturb')
        else:
            print('Invalid Command for UpdateDoNotDisturb')

    def SetDTMF(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']:
            cmdString = '{0} dtmf {1} {2}\n'.format(tag, line, value)
            self.__SetHelper('DTMF', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetDTMF')

    def SetFineLevelControl(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 16 and -100.0 <= value <= 12.0:
            label = '{0}_{1}'.format(tag, 'FineLevelControl')
            if tag not in self.Commands['FineLevelControl']['Status']:

                self.AddMatchString(compile('"publishToken":"{0}" "value":(.+)\r\n'.format(label).encode()), self.__MatchFineLevelControl, tag)
            if label not in self.Subscribe:

                self._SetSubscribeHelper('FineLevelControl', 'levels', tag, label, qualifier)

            if ' ' in tag:
                tag = '\"' + tag + '\"'

            cmdString = '{0} set level {1} {2:.1f}\n'.format(tag, chnl, value)
            self.__SetHelper('FineLevelControl', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetFineLevelControl')

    def UpdateFineLevelControl(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'FineLevelControl')
            if tag not in self.Commands['FineLevelControl']['Status']:

                self.AddMatchString(compile('"publishToken":"{0}" "value":(.+)\r\n'.format(label).encode()), self.__MatchFineLevelControl, tag)

            self._UpdateSubscribeHelper('FineLevelControl', 'levels', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateFineLevelControl')

    def __MatchFineLevelControl(self, match, tag):
        chnl = 1
        allValues = findall('(-?\d+\.\d+)', match.group(1).decode())
        for value in allValues:
            self.WriteStatus('FineLevelControl', float(value), {'Instance Tag': tag, 'Channel': str(chnl)})
            chnl += 1

    def SetGraphicEqualizerBandGain(self, value, qualifier):
        tag = qualifier['Instance Tag']
        band = qualifier['Band']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(band) <= 31 and -30 <= value <= 15:
            cmdString = '{0} set gain {1} {2}\n'.format(tag, band, value)
            self.__SetHelper('GraphicEqualizerBandGain', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetGraphicEqualizerBandGain')

    def UpdateGraphicEqualizerBandGain(self, value, qualifier):
        tag = qualifier['Instance Tag']
        band = qualifier['Band']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(band) <= 31:
            res = self.__UpdateHelper('GraphicEqualizerBandGain', '{0} get gain {1}\n'.format(tag, band), value, qualifier)
            if res:
                result = findall('(-?\d+\.\d+)', res)
                if result:
                    value = round(float(result[0]), 1)
                    self.WriteStatus('GraphicEqualizerBandGain', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateGraphicEqualizerBandGain')
        else:
            print('Invalid Command for UpdateGraphicEqualizerBandGain')

    def SetInputLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48 and -100 <= value <= 12:
            cmdString = '{0} set inputLevel {1} {2}\n'.format(tag, chnl, value)
            self.__SetHelper('InputLevel', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetInputLevel')

    def UpdateInputLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            res = self.__UpdateHelper('InputLevel', '{0} get inputLevel {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('InputLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateInputLevel')
        else:
            print('Invalid Command for UpdateInputLevel')

    def SetInputMute(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            cmdString = '{0} set inputMute {1} {2}\n'.format(tag, chnl, state[value])
            self.__SetHelper('InputMute', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetInputMute')

    def UpdateInputMute(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            res = self.__UpdateHelper('InputMute', '{0} get inputMute {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('InputMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('InputMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateInputMute')
        else:
            print('Invalid Command for UpdateInputMute')

    def UpdateVerboseMode(self, value, qualifier):

        res = self.__UpdateHelper('VerboseMode', 'SESSION get verbose\r', value, qualifier)
        if res:
            if 'true' in res:
                self.WriteStatus('VerboseMode', 'True', qualifier)
            elif 'false' in res:
                self.WriteStatus('VerboseMode', 'False', qualifier)
                self.Send('SESSION set verbose true\r')
        else:
            print('Invalid/unexpected response for UpdateVerboseMode')

    def UpdateLastDialed(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('LastDialed', '{0} get lastNum {1}\r'.format(tag, line), value, qualifier)
            if res:
                try:
                    value = res.split(':')[1].replace('"', '')
                    self.WriteStatus('LastDialed', value, qualifier)
                except IndexError:
                    print('Unexpected response content in {}'.format('UpdateLastDialed'))
        else:
            print('Invalid Command for UpdateLastDialed')

    def SetLevelControl(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 16 and -100 <= value <= 12:
            label = '{0}_{1}'.format(tag, 'LevelControl')
            if tag not in self.Commands['LevelControl']['Status']:
                self.AddMatchString(compile('"publishToken":"{0}" "value":(.+)\r\n'.format(label).encode()), self.__MatchLevelControl, tag)
            if label not in self.Subscribe:
                self._SetSubscribeHelper('LevelControl', 'levels', tag, label, qualifier)

            if ' ' in tag:
                tag = '\"' + tag + '\"'

            cmdString = '{0} set level {1} {2}\n'.format(tag, chnl, value)
            self.__SetHelper('LevelControl', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetLevelControl')

    def UpdateLevelControl(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'LevelControl')
            if tag not in self.Commands['LevelControl']['Status']:
                self.AddMatchString(compile('"publishToken":"{0}" "value":(.+)\r\n'.format(label).encode()), self.__MatchLevelControl, tag)
            self._UpdateSubscribeHelper('LevelControl', 'levels', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateLevelControl')

    def __MatchLevelControl(self, match, tag):
        chnl = 1
        allValues = findall('(-?\d+)\.\d+', match.group(1).decode())
        for value in allValues:
            self.WriteStatus('LevelControl', int(value), {'Instance Tag': tag, 'Channel': str(chnl)})
            chnl += 1

    def SetLogicInputOutput(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 16:
            cmdString = '{0} set invert {1} {2}\n'.format(tag, chnl, value.lower())
            self.__SetHelper('LogicInputOutput', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetLogicInputOutput')

    def UpdateLogicInputOutput(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 16:
            res = self.__UpdateHelper('LogicInputOutput', '{0} get invert {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('LogicInputOutput', 'True', qualifier)
                elif 'false' in res:
                    self.WriteStatus('LogicInputOutput', 'False', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateLogicInputOutput')
        else:
            print('Invalid Command for UpdateLogicInputOutput')

    def SetLogicState(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            cmdString = '{0} set state {1} {2}\n'.format(tag, chnl, value.lower())
            self.__SetHelper('LogicState', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetLogicState')

    def UpdateLogicState(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            res = self.__UpdateHelper('LogicState', '{0} get state {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('LogicState', 'True', qualifier)
                elif 'false' in res:
                    self.WriteStatus('LogicState', 'False', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateLogicState')
        else:
            print('Invalid Command for UpdateLogicState')

    def SetMuteControl(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 16:
            label = '{0}_{1}'.format(tag, 'MuteControl')
            if tag not in self.Commands['MuteControl']['Status']:
                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(\[.+\])\r\n'.format(label).encode()), self.__MatchMuteControl, tag)
            if label not in self.Subscribe:
                self._SetSubscribeHelper('MuteControl', 'mutes', tag, label, qualifier)

            if ' ' in tag:
                tag = '\"' + tag + '\"'

            cmdString = '{0} set mute {1} {2}\n'.format(tag, chnl, state[value])
            self.__SetHelper('MuteControl', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetMuteControl')

    def UpdateMuteControl(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'MuteControl')
            if tag not in self.Commands['MuteControl']['Status']:
                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(\[.+\])\r\n'.format(label).encode()), self.__MatchMuteControl, tag)
            self._UpdateSubscribeHelper('MuteControl', 'mutes', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateMuteControl')

    def __MatchMuteControl(self, match, tag):
        chnl = 1
        allValues = findall('false|true', match.group(1).decode())
        for value in allValues:
            if 'true' in value:
                self.WriteStatus('MuteControl', 'On', {'Instance Tag': tag, 'Channel': str(chnl)})
            elif 'false' in value:
                self.WriteStatus('MuteControl', 'Off', {'Instance Tag': tag, 'Channel': str(chnl)})
            chnl += 1

    def SetNewSpeedDialEntryNameCommand(self, value, qualifier):

        name = value
        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        entry = qualifier['Entry']

        if '/' not in tag and '&' not in tag and name and line in ['1', '2'] and 1 <= int(entry) <= 16:
            name = name.replace('"', '\\"')
            NewSpeedDialEntryNameCommandCmdString = '"{0}" set speedDialLabel {1} {2} "{3}"\r'.format(tag, line, entry, name)
            self.__SetHelper('NewSpeedDialEntryNameCommand', NewSpeedDialEntryNameCommandCmdString, value, qualifier)
        else:
            print('Invalid Command for SetNewSpeedDialEntryNameCommand')

    def SetNewSpeedDialEntryNumberCommand(self, value, qualifier):

        number = value
        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        entry = qualifier['Entry']

        if '/' not in tag and '&' not in tag and number and line in ['1', '2'] and 1 <= int(entry) <= 16:
            number = number.replace('"', '\\"')
            NewSpeedDialEntryNumberCommandCmdString = '"{0}" set speedDialNum {1} {2} "{3}"\r'.format(tag, line, entry, number)
            self.__SetHelper('NewSpeedDialEntryNumberCommand', NewSpeedDialEntryNumberCommandCmdString, value, qualifier)
        else:
            print('Invalid Command for SetNewSpeedDialEntryNumberCommand')

    def SetOutputLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48 and -100 <= value <= 12:
            cmdString = '{0} set outputLevel {1} {2}\n'.format(tag, chnl, value)
            self.__SetHelper('OutputLevel', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetOutputLevel')

    def UpdateOutputLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            res = self.__UpdateHelper('OutputLevel', '{0} get outputLevel {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('OutputLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateOutputLevel')
        else:
            print('Invalid Command for UpdateOutputLevel')

    def SetOutputMute(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            cmdString = '{0} set outputMute {1} {2}\n'.format(tag, chnl, state[value])
            self.__SetHelper('OutputMute', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetOutputMute')

    def UpdateOutputMute(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(chnl) <= 48:
            res = self.__UpdateHelper('OutputMute', '{0} get outputMute {1}\n'.format(tag, chnl), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('OutputMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('OutputMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateOutputMute')
        else:
            print('Invalid Command for UpdateOutputMute')

    def UpdateSpeedDialEntryName(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        entry = qualifier['Entry']

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and 1 <= int(entry) <= 16:
            SpeedDialEntryNameCmdString = '"{0}" get speedDialLabel {1} {2}\r'.format(tag, line, entry)

            res = self.__UpdateHelper('SpeedDialEntryName', SpeedDialEntryNameCmdString, value, qualifier)
            if res:
                name = search('\+OK "value":"(.*)"\r\n', res)
                if name:
                    self.WriteStatus('SpeedDialEntryName', name.group(1), qualifier)
                else:
                    print('Unexpected response content in {}'.format('UpdateSpeedDialEntryName'))
        else:
            print('Invalid Command for UpdateSpeedDialEntryName')

    def UpdateSpeedDialEntryNumber(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        entry = qualifier['Entry']

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and 1 <= int(entry) <= 16:
            SpeedDialEntryNumberCmdString = '"{0}" get speedDialNum {1} {2}\r'.format(tag, line, entry)

            res = self.__UpdateHelper('SpeedDialEntryNumber', SpeedDialEntryNumberCmdString, value, qualifier)
            if res:
                num = search('\+OK "value":"(.*)"\r\n', res)
                if num:
                    self.WriteStatus('SpeedDialEntryNumber', num.group(1), qualifier)
                else:
                    print('Unexpected response content in {}'.format('UpdateSpeedDialEntryNumber'))
        else:
            print('Invalid Command for UpdateSpeedDialEntryNumber')

    def SetPresetRecall(self, value, qualifier):

        if 1 <= int(value) <= 128:
            cmdString = 'DEVICE recallPreset {0}\r'.format(int(value) + 1000)
            self.__SetHelper('PresetRecall', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetPresetRecall')

    def SetPresetRecallName(self, value, qualifier):

        name = qualifier['Name']
        if name:
            PresetRecallNameCmdString = 'DEVICE recallPresetByName {0}\r'.format(name)
            self.__SetHelper('PresetRecallName', PresetRecallNameCmdString, value, qualifier)
        else:
            print('Invalid Command for SetPresetRecallName')

    def SetPresetSave(self, value, qualifier):

        if 1 <= int(value) <= 128:
            PresetSaveCmdString = 'DEVICE savePreset {0}\r'.format(int(value) + 1000)
            self.__SetHelper('PresetSave', PresetSaveCmdString, value, qualifier)
        else:
            print('Invalid Command for SetPresetSave')

    def SetPresetSaveName(self, value, qualifier):

        name = qualifier['Name']
        if name:
            PresetSaveNameCmdString = 'DEVICE savePresetByName {0}\r'.format(name)
            self.__SetHelper('PresetSaveName', PresetSaveNameCmdString, value, qualifier)
        else:
            print('Invalid Command for SetPresetSaveName')

    def SetRoomCombinerGroup(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 56 and 0 <= int(value) <= 56:
            cmdString = '{0} set group {1} {2}\n'.format(tag, room, value)
            self.__SetHelper('RoomCombinerGroup', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerGroup')

    def UpdateRoomCombinerGroup(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 56:
            res = self.__UpdateHelper('RoomCombinerGroup', '{0} get group {1}\n'.format(tag, room), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('RoomCombinerGroup', str(value), qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerGroup')
        else:
            print('Invalid Command for UpdateRoomCombinerGroup')

    def SetRoomCombinerInputLevel(self, value, qualifier):

        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and ValueConstraints['Min'] <= value <= ValueConstraints['Max'] and 1 <= int(room) <= 32:
            RoomCombinerInputLevelCmdString = '{0} set levelIn {1} {2}\n'.format(tag, room, value)
            self.__SetHelper('RoomCombinerInputLevel', RoomCombinerInputLevelCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerInputLevel')

    def UpdateRoomCombinerInputLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerInputLevelCmdString = '{0} get levelIn {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerInputLevel', RoomCombinerInputLevelCmdString, value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('RoomCombinerInputLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerInputLevel')
        else:
            print('Invalid Command for UpdateRoomCombinerInputLevel')

    def SetRoomCombinerInputMute(self, value, qualifier):

        ValueStateValues = {
            'On': 'true',
            'Off': 'false'
        }

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerInputMuteCmdString = '{0} set muteIn {1} {2}\n'.format(tag, room, ValueStateValues[value])
            self.__SetHelper('RoomCombinerInputMute', RoomCombinerInputMuteCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerInputMute')

    def UpdateRoomCombinerInputMute(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerInputMuteCmdString = '{0} get muteIn {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerInputMute', RoomCombinerInputMuteCmdString, value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('RoomCombinerInputMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('RoomCombinerInputMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerInputMute')
        else:
            print('Invalid Command for UpdateRoomCombinerInputMute')

    def SetRoomCombinerOutputLevel(self, value, qualifier):

        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and ValueConstraints['Min'] <= value <= ValueConstraints['Max'] and 1 <= int(room) <= 32:
            RoomCombinerOutputLevelCmdString = '{0} set levelOut {1} {2}\n'.format(tag, room, value)
            self.__SetHelper('RoomCombinerOutputLevel', RoomCombinerOutputLevelCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerOutputLevel')

    def UpdateRoomCombinerOutputLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerOutputLevelCmdString = '{0} get levelOut {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerOutputLevel', RoomCombinerOutputLevelCmdString, value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('RoomCombinerOutputLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerOutputLevel')
        else:
            print('Invalid Command for UpdateRoomCombinerOutputLevel')

    def SetRoomCombinerOutputMute(self, value, qualifier):

        ValueStateValues = {
            'On': 'true',
            'Off': 'false'
        }

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerOutputMuteCmdString = '{0} set muteOut {1} {2}\n'.format(tag, room, ValueStateValues[value])
            self.__SetHelper('RoomCombinerOutputMute', RoomCombinerOutputMuteCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerOutputMute')

    def UpdateRoomCombinerOutputMute(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerOutputMuteCmdString = '{0} get muteOut {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerOutputMute', RoomCombinerOutputMuteCmdString, value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('RoomCombinerOutputMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('RoomCombinerOutputMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerOutputMute')
        else:
            print('Invalid Command for UpdateRoomCombinerOutputMute')

    def SetRoomCombinerSourceLevel(self, value, qualifier):

        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and ValueConstraints['Min'] <= value <= ValueConstraints['Max'] and 1 <= int(room) <= 32:
            RoomCombinerSourceLevelCmdString = '{0} set levelSource {1} {2}\n'.format(tag, room, value)
            self.__SetHelper('RoomCombinerSourceLevel', RoomCombinerSourceLevelCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerSourceLevel')

    def UpdateRoomCombinerSourceLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        room = qualifier['Room']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerSourceLevelCmdString = '{0} get levelSource {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerSourceLevel', RoomCombinerSourceLevelCmdString, value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('RoomCombinerSourceLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerSourceLevel')
        else:
            print('Invalid Command for UpdateRoomCombinerSourceLevel')

    def SetRoomCombinerSourceMute(self, value, qualifier):

        ValueStateValues = {
            'On': 'true',
            'Off': 'false'
        }

        room = qualifier['Room']
        tag = qualifier['Instance Tag']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerSourceMuteCmdString = '{0} set muteSource {1} {2}\n'.format(tag, room, ValueStateValues[value])
            self.__SetHelper('RoomCombinerSourceMute', RoomCombinerSourceMuteCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerSourceMute')

    def UpdateRoomCombinerSourceMute(self, value, qualifier):

        room = qualifier['Room']
        tag = qualifier['Instance Tag']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerSourceMuteCmdString = '{0} get muteSource {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerSourceMute', RoomCombinerSourceMuteCmdString, value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('RoomCombinerSourceMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('RoomCombinerSourceMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerSourceMute')
        else:
            print('Invalid Command for UpdateRoomCombinerSourceMute')

    def SetRoomCombinerSourceSelection(self, value, qualifier):

        ValueStateValues = {
            'No Source': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4'
        }

        room = qualifier['Room']
        tag = qualifier['Instance Tag']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerSourceSelectionCmdString = '{0} set sourceSelection {1} {2}\n'.format(tag, room, ValueStateValues[value])
            self.__SetHelper('RoomCombinerSourceSelection', RoomCombinerSourceSelectionCmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerSourceSelection')

    def UpdateRoomCombinerSourceSelection(self, value, qualifier):

        ValueStateValues = {
            '0': 'No Source',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4'
        }

        room = qualifier['Room']
        tag = qualifier['Instance Tag']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(room) <= 32:
            RoomCombinerSourceSelectionCmdString = '{0} get sourceSelection {1}\n'.format(tag, room)
            res = self.__UpdateHelper('RoomCombinerSourceSelection', RoomCombinerSourceSelectionCmdString, value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('RoomCombinerSourceSelection', ValueStateValues[str(value)], qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerSourceSelection')
        else:
            print('Invalid Command for UpdateRoomCombinerSourceSelection')

    def SetRoomCombinerWall(self, value, qualifier):

        state = {
            'Close': 'true',
            'Open': 'false',
        }

        tag = qualifier['Instance Tag']
        wall = qualifier['Wall']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(wall) <= 56:
            cmdString = '{0} set wallState {1} {2}\n'.format(tag, wall, state[value])
            self.__SetHelper('RoomCombinerWall', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetRoomCombinerWall')

    def UpdateRoomCombinerWall(self, value, qualifier):

        tag = qualifier['Instance Tag']
        wall = qualifier['Wall']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(wall) <= 56:
            res = self.__UpdateHelper('RoomCombinerWall', '{0} get wallState {1}\n'.format(tag, wall), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('RoomCombinerWall', 'Close', qualifier)
                elif 'false' in res:
                    self.WriteStatus('RoomCombinerWall', 'Open', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRoomCombinerWall')
        else:
            print('Invalid Command for UpdateRoomCombinerWall')

    def SetRouterControl(self, value, qualifier):

        tag = qualifier['Instance Tag']
        Output = qualifier['Output']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(Output) <= 56 and 0 <= int(value) <= 56:
            cmdString = '{0} set input {1} {2}\n'.format(tag, Output, value)
            self.__SetHelper('RouterControl', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetRouterControl')

    def UpdateRouterControl(self, value, qualifier):

        tag = qualifier['Instance Tag']
        Output = qualifier['Output']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and 1 <= int(Output) <= 56:
            res = self.__UpdateHelper('RouterControl', '{0} get input {1}\n'.format(tag, Output), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('RouterControl', str(value), qualifier)
                else:
                    print('Invalid/unexpected response for UpdateRouterControl')
        else:
            print('Invalid Command for UpdateRouterControl')

    def UpdateSignalPresentMeter(self, value, qualifier):

        tag = qualifier['Instance Tag']
        chnl = qualifier['Channel']
        label = qualifier['Meter Name']

        if '/' not in tag and '&' not in tag and label and 1 <= int(chnl) <= 32:
            commandstring = 'present {0}'.format(chnl)
            self.SigPresMetChnlName[qualifier['Meter Name']] = chnl

            if tag not in self.Commands['SignalPresentMeter']['Status']:
                self.AddMatchString(compile('\! "publishToken":"({0})" "value":(false|true)\r\n'.format(label).encode()), self.__MatchSignalPresentMeter, tag)
            self._UpdateSubscribeHelper('SignalPresentMeter', commandstring, tag, label, qualifier)
        else:
            print('Invalid Command for UpdateSignalPresentMeter')

    def __MatchSignalPresentMeter(self, match, tag):

        meterName = match.group(1).decode()
        value = match.group(2).decode()
        if value == 'true':
            self.WriteStatus('SignalPresentMeter', 'Signal Present', {'Instance Tag': tag, 'Channel': self.SigPresMetChnlName[meterName], 'Meter Name': meterName})
        elif value == 'false':
            self.WriteStatus('SignalPresentMeter', 'No Signal Present', {'Instance Tag': tag, 'Channel': self.SigPresMetChnlName[meterName], 'Meter Name': meterName})

    def SetSourceSelectorSourceSelection(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag and value == 'No Source' or 1 <= int(value) <= 32:
            label = '{0}_{1}'.format(tag, 'SourceSelectorSourceSelection')
            if tag not in self.Commands['SourceSelectorSourceSelection']['Status']:
                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(\d|\d\d)\r\n'.format(label).encode()), self.__MatchSourceSelectorSourceSelection, tag)
            if label not in self.Subscribe:
                self._SetSubscribeHelper('SourceSelectorSourceSelection', 'sourceSelection', tag, label, qualifier)

            if ' ' in tag:
                tag = '\"' + tag + '\"'
            if value == 'No Source':
                source = '0'
            else:
                source = value
            cmdString = '{0} set sourceSelection {1}\n'.format(tag, source)
            self.__SetHelper('SourceSelectorSourceSelection', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetSourceSelectorSourceSelection')

    def UpdateSourceSelectorSourceSelection(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'SourceSelectorSourceSelection')
            if tag not in self.Commands['SourceSelectorSourceSelection']['Status']:
                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(\d|\d\d)\r\n'.format(label).encode()), self.__MatchSourceSelectorSourceSelection, tag)
            self._UpdateSubscribeHelper('SourceSelectorSourceSelection', 'sourceSelection', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateSourceSelectorSourceSelection')

    def __MatchSourceSelectorSourceSelection(self, match, tag):
        value = match.group(1).decode()
        if value == '0':
            self.WriteStatus('SourceSelectorSourceSelection', 'No Source', {'Instance Tag': tag})
        elif 1 <= int(value) <= 32:
            self.WriteStatus('SourceSelectorSourceSelection', value, {'Instance Tag': tag})
        else:
            print('Invalid/unexpected response')

    def SetSpeedDial(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        call = qualifier['Call Appearance']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and 1 <= int(call) <= 6 and 1 <= int(value) <= 16:
            cmdString = '{0} speedDial {1} {2} {3}\n'.format(tag, line, call, value)
            self.__SetHelper('SpeedDial', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetSpeedDial')

    def UpdateTICallerID(self, value, qualifier):
        self.UpdateTICallStatus(value, qualifier)

    def UpdateTICallStatus(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'TICallStatus')
            if tag not in self.Commands['TICallStatus']['Status']:
                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(.+)\r\n'.format(label).encode()), self.__MatchTICallStatus, tag)
            self._UpdateSubscribeHelper('TICallStatus', 'callState', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateTICallStatus')

    def __MatchTICallStatus(self, match, tag):

        line = 1
        call = 1
        res = match.group(1).decode()

        stateValues = findall('\"state\":TI_CALL_STATE_(\w+) \"', res)
        for val in stateValues:
            value = val.replace('_', ' ').title()
            self.WriteStatus('TICallStatus', value, {'Instance Tag': tag, 'Line': str(line), 'Call Appearance': str(call)})
            if call >= 6:
                call = 0
                line += 1
            call += 1

        line = 1
        call = 1
        idValues = findall('"cid":"\x5C\x5C"(\d{8})\x5C\x5C"\x5C\x5C"(.*?)\x5C\x5C"\x5C\x5C"(.*?)\x5C\x5C""|"cid":""', res)
        for id_ in idValues:
            name = id_[2]
            number = id_[1]
            if number:
                if name:
                    value = name + ' : ' + number
                else:
                    value = number
            else:
                value = ''
            self.WriteStatus('TICallerID', value, {'Instance Tag': tag, 'Line': str(line), 'Call Appearance': str(call)})
            if call >= 6:
                call = 0
                line += 1
            call += 1

    def SetTIHook(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        call = qualifier['Call Appearance']
        if call == 'None':
            call = ''
        if line == 'None':
            line = ''
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2', 'None'] and call in ['1', '2', '3', '4', '5', '6', 'None']:
            if value in ['Redial', 'End', 'Flash', 'Send', 'Answer']:
                cmdString = '{0} {1} {2} {3}\n'.format(tag, value.lower(), line, call)
                self.__SetHelper('TIHook', cmdString, value, qualifier)
            elif value in ['Off', 'On']:
                cmdString = '{0} {1}Hook {2} {3}\n'.format(tag, value.lower(), line, call)
                self.__SetHelper('TIHook', cmdString, value, qualifier)
            elif value == 'Dial':
                number = qualifier['Number']
                if number:
                    cmdString = '{0} dial {1} {2} {3}\n'.format(tag, line, call, number)
                    self.__SetHelper('TIHook', cmdString, value, qualifier)
            else:
                print('Invalid Command for SetTIHook')
        else:
            print('Invalid Command for SetTIHook')

    def UpdateTILineInUse(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'TILineInUse')
            if tag not in self.Commands['TILineInUse']['Status']:
                self.AddMatchString(compile('\! "publishToken":"{0}" "value":(false|true)\r\n'.format(label).encode()), self.__MatchTILineInUse, tag)
            self._UpdateSubscribeHelper('TILineInUse', 'lineInUse', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateTILineInUse')

    def __MatchTILineInUse(self, match, tag):

        ValueStateValues = {
            'true': 'In Use',
            'false': 'Not in Use'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('TILineInUse', value, {'Instance Tag': tag})

    def UpdateVoIPCallerID(self, value, qualifier):

        self.UpdateVoIPCallStatus(value, qualifier)

    def UpdateVoIPCallStatus(self, value, qualifier):

        tag = qualifier['Instance Tag']

        if '/' not in tag and '&' not in tag:
            label = '{0}_{1}'.format(tag, 'VoIPCallStatus')
            if tag not in self.Commands['VoIPCallStatus']['Status']:
                self.AddMatchString(compile('"publishToken":"{0}" "value":(.+)\r\n'.format(label).encode()), self.__MatchVoIPCallStatus, tag)
            self._UpdateSubscribeHelper('VoIPCallStatus', 'callState', tag, label, qualifier)
        else:
            print('Invalid Command for UpdateVoIPCallStatus')

    def __MatchVoIPCallStatus(self, match, tag):

        line = 1
        call = 1
        res = match.group(1).decode()

        stateValues = findall('\"state\":VOIP_CALL_STATE_(\w+) \"', res)
        for val in stateValues:
            value = val.replace('_', ' ').title()
            self.WriteStatus('VoIPCallStatus', value, {'Instance Tag': tag, 'Line': str(line), 'Call Appearance': str(call)})
            if call >= 6:
                call = 0
                line += 1
            call += 1

        line = 1
        call = 1
        idValues = findall('"cid":"\x5C\x5C"(\d{8})\x5C\x5C"\x5C\x5C"(.*?)\x5C\x5C"\x5C\x5C"(.*?)\x5C\x5C""|"cid":""', res)
        for id_ in idValues:
            name = id_[2]
            number = id_[1]
            if number:
                value = number
                if name:
                    value = name + ' : ' + number
            else:
                value = ''
            self.WriteStatus('VoIPCallerID', value, {'Instance Tag': tag, 'Line': str(line), 'Call Appearance': str(call)})
            if call >= 6:
                call = 0
                line += 1
            call += 1

    def SetVoIPHook(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        call = qualifier['Call Appearance']
        if call == 'None':
            call = ''
        if line == 'None':
            line = ''
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2', 'None'] and call in ['1', '2', '3', '4', '5', '6', 'None']:
            if value in ['Redial', 'End', 'Flash', 'Send', 'Answer', 'Resume', 'Hold']:
                cmdString = '{0} {1} {2} {3}\n'.format(tag, value.lower(), line, call)
                self.__SetHelper('VoIPHook', cmdString, value, qualifier)
            elif value in ['Off', 'On']:
                cmdString = '{0} {1}Hook {2} {3}\n'.format(tag, value.lower(), line, call)
                self.__SetHelper('VoIPHook', cmdString, value, qualifier)
            elif value == 'Dial':
                number = qualifier['Number']
                cmdString = '{0} dial {1} {2} {3}\n'.format(tag, line, call, number)
                self.__SetHelper('VoIPHook', cmdString, value, qualifier)
            elif value == 'Conference':
                cmdString = '{0} lconf {1} {2}\n'.format(tag, line, call)
                self.__SetHelper('VoIPHook', cmdString, value, qualifier)
            elif value == 'Leave Conference':
                cmdString = '{0} leaveConf {1} {2}\n'.format(tag, line, call)
                self.__SetHelper('VoIPHook', cmdString, value, qualifier)
            else:
                print('Invalid Command for SetVoIPHook')
        else:
            print('Invalid Command for SetVoIPHook')

    def UpdateVoIPLineInUse(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        call = qualifier['Call Appearance']

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and 1 <= int(call) <= 6:
            label = '{0}_{1}_{2}'.format('VoIPLineInUse', line, call)
            if tag not in self.Commands['VoIPLineInUse']['Status']:
                self.AddMatchString(compile('\! "publishToken":"({0})" "value":(false|true)\r\n'.format(label).encode()), self.__MatchVoIPLineInUse, tag)
            self._UpdateSubscribeHelper('VoIPLineInUse', 'lineInUse {0} {1}'.format(line, call), tag, label, qualifier)
        else:
            print('Invalid Command for UpdateVoIPLineInUse')

    def __MatchVoIPLineInUse(self, match, tag):

        ValueStateValues = {
            'true': 'In Use',
            'false': 'Not in Use'
        }

        result = match.group(1).decode().split('_')
        line = result[1]
        call = result[2]
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('VoIPLineInUse', value, {'Instance Tag': tag, 'Line': line, 'Call Appearance': call})

    def SetVoIPReceiveLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and -100 <= value <= 12:
            cmdString = '{0} set level {1} {2}\n'.format(tag, line, value)
            self.__SetHelper('VoIPReceiveLevel', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetVoIPReceiveLevel')

    def UpdateVoIPReceiveLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('VoIPReceiveLevel', '{0} get level {1}\n'.format(tag, line), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('VoIPReceiveLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateVoIPReceiveLevel')
        else:
            print('Invalid Command for UpdateVoIPReceiveLevel')

    def SetVoIPReceiveMute(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            cmdString = '{0} set mute {1} {2}\n'.format(tag, line, state[value])
            self.__SetHelper('VoIPReceiveMute', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetVoIPReceiveMute')

    def UpdateVoIPReceiveMute(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('VoIPReceiveMute', '{0} get mute {1}\n'.format(tag, line), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('VoIPReceiveMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('VoIPReceiveMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateVoIPReceiveMute')
        else:
            print('Invalid Command for UpdateVoIPReceiveMute')

    def SetVoIPTransmitLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2'] and -100 <= value <= 12:
            cmdString = '{0} set level {1} {2}\n'.format(tag, line, value)
            self.__SetHelper('VoIPTransmitLevel', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetVoIPTransmitLevel')

    def UpdateVoIPTransmitLevel(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('VoIPTransmitLevel', '{0} get level {1}\n'.format(tag, line), value, qualifier)
            if res:
                result = findall(self.findDigit, res)
                if result:
                    value = int(result[0])
                    self.WriteStatus('VoIPTransmitLevel', value, qualifier)
                else:
                    print('Invalid/unexpected response for UpdateVoIPTransmitLevel')
        else:
            print('Invalid Command for UpdateVoIPTransmitLevel')

    def SetVoIPTransmitMute(self, value, qualifier):

        state = {
            'On': 'true',
            'Off': 'false',
        }
        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            cmdString = '{0} set mute {1} {2}\n'.format(tag, line, state[value])
            self.__SetHelper('VoIPTransmitMute', cmdString, value, qualifier)
        else:
            print('Invalid Command for SetVoIPTransmitMute')

    def UpdateVoIPTransmitMute(self, value, qualifier):

        tag = qualifier['Instance Tag']
        line = qualifier['Line']
        if ' ' in tag:
            tag = '\"' + tag + '\"'

        if '/' not in tag and '&' not in tag and line in ['1', '2']:
            res = self.__UpdateHelper('VoIPTransmitMute', '{0} get mute {1}\n'.format(tag, line), value, qualifier)
            if res:
                if 'true' in res:
                    self.WriteStatus('VoIPTransmitMute', 'On', qualifier)
                elif 'false' in res:
                    self.WriteStatus('VoIPTransmitMute', 'Off', qualifier)
                else:
                    print('Invalid/unexpected response for UpdateVoIPTransmitMute')
        else:
            print('Invalid Command for UpdateVoIPTransmitMute')

    def __MatchError(self, match, tag):

        print(match.group('error').decode().strip())

    def __CheckResponseForErrors(self, sourceCmdName, res):

        if '+OK' in res:
            self.Authenticated = 'True'
            return res
        elif '-ERR' in res:
            print('{0} {1}'.format(sourceCmdName, res))
            return ''
        else:
            return ''

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        if self.verboseDisable:
            self.Send('SESSION set verbose true\r')
        self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.Unidirectional == 'True':
            print('Inappropriate Command ', command)
            return ''
        else:
            if self.initializationChk:
                self.OnConnected()
                self.initializationChk = False

            self.counter = self.counter + 1
            if self.counter > self.connectionCounter and self.connectionFlag:
                self.OnDisconnected()

            if self.verboseDisable:
                self.Send('SESSION set verbose true\r')
            elif self.Authenticated == 'True' or (self.ConnectionType == 'Serial' and self.Authenticated not in ['Failed', 'Awaiting']):
                res = self.SendAndWait(commandstring, self.DefaultResponseTimeout, deliRex=self.UpdateRegex)
                return self.__CheckResponseForErrors(command, res.decode())
            else:
                print('Inappropriate Command ', command)
                return ''

    def _SetSubscribeHelper(self, command, commandstring, tag, label, qualifier):
        if self.Authenticated == 'True' and self.Unidirectional == 'False':
            self.Subscribe.append(label)

            unsubscribe = '"{0}" unsubscribe {1} "{2}"\n'.format(tag, commandstring, label)
            self.Send(unsubscribe)

            subscribe = '"{0}" subscribe {1} "{2}" {3}\n'.format(tag, commandstring, label, self.SUBSCRIPTION_RESPONSE_TIME)
            self.Send(subscribe)
        else:
            print('Inappropriate Command when subscribing Set', command)

    def _UpdateSubscribeHelper(self, command, commandstring, tag, label, qualifier):
        if self.Authenticated == 'True' and self.Unidirectional == 'False':
            if label not in self.Subscribe:
                self.Subscribe.append(label)

                unsubscribe = '"{0}" unsubscribe {1} "{2}"\n'.format(tag, commandstring, label)
                self.Send(unsubscribe)

                subscribe = '"{0}" subscribe {1} "{2}" {3}\n'.format(tag, commandstring, label, self.SUBSCRIPTION_RESPONSE_TIME)
                self.Send(subscribe)
        else:
            print('Inappropriate Command when subscribing Update', command)

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        self.Subscribe.clear()

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        self.Authenticated = 'Unknown'
        self.verboseDisable = True
        self.LoginAttemptCount = 0

    ######################################################
    # RECOMMENDED not to modify the code below this point
    ######################################################

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

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method': {}}

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
        if command in self.Subscription:
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

    def __ReceiveData(self, interface, data):
        # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para': arg}

    # Check incoming unsolicited data to see if it was matched with device expectancy.
    def CheckMatchedString(self):
        tempList = copy.copy(self._compile_list)
        for regexString in tempList:
            while True:
                result = search(regexString, self._ReceiveBuffer)
                if result:
                    tempList[regexString]['callback'](result, tempList[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True


class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=115200, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay)
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
