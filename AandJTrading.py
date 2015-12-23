from PyQt4 import QtGui, QtCore

import time
import os
import sys
import datetime
import ebaysdk

from ebaysdk.utils import getNodeText
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading

#TODO: AandJ.dat preset
path_Pictures = 'C:\\Projects\\AandJ\\Pictures'

'''
###########################################################
##  New Listing
###########################################################
'''

def getCat(cp, sid, llim):
    try:
        ## Sandbox
        api = Trading(domain='api.sandbox.ebay.com', config_file="ebay.yaml",
                      warnings=True, timeout=20)
        ## Production
        #api = Trading(config_file="ebay.yaml", warnings=True, timeout=20)

        callData = {
            'DetailLevel': 'ReturnAll',
            'CategoryParent': cp,
            'CategorySiteID': sid,
            'LevelLimit': llim,
            'OutputSelector': [
                'CategoryArray.Category.CategoryID',
                'CategoryArray.Category.CategoryName']
            }

        api.execute('GetCategories', callData)
        reply = "%s" % api.response.content
        getList = []

        while(reply.find('<CategoryID>') != -1):
            idx = reply.find('<CategoryID>')
            reply = reply[idx+12:]
            idx = reply.find('</CategoryID>')
            i = reply[:idx]
            idx = reply.find('<CategoryName>')
            reply = reply[idx+14:]
            idx = reply.find('</CategoryName>')
            j = reply[:idx]
            if (j.find('&amp;') != -1):
                j = j.replace('&amp;','&')
            if (i != str(cp)):
                getList.append([i,j])
        
        return getList
    
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def AddListing(p):
    print(str(p.CategoryValue))
    #PURL = UploadPhotos(p)
    PURL = ["http://i.ebayimg.com/00/s/NDgwWDY0MA==/z/HDcAAOSwNSxVSSBa/$_12.JPG?set_id=880000500F","http://i.ebayimg.com/00/s/NDgwWDY0MA==/z/HDcAAOSwNSxVSSBa/$_12.JPG"]
    Description = MakeDescription(p, PURL[0])
    
    Title = (p.PartNumber_ledit.text() + " " +
             p.Description_ledit.text() + ", " +
             p.Model_ledit.text())
    
    FreeShip = 'false'
    if (p.FShip_chbox.isChecked()):
        FreeShip = 'true'
        
    ShipService = []
    if (p.Ship1_chbox.isChecked()):
        ShipService.append('USPSPriority')
    if (p.Ship2_chbox.isChecked()):
        ShipService.append('UPSGround')
    if (p.Ship3_chbox.isChecked()):
        ShipService.append('USPSPriorityMailLargeFlatRateBox')

    '''PicURL = []
    for url in PURL:
        PicURL.append({"PictureDetails": {"PictureURL": url}})'''
    #############
    #TODO: AandJ.dat preset
    PayPal = "aandjproparts@gmail.com"
    ZipCode = "95828"
    #############
    try:
        ## Sandbox
        api = Trading(domain='api.sandbox.ebay.com', config_file="ebay.yaml",
                      warnings=False)
        ## Production
        #api = Trading(config_file="ebay.yaml", warnings=False)

        myitem = {
            "Item": {
                "Title": Title,
                "Description": Description,
                "PrimaryCategory": {"CategoryID": str(p.CategoryValue)},
                "StartPrice": str(p.Price_sbox.value()),
                "CategoryMappingAllowed": "true",
                "Country": "US",
                #"ConditionID": "3000",#TODO: Do Condition ID GetCategoryFeatures
                #"ConditionDescription": p.CondDetail_tedit.toPlainText(),
                "Currency": "USD",
                "DispatchTimeMax": "1",
                "ListingDuration": "GTC", #TODO: Do Listing Duration GetCategoryFeatures
                "ListingType": "FixedPriceItem",
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": PayPal,
                "PictureDetails": {"PictureURL": PURL},
                "PostalCode": ZipCode,
                "Quantity": str(p.Quantity_sbox.value()),
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "Description": "14 days money back, you pay return shipping",
                    "ReturnsWithinOption": "Days_14",
                    "ShippingCostPaidByOption": "Buyer" },
                "ShippingDetails": {
                    "ShippingType": "Calculated",
                    "PaymentInstructions": "1 business days of handling time, usually shipped next day. Make sure your address is correct, especially when shipping to foreign countries.",
                    "ShippingServiceOptions": {
                        "FreeShipping": FreeShip,
                        "ShippingService": ShipService
                        },
                    "CalculatedShippingRate": {"OriginatingPostalCode": ZipCode} },
                "ShippingPackageDetails": {
                    "MeasurementUnit": "English",
                    "WeightMajor": str(p.WeightLbs_sbox.value()),
                    "WeightMinor": str(p.WeightOz_sbox.value()),
                    "PackageDepth": str(p.DimensionH_sbox.value()),
                    "PackageLength": str(p.DimensionL_sbox.value()),
                    "PackageWidth": str(p.DimensionW_sbox.value()),
                    "ShippingPackage": "PackageThickEnvelope"},
                "ShipToLocations": "Worldwide",
                "Site": "eBayMotors",
                "SKU": p.ItemID_ledit.text() } }
        IntShip = []
        boolint = False
        if(p.IntShip1_chbox.isChecked()):
            IntShip.append('USPSPriorityMailInternational')
            boolint = True
        if(p.IntShip2_chbox.isChecked()):
            IntShip.append('USPSPriorityMailInternationalLargeFlatRateBox')
            boolint = True
        if(boolint):
            myitem['Item']['ShippingDetails']['ShippingServiceOptions']['InternationalShippingServiceOption'] = IntShip
        if(p.BestOffer_chbox.isChecked()):
            myitem['Item']['BestOfferDetails'] = {'BestOfferEnabled': 'true'}

        #print(myitem)
        api.execute('VerifyAddItem', myitem)
        print("%s" % api.response.content)
                    
    except ConnectionError as e:
        for node in api.response.dom().findall('ErrorCode'):
            print("error code: %s" % node.text)
        if 37 in api.response_codes():
            print("Invalid data in request")
        print(e)
        print(e.response.dict())

