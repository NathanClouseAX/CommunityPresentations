import csv
from datetime import date

# written by nathan clouse - sorry

entities = [['Products', 'Products V2'], 
['Released products', 'Released products V2'], 
['External item descriptions for vendors', 'External item descriptions for vendors V2'], 
['Item coverage groups', 'Item coverage groups'], 
['Released product warehouse defaults', 'Released product warehouse defaults V2'], 
['Product category hierarchies', 'Product category hierarchies'], 
['Product categories', 'Product categories'], 
['Bill of materials headers and versions', 'Bill of materials headers and versions V3'], 
['Bill of materials lines', 'Bill of materials lines V3'], 
['Route Headers', 'Route Headers'], 
['Route operations', 'Route operations V2'], 
['Route operation properties', 'Route operation properties V2'], 
['Route versions', 'Route versions V2'], 
['Pending item prices', 'Pending item prices V2'], 
['Trade agreement journal table V2', 'Trade agreement journal table V2'], 
['Released product document attachments', 'Released product document attachments'], 
['Customers', 'Customers V3'], 
['Customer postal addresses', 'Customer postal addresses'], 
['Customer Contact Persons', 'Customer Contact Persons'], 
['Customer attachments', 'Customer V2 attachments'], 
['Vendors', 'Vendors V3'], 
['Vendor postal addresses', 'Vendor postal addresses'], 
['Vendor Contact Persons', 'Vendor Contact Persons'], 
['Vendor document attachments', 'Vendor document attachments'], 
['Main Accounts', 'Main Account'], 
['Chart of Accounts', 'Chart of Accounts'], 
['Worker', 'Worker'], 
['Positions', 'Positions V2'], 
['Opening GL Balances', 'Opening GL Balances (General journal)'], 
['Inventory balances - Header', 'Inventory adjustment headers'], 
['Inventory balances - Line', 'Inventory adjustment journal headers and lines V2'], 
['General journal account entry (Open AR)', 'General journal account entry'], 
['Item batches', 'Item batches'], 
['Default Order Settings', 'Default Order Settings'], 
['Bar codes', 'Bar codes'], 
['Physical dimension groups', 'Physical dimension groups'], 
['Approved vendor list by products', 'Approved vendor list by products'], 
['General journal account entry (Open AP)', 'General journal account entry'], 
['Sales order headers ', 'Sales order headers V2'], 
['Sales Order Lines', 'Sales Order Lines V2'], 
['Purchase Order Headers', 'Purchase Order Headers V2'], 
['Purchase Order Lines', 'Purchase Order Lines V2'], 
['Fixed assets', 'Fixed assets V2 entity'], 
['Fixed asset book', 'Fixed asset book V2'], 
['Fixed asset journal  (ACQ)', 'Fixed asset journal V2 entity (ACQ)'], 
['Fixed asset journal (DEPR)', 'Fixed asset journal V2 entity (DEPR)'], 
['Asset management asset management plans', 'Asset management asset management plans'], 
['Purchase agreements', 'Purchase agreements V2'], 
['Purchase agreement lines', 'Purchase agreement lines V2'], 
['Sales agreement headers', 'Sales agreement headers'], 
['Sales agreement lines', 'Sales agreement lines']
           ]



passes = [
          ['Pass 1', date(2023, 5,6)],
          ['Pass 2', date(2023, 6,14)],
          ['UAT', date(2023, 7,15)],
          ['Mock go-live', date(2023, 8,1)],
          ['Go Live', date(2023, 9,13)],
         ]



prework_tasks = [['Data Cleanup', date(2023, 2,6) ]]

initial_tasks = []

run_tasks = [['Groundwork', 1, ''],
             ['Mapping', 2, ''],
             ['Extraction', 3, ''],
             ['Source File Validation', 4, ''],
             ['Import & Check', 5, ''],
             ['Review & Test', 6, '']]

legal_entities = ['03']

crossCompanyEntities = ['Products', 'Vendor master', 'Vendor addresses', 'Vendor contacts', 'Vendor document handling',
                        'Chart of Accounts', 'Workers', 'Positions']

suffix = ''

with open('c:\\temp\\out.csv','w', newline='') as out:
    csv = csv.writer(out,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL );

    row = [ 'Work Item Type', 
            'Title 1', 
            'Title 2', 
            'Title 3', 
            'Assigned To', 
            'State', 
            'Tags', 
            'Legal Entity',
            'Client Owner',
            'Migration Step',
            'Migration Pass',
            'Area Path', 
            'Data Load Method', 
            'Iteration Path', 
            'Reason', 
            'Effort', 
            'Required Date',
            'Stack Rank']

    csv.writerow(row)

    entityStackRank = 0
    milestoneStackRank = 0
    activityStackRank = 0
    
    for entity, tag in entities:
        suffix = entity
        entityStackRank = entityStackRank + 1
        milestoneStackRank = 0
        if tag == '' : tag = 'Extension Required'

        row = ['Data Entity', suffix, '','','','New',tag, '', '', '', '','\\Data Migration\\' +  entity,'DIXF','\\Data Migration\\',"","","", entityStackRank]      
        csv.writerow(row);
        
        for task, due_date in prework_tasks:
            row = ['Migration Milestone','', task + ' - ' + suffix, '', '', 'New', '','','', '','','\\Data Migration\\Data Cleanup','','\\Data Migration\\',"","",due_date]
            csv.writerow(row);

        suffix = 'Initial Entity Setup - ' + entity
        for task, due_date in initial_tasks:
            for legal_entity in legal_entities:
                row = ['Migration Activity', '', '', task + ' - ' + suffix + ' - ' + legal_entity, '', '','','','', legal_entity, "0", task[0], '', '\\Data Migration\\' +  entity,'','\\Data Migration\\',"","",due_date]
                csv.writerow(row);

        for pas, due_date in passes:
            milestoneStackRank = milestoneStackRank + 1
            activityStackRank = 0
            i = 1
            suffix = pas + ' - ' + entity

            row = ["Migration Milestone", "", suffix, "","","New", '','','','',milestoneStackRank,'\\Data Migration\\' + entity,'','\\Data Migration\\' + pas,"","",due_date, milestoneStackRank]
            csv.writerow(row);

            for task in run_tasks:
                j = 0
                activityStackRank = activityStackRank + 10
                
                for legal_entity in legal_entities:
                    print = 1
                    j = j + 1
                    #entity that are uploaded once (shared across all companies)
                    if entity in crossCompanyEntities :
                        legal_entity = 'All'
                        if j > 1 : print = 0

                    #Only the Sales legal entity will have customer data
                    #if "Customer" in entity:
                    #    if legal_entity == "Sales":
                    #        print = 1
                    #    else:
                    #        print = 0
                    #else:
                    #    print = print

                    #The sales legal entity should not have Vendor external item descriptions
                    #if entity == "Vendor external item descriptions" and legal_entity == "Sales":
                    #    print = 0
                    #else:
                    #    print = print
                    
                    row = ['Migration Activity', '', '', task[0] + ' - ' + suffix + ' - ' + legal_entity, task[2], 'New', '', legal_entity, '', str(task[1]) + " " + task[0], milestoneStackRank, '\\Data Migration\\' +  entity,'','\\Data Migration\\' + pas,"","",due_date, activityStackRank]

                    if print == 1 : csv.writerow(row);
                    i = i+1
            
        

