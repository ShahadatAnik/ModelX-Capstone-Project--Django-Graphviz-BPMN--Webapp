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

def bpmnMaker(feature_index,extracted_features):
    

    feature_checklist=[]
    for i in range(38):
        feature_checklist.append('X')

    for feature in extracted_features:
        feature_checklist[feature_index[feature]]=feature

    if feature_checklist[feature_index["admin account"]]=="admin account" or feature_checklist[feature_index["customer analytics"]]=="customer analytics" or feature_checklist[feature_index["sales analytics"]]=="sales analytics" or feature_checklist[feature_index["custom report"]]=="custom report" or feature_checklist[feature_index["staff analytics"]]=="staff analytics":
        or1Score=0
        or2Score=0
        or3Score=0
        if feature_checklist[feature_index["custom report"]]=="custom report":
            or1Score+=1
            or2Score+=1
        if feature_checklist[feature_index["staff analytics"]]=="staff analytics":
            or1Score+=1
            or2Score+=1
        if feature_checklist[feature_index["sales analytics"]]=="sales analytics":
            or1Score+=1
            or2Score+=1
        if feature_checklist[feature_index["customer profile"]]=="customer profile" or feature_checklist[feature_index["customer analytics"]]=="customer analytics" or feature_checklist[feature_index["personalized offers"]]=="personalized offers":
            or1Score+=1
            or2Score+=1
        if feature_checklist[feature_index["employee profile"]]=="employee profile":
            or1Score+=1
            or3Score+=1
        if feature_checklist[feature_index["customer profile"]]=="customer profile" or feature_checklist[feature_index["customer analytics"]]=="customer analytics" or feature_checklist[feature_index["personalized offers"]]=="personalized offers" or feature_checklist[feature_index["custom report"]]=="custom report" or feature_checklist[feature_index["staff analytics"]]=="staff analytics" or feature_checklist[feature_index["sales analytics"]]=="sales analytics":
            or3Score+=1
        
        file_path_admin = os.path.join(module_dir, 'graphGen/adminProcessBPMN.dot')
        fA = open(file_path_admin, "w")
        fA.write("digraph G { \n")
        fA.write('  graph [compound = true, ranksep = .5,color = crimson, bgcolor = white, fontname="Helvetica,Arial,sans-serif", fontsize = 18, labeljust = c, labelloc = t, margin = .9, nodesep = .5, rankdir = LR, ranksep = .25, splines = true]; \n')
        fA.write('  node [fontname="Helvetica,Arial,sans-serif", shape="Mrecord", fillcolor="#F4F06A", fontcolor=black, style=filled]; \n')
        fA.write('	edge [fontname="Helvetica,Arial,sans-serif"]; \n')
        fA.write('	subgraph cluster_0 {  \n')
        fA.write('        label = "Admin"; \n')
        fA.write('        startAdmin [shape=circle, label="", color = green, width = 0.3, fillcolor=green, style=filled];\n')
        fA.write('        endAdmin [shape=circle, label="", color = red, width = 0.3, fillcolor=red, style=filled];\n')

        if or1Score>1:
            fA.write('        or1 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ; \n')
        if or2Score>1:
            fA.write('        or2 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ; \n')
        if or3Score>1:
            fA.write('        or3 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ; \n')
        
        if feature_checklist[feature_index["admin account"]]=="admin account":
            fA.write('        "Access Admin Account";  \n')
            fA.write('        "Admin Logout";  \n')
        if feature_checklist[feature_index["customer profile"]]=="customer profile" or feature_checklist[feature_index["customer analytics"]]=="customer analytics" or feature_checklist[feature_index["personalized offers"]]=="personalized offers" or feature_checklist[feature_index["custom report"]]=="custom report" or feature_checklist[feature_index["staff analytics"]]=="staff analytics" or feature_checklist[feature_index["sales analytics"]]=="sales analytics":
            fA.write('        "Print Report";  \n')
        if feature_checklist[feature_index["employee profile"]]=="employee profile":
            fA.write('        "Create Employee Profile";  \n')
        if feature_checklist[feature_index["sales analytics"]]=="sales analytics":
            fA.write('        "Sales Analytics";  \n')
        if feature_checklist[feature_index["custom report"]]=="custom report":
            fA.write('        "Customized Report";  \n')
        if feature_checklist[feature_index["staff analytics"]]=="staff analytics":
            fA.write('        "Staff Analytics";  \n')

        fA.write('	} \n')

        fA.write('	subgraph cluster_1 {  \n')
        fA.write('        label = "Customer"; \n')

        cust_list=[]
        if feature_checklist[feature_index["customer profile"]]=="customer profile":
            fA.write('        "Customer Account";  \n')
            cust_list.append('"Customer Account"')
        if feature_checklist[feature_index["customer analytics"]]=="customer analytics":
            fA.write('        "Customer Analytics";  \n')
            cust_list.append('"Customer Analytics"')
        if feature_checklist[feature_index["personalized offers"]]=="personalized offers":
            fA.write('        "Personalized Offers";  \n')
            cust_list.append('"Personalized Offers"')
        cust_len=len(cust_list)

        fA.write('	} \n')

        if feature_checklist[feature_index["admin account"]]=="admin account":
            fA.write('        startAdmin -> "Access Admin Account";  \n')
            if or1Score>1:
                fA.write('        "Access Admin Account" -> or1;  \n')
                if feature_checklist[feature_index["custom report"]]=="custom report":
                    fA.write('        or1 -> "Customized Report";  \n')
                    if or2Score>1:
                        fA.write('        "Customized Report" -> or2;  \n')
                    else:
                        fA.write('        "Customized Report" -> "Print Report";  \n')
                if feature_checklist[feature_index["staff analytics"]]=="staff analytics":
                    fA.write('        or1 -> "Staff Analytics";  \n')
                    if or2Score>1:
                        fA.write('        "Staff Analytics" -> or2;  \n')
                    else:
                        fA.write('        "Staff Analytics" -> "Print Report";  \n')
                if feature_checklist[feature_index["sales analytics"]]=="sales analytics":
                    fA.write('        or1 -> "Sales Analytics";  \n')
                    if or2Score>1:
                        fA.write('        "Sales Analytics" -> or2;  \n')
                    else:
                        fA.write('        "Sales Analytics" -> "Print Report";  \n')
                if feature_checklist[feature_index["employee profile"]]=="employee profile":
                    fA.write('        or1 -> "Create Employee Profile";  \n')
                    if or3Score>1:
                        fA.write('        "Create Employee Profile" -> or3;  \n')
                if cust_len!=0:
                    fA.write('        or1 -> '+cust_list[0]+';  \n')
                    ws=''
                    if cust_len>1:
                        for i in range(0,cust_len):
                            if i!=0:
                                ws=ws+' -> '
                            ws=ws+cust_list[i]
                        fA.write('        '+ws+';  \n')
                    if or2Score>1:
                        fA.write('        '+cust_list[cust_len-1]+' -> or2;  \n')
                    else:
                        fA.write('        '+cust_list[cust_len-1]+' -> "Print Report";  \n')
                if or2Score>1:
                    fA.write('        or2 -> "Print Report";  \n')
                if or3Score>1:
                    fA.write('        "Print Report" -> or3;  \n')
                    fA.write('        or3 -> "Admin Logout" -> endAdmin;  \n')
                else:
                    fA.write('        "Print Report" -> "Admin Logout" -> endAdmin;  \n')
            else:
                if feature_checklist[feature_index["custom report"]]=="custom report":
                    fA.write('        "Access Admin Account" -> "Customized Report" -> "Print Report" -> "Admin Logout" -> endAdmin;  \n')
                elif feature_checklist[feature_index["staff analytics"]]=="staff analytics":
                    fA.write('        "Access Admin Account" -> "Staff Analytics" -> "Print Report" -> "Admin Logout" -> endAdmin;  \n')
                elif feature_checklist[feature_index["sales analytics"]]=="sales analytics":
                    fA.write('        "Access Admin Account" -> "Sales Analytics" -> "Print Report" -> "Admin Logout" -> endAdmin;  \n')
                elif feature_checklist[feature_index["employee profile"]]=="employee profile":
                    fA.write('        "Access Admin Account" -> "Create Employee Profile" -> "Admin Logout" -> endAdmin;  \n')
                elif cust_len!=0:
                    fA.write('        "Access Admin Account" -> '+cust_list[0]+';  \n')
                    ws=''
                    if cust_len>1:
                        for i in range(0,cust_len):
                            if i!=0:
                                ws=ws+' -> '
                            ws=ws+cust_list[i]
                        fA.write('        '+ws+';  \n')
                    fA.write('        '+cust_list[cust_len-1]+' -> "Print Report" -> "Admin Logout" -> endAdmin;  \n')
                else:
                    fA.write('        "Access Admin Account" -> "Admin Logout" -> endAdmin;')
        elif or1Score>1:
            fA.write('        startAdmin -> or1;  \n')
            if feature_checklist[feature_index["custom report"]]=="custom report":
                fA.write('        or1 -> "Customized Report";  \n')
                if or2Score>1:
                    fA.write('        "Customized Report" -> or2;  \n')
                else:
                    fA.write('        "Customized Report" -> "Print Report";  \n')
            if feature_checklist[feature_index["staff analytics"]]=="staff analytics":
                fA.write('        or1 -> "Staff Analytics";  \n')
                if or2Score>1:
                    fA.write('        "Staff Analytics" -> or2;  \n')
                else:
                    fA.write('        "Staff Analytics" -> "Print Report";  \n')
            if feature_checklist[feature_index["sales analytics"]]=="sales analytics":
                fA.write('        or1 -> "Sales Analytics";  \n')
                if or2Score>1:
                    fA.write('        "Sales Analytics" -> or2;  \n')
                else:
                    fA.write('        "Sales Analytics" -> "Print Report";  \n')
            if feature_checklist[feature_index["employee profile"]]=="employee profile":
                fA.write('        or1 -> "Create Employee Profile";  \n')
                if or3Score>1:
                    fA.write('        "Create Employee Profile" -> or3;  \n')
            if cust_len!=0:
                fA.write('        or1 -> '+cust_list[0]+';  \n')
                ws=''
                if cust_len>1:
                    for i in range(0,cust_len):
                        if i!=0:
                            ws=ws+' -> '
                        ws=ws+cust_list[i]
                    fA.write('        '+ws+';  \n')
                if or2Score>1:
                    fA.write('        '+cust_list[cust_len-1]+' -> or2;  \n')
                else:
                    fA.write('        '+cust_list[cust_len-1]+' -> "Print Report";  \n')
            if or2Score>1:
                fA.write('        or2 -> "Print Report";  \n')
            if or3Score>1:
                fA.write('        "Print Report" -> or3;  \n')
                fA.write('        or3 -> endAdmin;  \n')
            else:
                fA.write('        "Print Report" -> endAdmin;  \n')

        else:
            if feature_checklist[feature_index["custom report"]]=="custom report":
                fA.write('        startAdmin -> "Customized Report" -> "Print Report" -> endAdmin;  \n')
            elif feature_checklist[feature_index["staff analytics"]]=="staff analytics":
                fA.write('        startAdmin -> "Staff Analytics" -> "Print Report" -> endAdmin;  \n')
            elif feature_checklist[feature_index["sales analytics"]]=="sales analytics":
                fA.write('        startAdmin -> "Sales Analytics" -> "Print Report" -> endAdmin;  \n')
            elif feature_checklist[feature_index["employee profile"]]=="employee profile":
                fA.write('        startAdmin -> "Create Employee Profile" -> endAdmin;  \n')
            elif cust_len!=0:
                fA.write('        startAdmin -> '+cust_list[0]+';  \n')
                ws=''
                if cust_len>1:
                    for i in range(0,cust_len):
                        if i!=0:
                            ws=ws+' -> '
                        ws=ws+cust_list[i]
                    fA.write('        '+ws+';  \n')
                fA.write('        '+cust_list[cust_len-1]+' -> "Print Report" -> endAdmin;  \n')
        
        fA.write('}\n')
        fA.close()
    else:
        file_path_admin = os.path.join(module_dir, 'graphGen/adminProcessBPMN.dot')
        fA = open(file_path_admin, "w")
        fA.write("digraph G { \n")
        fA.write('    graph[label="No Admin Process!"];\n')
        fA.write('}\n')
        fA.close()

    if True:
        isOR6=False
        isOR7=False
        if feature_checklist[feature_index["return product"]]=="return product" or feature_checklist[feature_index["stock alert"]]=="stock alert":
            isOR6=True
        if feature_checklist[feature_index["home delivery"]]=="home delivery":
            isOR7=True

        file_path_purchase = os.path.join(module_dir, 'graphGen/purchaseProcessBPMN.dot')
        fP = open(file_path_purchase, "w")
        fP.write("digraph G { \n")
        fP.write('    graph [compound = true, ranksep = .5, color = crimson, bgcolor = white, fontname="Helvetica,Arial,sans-serif", fontsize = 18, labeljust = c, labelloc = t, margin = .9, nodesep = .5, rankdir = LR, ranksep = .25, splines = true]; \n')
        fP.write('	  node [fontname="Helvetica,Arial,sans-serif", shape="Mrecord", fillcolor="#F4F06A", fontcolor=black, style=filled]; \n')
        fP.write('	  edge [fontname="Helvetica,Arial,sans-serif"]; \n')
        fP.write('	  subgraph cluster_0 { \n')
        fP.write('        label = "Customer"; \n')
        fP.write('        startCustomer [shape=circle, label="", color = green, width = 0.3, fillcolor=green, style=filled];\n')
        fP.write('        or4 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ;\n')
        fP.write('        or5 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ;\n')
        fP.write('        "Add Product";\n')
        fP.write('        "Remove Product";\n')
        fP.write('        "Final Cart";\n')
        fP.write('    }\n')

        fP.write('	  subgraph cluster_1 { \n')
        fP.write('        label = "Employee"; \n')
        fP.write('        "Checkout Cart / Enter Order"; \n')
        fP.write('    }\n')

        fP.write('	  subgraph cluster_2 { \n')
        fP.write('        label = "POS System"; \n')
        if isOR6:
            fP.write('        or6 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ;\n')
        if isOR7:
            fP.write('        or7 [shape=diamond,style=filled,label=<<B>X</B>>,height=.1,width=.1,fillcolor=white] ;\n')
        fP.write('        endPOS [shape=circle, label="", color = red, width = 0.3, fillcolor=red, style=filled];\n')

        if feature_checklist[feature_index["scan product"]]=="scan product":
            fP.write('        "Product Scan";\n')
        fP.write('        "Check Inventory List";\n')
        if feature_checklist[feature_index["stock alert"]]=="stock alert":
            fP.write('        "Stock Alert";\n')
        if feature_checklist[feature_index["return product"]]=="return product":
            fP.write('        "Return Product";\n')
        if feature_checklist[feature_index["refund"]]=="refund":
            fP.write('        "Refund";\n')
        
        pur_list=[]
        if feature_checklist[feature_index["customer profile"]]=="customer profile":
            fP.write('        "Customer Profile";\n')
            pur_list.append('"Customer Profile"')
        if feature_checklist[feature_index["personalized offers"]]=="personalized offers":
            fP.write('        "Personalized Offer";\n')
            pur_list.append('"Personalized Offer"')
        if feature_checklist[feature_index["discount offer"]]=="discount offer":
            fP.write('        "Discount Offer";\n')
            pur_list.append('"Discount Offer"')
        if feature_checklist[feature_index["taxes"]]=="taxes":
            fP.write('        "VAT and Taxes";\n')
            pur_list.append('"VAT and Taxes"')
        fP.write('        "Billing";\n')
        pur_list.append('"Billing"')
        fP.write('        "Payment Method";\n')
        pur_list.append('"Payment Method"')
        fP.write('        "Print Receipt";\n')
        pur_list.append('"Print Receipt"')
        pur_len=len(pur_list)

        if feature_checklist[feature_index["home delivery"]]=="home delivery":
            fP.write('        "Home Delivery";\n')

        fP.write('    }\n')

        fP.write('    startCustomer -> or4;\n')
        fP.write('    or4 -> "Add Product" -> or5;\n')
        fP.write('    or4 -> "Remove Product" -> or5;\n')
        fP.write('    or5 -> "Final Cart";\n')
        fP.write('    "Final Cart" -> "Checkout Cart / Enter Order";\n')
        if feature_checklist[feature_index["scan product"]]=="scan product":
            fP.write('    "Checkout Cart / Enter Order" -> "Product Scan" -> "Check Inventory List";\n')
        else:
            fP.write('    "Checkout Cart / Enter Order" -> "Check Inventory List";\n')
        if isOR6:
            fP.write('    "Check Inventory List" -> or6;\n')
            fP.write('    or6 ->'+pur_list[0]+';\n')
            ws=''
            for i in range(0,pur_len):
                if i!=0:
                    ws=ws+' -> '
                ws=ws+pur_list[i]
            fP.write('    '+ws+';\n')
            if feature_checklist[feature_index["return product"]]=="return product":
                fP.write('    or6 -> "Return Product";\n')
                if feature_checklist[feature_index["refund"]]=="refund":
                    fP.write('    "Return Product" -> "Refund" -> endPOS;\n')
                else:
                    fP.write('    "Return Product" -> endPOS;\n')
            if feature_checklist[feature_index["stock alert"]]=="stock alert":
                fP.write('    or6 -> "Stock Alert" -> endPOS;\n')
        else:
            fP.write('    "Check Inventory List" ->'+pur_list[0]+';\n')
            ws=''
            for i in range(0,pur_len):
                if i!=0:
                    ws=ws+' -> '
                ws=ws+pur_list[i]
            fP.write('    '+ws+';\n')
        if isOR7:
            fP.write('    '+pur_list[pur_len-1]+' -> or7 -> endPOS;\n')
            fP.write('    or7 -> "Home Delivery" -> endPOS;\n')
        else:
            fP.write('    '+pur_list[pur_len-1]+' -> endPOS;\n')
        
        fP.write('}\n')
        fP.close()

    if True:
        orScore=1
        
        if feature_checklist[feature_index["employee permission"]]=="employee permission":
            orScore+=1
        if feature_checklist[feature_index["employee timesheets"]]=="employee timesheets":
            orScore+=1
        if feature_checklist[feature_index["employee wages"]]=="employee wages":
            orScore+=1
        if feature_checklist[feature_index["daily sales report"]]=="daily sales report":
            orScore+=1
        
        file_path_employee = os.path.join(module_dir, 'graphGen/empProcessBPMN.dot')
        fE = open(file_path_employee, "w")
        fE.write("digraph G { \n")
        fE.write('  graph [compound = true, ranksep = .5,color = crimson, bgcolor = white, fontname="Helvetica,Arial,sans-serif", fontsize = 18, labeljust = c, labelloc = t, margin = .9, nodesep = .5, rankdir = LR, ranksep = .25, splines = true];\n')
        fE.write('  node [fontname="Helvetica,Arial,sans-serif", shape="Mrecord", fillcolor="#F4F06A", fontcolor=black, style=filled];\n')
        fE.write('	edge [fontname="Helvetica,Arial,sans-serif"];\n')
        fE.write('	subgraph cluster_0 {  \n')
        fE.write('        label = "Employee"; \n')
        fE.write('        startEmployee [shape=circle, label="", color = green, width = 0.3, fillcolor=green, style=filled];\n')
        fE.write('        endEmployee [shape=circle, label="", color = red, width = 0.3, fillcolor=red, style=filled];\n')

        if orScore>1:
            fE.write('        or8 [shape=diamond,style=filled,label=<<B>O</B>>,height=.1,width=.1,fillcolor=white] ;\n')
            fE.write('        or9 [shape=diamond,style=filled,label=<<B>O</B>>,height=.1,width=.1,fillcolor=white] ;\n')
        
        fE.write('        "Employee Login"; \n')
        if feature_checklist[feature_index["employee profile"]]=="employee profile":
            fE.write('        "Employee Profile"; \n')
        
        emp_list=[]
        if feature_checklist[feature_index["employee permission"]]=="employee permission":
            fE.write('        "Employee Performance"; \n')
            emp_list.append('"Employee Performance"')
        if feature_checklist[feature_index["daily sales report"]]=="daily sales report":
            fE.write('        "Daily Sales Report"; \n')
            emp_list.append('"Daily Sales Report"')
        fE.write('        "Order Entries"; \n')
        emp_list.append('"Order Entries"')
        if feature_checklist[feature_index["employee timesheets"]]=="employee timesheets":
            fE.write('        "Employee Timesheet"; \n')
            emp_list.append('"Employee Timesheet"')
        if feature_checklist[feature_index["employee wages"]]=="employee wages":
            fE.write('        "Employee Salary Report"; \n')
            emp_list.append('"Employee Salary Report"')
        fE.write('        "Employee Logout"; \n')

        fE.write('    }\n')

        if feature_checklist[feature_index["employee profile"]]=="employee profile":
            fE.write('    startEmployee -> "Employee Login" -> "Employee Profile";\n')
            if orScore>1:
                fE.write('    "Employee Profile" -> or8;\n')
            else:
                fE.write('    "Employee Profile" -> "Order Entries" -> "Employee Logout" -> endEmployee;\n')
        else:
            if orScore>1:
                fE.write('    startEmployee -> "Employee Login" -> or8;\n')
            else:
                fE.write('    startEmployee -> "Employee Login" -> "Order Entries" -> "Employee Logout" -> endEmployee;\n')
        if orScore>1:
            for it in emp_list:
                fE.write('    or8 -> '+it+' -> or9;\n')
            fE.write('    or9 -> "Employee Logout" -> endEmployee;\n')
        
        fE.write('}\n')
        fE.close()

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    graphsA = pydot.graph_from_dot_file(file_path_admin)
    graph = graphsA[0]
    graph.write_svg(f'{BASE_DIR}\\static\\images\\outputAdminBPMN.svg')
 

    graphsP = pydot.graph_from_dot_file(file_path_purchase)
    graph = graphsP[0]
    graph.write_svg(f'{BASE_DIR}\\static\\images\\outputPurchaseBPMN.svg')


    graphsE = pydot.graph_from_dot_file(file_path_employee)
    graph = graphsE[0]
    graph.write_svg(f'{BASE_DIR}\\static\\images\\outputEmpBPMN.svg')




    









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
        f.write('   POS -> "Central Database" [arrowhead="odot"];\n')
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

    to_be_added=[]
    if feature_checklist[feature_index["staff login"]]!="staff login" and feature_checklist[feature_index["staff logout"]]!="staff logout":
        f.write('   "Employee Authentication System" [color=red,fontcolor=red];\n')
        f.write('   POS -> "Employee Authentication System" [color=red];\n')
    if feature_checklist[feature_index["staff login"]]!="staff login":
        to_be_added.append("staff login")
        f.write('   "Employee Login" [color=red,fontcolor=red];\n')
        f.write('       "Employee Authentication System" -> "Employee Login" [color=red];\n')
    if feature_checklist[feature_index["staff logout"]]!="staff logout":
        to_be_added.append("staff logout")
        f.write('   "Employee Logout" [color=red,fontcolor=red];\n')
        f.write('       "Employee Authentication System" -> "Employee Logout" [color=red];\n')
    if feature_checklist[feature_index["inventory list"]]!="inventory list":
        to_be_added.append("inventory list")
        f.write('   "Inventory List" [color=red,fontcolor=red];\n')
        f.write('   POS -> "Inventory List" [color=red];\n')
    if feature_checklist[feature_index["payment"]]!="payment" and feature_checklist[feature_index["order product"]]!="order product" and feature_checklist[feature_index["print receipt"]]!="print receipt" and feature_checklist[feature_index["scan product"]]!="scan product" and feature_checklist[feature_index["items cart"]]!="items cart":
        f.write('   "Product Purchase System" [color=red,fontcolor=red];\n')
        f.write('   POS -> "Product Purchase System" [color=red];\n')
    if feature_checklist[feature_index["payment"]]!="payment":
        to_be_added.append("payment")
        f.write('   "Payment System" [color=red,fontcolor=red];\n')
        f.write('   "Product Purchase System" -> "Payment System" [color=red];\n')
    if feature_checklist[feature_index["order product"]]!="order product":
        to_be_added.append("order product")
        f.write('   "Order Entry" [color=red,fontcolor=red];\n')
        f.write('   "Product Purchase System" -> "Order Entry" [color=red];\n')
    if feature_checklist[feature_index["print receipt"]]!="print receipt":
        to_be_added.append("print receipt")
        f.write('   "Receipt Generation" [color=red,fontcolor=red];\n')
        f.write('   "Product Purchase System" -> "Receipt Generation" [color=red];\n')
    if feature_checklist[feature_index["items cart"]]!="items cart":
        to_be_added.append("items cart")
        f.write('   "Cart System" [color=red,fontcolor=red];\n')
        f.write('   "Product Purchase System" -> "Cart System" [color=red];\n')
    if feature_checklist[feature_index["add cart"]]!="add cart":
        to_be_added.append("add cart")
        f.write('       "Cart Append" [color=red,fontcolor=red];\n')
        f.write('       "Cart System" -> "Cart Append" [color=red];\n')
    if feature_checklist[feature_index["remove cart"]]!="remove cart":
        to_be_added.append("remove cart")
        f.write('       "Cart Remove" [color=red,fontcolor=red];\n')
        f.write('       "Cart System" -> "Cart Remove" [color=red];\n')
    if feature_checklist[feature_index["confirm cart"]]!="confirm cart":
        to_be_added.append("confirm cart")
        f.write('       "Cart Confirmation" [color=red,fontcolor=red];\n')
        f.write('       "Cart System" -> "Cart Confirmation" [color=red];\n')
    if feature_checklist[feature_index["billing"]]!="billing":
        to_be_added.append("billing")
        f.write('   "Billing Management" [color=red,fontcolor=red];\n')
        f.write('   POS -> "Billing Management" [color=red];\n')

    f.write('}')    
    f.close()



    f = open(file_path, "r")
    print(f.read())
    graphs = pydot.graph_from_dot_file(file_path)
    graph = graphs[0]
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    graph.write_svg(f'{BASE_DIR}\\static\\images\\outputGraph.svg')
    return to_be_added




def keywordExtractorFunc(request):

    file_path = os.path.join(module_dir, 'jsons/stopwords.json')
    with open(file_path, 'rb') as fp:
        stop_words = json.load(fp)
    fp.close()

    # print(stop_words)

    text=request.POST.get('userText')
    showText = text
    if text.strip() == "":
        return render(request,'landingPage.html',{"error":"Please enter some text to extract keywords from."})

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
    if len(extracted_features)==0:
        return render(request,'landingPage.html',{"error":"Please write some meaningful POS keywords to get the diagrams."})
    print("These are the extracted features form the form")
    print(extracted_features)
    toBeaddedList=graphMaker(feature_checklist,feature_index)
    
    totalFeature=[]
    totalFeature.extend(extracted_features)
    totalFeature.extend(required)
    totalFeature.extend(toBeaddedList)
    
    # print(totalFeature," ", type(totalFeature) )
    bpmnMaker(feature_index,totalFeature)
    context={'features':extracted_features,'dependent_features':required,'mandatory_features':toBeaddedList, 'generated':True, 'userText':showText}
    return render(request,'landingPage.html',context)
  

  