from javax.swing import JFrame
from javax.swing import JButton
from javax.swing import JPanel
from javax.swing import JTable
from javax.swing import JScrollPane

FRAME_WIDTH = 600
FRAME_HEIGHT = 400

def listPatches(parent_frame):
    columns = ["Offset", "Instruction Change"]
    prog = getCurrentProgram()
    mem2 = prog.getMemory()
    fileBytes = mem2.getAllFileBytes()[0]
    data = []
    for i in range(fileBytes.getSize()):
	if (fileBytes.getModifiedByte(i) != fileBytes.getOriginalByte(i)):
            data.append([str(i), str(hex(fileBytes.getOriginalByte(i))) + " -> " + str(hex(fileBytes.getModifiedByte(i)))])

    patchTable = JTable(data, columns)
    patchTable.setBounds(100,100,200,300)
    scrollPane = JScrollPane(patchTable)
    parent_frame.add(scrollPane)

def generateMainFrame():
    mainFrame = JFrame("Patch Pal")
    mainFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
    mainFrame.setLocation(100, 100)
    mainFrame.setSize(FRAME_WIDTH, FRAME_HEIGHT)
	
    listPatches(mainFrame)

    return mainFrame

if __name__ == "__main__":
    mainFrame = generateMainFrame()
    mainFrame.setVisible(True)
