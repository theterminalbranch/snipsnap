import re
from Tkinter import *
import Tkinter, tkFileDialog
import csv

def snipSnap(snip,snap):
    siteThreshold = 10
    root = Tkinter.Tk()
    root.withdraw()
    belowThreshold = []
# Make it almost invisible - no decorations, 0 size, top left corner.
    root.overrideredirect(True)
    root.geometry('0x0+0+0')

# Show window again and lift it to top so it can get focus,
# otherwise dialogs will end up behind the terminal.
    root.deiconify()
    root.lift()
    root.focus_force()
    root.call('wm', 'attributes', '.', '-topmost', True)
    root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
    print("Select Input file in PHYTAB format")
    inputFile = tkFileDialog.askopenfilename(parent=root,title=
                                        "Input file in PHYTAB format")
    #inputFile = "D:/Bio_Files/Pyscripts/snipSnap/testdata.fasta"
    saveLocation = tkFileDialog.askdirectory(parent=root, title= "Save location for output files")
    #saveLocation = "D:/Bio_Files/Pyscripts/snipSnap"
##  clear the previous output file & get ready for writing.
    out = open("{0}/OUTPUT.fasta".format(saveLocation),'w')
    out.close()
    out = open("{0}/OUTPUT.fasta".format(saveLocation),'a')
##  open the phytab file and get trim the sequences.
##  re-save as fasta file.
    with open(inputFile) as CSVfile:
        field_names = ['species','partition','seqname','sequence']
        file = csv.DictReader(CSVfile,fieldnames = field_names,delimiter="\t")
        for row in file:
##          Check if the row is long enough to support the trim. No row is allowed to go to 0.
            snappet = len(row['sequence'])-(snap+snip)
            if snappet <= 0:
                raise ValueError("Sequence for {0} is not long enough!".format(row['seqname']))
            if snappet < siteThreshold:
                print("Woah! Sequence {0} is below {1} sites! Consider removing it.".format(row['seqname'],siteThreshold))
                belowThreshold.append(row['seqname'])
            out.write(">{0}\n{1}\n".format(row['seqname'],row['sequence'][snip:snappet]))
        out.close()
    if len(belowThreshold) >= 1:
        print("You have sequences below the threshold - they are located in the list below")
        return(belowThreshold)
