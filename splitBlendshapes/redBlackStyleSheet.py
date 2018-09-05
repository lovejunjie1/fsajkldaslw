class RedBlackStyleSheet():
    iconPath = ''
    bgColor = 'rgb(68,68,68)'
    fontBlack = 'rgb(143,143,143)'
    fontWhite = 'rgb(206,206,206)'
    btnMainColor = 'rgb(235,75,57)'

    def __init__(self):
        self.bgColor_light = self.lighterColor(self.bgColor)
        self.bgColor_dark = self.dakerColor(self.bgColor)
        warningText = '========\nMstyle ver0_10\nthis version can not suit for older version.\n2017-11-16 15:17:20\n========'
        print warningText

    def setIconPath(self, path):
        self.iconPath = path.replace('\\', '/')
        # print self.iconPath

    def lighterColor(self, tc, times=1):
        theColor = tc[4:-1].split(',')
        r = int(theColor[0]) + (15 * times)
        g = int(theColor[1]) + (15 * times)
        b = int(theColor[2]) + (15 * times)
        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255
        return ('rgb({},{},{})'.format(str(r), str(g), str(b)))

    def dakerColor(self, tc, times=1):
        theColor = tc[4:-1].split(',')
        r = int(theColor[0]) - (15 * times)
        g = int(theColor[1]) - (15 * times)
        b = int(theColor[2]) - (15 * times)
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        return ('rgb({},{},{})'.format(str(r), str(g), str(b)))

    def QWidget(self):
        mainWidgetStyle = (
        'QWidget {background-color :' + self.bgColor + ';border:0px solid ' + self.fontBlack + ';color:' + self.fontWhite + ';}')
        return mainWidgetStyle

    def QPushButton(self, kw='on', lang='e', bordRad='8px', bordWid='0px'):
        font = ''
        btnStyle = ''
        if lang == 'e':
            font = 'Verdana'
        elif lang == 'c':
            font = 'Microsoft YaHei'

        colorSet = {
            'on': [['rgb(95,25,15)', self.fontBlack, self.btnMainColor],
                   ['white', self.fontBlack, self.btnMainColor],
                   ['rgb(150,150,150)', self.fontBlack, 'rgb(225,55,37)']],

            'off': [['rgb(208,208,208)', self.fontBlack, 'rgb(100,100,100)'],
                    ['white', self.fontBlack, self.lighterColor(self.bgColor, times=4)],
                    ['white', self.fontBlack, 'rgb(60,60,60)']],

            'b': [['rgb(90,50,40)', self.fontBlack, 'rgb(245,163,61)'],
                  ['white', self.fontBlack, 'rgb(245,163,61)'],
                  ['rgb(150,150,150)', self.fontBlack, 'rgb(225,143,41)']]
        }
        if kw in colorSet.keys():
            data = colorSet[kw]
            btnStyle = ('QPushButton   {font-family:' + font + ';font-size:13px;font-weight:None;font-style:oblique;'
                                                               'border-radius:' + bordRad + ';padding-top:0px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                            'color:' + data[0][
                            0] + ';border:' + bordWid + ' solid ' + data[0][1] + ';'
                                                                                 'background: ' + data[0][2] + ';}'

                                                                                                               'QPushButton:hover{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                              'color:' +
                        data[1][0] + ';border:' + bordWid + ' solid ' + data[1][1] + ';'
                                                                                     'background: ' + data[1][2] + ';}'

                                                                                                                   'QPushButton:pressed{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                    'color:rgb' +
                        data[2][0] + ';border:' + bordWid + ' solid ' + data[2][1] + ';'
                                                                                     'background: ' + data[2][2] + ';}')
        else:
            if kw == 'c':
                btnStyle = (
                'QPushButton   {font-family:' + font + ';font-size:13px;font-weight:None;font-style:oblique;'
                                                       'border-radius:' + bordRad + ';padding-top:0px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                    'color:rgb(230,230,230);border:' + bordWid + ' solid transparent;'
                                                                                                                                 'background: transparent;}'

                                                                                                                                 'QPushButton:hover{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                                'color:rgb(255,255,255);border:' + bordWid + ' solid transparent;'
                                                                                                                                                                                                                             'background: transparent;}'

                                                                                                                                                                                                                             'QPushButton:pressed{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                                                                                                                              'color:rgb(80,80,80);border:' + bordWid + ' solid transparent;'
                                                                                                                                                                                                                                                                                                                        'background: transparent;}')
            elif kw == 'radiobutton':
                btnStyle = (
                'QPushButton   {font-family:' + font + ';font-size:13px;font-weight:None;font-style:oblique;'
                                                       'border-radius:' + bordRad + ';padding-top:0px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                    'color:rgb(80,80,80);border:' + bordWid + ' solid transparent;'
                                                                                                                              'background: ' + self.btnMainColor + ';}'
                                                                                                                                                                   'QPushButton:checked{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                                                                    'color:rgb(230,230,230);border:' + bordWid + ' solid transparent;'
                                                                                                                                                                                                                                                                 'background: rgb(245,163,61);}'
                                                                                                                                                                                                                                                                 'QPushButton:hover{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                                                                                                                                                                'color:rgb(255,255,255);border:' + bordWid + ' solid transparent;}'

                                                                                                                                                                                                                                                                                                                                                             'QPushButton:pressed{border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                                                                                                                                                                                                                                                              'color:rgb(80,80,80);border:' + bordWid + ' solid transparent;'
                                                                                                                                                                                                                                                                                                                                                                                                                                                        'background: rgb(225,143,41);}'
                )
        return btnStyle

    def xBtnStyle(self):
        xBtnStyle = ('QPushButton   {font-family:Verdana;font-size:15px;font-weight:None;font-style:oblique;'
                     'border-radius:8px;padding-top:0px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                     'color:rgb(248,91,90);border:0px solid ' + self.fontBlack + ';'
                                                                                 'background: ' + self.bgColor + ';}'

                                                                                                                 'QPushButton:hover{border-radius:8px;padding-top:px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                 'color:rgb(255,0,0);border:0px solid ' + self.fontBlack + ';'
                                                                                                                                                                           'background: ' + self.bgColor + ';}'

                                                                                                                                                                                                           'QPushButton:pressed{border-radius:8px;padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;'
                                                                                                                                                                                                           'color:rgb(255,255,255);border:0px solid ' + self.fontBlack + ';'
                                                                                                                                                                                                                                                                         'background: ' + self.bgColor + ';}')
        return xBtnStyle

    def QLineEdit(self, kw='a', lang='e', bordRad='8px', bordWid='0px', fontSize='10px'):
        LineEditStyle = ''
        font = ''
        fontStyle = ''
        if lang == 'e':
            font = 'Verdana'
            fontStyle = 'oblique'
        elif lang == 'c':
            font = 'Microsoft YaHei'
            fontStyle = 'None'

        colorSet = {
            'a': ['rgb(220,220,220)', self.fontBlack, 'rgb(100,100,100)', 'rgb(220,220,220)', self.fontBlack,
                  'rgb(100,100,100)'],
            'b': [self.fontWhite, self.fontBlack, 'rgb(245,163,61)', self.fontWhite, self.fontBlack, 'rgb(245,163,61)'],
            'c': [self.fontWhite, self.fontBlack, 'rgb(68,68,68)', self.fontWhite, self.fontBlack, 'rgb(58,58,58)']
        }
        if kw in colorSet.keys():
            data = colorSet[kw]
            LineEditStyle = (
            'QLineEdit {font-family:' + font + ';font-size:' + fontSize + ';font-weight:None;font-style:' + fontStyle + ';color:' +
            data[0] + ';border:' + bordWid + ' solid ' + data[1] + ';border-radius:' + bordRad + ';background:' + data[
                2] + ';}'
                     'QLineEdit:hover {font-size:10px;font-weight:None;font-style:oblique;color:' + data[
                3] + ';border:' + bordWid + ' solid ' + data[4] + ';border-radius:' + bordRad + ';background:' + data[
                5] + ';}'

            )
        else:
            if kw == 'd':
                LineEditStyle = (
                'QLineEdit {font-family:' + font + ';font-size:' + fontSize + ';font-weight:None;font-style:' + fontStyle + ';color:' + self.fontWhite + ';border:' + bordWid + ' solid transparent;border-top-right-radius: ' + bordRad + '; border-top-left-radius: ' + bordRad + ';  border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;background:transparent;}'
                                                                                                                                                                                                                                                                                    'QLineEdit:hover {font-size:10px;font-weight:None;font-style:oblique;color:white;border:' + bordWid + ' solid transparent;border-radius:' + bordRad + ';background:rgb(120,120,120);}'
                )
        return LineEditStyle

    def QLabel(self, kw='a', lang='e', bordRad='8px', bordWid='0px', fontSize='20px'):
        font = ''
        fontStyle = ''
        LabelStyle = ''
        if lang == 'e':
            font = 'Verdana'
            fontStyle = 'oblique'
        elif lang == 'c':
            font = 'Microsoft YaHei'
            fontStyle = 'None'
        if kw == 'a':
            LabelStyle = (
            'QLabel {font-family:' + font + ';font-size:' + fontSize + ';font-weight:None;font-style:' + fontStyle + ';border:0px solid ' + self.fontBlack + ';}')
        elif kw == 'b':
            LabelStyle = (
            'QLabel {background:transparent;font-family:' + font + ';font-size:' + fontSize + ';font-weight:None;font-style:' + fontStyle + ';border:0px solid ' + self.fontBlack + ';}')

        return LabelStyle

    def QGroupBox(self, kw='a'):
        # 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 rgb(51,51,51),stop: 1.0 rgb(68,68,68))'
        QGroupBoxStyleA = ''
        if kw == 'a':
            QGroupBoxStyleA = (
            'QGroupBox{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop: 0 transparent,stop:0.8 rgb(55,55,55),stop:1 rgb(60,60,60));border:1px solid gray;border-radius:10px;margin-top:1ex;}'
            'QGroupBox:title{subcontrol-origin:margin;subcontrol-position:top left;padding:0 3px;}')
        elif kw == 'b':
            QGroupBoxStyleA = (
            'QGroupBox{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop: 0 transparent,stop:1 rgb(90,90,90));border:1px solid gray;border-radius:10px;margin-top:1ex;}'
            'QGroupBox:title{subcontrol-origin:margin;subcontrol-position:top left;padding-top:-5px;}')
        return QGroupBoxStyleA

    def QSpinBox(self):
        # 'QSpinBox::up-arrow {background-color:rgb(120,0,0)}'
        # 'QSpinBox::down-arrow {background-color:rgb(255,0,0);width: 7px;height: 7px;}'
        # 'QSpinBox::down-arrow:disabled,'
        # 'QSpinBox::down-arrow:off {background-color:rgb(255,0,0)}'

        spinBox = (
        'QSpinBox {color:rgb(170,170,170);border:1px solid rgb(170,170,170);padding-right: 0px;border-width: 1;}'
        'QSpinBox::hover {color:white;border:1px solid white;}'
        'QSpinBox::down-button {background-color:rgb(54,54,54);subcontrol-origin: border;subcontrol-position: bottom right;width: 8px;height:8px;border:1px solid rgb(170,170,170);border-width: 1px;border-top-width: 0;}'
        'QSpinBox::down-button:hover {background-color:orange;border:1px solid white;}'
        'QSpinBox::down-button:pressed {background-color:rgb(255,0,0)}'
        'QSpinBox::up-button {background-color:rgb(54,54,54);subcontrol-origin: border;subcontrol-position: top right;height:9px;width: 8px;border:1px solid rgb(170,170,170);border-width: 1px;}'
        'QSpinBox::up-button::hover {background-color:rgb(220,50,50);border:1px solid white;}'
        'QSpinBox::up-button::pressed {background-color:rgb(255,255,0)}')
        return spinBox

    def QListWidget(self, kw='a', lang='e', bordRad='16px', bordWid='0px', fontSize='9px'):
        QListWidgetStyleA = (
        'QListWidget                        {color:' + self.fontWhite + ';font-size:' + fontSize + ';background:transparent;border-radius:' + bordRad + ';border:' + bordWid + ' solid gray;}'
                                                                                                                                                                               'QListWidget QAbstractItemView      {border: 1px solid darkgray;selection-background-color: lightgray;}'
                                                                                                                                                                               'QListWidget QAbstractItemView:item {height:55px;}'
                                                                                                                                                                               'QListWidget::item:selected         {border: 0px solid rgb(150,150,150);border:none;background:rgb(135,200,149);}  '
                                                                                                                                                                               'QListWidget::item:selected:!active {border-width: 0px;}  '
                                                                                                                                                                               'QListWidget::item:selected:active  {border-width: 1px;}  '
                                                                                                                                                                               'QListWidget::item:hover            {color:rgb(98,81,50);background:rgb(159,219,173)}  '
                                                                                                                                                                               'QListWidget::item:pressed          {background:rgb(78,153,90)}  '
                                                                                                                                                                               'QScrollBar                         {background:' + self.lighterColor(
            self.bgColor) + '; width:4px;border-radius:5px; }'
                            'QScrollBar::handle                 {background:rgb(245,75,57); border-radius:5px; }'
                            'QScrollBar::handle:hover           {background:rgb(255,95,77);border-radius:5px; }'
                            'QScrollBar::handle:pressed         {background:rgb(205,53,43);}'
                            'QScrollBar::sub-line               {background:' + self.lighterColor(self.bgColor) + ';}'
                                                                                                                  'QScrollBar::add-line               {background:' + self.lighterColor(
            self.bgColor) + ';}'
                            'QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:transparent;border-radius:5px;}'
        )
        return QListWidgetStyleA

    def QTextEdit(self, kw='a', lang='e', bordRad='8px', bordWid='0px', useHover=False, fontSize='13px'):
        font = ''
        fontStyle = ''
        if lang == 'e':
            font = 'Verdana'
            fontStyle = 'oblique'
        elif lang == 'c':
            font = 'Microsoft YaHei'
            fontStyle = 'None'
        dataTemp = {
            'a': ['rgb(220,220,220)', 'rgb(143,143,143)', 'transparent', 'rgb(220,220,220)', 'rgb(143,143,143)',
                  'transparent', 'rgb(200,200,200)'],
            'b': ['rgb(220,220,220)', 'rgb(143,143,143)', 'rgb(58,58,58)', 'rgb(255,255,255)', 'rgb(143,143,143)',
                  'rgb(88,88,88)', 'rgb(200,200,200)'],
            'c': ['rgb(220,220,220)', 'rgb(143,143,143)',
                  'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 rgb(51,51,51),stop: 1.0 rgb(68,68,68))',
                  'rgb(220,220,220)', 'rgb(93,139,158)', 'rgb(68,68,68)', 'rgb(10,36,106)']

        }
        dt = dataTemp[kw]
        textStyle = (
        'QTextEdit          {font-family:' + font + ';font-size:' + fontSize + ';font-weight:None;font-style:' + fontStyle + ';border-radius:' + bordRad + ';color:' +
        dt[0] + ';border:' + bordWid + ' solid ' + dt[1] + ';background: ' + dt[2] + ';selection-background-color:' +
        dt[-1] + '}'
                 'QTextEdit:hover    {border-radius:' + bordRad + ';padding-top:-1px;padding-bottom:0px;padding-left:10px;padding-right:10px;color:' +
        dt[3] + ';border:' + bordWid + ' solid ' + dt[4] + ';background: ' + dt[5] + ';}')

        return textStyle

    def QCheckBox(self):
        QCheckBoxStyleA = (
        'QCheckBox {border-radius:2px;width: 13px;height: 13px;color:rgb(248,91,90);border:0px solid ' + self.fontBlack + ';'
                                                                                                                          'font-family:Verdana;font-size:13px;}'
                                                                                                                          'QCheckBox:hover{background: ' + self.lighterColor(
            self.bgColor) + ';}'
                            'QCheckBox::indicator {width: 13px;height: 13px;}'
                            'QCheckBox::indicator:checked {backgroud:#5D8B9E}'
        )
        return QCheckBoxStyleA

    def QScrollBar(self):
        QSclAreaStyleA = (
        'QScrollBar{background:' + self.lighterColor(self.bgColor) + '; width:4px;border-radius:5px; }'
                                                                     'QScrollBar::handle{background:rgb(245,75,57); border-radius:5px; }'
                                                                     'QScrollBar::handle:hover{background:rgb(255,95,77);border-radius:5px; }'
                                                                     'QScrollBar::handle:pressed{background:rgb(205,53,43);}'
                                                                     'QScrollBar::sub-line{background:' + self.lighterColor(
            self.bgColor) + ';}'
                            'QScrollBar::add-line{background:' + self.lighterColor(self.bgColor) + ';}'
                                                                                                   'QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:transparent;border-radius:5px;}'
        )
        return QSclAreaStyleA
        '''
        'QScrollBar{      background:transparent; width:4px;border-radius:5px; }'
                            'QScrollBar::handle                 {background:rgb(245,75,57); border-radius:5px; }'
                            'QScrollBar::handle:hover           {background:rgb(255,95,77);border-radius:5px; }'
                            'QScrollBar::handle:pressed         {background:rgb(205,53,43);}'
                            'QScrollBar::sub-line               {background:transparent;}'
                            'QScrollBar::add-line               {background:transparent;}' 
                            'QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:transparent;border-radius:5px;}'
        '''

    def QRadioButton(self, kw='a', lang='e', bordRad='5px', bordWid='1px'):
        font = ''
        if lang == 'e':
            font = 'Verdana'
        elif lang == 'c':
            font = 'Microsoft YaHei'

        colorSet = {
            'a': [['red', 'rgb(255,120,120)', 'rgb(205,70,70)'], [self.bgColor, 'rgb(84,84,84)', 'rgb(54,54,54)']],
            'b': [['orange', 'rgb(255,180,120)', 'rgb(205,70,70)'], [self.bgColor, 'rgb(84,84,84)', 'rgb(54,54,54)']]
        }
        data = colorSet[kw]

        radioBtnStyle = (
        'QRadioButton::indicator::checked               {color:blue;border: 0px solid ' + self.lighterColor(
            self.bgColor, times=4) + ';border-radius: ' + bordRad + ';background-color: ' + data[0][0] + ';}'
                                                                                                         'QRadioButton::indicator::checked:hover         {background-color: ' +
        data[0][1] + ';}'
                     'QRadioButton::indicator::checked:pressed       {background-color: ' + data[0][2] + ';}'
                                                                                                         'QRadioButton::indicator::unchecked             {border:' + bordWid + ' solid ' + self.lighterColor(
            self.bgColor, times=4) + ';border-radius: ' + bordRad + ';background-color: ' + data[1][0] + ';}'
                                                                                                         'QRadioButton::indicator::unchecked::hover      {background-color: ' +
        data[1][1] + ';}'
                     'QRadioButton::indicator::unchecked::pressed    {background-color: ' + data[1][2] + ';}')
        return radioBtnStyle

    def QToolButton(self, kw='a', lang='e', bordRad='5px', bordWid='1px'):
        font = ''
        if lang == 'e':
            font = 'Verdana'
        elif lang == 'c':
            font = 'Microsoft YaHei'
        if kw == 'b':
            toolBtnStyle = (
            'QToolButton{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #5B5F5F, stop: 0.5 #0C2436,stop: 1.0 #27405A); border-style: outset; border-width: 1px; border-radius: 5px; border-color: #11223F; padding: 1px; }   '
            'QToolButton::hover{ background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #758385, stop: 0.5 #122C39,stop: 1.0 #0E7788);border-color: #11505C;}   '
            'QToolButton::pressed{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #969B9C, stop: 0.5 #16354B,stop: 1.0 #244F76);border-color: #11505C; } '
            'QPushButton::disabled,QToolButton::disabled{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #282B2C, stop: 0.5 #09121A, stop: 1.0 #111D29); border-color: #0A1320;  color:#6A6864; }   ')
            return toolBtnStyle
        colorSet = {
            'a': [['red', 'rgb(255,120,120)', 'rgb(205,70,70)', self.bgColor, 'rgb(84,84,84)', 'rgb(54,54,54)']],
            'c': []
        }
        data = colorSet[kw]

        toolBtnStyle = (
        'QToolButton            {color:' + self.fontWhite + ';background: transparent; border-style: outset; border-width: 0px; border-radius: 5px; border-color: rgb(78,78,78); padding: 1px; }   '
                                                            'QToolButton::hover     {color:rgb(98,81,50);background: rgb(159,219,173);border-color: ' + self.btnMainColor + '}'
                                                                                                                                                                            'QToolButton::pressed   {background: rgb(135,200,149);border-color: rgb(225,85,67); } '
                                                                                                                                                                            'QToolButton::disabled  {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #282B2C, stop: 0.5 #09121A, stop: 1.0 #111D29); border-color: #0A1320;  color:#6A6864; }   ')

        return toolBtnStyle

    def QTabWidget(self):

        tabWidgetStyle = ('QTabWidget::pane             { border-top: 0px solid #C2C7CB;} '
                          'QTabWidget::tab-bar          { left: 0px; }'
                          'QTabBar::tab                 { color:rgb(150,150,150);background:transparent; border: 0px solid #C4C4C3;  min-height: 58px; min-width: 18px; border-bottom-color: #C2C7CB;border-top-left-radius: 8px;  border-bottom-left-radius: 8px;   padding: 0px; }'
                          'QTabBar::tab:hover           { color:rgb(255,255,255);background: transparent;  border: 1px solid #C4C4C3;border-right-color: transparent; padding: 0px; }'
                          'QTabBar::tab:selected        { background: rgb(109,109,109);  border-color: #9B9B9B; border-bottom-color: #C2C7CB;border-right-color: rgb(109,109,109);margin-left: 0px; margin-right: 0px;}  '
                          'QTabBar::tab:!selected       { margin-top: 0px; }'
                          'QTabBar::tab:first:hover     { color:rgb(130,255,202);background:transparent;margin-left: 0;border: 1px solid rgb(130,255,202);border-right-color: rgb(109,109,109);} '
                          'QTabBar::tab:first:selected  { background:rgb(109,109,109);margin-left: 0;} '
                          'QTabBar::tab:last:hover      { color:rgb(253,202,137);background:transparent;margin-right: 0;border: 1px solid rgb(253,202,137);border-right-color: rgb(109,109,109);} '
                          'QTabBar::tab:last:selected   { background:rgb(109,109,109);margin-right: 0;} '

                          'QTabBar::tab:only-one        { margin: 0;} ')
        return tabWidgetStyle

    def QMenu(self):

        MenuStyle = ('QMenu                          {background:rgb(88,88,88);border:0px solid lightgray;}'
                     'QMenu::icon                    {padding:0px 0px 0px 20px;}'
                     'QMenu::item                    {color:' + self.fontWhite + ';background:rgb(60,60,60);height:20px;padding:0px 20px 0px 30px;margin:1px 0px 0px 0px;border-top-right-radius: 10px;border-bottom-left-radius: 10px;}'
                                                                                 'QMenu::item:selected:enabled   {color:rgb(88,88,88);background:rgb(159,219,173);}'
                                                                                 'QMenu::item:selected:!enabled  {background:transparent;}'
                                                                                 'QMenu::separator               {background:transparent;height:50px;width:1px;margin:1px 1px 1px 1px;}'
                                                                                 'QMenu::indicator {background:rgb(245,45,45);width: 13px;height: 13px;}'


                                                                                 'QMenu::indicator:non-exclusive:unchecked {image: url(:/images/checkbox_unchecked.png);}'
                                                                                 'QMenu::indicator:non-exclusive:unchecked:selected {image: url(:/images/checkbox_unchecked_hover.png);}'
                                                                                 'QMenu::indicator:non-exclusive:checked {image: url(:/images/checkbox_checked.png);}'
                                                                                 'QMenu::indicator:non-exclusive:checked:selected {image: url(:/images/checkbox_checked_hover.png);}'
                                                                                 'QMenu::indicator:exclusive:unchecked {image: url(:/images/radiobutton_unchecked.png);}'
                                                                                 'QMenu::indicator:exclusive:unchecked:selected {image: url(:/images/radiobutton_unchecked_hover.png);}'
                                                                                 'QMenu::indicator:exclusive:checked {image: url(:/images/radiobutton_checked.png);}'
                                                                                 'QMenu::indicator:exclusive:checked:selected {image: url(:/images/radiobutton_checked_hover.png);}'

                     )
        return MenuStyle

    def QSpinBox(self):

        spinBoxStyle = ('QSpinBox {padding-right: 12px;border-radius:8px;border:1px solid gray;}'
                        'QSpinBox::up-button {subcontrol-origin: border;subcontrol-position: top right;width: 16px;border-width: 1px;}'
                        'QSpinBox::up-button:hover {image: url(D:/rig_manager_box/icon/writer_icon/arrowUp_hover.png);}'
                        'QSpinBox::up-button:pressed {background:lightgray;border-radius:3px}'
                        'QSpinBox::up-arrow {image: url(D:/rig_manager_box/icon/writer_icon/arrowUp.png);width: 7px;height: 7px;}'
                        'QSpinBox::up-arrow:disabled, QSpinBox::up-arrow:off {image: url(:/images/up_arrow_disabled.png);}'
                        'QSpinBox::down-button {subcontrol-origin: border;subcontrol-position: bottom right;width: 16px;border-width: 1px;border-top-width: 0;}'
                        'QSpinBox::down-button:hover {image: url(D:/rig_manager_box/icon/writer_icon/arrowDown_hover.png);}'
                        'QSpinBox::down-button:pressed {background:lightgray;border-radius:3px}'
                        'QSpinBox::down-arrow {image: url(D:/rig_manager_box/icon/writer_icon/arrowDown.png);width: 7px;height: 7px;}'
                        'QSpinBox::down-arrow:disabled,QSpinBox::down-arrow:off {image: url(:/images/down_arrow_disabled.png);}')
        return spinBoxStyle

    def QComboBox(self):
        comboBoxStyle = ('QComboBox{border:1px solid gray;border-radius:8px;padding:1px18px1px3px;min-width:6em;}'
                         'QComboBox:editable {background: #2b2b2b;}'
                         'QComboBox:!editable,QComboBox::drop-down:editable {background: #333333;border-radius:8px}'
                         'QComboBox:!editable:on,QComboBox::drop-down:editable:on {background: #555555}'
                         'QComboBox:on {padding-top:3px;padding-left:4px;}'
                         'QComboBox::drop-down {subcontrol-origin: padding;subcontrol-position: top right;width:15px;'
                         'border-left-width:1px;border-left-color: darkgray;border-left-style: solid;/* just a single line */'
                         'border-top-right-radius:3px;border-bottom-right-radius:3px;}'
                         'QComboBox::down-arrow {image: url(D:/rig_manager_box/icon/writer_icon/arrowDown.png);}'
                         'QComboBox::down-arrow:on {top:1px;left:1px;}'
                         'QComboBox QAbstractItemView{border:1px solid darkgray;selection-background-color: lightgray;}'
                         'QScrollBar {border: 0px solid grey;background: #89d962;width: 8px;}'
                         'QScrollBar::handle {background: #89d962;min-height: 20px;border-radius:4px;}'
                         )
        return comboBoxStyle

    def QTreeWidget(self, kw='a'):
        # print self.iconPath
        theTreeView = ''
        if kw == 'a':
            theTreeView = ('QTreeWidget{outline:0;background-color:rgb(68,68,68);border:0px;}'
                           'QTreeWidget::item{gridline-color: rgba(255, 255, 255, 255);padding-left:5px;background-color: transparent;color: rgb(180, 180, 180);}'
                           'QTreeView::item:open {background-color: rgb(108,108,108);color: rgb(210, 210, 210);}'
                           'QTreeWidget::item:hover{color: rgb(255, 255, 255);}'
                           'QTreeWidget::item:selected{background-color: rgb(108,108,108);color: rgb(210, 210, 210);}'
                           'QTreeView::branch {gridline-color: rgba(255, 255, 255, 255);background-color: rgb(68,68,68);}'
                           'QTreeView::branch:open {image: url(' + self.iconPath + '/arrow_open.png);}'
                                                                                   'QTreeView::branch:closed:has-children {image: url(' + self.iconPath + '/arrow_down.png);}')
        elif kw == 'b':
            theTreeView = ('QTreeWidget{outline:0;background-color:rgb(68,68,68);border:0px;}'
                           'QTreeWidget::item{gridline-color: rgba(255, 255, 255, 255);padding-left:5px;background-color: transparent;}'
                           'QTreeView::item:open {background-color: rgb(108,108,108);color: rgb(210, 210, 210);}'
                           'QTreeWidget::item:hover{background-color: rgb(128, 128, 128);}'
                           'QTreeWidget::item:selected{background-color: rgb(108,108,108);}'
                           'QTreeView::branch {gridline-color: rgba(255, 255, 255, 255);background-color: rgb(68,68,68);}'
                           'QTreeView::branch:open {image: url(' + self.iconPath + '/arrow_open.png);}'
                                                                                   'QTreeView::branch:closed:has-children {image: url(' + self.iconPath + '/arrow_down.png);}')

        # 'QTreeView::indicator:checked {background-color:rgb(255,0,0);image: url('+self.iconPath+'/arrow_down.png);}'
        # 'QTreeView::indicator:unchecked {background-color:rgb(0,0,255);image: url('+self.iconPath+'/arrow_down.png);} '
        # 'QTreeView::branch:hover {image: url(D:/AssetManegerSystem/icon/arrow_down.png);}'
        return theTreeView


#Mstyle = RedBlackStyleSheet()
#Mstyle.setIconPath(getAssetManagerPath()['icon'])