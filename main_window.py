# -*- coding: utf-8 -*-

#system modules
import sys, os, re, shutil

#custom functions and classes
import utils
from gromacs_instance import gromacs_instance

#pyqt5 widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#custom pymol widgets
from pymolwidget import PyMolWidget

#other functions
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#import gromacs
import gromacs.formats
import gmxapi as gmx


class Umbrella_samping_Main_Window(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("umbrella_sampling_gui.ui", self)

        self.figure = plt.figure(dpi=150)
        self.canvas = FigureCanvas(self.figure)
        self.figure_toolbar = NavigationToolbar(self.canvas, self)

        self.plot_viewer.layout().addWidget(self.canvas)
        self.plot_viewer.layout().addWidget(self.figure_toolbar)

        self.pymol_view = PyMolWidget()
        self.pymol_view.show()

        self.viewer_widget.layout().addWidget(self.pymol_view)
        self.default_plot()

## Main_GUI

        self.load_button.clicked.connect(self.load_topology)
        self.browse_button.clicked.connect(self.browse_folder)
#        self.protein_checkBox.stateChanged.connect(self.Change_display_Protein)

## Prepartion
        self.generate_button.clicked.connect(self.generate_mdp_file)
        self.init_pull_button.clicked.connect(self.init_pull)
        self.generate_clear_button.clicked.connect(self.clear_generation)
        self.pull_grp1_text.returnPressed.connect(self.update_distance_and_visulization)
        self.pull_grp2_text.returnPressed.connect(self.update_distance_and_visulization)
        self.min_win_text.returnPressed.connect(self.update_parameters)
        self.max_win_text.returnPressed.connect(self.update_parameters)
        self.win_size_text.returnPressed.connect(self.update_parameters)
        self.display_syntax_text.returnPressed.connect(self.update_pymol_display)

## Run
        self.em1_button.clicked.connect(self.em1_run)
        self.em2_button.clicked.connect(self.em2_run)
        self.eq_button.clicked.connect(self.eq_run)
        self.production_button.clicked.connect(self.production_run)

## Analysis
        self.wham_button.clicked.connect(self.wham_analysis)
        self.profile_xvg_plot_button.clicked.connect(self.plot_profile_xvg)
        self.histo_xvg_plot_button.clicked.connect(self.plot_histo_xvg)
        self.bsresult_xvg_plot_button.clicked.connect(self.plot_bsResult_xvg)

        self.bin_text.returnPressed.connect(self.update_analysis_parameters)
        self.temp_text.returnPressed.connect(self.update_analysis_parameters)
        self.b_text.returnPressed.connect(self.update_analysis_parameters)
        self.nbootstrap_text.returnPressed.connect(self.update_analysis_parameters)
        self.zprof0_text.returnPressed.connect(self.update_analysis_parameters)
        self.min_text.returnPressed.connect(self.update_analysis_parameters)
        self.max_text.returnPressed.connect(self.update_analysis_parameters)

## Set default parameters values
        self.update_parameters()
        self.update_analysis_parameters()

    def browse_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self,"Select Directory")
        if folder:
            self.topology_dir_text.setText(folder)

    def load_topology(self):
        self.load_dir = self.topology_dir_text.text()
        self.topology_dir = self.load_dir + "/parameters/"
        self.prep_load_dir = self.load_dir + "/initial_configurations/"
        self.production_load_dir =  self.load_dir + "/production/"
        self.analysis_dir =  self.load_dir + "/analysis/"
        self.display_pymol(self.prep_load_dir + "start.pdb")
        self.update_parameters()
        self.update_pull_grps()
        self.pymol_view.ShowSelect()

        self.pymol_view.ShowSelect(representation="spheres", select= "index " + "+".join(self.index_grp1))
        self.pymol_view.ShowSelect(representation="spheres", select= "index " + "+".join(self.index_grp2))
        self.retrieve_data()

    def retrieve_data(self):
       """retrieve existing simulation parameters and data."""
       return

    def update_distance_and_visulization(self):
        '''set min distance to current distance when editing pull groups'''

        self.update_pull_grps()
        current_distance = self.pymol_view.CalculateDistance(name = "distance", sele1 =  "index " + "+".join(self.index_grp1),sele2 =  "index " + "+".join(self.index_grp2))
### not the same as gromacs calculated
#        self.min_win_text.setText("{0:.1f}".format(current_distance/10))
        self.update_parameters()