def MakeDescription(p, s):
    template = open('template.txt', 'r')
    #newlist = open('newlist.txt', 'w')
    newlist = "<![CDATA[\n"
    for templine in template:
        if (templine.find('ENTER_') != -1):
            templine = templine.replace('ENTER_DESCRIPTION',p.Description_ledit.text())
            templine = templine.replace('ENTER_MODEL',p.Model_ledit.text())
            templine = templine.replace('ENTER_PART_NUMBER',p.PartNumber_ledit.text())
            templine = templine.replace('ENTER_ITEM_NUMBER',p.ItemID_ledit.text())
            templine = templine.replace('ENTER_CONDITION_DESCRIPTION',p.CondDetail_tedit.toPlainText())
            templine = templine.replace('ENTER_HEIGHT',str(p.DimensionH_sbox.value()))
            ############################
            ##TODO: GET IMAGE SOURCE
            ############################
            #templine = templine.replace('ENTER_IMG_SRC','http://i.ebayimg.com/00/s/NDgwWDY0MA==/z/HDcAAOSwNSxVSSBa/$_12.JPG?set_id=880000500F')
            ############################
            templine = templine.replace('ENTER_IMG_SRC',s)
            templine = templine.replace('ENTER_LBS',str(p.WeightLbs_sbox.value()))
            templine = templine.replace('ENTER_LENGTH',str(p.DimensionL_sbox.value()))
            templine = templine.replace('ENTER_LOCATION',p.Location_ledit.text())
            templine = templine.replace('ENTER_OZ',str(p.WeightOz_sbox.value()))
            templine = templine.replace('ENTER_WIDTH',str(p.DimensionW_sbox.value()))
        newlist = newlist + templine
    template.close()
    newlist = newlist + "]]>"
    return newlist
    #newlist.close()
    
