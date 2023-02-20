import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog,QMainWindow,QProgressBar,QPushButton,QGraphicsPixmapItem,QGraphicsScene
from PyQt5.uic import loadUi
from pytube import YouTube
import requests

import string
'''
18-02-23
Created basic program
Need to code the errors popups
Need to code the file already exists popup


'''






class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("yt_downloader.ui",self)
        qualities = ["360p","720p"]
        self.stream_quality.addItems(qualities)
        self.show()
        self.Browse.clicked.connect(self.browse_fn)
        self.Download.clicked.connect(self.download_fn)
    def browse_fn(self):
        global url
        self.fname = QFileDialog.getExistingDirectory(self,"Open File","C:")
        self.Url_Inp_2.setText(self.fname)
        self.url = self.Url_Inp.text()
    def download_fn(self):
        self.yt = YouTube(self.url)
        self.title = self.yt.title
        self.title = self.title.translate(str.maketrans(" "," ",string.punctuation))
        path_test = self.fname + '/' +self.title+ ".mp4"
        print(self.stream_quality.currentText())
        print("Path: ",path_test)
        print(os.path.isfile(path_test))
        #Markipliers reaction to MrHippo.mp4
        if os.path.isfile(path_test) == True:
            print("Already exists")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("The give path already contains the file you have chosen to download... Please choose a different location")
            msg.setWindowTitle("Location Conflict")
            msg.StandardButton(QMessageBox.Ok)
            msg.exec_()
            return
        else:
            self.yt = YouTube(self.url)
            print(self.stream_quality.currentText())
            temp = self.yt.streams.filter(type="video").get_by_resolution(self.stream_quality.currentText())
            self.second = Confirmation_Window(self.url,self.fname,temp.filesize_mb,self.stream_quality.currentText())
            #self.hide()

#For the confimation window   


class Confirmation_Window(QMainWindow):
    def __init__(self,url,fname,size,quality):
        #down = Downloading_Window()
        self.url = url
        self.quality = quality
        self.fname = fname
        self.sizes = size
        print("In confirmation")
        super().__init__()
        #Load the UI for the confirmation window
        qualities = ["360p","720p"]
        print(qualities)
        print("loaded UI")
        loadUi("yt_downloader_confirmation.ui",self)
        self.yt = YouTube(self.url)
        print(self.yt.thumbnail_url)
        #Loading Thumbnail image
        print("Loading Thumbnail")
        img = QImage()
        img.loadFromData(requests.get(self.yt.thumbnail_url).content)
        self.Img_Label.setPixmap(QPixmap(img))

        #Setting the title label
        print("Loading Title")
        self.Vid_Title.setText(self.yt.title)

        #Setting the size label
        print("loading size")
        self.Size.setText(str(round(size,2)))
        
        self.show()
        self.Download_But.clicked.connect(self.download_but)
        self.Cancel_But.clicked.connect(self.close)
    def close(self):
        self.hide()
            
    def download_but(self):
        print("Sizes :",self.sizes)
        file = self.yt.streams.filter(file_extension="mp4").get_by_resolution(self.quality)
        print("Size of vid: ",self.sizes)
        #Download
        download = Downloading_Window(self.url,self.quality,self.fname)
        self.hide()


        #Should open a dialogue box with a progress window and the size of the download

class Downloading_Window(QMainWindow):
    def __init__(self,url,quality,filename):
        super().__init__
        self.url = url
        self.quality = quality
        self.filename = filename
        self.yt = YouTube(self.url,on_progress_callback=self.on_progress)
        file = self.yt.streams.filter(file_extension="mp4").get_by_resolution(self.quality)
        global pct_completed
        print("Download window opened")
        super(Downloading_Window,self).__init__()
        #Load the UI
        loadUi("Download_Window.ui",self)
        print("Loaded UI")
        self.show()
        file.download(filename)
        self.hide()
        pct_completed = 0
    def on_progress(self,stream, chunk, bytes_remaining):
        QApplication.processEvents()
        #print(dir(self))
        print("In on_progress")
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded/total_size*100

        print(int(round(pct_completed)))
        self.progressBar.setValue(int(round(pct_completed)))
        if int(round(pct_completed)) == 100:
            QMessageBox.about(self,"Download Complete","Download has been completed")
            self.hide()

        
app = QApplication(sys.argv)
main = MainWindow()
sys.exit(app.exec_())