#        self.pymol_view.ShowSelect(representation="dashes",select = "model distance")
        self.display_pull_grp()


    def update_parameters(self):
        self.min_window = float(self.min_win_text.text())
        self.max_window = float(self.max_win_text.text())
        self.window_size = float(self.win_size_text.text())
        self.pull_grp1 = self.pull_grp1_text.text()
        self.pull_grp2 = self.pull_grp2_text.text()

    def update_pull_grps(self):
        self.pull_grp1 = self.pull_grp1_text.text()
        self.pull_grp2 = self.pull_grp2_text.text()
        make_ndx_grp1 = gmx.commandline_operation(
                                        'gmx',
                                        'select',
                                        input_files={
                                                     '-f': self.prep_load_dir + "start.gro",
                                                     '-s': self.prep_load_dir + "start.gro",
                                                     '-select': self.pull_grp1},
                                        output_files={'-on': self.prep_load_dir + "index_grp1.ndx"})
        make_ndx_grp1.run()
        self.preparation_textBrowser.append(make_ndx_grp1.output.erroroutput.result())

        make_ndx_grp2 = gmx.commandline_operation(
                                        'gmx',
                                        'select',
                                        input_files={
                                                     '-f': self.prep_load_dir + "start.gro",
                                                     '-s': self.prep_load_dir + "start.gro",
                                                     '-select': self.pull_grp2},
                                        output_files={'-on': self.prep_load_dir + "index_grp2.ndx"})
        make_ndx_grp2.run()
        self.preparation_textBrowser.append(make_ndx_grp2.output.erroroutput.result())

        with open(self.prep_load_dir + "index_grp1.ndx","r") as index_grp1_ndx:
            index_grp1_ndx.readline()
            index_grp1 = index_grp1_ndx.read()
        self.index_grp1 = index_grp1.split()
        with open(self.prep_load_dir + "index_grp2.ndx","r") as index_grp2_ndx:
            index_grp2_ndx.readline()
            index_grp2 = index_grp2_ndx.read()
        self.index_grp2 = index_grp2.split()

    def update_analysis_parameters(self):
        self.wham_bin = self.bin_text.text()
        self.wham_temp = self.temp_text.text()
        self.wham_b = self.b_text.text()
        self.wham_nbootstrap = self.nbootstrap_text.text()
        self.wham_zprof0 = self.zprof0_text.text()
        self.wham_min = self.min_text.text()
        self.wham_max = self.max_text.text()




    def generate_mdp_file(self):
        self.update_parameters()

        min_window = self.min_window
        max_window = self.max_window
        window_size = self.window_size
        pull_grp1 = self.pull_grp1
        pull_grp2 = self.pull_grp2

        prep_load_dir =  self.prep_load_dir
        production_load_dir =  self.production_load_dir

        for window in np.arange(min_window,max_window + window_size,window_size):
            folder_name = "{0:.1f}".format(window)
            try:
                os.mkdir(prep_load_dir + folder_name)
            except:
                print("folder exist.")
            try:
                os.mkdir(production_load_dir + folder_name)
            except:
                print("folder exist.")

#edit mdp files
            for mdp_file in ['pull.mdp','em.mdp','em2.mdp','eq.mdp']:
                utils.sed_implementation(prep_load_dir + mdp_file, prep_load_dir + folder_name + '/' + mdp_file,"PULL1",pull_grp1)
                utils.sed_implementation(prep_load_dir + folder_name + '/' + mdp_file, prep_load_dir + folder_name + '/' + mdp_file,"PULL2",pull_grp2)
                utils.sed_implementation(prep_load_dir + folder_name + '/' + mdp_file, prep_load_dir + folder_name + '/' + mdp_file,"POS1",folder_name)

#edit pruduction mdp files
            utils.sed_implementation(production_load_dir + 'md.mdp', production_load_dir + folder_name + '/md.mdp',"PULL1",pull_grp1)
            utils.sed_implementation(production_load_dir + folder_name + '/md.mdp', production_load_dir + folder_name + '/md.mdp',"PULL2",pull_grp2)
            utils.sed_implementation(production_load_dir + folder_name + '/md.mdp', production_load_dir + folder_name + '/md.mdp',"POS1",folder_name)


    def init_pull(self):
        self.preparation_textBrowser.append("pull init start...")

        self.update_parameters()
        self.update_pull_grps()
        min_window = self.min_window
        max_window = self.max_window
        window_size = self.window_size

        prep_load_dir =  self.prep_load_dir

        for window in np.arange(min_window,max_window + window_size,window_size):
            folder_name = "{0:.1f}".format(window)
            pull_instance = gromacs_instance(mdp_file = prep_load_dir + folder_name + '/pull.mdp',
                                            starting_structure = prep_load_dir + 'start.gro',
                                            restraining_structure = prep_load_dir + 'start.gro',
                                            topology_file = self.topology_dir + 'topol.top',
                                            tpr_file = prep_load_dir + folder_name + '/pull.tpr' )
            pull_instance.generate_tpr_file()
            print(pull_instance.grompp_erroroutput)
            pull_instance.mdrun_process()
            if pull_instance.grompp_erroroutput != " ":
                self.preparation_textBrowser.append(pull_instance.grompp_erroroutput)

        for window in np.arange(min_window,max_window + window_size,window_size):
            folder_name = "{0:.1f}".format(window)
            self.display_pymol(prep_load_dir + folder_name + '/pull.gro',object = folder_name)