def UploadPhotos(p):
    ## Sandbox
    api = Trading(domain='api.sandbox.ebay.com', config_file="ebay.yaml",
                  warnings=True)
    ## Production
    #api = Trading(config_file="ebay.yaml", warnings=True)
    PicURL = []
    if (len(p.Picture_lw.selectedItems()) == 0):
        1 + 1
    else:
        for photo in p.Picture_lw.selectedItems():
            filepath = path_Pictures + '\\' + photo.text()
            try:
                files = {'file': ('EbayImage', open(filepath, 'rb'))}
                pictureData = {
                    "WarningLevel": "High",
                    "PictureName": photo.text()
                }

                api.execute('UploadSiteHostedPictures', pictureData, files=files)

                reply = "%s" % api.response.content

                if(reply.find('<FullURL>') != -1):
                    idx = reply.find('<FullURL>')
                    reply = reply[idx+9:]
                    idx = reply.find('</FullURL>')
                    i = reply[:idx]
                    PicURL.append(i)
                    print(PicURL)
                    
            except ConnectionError as e:
                print(e)
                print(e.response.dict())
                
        return PicURL

def CatFeatures(p):
    try:
        ## Sandbox
        api = Trading(domain='api.sandbox.ebay.com', config_file="ebay.yaml",
                      warnings=True)
        ## Production
        #api = Trading(config_file="ebay.yaml", warnings=True)

        callData = {
            "CategoryID": p.CategoryValue,
            "DetailLevel": "ReturnAll",
            "FeatureID": ["ConditionEnabled",
                          "ConditionValues",
                          "ListingDurations",
                          "BestOfferEnabled"]
            }

        api.execute('GetCategoryFeatures', callData)

        reply = "%s" % api.response.content
        print(reply)
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

'''
###########################################################
##  Update Inventory
###########################################################
'''

