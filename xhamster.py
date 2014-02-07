#============================================
#   python xhamster gallery scraper
#   written by qt
#   usage: $program_name $url $output_dir
#
#   TODO:
#   - add a feature to tell whether the out dir ends in a backslash or slash (depending on OS)
#   - split the program into functions
#   - make it portable to different websites
#   - port it to different sites
#============================================

import sys
import re
from file_io import *
from urllib import request

def clean_page(page):
	return(str(page.read()).replace(r"\n", "\n")).replace(r"\r", "\r")
#----------------------------------------------------------------------------------------------------------------
# stage 0
# parse args
try:
    gallery_url, output_directory = sys.argv[1], sys.argv[2] + "/"
except:
    print("fuck, cant process arguments")
    sys.exit()
    
print("stage 0 complete")
#----------------------------------------------------------------------------------------------------------------
# stage 1
# get gallery index
try:
	index_page = request.urlopen(gallery_url)
	page_file_data = clean_page(index_page)
except:
	print("fuck, cant retrieve and store file located at the given URL")
	sys.exit()
	
print("stage 1 complete")
#----------------------------------------------------------------------------------------------------------------
# stage 2
# build image page list
try:
    image_page_URL = "http://xhamster.com/photos/view/"
    print(" - " + str(page_file_data.count(image_page_URL)) + " images identified")#debug

    stage2_search_expression = 'http://xhamster\.com/photos/view/(.*?).html'
    search_results = re.findall(stage2_search_expression, page_file_data)

    page_list = []
    for i in search_results:
        page_list.append(image_page_URL + i + ".html")
except:
    print("fuck, cant build wrapper page list")
    sys.exit()
    
print("stage 2 complete")
#----------------------------------------------------------------------------------------------------------------
#stage 3
#with each page, identify the image link save that fucker
try:
    image_URL_prefix = r"http://ep.xhamster.com/"
    stage3_search_expression = image_URL_prefix + "(.*?\.jpg|png|gif)"
    for i in page_list:
        wrapper_page = request.urlopen(i)
        wrapper_page_data = clean_page(wrapper_page)
        image_URL_suffix = re.findall(stage3_search_expression, wrapper_page_data)[0]
        image = request.urlopen(image_URL_prefix + image_URL_suffix)
        
        image_name = ""
        for c in reversed(image_URL_suffix):
            if c != "/":
                image_name = image_name + c
            else:
                image_name = image_name[::-1]
                break
            
        image_file = open(output_directory + image_name, "wb+")
        image_file.write(image.read())
        print(image_name + " saved")
except:
    print("fuck, cant parse containers and/or save images")
    sys.exit()
    
print("stage 3 complete: fucking done")





