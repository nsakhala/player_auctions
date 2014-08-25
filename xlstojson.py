import xlrd
from collections import OrderedDict
import simplejson as json
 
# Open the workbook and select the first worksheet
workbookRead = xlrd.open_workbook('player_data.xls')
sheetRead = workbookRead.sheet_by_index(0)

# List to hold dictionaries
players_list = []
pk=0
 
# Iterate through each row in worksheet and fetch values into dict
for rownum in range(1, sheetRead.nrows):
    players = OrderedDict()
    row_values = sheetRead.row_values(rownum)
    if row_values[3]:
        pk+=1
        players['pk'] = pk
        players['model'] = "rn.player"
        tempDict = {}
        tempDict['pName'] = row_values[3]
    	tempDict['pCountry'] = row_values[4]
        
        if row_values[5]:
            tempDict['pAge'] = row_values[5]
        else:
            tempDict['pAge'] = 0
        
        if row_values[7]:
            tempDict['pMatches'] = row_values[7]
        else:
            tempDict['pMatches'] = 0
        
        if row_values[10]:
            tempDict['pBaseprice'] = row_values[10]
        else:
            tempDict['pBaseprice'] = 0
        
        
        tempDict['pExpertise'] = row_values[6]
        tempDict['pStatus'] = "Unsold"
        tempDict['pTeam'] = 'DUM'
        tempDict['pBid'] = 0
        tempDict['pAuctioned'] = 0
        players['fields'] = tempDict
        players_list.append(players)

 
# Serialize the list of dicts to JSON
j = json.dumps(players_list)
 
# Write to file
with open('player_data.json', 'w') as f:
    f.write(j)