#            self.pymol_view.ShowSelect(representation="spheres", select= "resname " + self.pull_grp1)
            self.pymol_view.ShowSelect(representation="spheres", select= "index " + "+".join(self.index_grp2))
            self.pymol_view.ShowSelect(select = "model start")

        self.preparation_textBrowser.append("pull init finish!")

    def clear_generation(self):
        self.update_parameters()

        for window in np.arange(self.min_window,self.max_window + self.window_size,self.window_size):
            folder_name = "{0:.1f}".format(window)

#            shutil.rmtree(self.prep_load_dir + folder_name)
#            shutil.rmtree(self.production_load_dir + folder_name)

            print("% s has been removed successfully" % folder_name)
            self.pymol_view.DeleteSelect(name = folder_name)
        self.pymol_view.HideAll()
        self.pymol_view.ShowSelect()
        self.pymol_view.ShowSelect(representation="spheres", select= "resname " + self.pull_grp1)
        self.pymol_view.ShowSelect(representation="spheres", select= "resname " + self.pull_grp2)
        self.default_plot()
        self.preparation_textBrowser.append("clear finish!")

###Gromacs Run part
    def em1_run(self):
        prep_load_dir =  self.prep_load_dir

        for window in np.arange(self.min_window,self.max_window + self.window_size,self.window_size):
            folder_name = "{0:.1f}".format(window)

            em1_instance = gromacs_instance(mdp_file = prep_load_dir + folder_name + '/em.mdp',
                                            starting_structure = prep_load_dir + folder_name + '/pull.gro',
                                            restraining_structure = prep_load_dir + folder_name + '/pull.gro',
                                            topology_file = self.topology_dir + 'topol.top',
                                            tpr_file = prep_load_dir + folder_name + '/em1.tpr' )
            em1_instance.generate_tpr_file()
            em1_instance.mdrun_process()
            self.run_textBrowser.append("em1 finish!")


    def em2_run(self):
        prep_load_dir =  self.prep_load_dir

        for window in np.arange(self.min_window,self.max_window + self.window_size,self.window_size):
            folder_name = "{0:.1f}".format(window)

            em2_instance = gromacs_instance(mdp_file = prep_load_dir + folder_name + '/em2.mdp',
                                            starting_structure = prep_load_dir + folder_name + '/em1.gro',
                                            restraining_structure = prep_load_dir + folder_name + '/em1.gro',
                                            topology_file = self.topology_dir + 'topol.top',
                                            tpr_file = prep_load_dir + folder_name + '/em2.tpr' )
            em2_instance.generate_tpr_file()
            em2_instance.mdrun_process()
            self.run_textBrowser.append("em2 finish!")

    def eq_run(self):
        prep_load_dir =  self.prep_load_dir

        for window in np.arange(self.min_window,self.max_window + self.window_size,self.window_size):
            folder_name = "{0:.1f}".format(window)

            eq_instance = gromacs_instance(mdp_file = prep_load_dir + folder_name + '/eq.mdp',
                                            starting_structure = prep_load_dir + folder_name + '/em2.gro',
                                            restraining_structure = prep_load_dir + folder_name + '/em2.gro',
                                            topology_file = self.topology_dir + 'topol.top',
                                            tpr_file = prep_load_dir + folder_name + '/eq.tpr' )
            eq_instance.generate_tpr_file()
            eq_instance.mdrun_process()
            self.run_textBrowser.append("eq finish!")

    def production_run(self):
        prep_load_dir =  self.prep_load_dir

        for window in np.arange(self.min_window,self.max_window + self.window_size,self.window_size):
            folder_name = "{0:.1f}".format(window)

            md_instance = gromacs_instance(mdp_file = self.production_load_dir + folder_name + '/md.mdp',
                                            starting_structure = prep_load_dir + folder_name + '/eq.gro',
                                            restraining_structure = prep_load_dir + folder_name + '/eq.gro',
                                            topology_file = self.topology_dir + 'topol.top',
                                            tpr_file = self.production_load_dir + folder_name + '/md.tpr' )
            md_instance.generate_tpr_file()
            md_instance.mdrun_process()
            self.run_textBrowser.append("production finish!")


