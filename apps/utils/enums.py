'''
Created on Feb 19, 2024

@author: nimaiuser
'''
from enum import Enum


class ResStatus(Enum):
    success = "success"
    error = "error"

class StatusType(Enum):
    AC = "AC"
    NA = "NA"

class OTPSourceType(Enum):
    MBL = "MBL"
    EML = "EML"

class DeviceType(Enum):
    MBL = "MBL"
    WEB = "WEB"

class UserType(Enum):
    ADMN = "ADMN"
    OPTR = "OPTR"


class TemplateSections(Enum):
    linkSet = 'Links Set'
    links = 'Links'
    carouselImgs = 'Carousel Images'
    images = 'Images'
    colors = 'Colors'
    fonts = 'Fonts'
    fontSizes = 'Font Sizes'
    options = 'Options'
    inputs = 'Inputs'
    time = 'Time'
    textArea = 'TextArea'

class TemplateGroups(Enum):
    common = 'COMMON'
    home = 'HOME'
    sd_donations = 'SD_DONATIONS'
    wd_donations = 'WD_DONATIONS'


class donationMoneyReceiptCategories(Enum):
    SEVAS = 'SEVAS'
    OFFLINE = 'OFFLINE'
    DIRECT_TRANSFER = 'DIRECT_TRANSFER'
    DIRECT_MONEY = 'DIRECT_MONEY'


class SummaryConfigCodes(Enum):
    donation = 'DONATION'


class FeeType(Enum):
    buildingFund = 'Building fund'
    hostelFee = 'Hostel Fee'
    tutionFee = 'Tution Fee'
    securityDeposit = 'Security Deposit'
    booksFee = 'Books Fee'


class AdminConsoleTypes(Enum):
    main_admin = 'MAIN_ADMIN'
    client_admin = 'CLIENT_ADMIN'


smsTypeEnum = {
  'transnational': 'transnational',
  'promotional': 'promotional'
}

paymentGatewayEnum = {
  'RZPAY': 'RZPAY',
  'PAYU': 'PAYU',
  'CASFRE': 'CASFRE',
  'PAYPL': 'PAYPL',
  'STRIP': 'STRIP',
  'INSTAMOJO': 'INSTAMOJO',
  'PHONEPE':'PHONEPE'
}

paymentGatewayDisplayEnum = {
  'RZPAY': 'RazorPay',
  'PAYU': 'PayU',
  'CASFRE': 'Cashfree',
  'PAYPL': 'PayPal',
  'STRIP': 'Stripe',
  'INSTAMOJO': 'INSTAMOJO',
  'PHONEPE':'PhonePe'
}

class paymentGatewayNamesEnum(Enum):
    razorpay = 'razorpay'
    payu = 'payu'
    cashfree = 'cashfree'
    paypal = 'paypal'
    stripe = 'stripe'
    instamojo = 'instamojo'
    phonepe = 'phonepe'

class statesEnum(Enum):
    AN="Andaman and Nicobar Islands"
    AP="Andhra Pradesh"
    AR="Arunachal Pradesh"
    AS="Assam"
    BR="Bihar"
    CH="Chandigarh"
    CT="Chhattisgarh"
    DN="Dadra and Nagar Haveli"
    DD="Daman and Diu"
    DL="Delhi"
    GA="Goa"
    GJ="Gujarat"
    HR="Haryana"
    HP="Himachal Pradesh"
    JK="Jammu and Kashmir"
    JH="Jharkhand"
    KA="Karnataka"
    KL="Kerala"
    LA="Ladakh"
    LD="Lakshadweep"
    MP="Madhya Pradesh"
    MH="Maharashtra"
    MN="Manipur"
    ML="Meghalaya"
    MZ="Mizoram"
    NL="Nagaland"
    OR="Odisha"
    PY="Puducherry"
    PB="Punjab"
    RJ="Rajasthan"
    SK="Sikkim"
    TN="Tamil Nadu"
    TG="Telangana"
    TR="Tripura"
    UP="Uttar Pradesh"
    UT="Uttarakhand"
    WB="West Bengal"

