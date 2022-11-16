from django.shortcuts import render,redirect,HttpResponse
import json
from django.http import JsonResponse
from multiprocessing.resource_sharer import stop
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import OrderedDict 
import os
import pydot
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'baz.txt')
# Create your views here.
def keywordExtractorPage(request):
    print("the page has loaded")
    return render(request, 'landingPage.html')


def graphMaker(feature_checklist,feature_index):
   
    isOR_1=False
    isOR_2=False
    isOR_3=False

    file_path = os.path.join(module_dir, 'graphGen/featureModel.dot')

    f = open(file_path, "w")
    f.write("digraph pos{ \n")
    f.write('   node [shape="box"]; \n')
    f.write('   edge [arrowhead="dot"]; \n')
    if feature_checklist[feature_index["payment"]]=="payment":
        num=0
        if feature_checklist[feature_index["cash"]]=="cash":
            num+=1
        if feature_checklist[feature_index["credit card"]]=="credit card":
            num+=1
        if feature_checklist[feature_index["debit card"]]=="debit card":
            num+=1
        if feature_checklist[feature_index["bank check"]]=="bank check":
            num+=1
        if num>=2:
            f.write('   OR_1 [label="OR" shape="ellipse" style="filled"]\n')
            isOR_1=True

    num2=0
    if feature_checklist[feature_index["staff database"]]=="staff database":
        num2+=1
    if feature_checklist[feature_index["customer database"]]=="customer database":
        num2+=1
    if feature_checklist[feature_index["product database"]]=="product database":
        num2+=1
    if num2>=2:
        f.write('   OR_2 [label="OR" shape="ellipse" style="filled"]\n')
        isOR_2=True

    num3=0
    if feature_checklist[feature_index["taxes"]]=="taxes":
        num3+=1
    if feature_checklist[feature_index["home delivery"]]=="home delivery":
        num3+=1
    if num3>=2:
        f.write('   OR_3 [label="OR" shape="ellipse" style="filled"]\n')
        isOR_3=True

    if feature_checklist[feature_index["staff login"]]=="staff login":
        f.write('   POS -> "Employee Authentication System";\n')
        f.write('       "Employee Authentication System" -> "Employee Login";\n')
        f.write('       "Employee Authentication System" -> "Employee Logout";\n')

    if feature_checklist[feature_index["inventory list"]]=="inventory list":
        f.write('   POS -> "Inventory List";\n')

    if feature_checklist[feature_index["order product"]]=="order product" or feature_checklist[feature_index["scan product"]]=="scan product" or feature_checklist[feature_index["items cart"]]=="items cart" or feature_checklist[feature_index["print receipt"]]=="print receipt" or feature_checklist[feature_index["payment"]]=="payment":
        f.write('   POS -> "Product Purchase System";\n')
        if feature_checklist[feature_index["order product"]]=="order product":
            f.write('       "Product Purchase System" -> "Order Entry";\n')
        if feature_checklist[feature_index["scan product"]]=="scan product":
            f.write('       "Product Purchase System" -> "Product Scanning System" [arrowhead="odot"];\n')
        if feature_checklist[feature_index["items cart"]]=="items cart":
            f.write('       "Product Purchase System" -> "Cart System";\n')
            if feature_checklist[feature_index["add cart"]]=="add cart":
                f.write('           "Cart System" -> "Cart Append";\n')
            if feature_checklist[feature_index["remove cart"]]=="remove cart":
                f.write('           "Cart System" -> "Cart Remove";\n')
            if feature_checklist[feature_index["confirm cart"]]=="confirm cart":
                f.write('           "Cart System" -> "Cart Confirmation";\n')
        if feature_checklist[feature_index["print receipt"]]=="print receipt":
            f.write('       "Product Purchase System" -> "Receipt Generation";\n')
        if feature_checklist[feature_index["payment"]]=="payment":
            f.write('       "Product Purchase System" -> "Payment System";\n')
            if isOR_1:
                f.write('           "Payment System" -> OR_1 [arrowhead=none];\n')
            if feature_checklist[feature_index["cash"]]=="cash":
                if isOR_1:
                    f.write('               OR_1 -> Cash [arrowhead=none];\n')
                else:
                    f.write('               "Payment System" -> Cash;\n')
            if feature_checklist[feature_index["credit card"]]=="credit card":
                if isOR_1:
                    f.write('               OR_1 -> "Credit Card" [arrowhead=none];\n')
                else:
                    f.write('               "Payment System" -> "Credit Card";\n')
            if feature_checklist[feature_index["debit card"]]=="debit card":
                if isOR_1:
                    f.write('               OR_1 -> "Debit Card" [arrowhead=none];\n')
                else:
                    f.write('               "Payment System" -> "Debit Card";\n')
            if feature_checklist[feature_index["bank check"]]=="bank check":
                if isOR_1:
                    f.write('               OR_1 -> Check [arrowhead=none];\n')
                else:
                    f.write('               "Payment System" -> Check;\n')

    if feature_checklist[feature_index["staff database"]]=="staff database" or feature_checklist[feature_index["customer database"]]=="customer database" or feature_checklist[feature_index["product database"]]=="product database":
        f.write('   POS -> "Central Database";\n')
        if isOR_2:
            f.write('       "Central Database" -> OR_2 [arrowhead=none];\n')
        if feature_checklist[feature_index["staff database"]]=="staff database":
            if isOR_2:
                f.write('            OR_2 -> "Employee Database" [arrowhead=none];\n')
            else:
                f.write('            "Central Database" -> "Employee Database";\n')
        if feature_checklist[feature_index["customer database"]]=="customer database":
            if isOR_2:
                f.write('            OR_2 -> "Customer Database" [arrowhead=none];\n')
            else:
                f.write('            "Central Database" -> "Customer Database";\n')
        if feature_checklist[feature_index["product database"]]=="product database":
            if isOR_2:
                f.write('            OR_2 -> "Product Database" [arrowhead=none];\n')
            else:
                f.write('            "Central Database" -> "Product Database";\n')

    if feature_checklist[feature_index["employee profile"]]=="employee profile":
        f.write('   POS -> "Employee Profile Management" [arrowhead="odot"];\n')
        f.write('       "Employee Profile Management" -> "Employee Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["employee wages"]]=="employee wages":
        f.write('   POS -> "Employee Payroll" [arrowhead="odot"];\n')
        f.write('       "Employee Payroll" -> "Employee Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["employee permission"]]=="employee permission" or feature_checklist[feature_index["employee timesheets"]]=="employee timesheets":
        f.write('   POS -> "Employee Access and Performance Management" [arrowhead="odot"];\n')
        f.write('       "Employee Access and Performance Management" -> "Employee Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["stock alert"]]=="stock alert" or feature_checklist[feature_index["discount offer"]]=="discount offer":
        f.write('   POS -> "Product Inventory Management" [arrowhead="odot"];\n')
        if feature_checklist[feature_index["stock alert"]]=="stock alert":
            f.write('       "Product Inventory Management" -> "Stock Alert" [arrowhead="odot"];\n')
            f.write('           "Stock Alert" -> "Product Database" [style="dashed" arrowhead="normal"];\n')
        if feature_checklist[feature_index["discount offer"]]=="discount offer":
            f.write('       "Product Inventory Management" -> "Product Offers and Discount Management" [arrowhead="odot"];\n')
            f.write('           "Product Offers and Discount Management" -> "Product Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["billing"]]=="billing":
        f.write('   POS -> "Billing Management";\n')

    if feature_checklist[feature_index["taxes"]]=="taxes" or feature_checklist[feature_index["home delivery"]]=="home delivery":
        f.write('   POS -> "Advanced Billing System" [arrowhead="odot"];\n')
        if isOR_3:
            f.write('       "Advanced Billing System" -> OR_3 [arrowhead=none];\n')
        if feature_checklist[feature_index["taxes"]]=="taxes":
            if isOR_3:
                f.write('           OR_3 -> "VAT and Tax Management" [arrowhead=none];\n')
            else:
                f.write('           "Advanced Billing System" -> "VAT and Tax Management";\n')
        if feature_checklist[feature_index["home delivery"]]=="home delivery":
            if isOR_3:
                f.write('           OR_3 -> "Home Delivery Service" [arrowhead=none];\n')
            else:
                f.write('           "Home Delivery Service" -> "VAT and Tax Management";\n')

    if feature_checklist[feature_index["customer profile"]]=="customer profile":
        f.write('   POS -> "Customer Profile Management" [arrowhead="odot"];\n')
        f.write('       "Customer Profile Management" -> "Customer Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["return product"]]=="return product" or feature_checklist[feature_index["refund"]]=="refund":
        f.write('   POS -> "Product Return System" [arrowhead="odot"];\n')
        if feature_checklist[feature_index["return product"]]=="return product":
            f.write('       "Product Return System" -> "Return Product" [arrowhead="odot"];\n')
        if feature_checklist[feature_index["refund"]]=="refund":
            f.write('       "Product Return System" -> Refund [arrowhead="odot"];\n')
            f.write('           Refund -> "Return Product" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["personalized offers"]]=="personalized offers":
        f.write('   POS -> "Customer Relations and Offers Management" [arrowhead="odot"];\n')
        f.write('       "Customer Relations and Offers Management" -> "Customer Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["daily sales report"]]=="daily sales report":
        f.write('   POS -> "Daily Sales Report" [arrowhead="odot"];\n')
        f.write('       "Daily Sales Report" -> "Product Database" [style="dashed" arrowhead="normal"];\n')

    if feature_checklist[feature_index["admin account"]]=="admin account" or feature_checklist[feature_index["custom report"]]=="custom report" or feature_checklist[feature_index["sales analytics"]]=="sales analytics" or feature_checklist[feature_index["staff analytics"]]=="staff analytics" or feature_checklist[feature_index["customer analytics"]]=="customer analytics":
        f.write('    POS -> "Specialized Admin System" [arrowhead="odot"];\n')
        if feature_checklist[feature_index["admin account"]]=="admin account":
            f.write('       "Specialized Admin System" -> "Admin Account" [arrowhead="odot"];\n')
        if feature_checklist[feature_index["custom report"]]=="custom report":
            f.write('       "Specialized Admin System" -> "Customized Reports" [arrowhead="odot"];\n')
            f.write('           "Customized Reports" -> "Admin Account" [style="dashed" arrowhead="normal"];\n')
        if feature_checklist[feature_index["sales analytics"]]=="sales analytics" or feature_checklist[feature_index["staff analytics"]]=="staff analytics" or feature_checklist[feature_index["customer analytics"]]=="customer analytics":
            f.write('       "Specialized Admin System" -> "Sector Specific Analytics" [arrowhead="odot"];\n')
            if feature_checklist[feature_index["sales analytics"]]=="sales analytics":
                f.write('           "Sector Specific Analytics" -> "Sales Analytics" [arrowhead="odot"];\n')
                f.write('               "Sales Analytics" -> "Product Database" [style="dashed" arrowhead="normal"];\n')
                f.write('               "Sales Analytics" -> "Admin Account" [style="dashed" arrowhead="normal"];\n')
            if feature_checklist[feature_index["staff analytics"]]=="staff analytics":
                f.write('           "Sector Specific Analytics" -> "Employee Analytics" [arrowhead="odot"];\n')
                f.write('               "Employee Analytics" -> "Employee Database" [style="dashed" arrowhead="normal"];\n')
                f.write('               "Employee Analytics" -> "Admin Account" [style="dashed" arrowhead="normal"];\n')
            if feature_checklist[feature_index["customer analytics"]]=="customer analytics":
                f.write('           "Sector Specific Analytics" -> "Customer Analytics" [arrowhead="odot"];\n')
                f.write('               "Customer Analytics" -> "Customer Database" [style="dashed" arrowhead="normal"];\n')
                f.write('               "Customer Analytics" -> "Admin Account" [style="dashed" arrowhead="normal"];\n')

    f.write('}')    
    f.close()



    f = open(file_path, "r")
    print(f.read())
    graphs = pydot.graph_from_dot_file(file_path)
    graph = graphs[0]
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    graph.write_svg(f'{BASE_DIR}\\static\\images\\outputGraph.svg')




def keywordExtractorFunc(request):

    file_path = os.path.join(module_dir, 'jsons/stopwords.json')
    with open(file_path, 'rb') as fp:
        stop_words = json.load(fp)
    fp.close()

    # print(stop_words)

    text=request.POST.get('userText')


    text=text.lower()

    tokens = word_tokenize(text)
    lem_tokens=[t for t in tokens if t not in stop_words]


    file_path = os.path.join(module_dir, 'jsons/syn_map.json')
    fr=open(file_path, "r")
    syn_map=json.load(fr)
    fr.close()

    extracted_features=[]


    n=1
    while n<=3:
        for i in range(len(lem_tokens)- n+1):
            phrase_list=lem_tokens[i:i+n]
            if ('.' in phrase_list) or (',' in phrase_list):
                continue
            phrase=" ".join(phrase_list)
            try:
                feature=syn_map[phrase]
                extracted_features.append(feature)
            except:
                continue
        n+=1

    print(extracted_features)

    file_path = os.path.join(module_dir, 'jsons/feature_index.json')
    fr=open(file_path, "r")
    feature_index=json.load(fr)
    fr.close()

    feature_checklist=[]
    for i in range(38):
        feature_checklist.append('X')

    for feature in extracted_features:
        feature_checklist[feature_index[feature]]=feature
    # print(feature_checklist)
    file_path = os.path.join(module_dir, 'jsons/dependencies.json')
    fr=open(file_path, "r")
    dependencies=json.load(fr)
    fr.close()

    required=[]
    for feature in extracted_features:
        for i in dependencies[feature]:
            if feature_checklist[i]=='X':
                value = list(feature_index.keys())[list(feature_index.values()).index(i)]
                required.append(value)
                feature_checklist[feature_index[value]]=value
    required = list(OrderedDict.fromkeys(required))

    # if len(required)!=0:
    #     print('These Features are Required: '+str(required))
    #     print('Add these features?')
    #     add_Req=True
    #     if add_Req:
    #         print('Adding these features...')
    #         extracted_features.extend(required)

    extracted_features = list(OrderedDict.fromkeys(extracted_features))
    print(text)
    print("These are the extracted features form the form")
    print(extracted_features)

    graphMaker(feature_checklist,feature_index)

    context={'features':extracted_features,'dependent_features':required, 'generated':True}
    return render(request,'landingPage.html',context)
  