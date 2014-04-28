#============================================
#   python xhamster gallery scraper v1.3
#   copyright 2014 qt
#   this program is free software under the GNU GPL version 3
#   usage: $program_name $url $output_dir
#
#   KNOWN BUGS:
#   - cant handle backslashes at the end of the output_dir argument
#
#   TODO:
#   - port it to different sites
#============================================
import sys
import os
import re
from urllib import request
#----------------------------------------------------------------------------------------------------------------
#   utility functions
#----------------------------------------------------------------------------------------------------------------
def clean_page(page):
	return(str(page.read()).replace(r"\n", "\n")).replace(r"\r", "\r")
#----------------------------------------------------------------------------------------------------------------
#   main functions
#----------------------------------------------------------------------------------------------------------------
def get_page(URL):
    #stage 2
    #retrieve and return the index page
    try:
        page = request.urlopen(URL)
        return(clean_page(page))
    except:
        print("fuck, cant retrieve and store file located at the given URL")
        sys.exit()
#----------------------------------------------------------------------------------------------------------------
def build_list(index_file):
    #stage 3
    #build and return a list of image container page URLs to grab
    try:
        image_page_URL = "http://xhamster.com/photos/view/"
        print(" - " + str(index_file.count(image_page_URL)) + " images identified")#debug

        search_expression = 'http://xhamster\.com/photos/view/(.*?).html'
        search_results = re.findall(search_expression, index_file)

        page_list = []
        for i in search_results:
            page_list.append(image_page_URL + i + ".html")
        return(page_list)
    except:
        print("fuck, cant build wrapper page list")
        sys.exit()
#----------------------------------------------------------------------------------------------------------------
def grab_files(page_list):
    #stage 4
    #with each container URL get the file, search for the image and then save it
    try:
        #image_URL_prefix = r"http://ep.xhamster.com/"
        #search_expression = image_URL_prefix + "(.*?\.jpg|.*?\.png|.*?\.gif|.*?\.jpeg)"
        image_URL_prefix = r"http://"
        search_expression = image_URL_prefix + "(ep[1-9]\.xhamster\.com\/(?:.*?\$

        for i in page_list:
            wrapper_page = get_page(i)
            image_URL_suffix = re.findall(search_expression, wrapper_page, re.IGNORECASE)[0]
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
#----------------------------------------------------------------------------------------------------------------
#   main procedure
#----------------------------------------------------------------------------------------------------------------

# stage 0
# parse args
try:
    gallery_URL, output_directory = sys.argv[1], sys.argv[2] + "/"
except:
    print("fuck, cant process arguments")
    sys.exit()
    
print("stage 0 complete")

# stage 1
# make directory
try:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
except:
    print("fuck, cant make target directory")
    sys.exit()
print("stage 1 complete")

index_file = get_page(gallery_URL)
print("stage 2 complete")

page_list = build_list(index_file)
print("stage 3 complete")

grab_files(page_list)
print("stage 4 complete: fucking done")
#----------------------------------------------------------------------------------------------------------------

    






