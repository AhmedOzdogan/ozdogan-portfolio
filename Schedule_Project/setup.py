# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 23:09:21 2023

@author: ahmed
"""

from cx_Freeze import setup, Executable

base = None

executables = [Executable("ScheduleV4.3.py", base=base)]

setup(
    name="Teaching Schedule",
    version="4.3",
    description="SQL based schedule",
    options={"build_exe": {"packages": [], "include_files": []}},
    executables=executables
)

import sys
sys.setrecursionlimit(10000)