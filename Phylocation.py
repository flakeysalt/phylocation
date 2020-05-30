from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import numpy as np

if __name__ == "__main__":
    file_names = ["DonovanSM.txt", "RidlonJM.txt", "HeathKD.txt", "KuehnS.txt", "SirkSJ.txt", "PanD.txt", "JensenPA.txt", "SmithRL.txt"]
    with open("names.csv",'r') as f:
        reader = csv.reader(f, delimiter=',')
        names = list(reader)
    file_names = [name[0].replace(" ","") +"_"+ name[1].replace(" ","")+".txt" for name in names]
    documents = []
    for file_name in file_names:
        file = open("Abstracts2\\"+file_name,"r",encoding="utf-8")
        print(file_name)
        text = ""
        for line in file:
            text += line.replace("\n","")
        documents.append(text)
    print(len(documents))
    tfidf = TfidfVectorizer().fit_transform(documents)
    print(tfidf.A.shape)
    np.savetxt("tfidf_vectors.csv", tfidf.A, delimiter=",")
    # for file_name in file_names:
    #     file = open("Abstracts2\\"+file_name,"r",encoding="utf-8")
    #     text = ""
    #     for line in file:
    #         text += line.replace("\n","")
    #     vector = TfidfVectorizer().transform(text)
    #     print(vector.shape)
    #     print(vector.toarray())

    pairwise_similarity = tfidf * tfidf.T

    print(pairwise_similarity.A)
    np.savetxt("sim_mat.csv", pairwise_similarity.A, delimiter=",", header = ",".join(file_names))
