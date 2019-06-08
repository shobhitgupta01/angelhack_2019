#############################################################################################################################
#Purpose    : Accept url and return the visible text in the url
#Author     : Shobhit Gupta
#Madefor    : Angelhack 2019
########################################################################################################################### 


#Importing the libraries
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import json

#--------------------------------------------------method description-----------------------------------------------------------
#Name       : find_visible
#purpose    : to find visible elements of the url page
#Input:
    #type   : string
    #value  : all html tags
#Output:
    #type   : bool
    #value  : True if text is visible else False
#-------------------------------------------------------------------------------------------------------------------------------

def find_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
    
    
#--------------------------------------------------method description-----------------------------------------------------------
#Name       : get_text
#purpose    : to get visible text from url
#Input:
    #type   : string
    #value  : url to extract content from
#Output:
    #type   :   string
    #value  : text content from url
#-------------------------------------------------------------------------------------------------------------------------------

def get_text(page_url):

    #hitting the page url
    try:
        page = requests.get(page_url)
    
    #return exception if any
    except requests.exceptions.RequestException as e :
        return e

    #creating soup
    soup = BeautifulSoup(page.text,'html.parser')

    #finding all texts
    texts = soup.findAll(text=True)

    #filtering texts
    visible_texts = filter(find_visible, texts)

    #removing non-ascii characters  
    final_text = "".join(t.strip() for t in visible_texts)
    
    #returning the filtered texts
    my_data = "".join([i if ord(i) < 128 else ' ' for i in final_text])

    data_object = {'text_output':my_data}

    with open('./test_data/job_safe.json','w+') as f:
        json.dump(data_object,f) 
 