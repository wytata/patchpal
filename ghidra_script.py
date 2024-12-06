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
import os
import shutil

FRAME_WIDTH = 800
FRAME_HEIGHT = 600

def setup(dir, user_binary):
    if os.path.isdir(dir + "/.data"):
        return

    try:
        absolute_file_path = os.path.abspath(user_binary)
        directory = os.path.join(os.path.dirname(absolute_file_path), ".data")
        os.mkdir(directory)
        os.mkdir(directory + "/patches")
        original_bin_path = directory + "/orig.bin"
        shutil.copy(absolute_file_path, original_bin_path)
        print("Your patch pal project directory has been set up. You can now create patches!")

    except Exception as e:
        print(e)

def writeTomlFile(name, description, data, path):
    project_dir = os.path.dirname(path)
    setup(project_dir, path)
    filename = project_dir + "/.data/patches/" + name + ".ps"
    offsets = [modification[0] for modification in data]
    bytes = [modification[1].split("->")[1].strip().strip("0x") for modification in data]
    output_bytes = ["'" + "0" + bytes[i] + "'" if len(bytes[i]) == 1 else "'" + bytes[i] + "'" for i in range(len(bytes))]
    
    output_file = open(filename.replace(" ", "-"), "a+")
    output_file.write("name = \"" + name + "\"\n")
    output_file.write("description = \"" + description + "\"\n\n")
    output_file.write("[content]\n")
    output_file.write("offsets = [" + ', '.join(offsets) + "]\n") 
    output_file.write("bytes = [" + ', '.join(output_bytes) + "]\n")
    output_file.close()


def acceptAllPatches(data, prog):
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
    	name = nameInput.getText()
    	description = descriptionInput.getText()
	writeTomlFile(name, description, data, prog.getExecutablePath())

    exportButton = JButton("Export Patches", actionPerformed=exportPatchesHandler)
    exportButton.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(exportButton)

    patchExportFrame.add(panel)

    patchExportFrame.setVisible(True)

def listPatches(parent_frame):
    columns = ["Offset", "Instruction Change"]
    prog = getCurrentProgram()
    print(prog.getExecutablePath())
    mem2 = prog.getMemory()
    fileBytes = mem2.getAllFileBytes()[0]
    data = []
    for i in range(fileBytes.getSize()):
	if ((fileBytes.getModifiedByte(i) & 0xFF) != (fileBytes.getOriginalByte(i) & 0xFF)):
            data.append([str(i), str(hex(fileBytes.getOriginalByte(i) & 0xFF)) + " -> " + str(hex(fileBytes.getModifiedByte(i) & 0xFF))])

    patchTable = JTable(data, columns)
    patchTable.setRowSelectionAllowed(True)
    scrollPane = JScrollPane(patchTable)
    scrollPane.setPreferredSize(Dimension(300,300))
    
    panel = JPanel()
    panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
    panel.setBounds(200,200,400,400)
    panel.add(scrollPane)
    parent_frame.add(panel)

    def acceptAllHandler(event):
        acceptAllPatches(data, prog)

    acceptAllButton = JButton("Accept All", actionPerformed=acceptAllHandler)
    acceptAllButton.setBounds(0, 0, 150, 50)
    acceptAllButton.setAlignmentX(panel.CENTER_ALIGNMENT)
    panel.add(acceptAllButton)


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
