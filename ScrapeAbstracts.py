import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv

if __name__ == "__main__":
    with open("names.csv",'r') as f:
        reader = csv.reader(f, delimiter=',')
        names = list(reader)
    # print(names)

    my_urls = []
    base_url = "https://www.ncbi.nlm.nih.gov/pubmed/?term={}+{}%5Bauthor%5D"
    base_paper_url = "https://www.ncbi.nlm.nih.gov"
    for name in names:
        my_urls.append(base_url.format(name[0].replace(" ",""),name[1].replace(" ","")))
    # print(my_urls)

    for idx,url in enumerate(my_urls):
        print(names[idx])
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        papers = page_soup.findAll("div",{"class":"rslt"})
        # print(papers)
        titles = page_soup.findAll("p",{"class":"title"})
        # print(titles)
        possible_abstract = page_soup.findAll("div",{"class":"abstr"})
        text = ""
        for title in titles:
            ref_to_paper = title.findAll('a',href=True)[0]['href']
            # print(title['href'])
            paper_client = uReq(base_paper_url+ref_to_paper)
            paper_html = paper_client.read()
            paper_client.close()
            paper_soup = soup(paper_html, "html.parser")
            abstract = paper_soup.findAll("div",{"class":"abstr"})
            if abstract:
                text += abstract[0].find('p').getText() +" "
        if text == "" and possible_abstract:
            text += possible_abstract[0].find('p').getText() +" "
        # elif text == "":
        #     for title in titles:
        #         ref_to_paper = title.findAll('a',href=True)[0]['href']
        #         # print(title['href'])
        #         print(ref_to_paper)
        #         try:
        #             paper_client = uReq(base_paper_url+ref_to_paper)
        #         except:
        #             break
        #         paper_html = paper_client.read()
        #         paper_client.close()
        #         paper_soup = soup(paper_html, "html.parser")
        #         abstract = paper_soup.findAll("div",{"class":"abstr"})
        #         if abstract:
        #             text += abstract[0].find('p').getText() +" "

        print(text)
        file = open("Abstracts2\{}_{}.txt".format(names[idx][0],names[idx][1]),"w",encoding="utf-8")
        file.write(text)
        file.close()