stateDisplayEnum = {
        
    "AN" : "Andaman and Nicobar Islands",
    "AP" : "Andhra Pradesh",
    "AR" : "Arunachal Pradesh",
    "AS" : "Assam",
    "BR" : "Bihar",
    "CH" : "Chandigarh",
    "CT" : "Chhattisgarh",
    "DN" : "Dadra and Nagar Haveli",
    "DD" : "Daman and Diu",
    "DL" : "Delhi",
    "GA" : "Goa",
    "GJ" : "Gujarat",
    "HR" : "Haryana",
    "HP" : "Himachal Pradesh",
    "JK" : "Jammu and Kashmir",
    "JH" : "Jharkhand",
    "KA" : "Karnataka",
    "KL" : "Kerala",
    "LA" : "Ladakh",
    "LD" : "Lakshadweep",
    "MP" : "Madhya Pradesh",
    "MH" : "Maharashtra",
    "MN" : "Manipur",
    "ML" : "Meghalaya",
    "MZ" : "Mizoram",
    "NL" : "Nagaland",
    "OR" : "Odisha",
    "PY" : "Puducherry",
    "PB" : "Punjab",
    "RJ" : "Rajasthan",
    "SK" : "Sikkim",
    "TN" : "Tamil Nadu",
    "TG" : "Telangana",
    "TR" : "Tripura",
    "UP" : "Uttar Pradesh",
    "UT" : "Uttarakhand",
    "WB" : "West Bengal",
    "Andhra Pradesh" : "Andhra Pradesh"
        
}


ExelStateDisplayEnum = {
        
    "ANDAMAN AND NICOBAR ISLANDS" : "WB" ,
    "ANDHRA PRADESH" : "AP" ,
    "ARUNACHAL PRADESH" : "AR" ,
    "ASSAM" : "AS" ,
    "BIHAR" : "BR" ,
    "CHANDIGARH" : "PB"  ,
    "CHHATTISGARH" : "CT" ,
    "DADRA AND NAGAR HAVELI" : "GJ" ,
    "DAMAN AND DIU" : "GJ"  ,
    "DELHI" : "DL" ,
    "GOA" : "MH"  ,
    "GUJARAT" : "GJ" ,
    "HARYANA" : "HR" ,
    "HIMACHAL PRADESH" : "HP" ,
    "JAMMU AND KASHMIR" : "JK" ,
    "JHARKHAND" : "BR" ,
    "KARNATAKA" : "KA" ,
    "KERALA" : "KL" ,
    "LADAKH" : "LA" ,
    "LAKSHADWEEP" : "KL" ,
    "MADHYA PRADESH" : "MP" ,
    "MAHARASHTRA" : "MH" ,
    "MANIPUR" : "AR" ,
    "MEGHALAYA" : "AR" ,
    "MIZORAM" : "AR" ,
    "NAGALAND" : "AR",
    "ORISSA" : "OR" ,
    "PANDUCHERRY" : "TN",
    "PUNJAB" : "PB" ,
    "RAJASTHAN" : "RJ" ,
    "SIKKIM" : "WB" ,
    "TAMILNADU" : "TN" ,
    "TELANGANA" : "AP" ,
    "TRIPURA" : "AR" ,
    "UTTAR PRADESH" : "UP" ,
    "UTTARAKHAND" : "UP" ,
    "WEST BENGAL" : "WB" 
        
}



order_status = {
  'NYORD': 'NYORD',
  'ORDRD': 'ORDRD',
  'SHIPD': 'SHIPD',
  'CNCLD': 'CNCLD',
  'DLVRD': 'DLVRD',
  'TRNST': 'TRNST',
  'RTRND': 'RTRND',
  'SUSPD': 'SUSPD',
  'PACKD': 'PACKD',
  'DSPTD': 'DSPTD'
}

product_display_status = {
  'AC': 'Active',
  'DL': 'Deleted',
  'NA': 'Not Active'
}

customer_gender = {
  'M': 'Male',
  'F': 'Female'
}

order_display_status = {
  'NYORD': 'Pending Payment',
  'ORDRD': 'Processing',
  'SHIPD': 'Shipping',
  'CNCLD': 'Cancelled',
  'DLVRD': 'Delivered',
  'TRNST': 'Transit',
  'RTRND': 'Returned',
  'SUSPD': 'Suspended',
  'PACKD': 'Packed',
  'DSPTD': 'Dispatched',
  'CNCTD': 'Processing',
  'OUTDL': 'Out For Delivery'
}

order_to_shipment_status = {
    
    'NYORD': 'NYORD',
    'ORDRD': 'ORDRD',
    'CSHIPD': 'SHIPD',
    'CNCLD': 'CNCLD',
    'DLVRD': 'DLVRD',
    'TRNSIT': 'TRNST',
    'RETRND': 'RTRND',
    'SUSPD': 'SUSPD',
    'PACKED': 'PACKD',
    'DSPTD': 'DSPTD',
    'CNCTD': 'CNCTD',
    'OUTDLV': 'OUTDL',
    'DAMAGD': 'TRNST',
    'PSHIPD': 'CNCTD'
    }

shipment_status_display = {
    
    'PSHIPD':'Shipping',
    'SUSPND': 'Suspended',
    'SUSPND': 'Rejected',
    'TRNSIT': 'Transit',
    'CSHIPD': 'Shipping',
    'DAMAGD': 'Damaged',
    'OUTDLV':'Out For Delivery',
    'DELVRD': 'Delivered',
    'REJCTD': 'Rejected'
    
    }



