from javax.swing import JFrame
from javax.swing import JButton
from javax.swing import JPanel
from javax.swing import JTable
from javax.swing import JLabel
from javax.swing import JTextField
from javax.swing import JScrollPane
from javax.swing import BoxLayout
from javax.swing import SwingConstants
from java.awt import Dimension

FRAME_WIDTH = 800
FRAME_HEIGHT = 600

def acceptAllPatches(event):
    patchExportFrame = JFrame("Export Patches")
    patchExportFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
    patchExportFrame.setLocation(300, 300)
    patchExportFrame.setSize(300, 150)
    patchExportFrame.setLayout(None)
 
    panel = JPanel()
    #panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
    panel.setBounds(0,0,300,150)

    nameLabel = JLabel("Patch Name:")
    nameLabel.setAlignmentX(panel.CENTER_ALIGNMENT)
    #nameLabel.setSize(nameLabel.getPreferredSize())
    panel.add(nameLabel)

    nameInput = JTextField("", 16)
    nameInput.setSize(50,50)
    nameInput.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(nameInput)

    descriptionLabel = JLabel("Patch Description:")
    descriptionLabel.setAlignmentX(panel.CENTER_ALIGNMENT)
    #nameLabel.setSize(nameLabel.getPreferredSize())
    panel.add(descriptionLabel)

    descriptionInput = JTextField("", 16)
    descriptionInput.setSize(50,50)
    descriptionInput.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(descriptionInput)

    def exportPatchesHandler(event):
        print("Hello world")
    exportButton = JButton("Export Patches", actionPerformed=exportPatchesHandler)
    exportButton.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(exportButton)

    patchExportFrame.add(panel)

    patchExportFrame.setVisible(True)

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
    patchTable.setRowSelectionAllowed(True)
    scrollPane = JScrollPane(patchTable)
    scrollPane.setPreferredSize(Dimension(300,300))
    
    panel = JPanel()
    panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
    panel.setBounds(200,200,400,400)
    panel.add(scrollPane)
    parent_frame.add(panel)

    acceptAllButton = JButton("Accept All", actionPerformed=acceptAllPatches)
    acceptAllButton.setBounds(0, 0, 150, 50)
    acceptAllButton.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(acceptAllButton)

    def exportPatches(event):
	print("This function is still under development.")
    acceptPatchesButton = JButton("Accept Chosen Patches", actionPerformed=exportPatches)

    acceptPatchesButton.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(acceptPatchesButton)


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