### Wham analysis
    def wham_analysis(self):
        self.update_analysis_parameters()

        tpr_ensemble = []
        pullx_ensemble = []
        for window in np.arange(self.min_window,self.max_window + self.window_size,self.window_size):
            folder_name = "{0:.1f}".format(window)

            tpr_ensemble.append(self.production_load_dir + folder_name + '/md.tpr')
            pullx_ensemble.append(self.production_load_dir + folder_name + '/md_x.xvg')

        with open(self.analysis_dir + 'tpr-files.dat', 'w') as tpr_dat_file:
            tpr_dat_file.write("\n".join(tpr_ensemble))

        with open(self.analysis_dir + 'pullx-files.dat', 'w') as pullx_dat_file:
            pullx_dat_file.write("\n".join(pullx_ensemble))

        wham = gmx.commandline_operation(
                                        'gmx',
                                        'wham',
                                        input_files={
                                                     '-ix': self.analysis_dir + 'pullx-files.dat',
                                                     '-it': self.analysis_dir + 'tpr-files.dat',
                                                     '-bins': self.wham_bin,
                                                     '-temp': self.wham_temp,
                                                     '-unit': 'kJ',
                                                     '-b': self.wham_b,
                                                     '-nBootstrap': self.wham_nbootstrap,
                                                     '-zprof0': self.wham_zprof0,
                                                     '-min': self.wham_min,
                                                     '-max': self.wham_max},
                                        output_files={'-o': self.analysis_dir + 'profile.xvg',
                                                    '-hist': self.analysis_dir + 'histo.xvg',
                                                    '-bsres': self.analysis_dir + 'bsResult.xvg',
                                                    '-bsprof': self.analysis_dir + 'bsProfs.xvg'})
        wham.run()
        if wham.output.erroroutput.result() != "":
            self.wham_textBrowser.append(wham.output.erroroutput.result())
        else:
            self.wham_textBrowser.append("wham finish!")

### Matplotlib Plotting functions
    def default_plot(self):
        """Default protocol plotting"""

        self.figure.clear()
        axes = self.figure.gca()

        protocol_img = mpimg.imread("umbrella_sampling_protocol.jpg")
        axes.imshow(protocol_img)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.figure.canvas.update()
    def plot_profile_xvg(self):
        self.figure.clear()
        axes = self.figure.gca()
        data = gromacs.fileformats.xvg.XVG(filename=self.analysis_dir + 'profile.xvg')
        axes.plot(data.array[0],data.array[1])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.figure.canvas.update()

    def plot_histo_xvg(self):
        self.figure.clear()
        axes = self.figure.gca()
        data = gromacs.fileformats.xvg.XVG(filename=self.analysis_dir + 'histo.xvg')
        for i in range(len(data.array)-1):
        	axes.plot(data.array[0],data.array[i+1])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.figure.canvas.update()

    def plot_bsResult_xvg(self):
        self.figure.clear()
        axes = self.figure.gca()

        data = gromacs.fileformats.xvg.XVG(filename=self.analysis_dir + 'bsResult.xvg')
        axes.plot(data.array[0],data.array[1])
        axes.fill_between(data.array[0],data.array[1]-data.array[2],data.array[1]+data.array[2],alpha=0.5)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.figure.canvas.update()

### Pymol Visulization functions
    def Change_display_Protein(self,state):
        if state == Qt.Checked:
            self.pymol_view.ShowSelect(representation="spheres", select = "protein")
        else:
            self.pymol_view.HideSelect(representation="spheres", select = "protein")

    def update_pymol_display(self):
        self.pymol_view.ShowSelect(representation="spheres", select = self.display_syntax_text.text())

    def display_pull_grp(self):
        self.pymol_view.HideAll()

        self.pymol_view.ShowSelect()
        self.pymol_view.ShowSelect(representation="spheres", select= "index " + "+".join(self.index_grp1))
        self.pymol_view.ShowSelect(representation="spheres", select= "index " + "+".join(self.index_grp2))

    def display_pymol(self,mol_location,**argv):
       self.pymol_view.loadMolFile(mol_location,**argv)