'''
['AllowNestedDocks', 'AllowTabbedDocks', 'AnimatedDocks', 'DockOption', 'DockOptions', 'DrawChildren', 'DrawWindowBackground', 'ForceTabbedDocks', 'GroupedDragging', 'IgnoreMask', 'PaintDeviceMetric', 'PdmDepth', 'PdmDevicePixelRatio', 'PdmDevicePixelRatioScaled', 'PdmDpiX', 'PdmDpiY', 'PdmHeight', 'PdmHeightMM', 'PdmNumColors', 'PdmPhysicalDpiX', 'PdmPhysicalDpiY', 'PdmWidth', 'PdmWidthMM', 'RenderFlag', 'RenderFlags', 'VerticalTabs', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'acceptDrops', 'accessibleDescription', 'accessibleName', 'actionEvent', 'actions', 'activateWindow', 'addAction', 'addActions', 'addDockWidget', 'addToolBar', 'addToolBarBreak', 'adjustSize', 'autoFillBackground', 'backgroundRole', 'baseSize', 'blockSignals', 'centralWidget', 'changeEvent', 'childAt', 'childEvent', 'children', 'childrenRect', 'childrenRegion', 'clearFocus', 'clearMask', 'close', 'closeEvent', 'colorCount', 'connectNotify', 'contentsMargins', 'contentsRect', 'contextMenuEvent', 'contextMenuPolicy', 'corner', 'create', 'createPopupMenu', 'createWindowContainer', 'cursor', 'customContextMenuRequested', 'customEvent', 'deleteLater', 'depth', 'destroy', 'destroyed', 'devType', 'devicePixelRatio', 'devicePixelRatioF', 'devicePixelRatioFScale', 'disconnect', 'disconnectNotify', 'dockOptions', 'dockWidgetArea', 'documentMode', 'dragEnterEvent', 'dragLeaveEvent', 'dragMoveEvent', 'dropEvent', 'dumpObjectInfo', 'dumpObjectTree', 'dynamicPropertyNames', 'effectiveWinId', 'ensurePolished', 'enterEvent', 'event', 'eventFilter', 'filename', 'find', 'findChild', 'findChildren', 'focusInEvent', 'focusNextChild', 'focusNextPrevChild', 'focusOutEvent', 'focusPolicy', 'focusPreviousChild', 'focusProxy', 'focusWidget', 'font', 'fontInfo', 'fontMetrics', 'foregroundRole', 'frameGeometry', 'frameSize', 'geometry', 'getContentsMargins', 'grab', 'grabGesture', 'grabKeyboard', 'grabMouse', 'grabShortcut', 'graphicsEffect', 'graphicsProxyWidget', 'hasFocus', 'hasHeightForWidth', 'hasMouseTracking', 'hasTabletTracking', 'height', 'heightForWidth', 'heightMM', 'hide', 'hideEvent', 'iconSize', 'iconSizeChanged', 'inherits', 'initPainter', 'inputMethodEvent', 'inputMethodHints', 'inputMethodQuery', 'insertAction', 'insertActions', 'insertToolBar', 'insertToolBarBreak', 'installEventFilter', 'isActiveWindow', 'isAncestorOf', 'isAnimated', 'isDockNestingEnabled', 'isEnabled', 'isEnabledTo', 'isFullScreen', 'isHidden', 'isLeftToRight', 'isMaximized', 'isMinimized', 'isModal', 'isRightToLeft', 'isSeparator', 'isSignalConnected', 'isVisible', 'isVisibleTo', 'isWidgetType', 'isWindow', 'isWindowModified', 'isWindowType', 'keyPressEvent', 'keyReleaseEvent', 'keyboardGrabber', 'killTimer', 'layout', 'layoutDirection', 'leaveEvent', 'locale', 'logicalDpiX', 'logicalDpiY', 'lower', 'mapFrom', 'mapFromGlobal', 'mapFromParent', 'mapTo', 'mapToGlobal', 'mapToParent', 'mask', 'maximumHeight', 'maximumSize', 'maximumWidth', 'menuBar', 'menuWidget', 'metaObject', 'metric', 'minimumHeight', 'minimumSize', 'minimumSizeHint', 'minimumWidth', 'mouseDoubleClickEvent', 'mouseGrabber', 'mouseMoveEvent', 'mousePressEvent', 'mouseReleaseEvent', 'move', 'moveEvent', 'moveToThread', 'nativeEvent', 'nativeParentWidget', 'nextInFocusChain', 'normalGeometry', 'objectName', 'objectNameChanged', 'on_progress', 'overrideWindowFlags', 'overrideWindowState', 'paintEngine', 'paintEvent', 'paintingActive', 'palette', 'parent', 'parentWidget', 'physicalDpiX', 'physicalDpiY', 'pos', 'previousInFocusChain', 'progression', 'property', 'pyqtConfigure', 'quality', 'raise_', 'receivers', 'rect', 'releaseKeyboard', 'releaseMouse', 'releaseShortcut', 'removeAction', 'removeDockWidget', 'removeEventFilter', 'removeToolBar', 'removeToolBarBreak', 'render', 'repaint', 'resize', 'resizeDocks', 'resizeEvent', 'restoreDockWidget', 'restoreGeometry', 'restoreState', 'saveGeometry', 'saveState', 'screen', 'scroll', 'sender', 'senderSignalIndex', 'setAcceptDrops', 'setAccessibleDescription', 'setAccessibleName', 'setAnimated', 'setAttribute', 'setAutoFillBackground', 'setBackgroundRole', 'setBaseSize', 'setCentralWidget', 'setContentsMargins', 'setContextMenuPolicy', 'setCorner', 'setCursor', 'setDisabled', 'setDockNestingEnabled', 'setDockOptions', 'setDocumentMode', 'setEnabled', 'setFixedHeight', 'setFixedSize', 'setFixedWidth', 'setFocus', 'setFocusPolicy', 'setFocusProxy', 'setFont', 'setForegroundRole', 'setGeometry', 'setGraphicsEffect', 'setHidden', 'setIconSize', 'setInputMethodHints', 'setLayout', 'setLayoutDirection', 'setLocale', 'setMask', 'setMaximumHeight', 'setMaximumSize', 'setMaximumWidth', 'setMenuBar', 'setMenuWidget', 'setMinimumHeight', 'setMinimumSize', 'setMinimumWidth', 'setMouseTracking', 'setObjectName', 'setPalette', 'setParent', 'setProperty', 'setShortcutAutoRepeat', 'setShortcutEnabled', 'setSizeIncrement', 'setSizePolicy', 'setStatusBar', 'setStatusTip', 'setStyle', 'setStyleSheet', 'setTabOrder', 'setTabPosition', 'setTabShape', 'setTabletTracking', 'setToolButtonStyle', 'setToolTip', 'setToolTipDuration', 'setUnifiedTitleAndToolBarOnMac', 'setUpdatesEnabled', 'setVisible', 'setWhatsThis', 'setWindowFilePath', 'setWindowFlag', 'setWindowFlags', 'setWindowIcon', 'setWindowIconText', 'setWindowModality', 'setWindowModified', 'setWindowOpacity', 'setWindowRole', 'setWindowState', 'setWindowTitle', 'sharedPainter', 'show', 'showEvent', 'showFullScreen', 'showMaximized', 'showMinimized', 'showNormal', 'signalsBlocked', 'size', 'sizeHint', 'sizeIncrement', 'sizePolicy', 'splitDockWidget', 'stackUnder', 'startTimer', 'staticMetaObject', 'statusBar', 'statusTip', 'style', 'styleSheet', 'tabPosition', 'tabShape', 'tabifiedDockWidgetActivated', 'tabifiedDockWidgets', 'tabifyDockWidget', 'tabletEvent', 'takeCentralWidget', 'testAttribute', 'thread', 'timerEvent', 'toolBarArea', 'toolBarBreak', 'toolButtonStyle', 'toolButtonStyleChanged', 'toolTip', 'toolTipDuration', 'tr', 'underMouse', 'ungrabGesture', 'unifiedTitleAndToolBarOnMac', 'unsetCursor', 'unsetLayoutDirection', 'unsetLocale', 'update', 'updateGeometry', 'updateMicroFocus', 'updatesEnabled', 'url', 'visibleRegion', 'whatsThis', 'wheelEvent', 'width', 'widthMM', 'winId', 'window', 'windowFilePath', 'windowFlags', 'windowHandle', 'windowIcon', 'windowIconChanged', 'windowIconText', 'windowIconTextChanged', 'windowModality', 'windowOpacity', 'windowRole', 'windowState', 'windowTitle', 'windowTitleChanged', 'windowType', 'x', 'y']
'''