#!/usr/bin/env python

import runregistry
import json
import argparse
import sys
from operator import itemgetter

def runs_list(filter_in): 
     runs = runregistry.get_runs(filter = filter_in)
     return runs

#print ( type(runs) )

def get_run_ls( run_in ):
     oms_lumisections = runregistry.get_oms_lumisections(run_in)
     lumi_store = []
     if run_in not in main_obj:
          main_obj[run_in] = []
     
     check_lumi_range = False

     for lumi in range(0, len(oms_lumisections)):
          if oms_lumisections[lumi]["fpix_ready"] == True and oms_lumisections[lumi]["bpix_ready"] == True and oms_lumisections[lumi]["tecm_ready"] == True and oms_lumisections[lumi]["tecp_ready"] == True and oms_lumisections[lumi]["tob_ready"] == True and oms_lumisections[lumi]["tibtid_ready"] == True and oms_lumisections[lumi]["cms_active"]  == True and oms_lumisections[lumi]["beam1_present"] == True and oms_lumisections[lumi]["beam2_present"] == True and oms_lumisections[lumi]["beam1_stable"] == True and oms_lumisections[lumi]["beam2_stable"] == True: 
               if check_lumi_range:
                    start_of_current_range = main_obj[run_in][-1][0] 
                    main_obj[run_in][-1] = [start_of_current_range,lumi+1]   

               if check_lumi_range is False:
                    main_obj[run_in].append([lumi+1,lumi+1]) 
                    check_lumi_range=True

          else:
               check_lumi_range=False

#     for el in main_obj:                                                                                              
#          main_obj[el] = sorted(main_obj[el], key=itemgetter(0))

     return main_obj[run_in]

def write_json(main_obj_read):
     with open(options.outfile, "w") as f:
         f.write(json.dumps(main_obj_read, indent=0, sort_keys=True))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Give list of Collisions runs for Online datasets')
    parser.add_argument("-o", "--outfile",
        dest="outfile", type=str, default="json_out.txt", help="Output file name")
    parser.add_argument("-v", "--verbose",
            dest="verbose", action="store_true", default=False, help="Display more info")
    parser.add_argument("-g", "--group",
        dest="dataset_group", type=str, default="Collisions18", help="Run class type")
    parser.add_argument("-min", "--min_run", dest="min_run", type=int, default=314472, help="minimum run for json")
    parser.add_argument("-max", "--max_run", dest="max_run",type=int, default=325175, help="maximum run for json")

    options = parser.parse_args()

    # generate filter 
    filter_arg = { 'run_number': { 'and':[ {'>=': options.min_run}, {'<=': options.max_run}] }, 
                   'class': { 'like': 'Collisions18'},
                   'oms_attributes.b_field': {">": 3.7},
                   'oms_attributes.pixel_included': {"=": True},
                   'oms_attributes.tracker_included': {"=": True},
              }

    out_runs = runs_list(filter_arg)

#    print (out_runs)

    main_obj = {}                                                                                                                                            
    for run in out_runs:
         main_obj[run["run_number"]]= get_run_ls(run["run_number"])


    for el in main_obj:
         main_obj[el] = sorted(main_obj[el], key=itemgetter(0))


    write_json(main_obj)
