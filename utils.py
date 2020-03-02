import sys, os,re
import shutil

'''implementation of sed'''
def sed_implementation(file_open,file_write,org_str,sub_str):
    with open(file_open, "r") as sources:
        lines = sources.readlines()
    with open(file_write, "w") as sources:
        for line in lines:
            sources.write(re.sub(org_str, sub_str, line))