def UpdateInventory(p):
    try:
        ## Sandbox
        #api = Trading(domain='api.sandbox.ebay.com', config_file="ebay.yaml",
        #              warnings=True)
        ## Production
        api = Trading(config_file="ebay.yaml", warnings=True)

        callData = { "ActiveList":
                {
                    "Include": "true",
                    "Sort": "TimeLeft"
                }
            }

        api.execute('GetMyeBaySelling', callData)
        reply = "%s" % api.response.content
        ret = {}
        ItemID = []
        StartTime = []
        ListDuration = []
        BuyPrice = []
        TimeLeft = []
        Title = []
        Quantity = []
        add = False

        while(reply.find('<Item>') != -1):
            add = True

            idx = reply.find('<ItemID>')
            reply = reply[idx+8:]
            idx = reply.find('</ItemID>')
            i = reply[:idx]
            ItemID.append(i)
            
            idx = reply.find('<StartTime>')
            reply = reply[idx+11:]
            idx = reply.find('</StartTime>')
            i = reply[:idx]
            year = i[2:4]
            if(i[5:7] == '01'):
                mon = "Jan"
            elif(i[5:7] == '02'):
                mon = "Feb"
            elif(i[5:7] == '03'):
                mon = "Mar"
            elif(i[5:7] == '04'):
                mon = "Apr"
            elif(i[5:7] == '05'):
                mon = "May"
            elif(i[5:7] == '06'):
                mon = "Jun"
            elif(i[5:7] == '07'):
                mon = "Jul"
            elif(i[5:7] == '08'):
                mon = "Aug"
            elif(i[5:7] == '09'):
                mon = "Sep"
            elif(i[5:7] == '10'):
                mon = "Oct"
            elif(i[5:7] == '11'):
                mon = "Nov"
            elif(i[5:7] == '12'):
                mon = "Dec"
            day = i[8:10]
            StartTime.append(mon+'-'+day+'-'+year)
            
            idx = reply.find('<ListingDuration>')
            reply = reply[idx+17:]
            idx = reply.find('</ListingDuration>')
            i = reply[:idx]
            if (i.find('Days_') != -1):
                i = i[5:] + " Days"
            elif (i.find('GTC') != -1):
                i = "Forever"
            ListDuration.append(i)

            idx = reply.find('<CurrentPrice currencyID="USD">')
            reply = reply[idx+31:]
            idx = reply.find('</CurrentPrice>')
            i = reply[:idx]
            BuyPrice.append("$%.2f" % float(i))

            idx = reply.find('<TimeLeft>')
            reply = reply[idx+10:]
            idx = reply.find('</TimeLeft>')
            i = reply[:idx]
            nohour = False
            nominute = False
            if (i.find('D') != -1):
                day = i[i.find('P')+1:i.find('D')] + "d "
            else:
                day = "0d "
            if (i.find('H') != -1):
                hour = i[i.find('T')+1:i.find('H')] + "h "
            else:
                hour = "0h "
                nohour = True
            if (i.find('M') != -1):
                if(not nohour):
                    minute = i[i.find('H')+1:i.find('M')] + "m "
                else:
                    minute = i[i.find('T')+1:i.find('M')] + "m "
            else:
                minute = "0m "
                nominute = True
            if (i.find('S') != -1):
                if(not nominute):
                    second = i[i.find('M')+1:i.find('S')] + "s"
                else:
                    if(not nohour):
                        second = i[i.find('H')+1:i.find('S')] + "s"
                    else:
                        second = i[i.find('T')+1:i.find('S')] + "s"
            else:
                second = "0s"
            TimeLeft.append(day + hour + minute + second)

            idx = reply.find('<Title>')
            reply = reply[idx+7:]
            idx = reply.find('</Title>')
            i = reply[:idx]
            if (i.find('&amp;') != -1):
                i = i.replace('&amp;','&')
            if (i.find('&quot;') != -1):
                i = i.replace('&quot;','"')
            Title.append(i)

            idx = reply.find('<QuantityAvailable>')
            reply = reply[idx+19:]
            idx = reply.find('</QuantityAvailable>')
            i = reply[:idx]
            Quantity.append(i)

        if(add):
            ret = {"Title": Title,
                   "Price": BuyPrice,
                   "Quantity": Quantity,
                   "TimeStarted": StartTime,
                   "TimeLeft": TimeLeft,
                   "ListDuration": ListDuration,
                   "ItemID": ItemID}
                    
        return ret
        
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def getItemDetails(ID):
    try:
        ## Sandbox
        #api = Trading(domain='api.sandbox.ebay.com', config_file="ebay.yaml",
        #              warnings=True)
        ## Production
        api = Trading(config_file="ebay.yaml", warnings=True)

        callData = {
            "ItemID": str(ID),
            "OutputSelector":
                ["Item.ListingDetails.EndTime",
                 "Item.PictureDetails.PictureURL",
                 "Item.Description"]
            }

        api.execute('GetItem', callData)
        reply = "%s" % api.response.content
        
        idx = reply.find('<EndTime>')
        reply = reply[idx+9:]
        idx = reply.find('</EndTime>')
        i = reply[:idx]
        year = i[2:4]
        if(i[5:7] == '01'):
            mon = "Jan"
        elif(i[5:7] == '02'):
            mon = "Feb"
        elif(i[5:7] == '03'):
            mon = "Mar"
        elif(i[5:7] == '04'):
            mon = "Apr"
        elif(i[5:7] == '05'):
            mon = "May"
        elif(i[5:7] == '06'):
            mon = "Jun"
        elif(i[5:7] == '07'):
            mon = "Jul"
        elif(i[5:7] == '08'):
            mon = "Aug"
        elif(i[5:7] == '09'):
            mon = "Sep"
        elif(i[5:7] == '10'):
            mon = "Oct"
        elif(i[5:7] == '11'):
            mon = "Nov"
        elif(i[5:7] == '12'):
            mon = "Dec"
        day = i[8:10]
        end = mon+'-'+day+'-'+year

        idx = reply.find('<PictureURL>')
        reply = reply[idx+12:]
        idx = reply.find('</PictureURL>')
        i = reply[:idx]

        ret = [end, i]

        print(ret)
        return ret
    
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
