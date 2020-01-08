from tkinter import Tk, Canvas, Button, Label, Frame, Text, StringVar, \
                    Radiobutton, Entry, Scrollbar, X, Y, LEFT, RIGHT, \
                    BOTTOM, END, YES
from tkinter.ttk import Combobox
from core import *
from webbrowser import open as webopen
import os.path

this_dir, this_filename = os.path.split(__file__)
_iconPath = os.path.join(this_dir, "data", "YEPT.ico")

_BLAST_WAIT_MSG = '''BLASTing...
The BLAST function requires the Internet connection.
You may wait for about 10-20s for it to return the results, if your network works well...
Sometimes it crashes when using this function, restarting this program might help.'''

_BLAST_CONN_ERROR_MSG = '''Failed to connect to the Internet. Please check it.
========================================================================================='''


class YEPT_window():

    def __init__(self):
        self.root = Tk()
        self.root.resizable(width = False, height = True)
        self._add_icon()
        self.layout()
    
    def layout(self):
        self._layout_main()
        self._layout_blast()
        canvas = Canvas(self.total, width = 14, height = 150)
        canvas.create_line(10, 0, 10, 150, fill = "#D8D8D8", width = 2)
        canvas.pack(after = self.blast, side = LEFT)
        self._layout_primerDesign()
        self.b2 = Button(self.frmbt, 
                         text = 'Get Checking Primers', 
                         font = ("Arial", 12))
        #self.b2.bind("<Button-1>", self.getCheckPrimerWindow)
        self.b2.bind("<Button-1>", self.openCheckPrimerWindow)
        self._layout_bottom()

    def _add_icon(self):
        self.root.iconbitmap(_iconPath)
    
    def _layout_main(self):
        self.root.title("YEPT - SLST,ShanghaiTech")
        # Up center banner
        l = Label(self.root, 
                  text="Welcome to YEPT!", 
                  font = ("Arial", 13), 
                  width = 15, height = 2)
        l.pack()

        # Main frame
        self.total = Frame(self.root)
        self.total.pack(fill = X)

    def _layout_blast(self):
        # Frame at the left side
        self.blast = Frame(self.total)
        self.blast.pack(pady = 5, padx = 8, side = LEFT)
        self.btf = Frame(self.blast)
        self.btf.pack(pady=5,fill=X)
        btitle = Label(self.btf, 
                       text = 'BLAST to get AccessionID', 
                       font = ("Arial", 10), width = 19)
        btitle.pack(side = RIGHT)
        self.lblast = Label(self.btf, 
                            text = "(Don't like it? Do it yourself.)", 
                            font = ("Arial", 9), fg = 'blue', width = 22)
        self.lblast.bind('<Enter>', self._blast_showlink)
        self.lblast.bind('<Leave>', self._blast_notshowlink)
        self.lblast.bind('<Button-1>', self._blast_gotoBLAST)
        self.lblast.pack(side = RIGHT, padx = 5)

        self._layout_blast_line1()
        self._layout_blast_line2()

        self.tb = Text(self.blast, width = 65, height = 6)
        self.tb.pack(pady = 5, side = RIGHT)

    def _layout_blast_line1(self):
        # BLAST species selection
        b_species = Frame(self.blast)
        b_species.pack(pady = 5, fill = X)
        bspl = Label(b_species, 
                     text = "Target pecies:", 
                     font = ("Arial", 10), width = 10)
        self.bsp_var = StringVar()
        self.bsp_var.set(5)
        bIssj = Radiobutton(b_species, 
                            text = "S. japonicus", 
                            variable = self.bsp_var, value = "J")
        bIssj.bind("<Button-1>", self._focusB)
        bIssc = Radiobutton(b_species, 
                            text = "S. cryophilus", 
                            variable = self.bsp_var, value = "C")
        bIssc.bind("<Button-1>", self._focusB)
        bIsso = Radiobutton(b_species, 
                            text = "S. octosporus", 
                            variable = self.bsp_var, value = "O")
        bIsso.bind("<Button-1>", self._focusB)
        bIsso.pack(side = RIGHT)
        bIssc.pack(side = RIGHT)
        bIssj.pack(side = RIGHT)
        bspl.pack(side = RIGHT)
    
    def _layout_blast_line2(self):
        # Gene name entry line
        sp_name = Frame(self.blast)
        sp_name.pack(pady = 5, fill = X)
        
        sp_name_l = Label(sp_name, 
                          text = 'Gene in S. pombe:', 
                          font = ("Arial", 10), width = 13)
        sp_name_l.pack(side = RIGHT)        
        self.sp_name_e = Entry(sp_name, width = 6)
        self.sp_name_e.bind("<Button-1>", self._focusB)
        self.sp_name_e.bind("<Return>", self._BLAST)
        self.sp_name_e.bind("<Key>", self._forgetb2)
        self.sp_name_e.pack(side = RIGHT, padx = 5, before = sp_name_l)

        cov_l = Label(sp_name, 
                      text = 'Cov cutoff:', font = ("Arial", 10), width = 7)
        cov_l.pack(side = RIGHT, before = self.sp_name_e)
        self.cov_cutoff = Entry(sp_name, width = 4)
        self.cov_cutoff.insert(END, '0.15')
        self.cov_cutoff.bind("<Button-1>", self._focusB)
        self.cov_cutoff.bind("<Return>", self._BLAST)
        self.cov_cutoff.bind("<Key>", self._forgetb2)
        self.cov_cutoff.pack(side = RIGHT, padx = 5, before = cov_l)

        ev_l = Label(sp_name, 
                     text = 'evalue cutoff:', font = ("Arial", 10), width = 10)
        ev_l.pack(side = RIGHT, before = self.cov_cutoff)
        self.ev_cutoff = Entry(sp_name, width = 3)
        self.ev_cutoff.insert(END, '1')
        self.ev_cutoff.bind("<Button-1>", self._focusB)
        self.ev_cutoff.bind("<Return>", self._BLAST)
        self.ev_cutoff.bind("<Key>", self._forgetb2) 
        self.ev_cutoff.pack(side = RIGHT, padx = 5, before = ev_l)
        
        self.button_blast = Button(sp_name, text = 'BLAST', 
                                   font = ("Arial", 9))
        self.button_blast.bind('<Button-1>', self._BLAST)
        self.button_blast.bind('<Return>', self._BLAST)
        self.button_blast.pack(side = RIGHT, before = self.ev_cutoff)

    def _blast_showlink(self, event):
        self.lblast.config(bg = "#D8D8D8")
    
    def _blast_notshowlink(self, event):
        self.lblast.forget()
        self.lblast = Label(self.btf, 
                            text = "(Don't like it? Do it yourself.)", 
                            font = ("Arial", 9), fg = 'blue', width = 22)
        self.lblast.bind('<Enter>', self._blast_showlink)
        self.lblast.bind('<Leave>', self._blast_notshowlink)
        self.lblast.bind('<Button-1>', self._blast_gotoBLAST)
        self.lblast.pack(side=RIGHT,padx=5)
    
    def _blast_gotoBLAST(self, event):
        BLASTn_url = "http://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome"
        webopen(BLASTn_url, new = 2, autoraise = True)

    def _BLAST(self, event):
        self.tb.delete(0.0,END)
        gene_name = self.sp_name_e.get()
        species = self.bsp_var.get()
        ev_cutoff = float(self.ev_cutoff.get())
        cov_cutoff = float(self.cov_cutoff.get())

        if species == '5':
            self.tb.delete(0.0, END)
            self.tb.insert(END, 'Please choose a target species.')
        elif gene_name == '':
            self.tb.delete(0.0, END)
            self.tb.insert(END, 'Please enter a gene identifier.')
        else:
            output = BLAST_by_sp(gene_name, species, cov_cutoff, ev_cutoff)
            self.tb.delete(0.0, END)
            if output == []:
                self.tb.delete(0.0, END)
                self.tb.insert(END, 'No significant hit found.')
            elif output == 'NoName':
                self.tb.delete(0.0, END)
                self.tb.insert(END, 'There is no gene called "%s" in S. pombe. Please check the symbol twice.' % gene_name)
                self.tb.insert(END, str(output))
            else:
                self.tb.delete(0.0, END)
                for hit in output:
                    msg = "E-value: {}\tCov%: {:.2f}\tIdent%: {:.2f}\n".format(hit[0], hit[1], hit[2])
                    for cds in hit[3:]:
                        msg += '\t'.join(cds) + '\n'
                    self.tb.insert(END, msg)

    def _layout_primerDesign(self):
        self.options = Frame(self.total)
        self.options.pack(pady = 5, padx = 10, side = RIGHT)
        self.entries = Frame(self.options)
        self.entries.pack(fill = X, pady = 5)
        
        self._layout_primerDesign_line1()
        self._layout_primerDesign_line2()
        self._layout_primerDesign_line3()
        self._layout_primerDesign_line4_1()
        self._layout_primerDesign_line4_2()
        
        self.frmbt = Frame(self.options)
        self.frmbt.pack(pady = 5, fill = X, side = BOTTOM)
        self.b1 = Button(self.frmbt, text = 'Get Primer', font = ("Arial", 12))
        self.b1.bind("<Return>", self.getPrimer)
        self.b1.bind("<Button-1>", self.getPrimer)
        self.b1.pack(side = LEFT, pady = 5, ipady = 1, ipadx = 1)
        self.b2 = Button(self.frmbt, 
                         text = 'Get Checking Primers', 
                         font = ("Arial", 12))
        self.b2.bind("<Button-1>", self.openCheckPrimerWindow)

    def _layout_bottom(self):

        primer_result = Frame(self.root)
        primer_result.pack(pady = 5)

        rtf = Frame(primer_result) # result title frame
        rtf.pack(fill = X)
        result_title = Label(rtf, 
                             text = 'The primer we get is following:', 
                             font = ("Arial", 11))
        result_title.pack(side = LEFT)

        rcf = Frame(primer_result) # result content frame
        rcf.pack(fill = X)
        self.t = Text(rcf, width = 125, height = 5)
        self.t.pack(side = LEFT, fill = Y, expand = YES)
        scr = Scrollbar(rcf)
        scr.pack(side = RIGHT, fill = Y)
        self.t["yscrollcommand"] = scr.set
        scr['command'] = self.t.yview

    def _layout_primerDesign_line1(self):
        l2 = Label(self.entries, 
                   text = 'Accession ID for all or \ngene symbol in S. pombe:', 
                   font = ("Arial", 10), width = 20)
        l2.pack(side = LEFT)
        self.e2 = Entry(self.entries, width = 14)
        self.e2.bind("<Return>", self.getPrimer)
        self.e2.bind("<Key>", self._forgetb2)
        self.e2.pack(side = LEFT)
        l3 = Label(self.entries, text = 'length:',
                   font = ("Arial", 10), width = 6)
        l3.pack(side = LEFT)
        self.e3 = Entry(self.entries, width = 3)
        self.e3.insert(0, '80')
        self.e3.bind("<Return>", self.getPrimer)
        self.e3.bind("<Key>", self._forgetb2)
        self.e3.pack(side = LEFT)

    def _layout_primerDesign_line2(self):
        check_species = Frame(self.options)
        check_species.pack(fill = X, pady = 5)
        sp = Label(check_species, text = 'Species:', 
                   font = ("Arial", 10), width = 6)
        sp.pack(side = LEFT)
        self.species_var = StringVar()
        self.species_var.set(1)
        Issp = Radiobutton(check_species, text = "S. pombe", 
                           variable = self.species_var, value = "P")
        Issp.bind("<Button-1>", self._getfocusback)
        Issp.pack(side = LEFT)
        Issj = Radiobutton(check_species, text = "S. japonicus", 
                           variable=self.species_var, value = "J")
        Issj.bind("<Button-1>", self._getfocusback)
        Issj.pack(side = LEFT)
        Issc = Radiobutton(check_species, text = "S. cryophilus", 
                           variable = self.species_var, value = "C")
        Issc.bind("<Button-1>", self._getfocusback)
        Issc.pack(side = LEFT)
        Isso = Radiobutton(check_species, text = "S. octosporus", 
                           variable = self.species_var, value = "O")
        Isso.bind("<Button-1>", self._getfocusback)
        Isso.pack(side = LEFT)

    def _layout_primerDesign_line3(self):
        self.check_mode = Frame(self.options)
        self.check_mode.pack(fill = X, pady = 5)
        self.mode_var = StringVar()
        self.mode_var.set(2)
        md = Label(self.check_mode, text = 'Fuction:', 
                   font = ("Arial", 10), width = 6)
        md.pack(side = LEFT)
        Isdel = Radiobutton(self.check_mode,text = "Deletion", 
                            variable = self.mode_var, value="del", 
                            command = self._choose_plasmid)
        Isdel.bind("<Button-1>", self._getfocusback)
        Isdel.pack(side = LEFT)
        IsC = Radiobutton(self.check_mode, text = "C-terminal Tagging", 
                          variable = self.mode_var, value = "C", 
                          command = self._choose_Ctag)
        IsC.bind("<Button-1>", self._getfocusback)
        IsC.pack(side = LEFT)
        IsN = Radiobutton(self.check_mode, text = "N-terminal promoter adding", 
                          variable = self.mode_var, value = "N", 
                          command = self._choose_Ntag)
        IsN.bind("<Button-1>", self._getfocusback)
        IsN.pack(side = LEFT)

    def _layout_primerDesign_line4_1(self):
        self.blankframe = Frame(self.options)
        self.blankframe.pack(after = self.check_mode, pady = 18)
        self.check_plsmd = Frame(self.options)
        self.check_plsmd.pack(after = self.check_mode, pady = 5)
        self.check_plsmd.forget()
        pl = Label(self.check_plsmd, text = 'Plasmid:', 
                   font = ("Arial", 10), width = 10)
        pl.pack(side = LEFT)
        self.plasmid_var = StringVar()
        self.plasmid_var.set(3)
        IspFA6a = Radiobutton(self.check_plsmd, text = "pFA6a", 
                              variable = self.plasmid_var, value = 'pFA6a')
        IspFA6a.bind("<Button-1>", self._getfocusback)
        IspFA6a.pack(side = LEFT)
        IsKS = Radiobutton(self.check_plsmd, text = "KS-ura4", 
                           variable = self.plasmid_var, value = 'KS-ura4')
        IsKS.bind("<Button-1>", self._getfocusback)
        IsKS.pack(side = LEFT)

    def _layout_primerDesign_line4_2(self):
        self.check_Ntag = Frame(self.options)
        self.check_Ntag.pack(after = self.check_mode, pady = 5)
        self.check_Ntag.forget()
        nt = Label(self.check_Ntag, text = 'N-terminal Tag:', 
                   font = ("Arial", 10), width = 10)
        nt.pack(side = LEFT)
        self.Ntag_var = StringVar()
        self.Ntag_var.set(' ')
        Isnone = Radiobutton(self.check_Ntag, text = "None", 
                           variable = self.Ntag_var, value = ' ')
        Isnone.bind("<Button-1>", self._getfocusback)
        Isnone.pack(side=LEFT)
        Is3HA = Radiobutton(self.check_Ntag, text = "3HA", 
                          variable = self.Ntag_var, value = '3HA')
        Is3HA.bind("<Button-1>", self._getfocusback)
        Is3HA.pack(side = LEFT)
        IsGST = Radiobutton(self.check_Ntag, text = "GST", 
                          variable = self.Ntag_var, value = 'GST')
        IsGST.bind("<Button-1>", self._getfocusback)
        IsGST.pack(side = LEFT)
        IsGFP = Radiobutton(self.check_Ntag, text = "GFP", 
                            variable = self.Ntag_var, value = 'GFP')
        IsGFP.bind("<Button-1>", self._getfocusback)
        IsGFP.pack(side = LEFT)

    def _choose_Ntag(self):
        self.blankframe.forget()
        self.check_plsmd.forget()
        self.check_Ntag.pack(after = self.check_mode, pady = 5)

    def _choose_plasmid(self):
        self.blankframe.forget()
        self.check_Ntag.forget()
        self.check_plsmd.pack(after = self.check_mode, pady = 5)

    def _choose_Ctag(self):
        self.blankframe.pack(pady = 18)
        self.check_Ntag.forget()
        self.check_plsmd.forget()

    def _noResultMsg(self, keyword, species):
        self.t.delete(0.0, END)
        self.t.insert(END, 
            "No gene matches \"{}\" in {}.".format(keyword, species))

    def _ambResultMsg(self, keyword, species, results):
        self.t.delete(0.0, END)
        nResult, dfRepr = formatMultiResult(results)
        self.t.insert(END, 
            "{0} entries found to match \"{1}\" in {2}:\n{3}".format(nResult, keyword, species, dfRepr))

    def getPrimer(self, event):
        self.b1.focus_set()
        mode = self.mode_var.get()
        species = self.species_var.get()
        gene = self.e2.get()
        plasmid = self.plasmid_var.get()

        if mode != 'del':
            plasmid = 'pFA6a'

        if species == "1" or mode == "2" or plasmid == "3":
            self.t.delete(0.0, END)
            self.t.insert(END, "Please check all the radiobutton needed!\n")
        else:
            fullSpeciesNameMap = {'P': 'S. pombe', 'J': 'S. japonicus', 
                            'C': 'S. cryophilus', 'O': 'S. octosporus'}
            fullSpeciesName = fullSpeciesNameMap[species]
            
            Ntag = self.Ntag_var.get()
            length = int(self.e3.get())
            
            if plasmid == "pFA6a":
                forward_plmd_del = "CGGATCCCCGGGTTAATTAA"
                reverse_plmd_del = "GAATTCGAGCTCGTTTAAAC"
                forward_plmd_N = "GAATTCGAGCTCGTTTAAAC"
                reverse_plmd_N = "CATGATTTAACAAAGCGACTATA"
                reverse_plmd_N_3HA = "GCACTGAGCAGCGTAATCTG"
                reverse_plmd_N_GST = "ACGCGGAACCAGATCCGATT"
                reverse_plmd_N_GFP = "TTTGTATAGTTCATCCATGC"
            elif plasmid == "KS-ura4":
                forward_plmd_del = "CGCCAGGGTTTTCCCAGTCACGAC"
                reverse_plmd_del = "AGCGGATAACAATTTCACACAGGA"

            if mode == 'del':
                primer = get_del_primer(species, gene, length)
                if primer == []:
                    self._noResultMsg(gene, fullSpeciesName)
                elif type(primer) == list and len(primer) > 1:
                    self._ambResultMsg(gene, fullSpeciesName, primer)
                else:
                    self.t.delete(0.0, END)
                    self.t.insert(END, 'Found gene: {}, GenBank: {}, systematic ID: {}\n'.format(primer[2][0], primer[2][1], primer[2][2]))
                    self.t.insert(END, 'Forward primer: {} - {}\n'.format(primer[0], forward_plmd_del))
                    self.t.insert(END, '                %GC content = {} TM = {}\n'.format(GC(primer[0] + forward_plmd_del), TM(primer[0] + forward_plmd_del)))
                    self.t.insert(END, 'Reverse primer: {} - {}\n'.format(primer[1], reverse_plmd_del))
                    self.t.insert(END, '                %GC content = {} TM = {}'.format(GC(primer[1] + reverse_plmd_del), TM(primer[1] + reverse_plmd_del)))
                    self.b2.pack(side = LEFT, pady = 5, padx = 7, ipady = 1, ipadx = 1)
                    self.b2.focus_set()
            elif mode == 'C':
                primer = get_Ctag_primer(species, gene, length)
                if primer == []:
                    self._noResultMsg(gene, fullSpeciesName)
                elif type(primer) == list and len(primer) > 1:
                    self._ambResultMsg(gene, fullSpeciesName, primer)
                else:
                    self.t.delete(0.0, END)
                    self.t.insert(END, 'Found gene: {}, GenBank: {}, systematic ID: {}\n'.format(primer[2][0], primer[2][1], primer[2][2]))
                    self.t.insert(END, 'Forward primer: {} - {}\n'.format(primer[0], forward_plmd_del))
                    self.t.insert(END, '                %GC content = {} TM = {}\n'.format(GC(primer[0] + forward_plmd_del), TM(primer[0] + forward_plmd_del)))
                    self.t.insert(END, 'Reverse primer: {} - {}\n'.format(primer[1], reverse_plmd_del))
                    self.t.insert(END, '                %GC content = {} TM = {}'.format(GC(primer[1] + reverse_plmd_del), TM(primer[1] + reverse_plmd_del)))
                    self.b2.pack(side = LEFT, pady = 5, padx = 7, ipady = 1, ipadx = 1)
                    self.b2.focus_set()
            elif mode == 'N':
                if Ntag == ' ':
                    primer = get_Ntag_none_primer(species, gene,length)
                else:
                    primer = get_Ntag_tag_primer(species, gene,length)
                    if Ntag == "3HA":
                        reverse_plmd_N = reverse_plmd_N_3HA
                    elif Ntag == "GST":
                        reverse_plmd_N = reverse_plmd_N_GST
                    elif Ntag == "GFP":
                        reverse_plmd_N = reverse_plmd_N_GFP
                if primer == []:
                    self._noResultMsg(gene, fullSpeciesName)
                elif type(primer) == list and len(primer) > 1:
                    self._ambResultMsg(gene, fullSpeciesName, primer)
                else:
                    self.t.delete(0.0, END)
                    self.t.insert(END, 'Found gene: {}, GenBank: {}, systematic ID: {}\n'.format(primer[2][0], primer[2][1], primer[2][2]))
                    self.t.insert(END, 'Forward primer: {} - {}\n'.format(primer[0], forward_plmd_N))
                    self.t.insert(END, '                %GC content = {} TM = {}\n'.format(GC(primer[0] + forward_plmd_N), TM(primer[0] + forward_plmd_N)))
                    self.t.insert(END, 'Reverse primer: {} - {}\n'.format(primer[1], reverse_plmd_N))
                    self.t.insert(END, '                %GC content = {} TM = {}'.format(GC(primer[1] + reverse_plmd_N), TM(primer[1] + reverse_plmd_N)))
                    self.b2.pack(side = LEFT, pady = 5, padx = 7, ipady = 1, ipadx = 1)
                    self.b2.focus_set()

    def _backtob3(self, event):
        self.b3.focus_set()

    def _focusB(self, event):
        self.button_blast.focus_set()

    def _getfocusback(self, event):
        self.b1.focus_set()
        self.b2.forget()

    def _forgetb2(self, event):
        self.b2.forget()

    def start(self):
        self.root.mainloop()

    def openCheckPrimerWindow(self, event):
        CheckPrimerWindow(self)

