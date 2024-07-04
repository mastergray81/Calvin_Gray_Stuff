import os, sys, shutil, csv, time, datetime, glob, re, logging

def circuitSearch(circuits_complete, all_circuits_dict):

    circuit_paths = list(all_circuits_dict.values())
    for x in circuits_complete:
        for y in circuit_paths:
            if x in y:
                circuit_paths.remove(y)


    print("Number of circuits to be processed:",len(circuit_paths),'\n------------\n',circuit_paths)

    return circuit_paths

