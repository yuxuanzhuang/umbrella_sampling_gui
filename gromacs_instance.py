import gmxapi as gmx
import os,shutil
class gromacs_instance():
    def __init__(self,mdp_file,starting_structure,restraining_structure,topology_file,tpr_file):
        self.mdp_file = mdp_file
        self.starting_structure = starting_structure
        self.restraining_structure = restraining_structure
        self.topology_file = topology_file
        self.tpr_file = tpr_file
    def generate_tpr_file(self):
        grompp = gmx.commandline_operation(
                                        'gmx',
                                        'grompp',
                                        input_files={'-f': self.mdp_file,
                                                     '-c': self.starting_structure,
                                                     '-r': self.restraining_structure,
                                                     '-p': self.topology_file},
                                        output_files={'-o': self.tpr_file})
        grompp.run()
        self.grompp_erroroutput = grompp.output.erroroutput.result()
    def mdrun_process(self):
        cwd = os.getcwd()
        mdrun_dir_path = os.path.dirname(self.tpr_file)
        print(cwd)
        print(mdrun_dir_path)
        os.chdir(cwd + '/' + mdrun_dir_path)
        mdrun = gmx.mdrun(os.path.split(self.tpr_file)[-1])
        mdrun.run()
        output_path = os.path.dirname(mdrun.output.trajectory.result())

        if os.path.splitext(os.path.split(self.tpr_file)[-1])[0] != "md":
            shutil.copy(os.path.join(output_path, "confout.gro"), cwd + '/' + mdrun_dir_path + '/' + os.path.splitext(os.path.split(self.tpr_file)[-1])[0] + '.gro')
        else:
            output_files = os.listdir(output_path)
            for file_name in output_files:
                full_file_name = os.path.join(output_path, file_name)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, cwd + '/' + mdrun_dir_path)
        os.chdir(cwd)
        return