class CheckPrimerWindow():
    def __init__(self, Main):
        self.Main = Main
        self.window = Tk()
        self.window.title("YEPT - Get Checking Primers - SLST,ShanghaiTech")
        self.window.iconbitmap(_iconPath)
        self.window.resizable(width = False, height = False)
        self.layout()

    def layout(self):
        l3 = Label(self.window, text = "Getting Checking Primers", font = ("Arial", 12), width = 30, height = 2)
        l3.pack(fill = X, pady = 5)
        self.options2 = Frame(self.window)
        self.options2.pack(pady = 5, padx = 10)

        preinf = Frame(self.options2)
        preinf.pack(fill = X, pady = 5)
    
        Label(preinf, 
              text = "AccessionID: " + self.Main.e2.get(), 
              font = ("Arial", 10), 
              width = len("AccessionID: " + self.Main.e2.get())).pack(side = LEFT)
        Label(preinf, 
              text = "Length: " + self.Main.e3.get(), 
              font = ("Arial", 10), width = 10).pack(side = LEFT)

        self._layout_line1()
        self._layout_line2()
        self._layout_line3()
        self._layout_line4()

        self.Main.b3 = Button(self.window, text = "Get Checking Primers", font = ("Arial", 12))
        self.Main.b3.focus_set()
        self.Main.b3.bind("<Button-1>", self.GetcheckPrimer)
        self.Main.b3.bind("<Return>", self.GetcheckPrimer)
        self.Main.b3.pack(pady = 5)

        self.textFrame = Text(self.window, width = 80, height = 3)
        self.textFrame.pack(fill = X, pady = 5, padx = 5)

    def _layout_line1(self):
        searchregion = Frame(self.options2)
        searchregion.pack(fill = X, pady = 5)
        Label(searchregion, 
              text = "Number of basepairs up- or downstream of the\ntarget sequence to use for primer search:", 
              font = ("Arial", 10), width = 33, height = 2).pack(side = LEFT)
        self.e_search = Entry(searchregion, width = 5)
        self.e_search.insert(0, '400')
        self.e_search.pack(side = LEFT, padx = 3)

    def _layout_line2(self):
        chlen = Frame(self.options2)
        chlen.pack(fill = X, pady = 5)
        Label(chlen, 
              text = "Opt. Primer Length:", 
              font = ("Arial", 10), width = 18).pack(side = LEFT)
        self.optlen = Entry(chlen, width = 5)
        self.optlen.insert(0, '22')
        self.optlen.bind("<Button-1>", self.Main._backtob3)
        self.optlen.pack(side = LEFT)
        Label(chlen, text = "Min. Primer Length:", 
              font = ("Arial", 10), width = 18 ).pack(side = LEFT)
        self.minlen = Entry(chlen, width = 5)
        self.minlen.insert(0, '20')
        self.minlen.bind("<Button-1>", self.Main._backtob3)
        self.minlen.pack(side = LEFT)
        Label(chlen, 
              text = "Max. Primer Length:", 
              font = ("Arial", 10), width = 18 ).pack(side = LEFT)
        self.maxlen = Entry(chlen, width = 5)
        self.maxlen.insert(0, '28')
        self.maxlen.bind("<Button-1>", self.Main._backtob3)
        self.maxlen.pack(side = LEFT)

    def _layout_line3(self):
        chTM = Frame(self.options2)
        chTM.pack(fill = X, pady = 5)
        Label(chTM, 
              text = "Opt. Primer TM:", 
              font = ("Arial", 10), width = 18).pack(side = LEFT)
        self.optTM = Entry(chTM, width = 5)
        self.optTM.insert(0, '60')
        self.optTM.bind("<Button-1>", self.Main._backtob3)
        self.optTM.pack(side = LEFT)
        Label(chTM, 
              text = "Min. Primer TM:", font = ("Arial", 10), width = 18).pack(side = LEFT)
        self.minTM = Entry(chTM, width = 5)
        self.minTM.insert(0, '57')
        self.minTM.bind("<Button-1>", self.Main._backtob3)
        self.minTM.pack(side = LEFT)
        Label(chTM, 
              text = "Max. Primer TM:", 
              font = ("Arial", 10), width = 18 ).pack(side = LEFT)
        self.maxTM = Entry(chTM, width = 5)
        self.maxTM.insert(0, '63')
        self.maxTM.bind("<Button-1>", self.Main._backtob3)
        self.maxTM.pack(side = LEFT)

    def _layout_line4(self):
        chGC = Frame(self.options2)
        chGC.pack(fill = X,pady = 5)
        Label(chGC, text = "Opt. Primer GC Content:", font = ("Arial",10), width = 18).pack(side = LEFT)
        self.minGC = Entry(chGC, width = 5)
        self.minGC.insert(0, '30')
        self.minGC.bind("<Button-1>", self.Main._backtob3)
        self.minGC.pack(side = LEFT)
        Label(chGC, text = "Min. Primer GC Content:", font = ("Arial", 10), width = 18).pack(side = LEFT)
        self.maxGC = Entry(chGC, width = 5)
        self.maxGC.insert(0, '70')
        self.maxGC.bind("<Button-1>", self.Main._backtob3)
        self.maxGC.pack(side = LEFT)

    def GetcheckPrimer(self, event):
        try:
            mode = self.Main.mode_var.get()
            species = self.Main.species_var.get()
            gene = self.Main.e2.get()
            plasmid = self.Main.plasmid_var.get()
            if mode != 'del':
                plasmid = 'pFA6a'
            Ntag = self.Main.Ntag_var.get()
            if Ntag == "4":
                Ntag = ' '
            
            length = int(self.Main.e3.get())
            scale = int(self.e_search.get())
            lenopt = int(self.optlen.get())
            TMopt = int(self.optTM.get())
            TMmin = int(self.minTM.get())
            TMmax = int(self.maxTM.get())
            GCmin = int(self.minGC.get())
            GCmax = int(self.maxGC.get())
            if species == "1" or mode == "2" or plasmid == "3":
                self.textFrame.delete(0.0, END)
                self.textFrame.insert(END, "Please check all the radiobutton needed!")
            chp_range = get_check_primer_range(species, gene, length, 
                                                  mode, Ntag, scale)
            chp_1, chp_2 = get_check_primer(chp_range[0], chp_range[1], lenopt, 
                                      GCmin, GCmax, TMopt, TMmin, TMmax)
            self.textFrame.delete(0.0, END)
            self.textFrame.insert(END, 
                'Left Checking primer:\t' + chp_1 + "\t%GC content = " + GC(chp_1) + "\tTM = " + TM2(chp_1) + '\n')
            self.textFrame.insert(END, 
                'Right Checking primer:\t' + chp_2 + "\t%GC content = " + GC(chp_2) + "\tTM = " + TM2(chp_2) + '\n')

        except ValueError:
            self.textFrame.delete(0.0, END)
            self.textFrame.insert(END, "Please fill the entries first!")

        except IndexError:
            self.textFrame.delete(0.0, END)
            self.textFrame.insert(END, "No checking primer can meet the requirements!")
