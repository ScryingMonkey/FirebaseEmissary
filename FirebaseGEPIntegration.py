from firebase import firebase


from ConstantContactFetcher import ConstantContactFetcher

CUSTOMER_NAME = ""
CONSTANT_CONTACT_CUSTOMER_TOKEN = "fc6b757b-e12b-460d-828d-67a9cdbbe887"
FIREBASE_BASE = "https://project-3617555751812177585.firebaseio.com/"

#....................

def sendToFirebase(customer, dataBucket, data):
    firebase.put("/customers/", customer, {"customerName":customer})
    print("[ Sending %s JSON objects to Firebase: ") % len(data),
    numSent = 0
    for w in data:
        try:
            firebase.put("/customers/%s/%s" % (customer,dataBucket),
                         w['object']['campaignTitle'],
                         {'campaignTitle':w['object']['campaignTitle'],
                          'timeSent':w['object']['timeSent'],
                          'openRate':w['object']['openRate'],
                          'openPercent':w['object']['openPercent'],
                          'clickThrough':w['object']['clickThrough'],
                          'clickPercent':w['object']['clickPercent'],
                          'totalSent':w['object']['totalSent']}
                         )
            print("."),
            numSent += 1
        except:
            print("ERROR writing campaign: %s" % w['object']['campaignTitle'])
    print "]"
    print ">>> sendToFirebase...%s records sent to Firebase" % (numSent)

firebase = firebase.FirebaseApplication(FIREBASE_BASE)
CONSTANT_CONTACT_CUSTOMER_TOKEN = "fc6b757b-e12b-460d-828d-67a9cdbbe887"
ccf = ConstantContactFetcher(CONSTANT_CONTACT_CUSTOMER_TOKEN)

customerData = ccf.getConstantContactCustomerData()
CUSTOMER_NAME = customerData['organization_name']
print "CUSTOMER_NAME: %s" % CUSTOMER_NAME
campaigns = ccf.getConstantContactCampaignData(20)
sendToFirebase(CUSTOMER_NAME, "constant_contact_campaign_summaries", campaigns)




