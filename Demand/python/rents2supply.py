import os,sys,csv

def importRents(combined_rent,old_supply_input,new_supply_input):
    rentDict = {}
    with open(combined_rent, "r") as rentFile:
        rentReader = csv.DictReader(rentFile)
        for rentRow in rentReader:
            vi = (rentRow['Realestate'],rentRow['Zone'])
            rentDict[vi] = float(rentRow['Value'])
    oldFile = open(old_supply_input, "r")
    oldReader = csv.DictReader(oldFile)
    newFile = open(new_supply_input, "w")
    newWriter = csv.DictWriter(newFile, fieldnames=oldReader.fieldnames)
    newWriter.writeheader()
    for oldRow in oldReader:
        mgra = oldRow['MGRA']
        newRow = oldRow
        newRow['Price_SF'] = rentDict[('1',mgra)]
        newRow['Price_MF'] = rentDict[('2',mgra)]
        newRow['Ind_Cost'] = rentDict[('4',mgra)]
        newRow['Ofc_Cost'] = rentDict[('6',mgra)]
        newRow['Ret_Cost'] = rentDict[('5',mgra)]
        newWriter.writerow(newRow)
    newFile.close()
    oldFile.close()

if __name__ == "__main__":
    combined_rent = sys.argv[1]
    old_supply_input = sys.argv[2]
    new_supply_input = sys.argv[3]
    importRents(combined_rent,old_supply_input,new_supply_input)
