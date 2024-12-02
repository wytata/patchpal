#Example script taken from previous 451 offering
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 
#@runtime Jython


#TODO Add User Code Here

from javax.swing import JFrame
from javax.swing import JButton
from javax.swing import JComboBox
from javax.swing import JLabel
from javax.swing import SwingConstants
from javax.swing import JTextField
from javax.swing import JPanel

from java.awt import Color
from java.awt import Dimension

from ghidra.program.model.symbol import RefType
from ghidra.program.model.symbol import SymbolType

FRAME_WIDTH = 600
FRAME_HEIGHT = 400

def setInputFile(text):
    file = open(text, "r")
    print(file.read())
    mem = getMemoryBlocks()
    print(type(mem))

def generateMainFrame():
    mainFrame = JFrame("Patch Pal")
    mainFrame.setLayout(None)
    mainFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
    mainFrame.setLocation(100, 100)
    mainFrame.setSize(FRAME_WIDTH, FRAME_HEIGHT)

    def setInputFileHandler(event):
        text = textInput.getText()
        setInputFile(text)

    textInput = JTextField(10)
    textInput.setBounds(50, 50, 200, 40)
    button = JButton("Set input file", actionPerformed=setInputFileHandler)
    button.setBounds(250, 50, 200, 40)
    mainFrame.add(textInput)
    mainFrame.add(button)

    return mainFrame

if __name__ == "__main__":
    mainFrame = generateMainFrame()
    mainFrame.setVisible(True)
