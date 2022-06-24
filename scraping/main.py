import requests
from bs4 import BeautifulSoup
import csv

def main():
  VOWELS =("a","i","u","e","o")
  CONSONANTS  = ("","k","s","t","n","h","m","y","r","w")
  index_pages_reaponse_list=[]
  for consonant in CONSONANTS:
    for vowel in VOWELS:
    
      charactor = consonant+vowel
      number=1
      noPage =False
      while not noPage:        
        response = requests.get("https://www.aozora.gr.jp/index_pages/sakuhin_"+charactor+str(number)+".html")
        if(response.status_code==200):
          index_pages_reaponse_list.append(response)
          number+=1
        else:
          noPage=True  
  url_list=[]        
  for index_pages_reaponse in  index_pages_reaponse_list:
    soup = BeautifulSoup(index_pages_reaponse.text, 'html.parser')
    link_list = soup.select("a")
    for link in link_list:
      
      url_list.append(link.get("href"))
  response_list=[]    
  for url in url_list:
    if url[:8]=="../cards":
      response = requests.get("https://www.aozora.gr.jp"+url[2:])
      if response.status_code==200:
        response_list.append(response)
  HEADER = ["name","name_pseudonym","author","author_name_pseudonym","author_birthday","author_day_of_dath"]  

  with open('books.csv',"w") as f:
    writer = csv.writer(f) 
    writer.writerow(HEADER)
    for response in response_list:
      soup = BeautifulSoup(response.content, 'html.parser')
      td_list=soup.select("td")   
      name=""  
      name_pseudonym="" 
      author=""
      author_pseudonym=""
      author_birth_day=""
      author_day_of_dath=""
      name_index=-2
      name_pseudonym_index=-2
      author_index=-2
      author_pseudonym_index=-2
      author_birthday_index=-2
      author_day_of_dath_index=-2
      for i,td in  enumerate(td_list):
        if "作品名：" in td.get_text():
          name_index=i+1
        if "作品名読み：" in td.get_text():
          name_pseudonym_index=i+1  
        if "作家名：" in  td.get_text():
          author_index=i+1  
        if "作家名読み：" in td.get_text():
          author_pseudonym_index=i+1
        if "生年：" in td.get_text():
          author_birthday_index=i+1  
        if "没年：" in  td.get_text():
          author_day_of_dath_index=i+1 
        if i==name_index:
          name=td.get_text()
        if i==name_pseudonym_index:
          name_pseudonym=td.get_text()  
        if i==author_index:
          author=td.get_text()
        if i==author_pseudonym_index:
          author_pseudonym=td.get_text()  
        if i==author_birthday_index:
          author_birth_day=td.get_text()
        if i==author_day_of_dath_index:
          author_day_of_dath=td.get_text()  
      row=[name,name_pseudonym,author,author_pseudonym,author_birth_day,author_day_of_dath]
      writer.writerow(row)
if __name__ == '__main__':
    main()
