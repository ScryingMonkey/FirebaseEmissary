import requests
import json
import unicodedata

#....................

class ConstantContactFetcher:
    
    CUSTOMER_NAME = ""
    CONSTANT_CONTACT_API_BASE = "https://api.constantcontact.com/v2"
    API_KEY = "hnxz4rut2fvrav9fpbnyg3d2"
    CONSTANT_CONTACT_CUSTOMER_TOKEN = ""

    def __init__(self):
        self.CONSTANT_CONTACT_CUSTOMER_TOKEN = "fc6b757b-e12b-460d-828d-67a9cdbbe887"

    def __init__(self, token):
        print "In Fetcher!"
        self.CONSTANT_CONTACT_CUSTOMER_TOKEN = token    

    def getConstantContactCustomerData(self):
        customerData = {}
        ccCustomerInfoTag = "/account/info"
        parameters = {'api_key': self.API_KEY,
                      'access_token': self.CONSTANT_CONTACT_CUSTOMER_TOKEN}
        response = requests.get(self.CONSTANT_CONTACT_API_BASE+ccCustomerInfoTag, params=parameters)
        print "API HTTP Response : ",response.status_code
        customerData = response.json()
        self.CUSTOMER_NAME = customerData['organization_name'].encode('ascii','replace')
        print ">>> getCustomerData...changing CUSTOMER_NAME value to...%s" % customerData['organization_name']
        #print ">>> getCustomerData...returning customerData...%s" % customerData
        return customerData  

    def makeConstantContactCampaignSummaryJSON(self,customerName,campaignTitle, timeSent, totalSent,
                                openRate, openPercent,
                                clickThrough, clickPercent):
        d = {'type':'campaignSummary',
             'campaignTitle': campaignTitle,
             'timeSent': timeSent,
             'totalSent': totalSent,
             'openRate': openRate,
             'openPercent': openPercent,
             'clickThrough': clickThrough,
             'clickPercent': clickPercent
             }
        campaignSummaryJSON = {'customerName':customerName,'object':d}
        #print ">>> makeCampaignSummaryJSON...JSON created...%s" % campaignSummaryJSON
        #print ">>> makeCampaignSummaryJSON...JSON created...returning campaignSummaryJSON"
        return campaignSummaryJSON

    def getConstantContactCampaigns(self,numCampaigns):
        campaigns = []
        ccCampaignsTag = "/emailmarketing/campaigns"
        parameters = {'status':'ALL',
                      'limit':numCampaigns,
                      'api_key': self.API_KEY,
                      'access_token': self.CONSTANT_CONTACT_CUSTOMER_TOKEN}
        response = requests.get(self.CONSTANT_CONTACT_API_BASE+ccCampaignsTag, params=parameters)
        print(response.status_code)
        data = response.json()
        #print data
        print("[ Searching %s records: ")% numCampaigns,
        numSearches = 0
        numResults = 0
        for i,d in enumerate(data['results']):
            if d['status'] == "SENT":
                #print "SENT campaign found"
                print("+"),
                numResults += 1
                c = {'campaignId':d['id'].encode('ascii','replace'),
                     'campaignTitle':d['name'].encode('ascii','replace'),
                     'timeSent':d['modified_date'].encode('ascii','replace')}
                #print c
                campaigns.append(c)
            else:
                print("-"),
            numSearches = i
        print "]"
        print "[ Searched %i records.  Found %i campaigns with status 'SENT' ]" % (numSearches+1, numResults)
        print ">>> getCampaigns..returning campaigns"
        #print ">>> getCampaigns..returning campaigns" % campaigns
        return campaigns

    def getOneConstantContactCampaignsData(self,campaignID):
        
        ccCampaignsTag = "/emailmarketing/campaigns/"
        campaignExtras = "/tracking/reports/summary"
        parameters = {
            'api_key': self.API_KEY,
            'access_token': self.CONSTANT_CONTACT_CUSTOMER_TOKEN
            }
        response = requests.get(self.CONSTANT_CONTACT_API_BASE+ccCampaignsTag+campaignID+campaignExtras, params=parameters)
        #print(response.status_code)
        data = response.json()
        #print ">>> getOneCampaignsData...returning campaign data"
        #print ">>> getOneCampaignsData...%s" % data
        return data

    def getConstantContactCampaignData(self,numCampaignsToSearch):
        campaignData = []
        campaignJSONdata = []
        campaigns = self.getConstantContactCampaigns(numCampaignsToSearch)
        numJSON = 0
        print("[ Retrieving data for %s campaigns: ") % len(campaigns),
        for c in campaigns:
            #print "c = %s" % c
            d = self.getOneConstantContactCampaignsData(c['campaignId'])
            campaignData.append(d)
            
            customerName = self.CUSTOMER_NAME
            campaignTitle = c['campaignTitle']
            timeSent = c['timeSent']
            totalSent = d['sends']
            openRate = d['opens']
            openPercent = openRate/totalSent
            clickThrough = d['clicks']
            clickPercent = clickThrough/totalSent
                    
            cj = self.makeConstantContactCampaignSummaryJSON(customerName,campaignTitle, timeSent, totalSent,
                                openRate, openPercent,
                                clickThrough, clickPercent)

            campaignJSONdata.append(cj)
            numJSON +=1
            print("."),
            
        #print ">>> getCampaignData...retrieved campaignData...%s" % campaignData
        #print ">>> getCampaignData...coverted to JSON...%s" % campaignJSONdata
        print "]"
        print "[ Coverted %s records to JSON objects ready to send to Firebase ]" % (numJSON)
        print ">>> getCampaignData...returning campaignJSONdata"
        return campaignJSONdata
