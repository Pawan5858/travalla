var serverEndPointUrl = "http://localhost:8000" //local instance
// var serverEndPointUrl = "http://192.168.108.57:8000" //local instance
// var serverEndPointUrl = "http://192.168.108.10:8001" //test instance

// var serverEndPointUrl = "https://swc.singledeck.in" // test instance



var serverAPIVersion = 'v1'
var serverAPIVersion2 = 'v2'
var baseUrl = serverEndPointUrl + "/api/" + serverAPIVersion + "/"

var RSA_PublicKey = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC9ITaISnuVTdhWW0008bVKqwMF\nEkxBB4dA0svzCuQMmRXCZ9EFP8PL4VVqsju3lNdcpgRa8MzwCPRJ932+M7d6WNPz\nfHoF/nK85//sVQdHCj0rF5PDfvTGOnDeYvN/cdI/cnqQCsSb5ThqO/lr5w+hPuPq\nri1okYc3yE2cWaYHSQIDAQAB\n-----END PUBLIC KEY-----'

var rsa_encrypt = new JSEncrypt();
rsa_encrypt.setPublicKey(RSA_PublicKey);

var loading
$(document).ready(function() {
  $('.modal').modal();
    Object.defineProperty(String.prototype, "toHTMLEntitiy", {
        value: function toHTMLEntitiy() {
            return $("<div>").text(this).html();
        },
        writable: true,
        configurable: true
    });
    initAjaxSetUp()
});

/**********************************************
 *   Countries
 ***********************************************/
var countriesList = [
    {
      name: "India",
      dial_code: "+91",
      code: "IN"
    }, {
      name: "United States",
      dial_code: "+1",
      code: "US"
    }, {
      name: "Afghanistan",
      dial_code: "+93",
      code: "AF"
    }, {
      name: "Albania",
      dial_code: "+355",
      code: "AL"
    }, {
      name: "Algeria",
      dial_code: "+213",
      code: "DZ"
    }, {
      name: "AmericanSamoa",
      dial_code: "+1 684",
      code: "AS"
    }, {
      name: "Andorra",
      dial_code: "+376",
      code: "AD"
    }, {
      name: "Angola",
      dial_code: "+244",
      code: "AO"
    }, {
      name: "Anguilla",
      dial_code: "+1 264",
      code: "AI"
    }, {
      name: "Antigua and Barbuda",
      dial_code: "+1268",
      code: "AG"
    }, {
      name: "Argentina",
      dial_code: "+54",
      code: "AR"
    }, {
      name: "Armenia",
      dial_code: "+374",
      code: "AM"
    }, {
      name: "Aruba",
      dial_code: "+297",
      code: "AW"
    }, {
      name: "Australia",
      dial_code: "+61",
      code: "AU"
    }, {
      name: "Austria",
      dial_code: "+43",
      code: "AT"
    }, {
      name: "Azerbaijan",
      dial_code: "+994",
      code: "AZ"
    }, {
      name: "Bahamas",
      dial_code: "+1 242",
      code: "BS"
    }, {
      name: "Bahrain",
      dial_code: "+973",
      code: "BH"
    }, {
      name: "Bangladesh",
      dial_code: "+880",
      code: "BD"
    }, {
      name: "Barbados",
      dial_code: "+1 246",
      code: "BB"
    }, {
      name: "Belarus",
      dial_code: "+375",
      code: "BY"
    }, {
      name: "Belgium",
      dial_code: "+32",
      code: "BE"
    }, {
      name: "Belize",
      dial_code: "+501",
      code: "BZ"
    }, {
      name: "Benin",
      dial_code: "+229",
      code: "BJ"
    }, {
      name: "Bermuda",
      dial_code: "+1 441",
      code: "BM"
    }, {
      name: "Bhutan",
      dial_code: "+975",
      code: "BT"
    }, {
      name: "Bosnia and Herzegovina",
      dial_code: "+387",
      code: "BA"
    }, {
      name: "Botswana",
      dial_code: "+267",
      code: "BW"
    }, {
      name: "Brazil",
      dial_code: "+55",
      code: "BR"
    }, {
      name: "British Indian Ocean Territory",
      dial_code: "+246",
      code: "IO"
    }, {
      name: "Bulgaria",
      dial_code: "+359",
      code: "BG"
    }, {
      name: "Burkina Faso",
      dial_code: "+226",
      code: "BF"
    }, {
      name: "Burundi",
      dial_code: "+257",
      code: "BI"
    }, {
      name: "Cambodia",
      dial_code: "+855",
      code: "KH"
    }, {
      name: "Cameroon",
      dial_code: "+237",
      code: "CM"
    }, {
      name: "Canada",
      dial_code: "+1",
      code: "CA"
    }, {
      name: "Cape Verde",
      dial_code: "+238",
      code: "CV"
    }, {
      name: "Cayman Islands",
      dial_code: "+ 345",
      code: "KY"
    }, {
      name: "Central African Republic",
      dial_code: "+236",
      code: "CF"
    }, {
      name: "Chad",
      dial_code: "+235",
      code: "TD"
    }, {
      name: "Chile",
      dial_code: "+56",
      code: "CL"
    }, {
      name: "China",
      dial_code: "+86",
      code: "CN"
    }, {
      name: "Christmas Island",
      dial_code: "+61",
      code: "CX"
    }, {
      name: "Colombia",
      dial_code: "+57",
      code: "CO"
    }, {
      name: "Comoros",
      dial_code: "+269",
      code: "KM"
    }, {
      name: "Congo",
      dial_code: "+242",
      code: "CG"
    }, {
      name: "Cook Islands",
      dial_code: "+682",
      code: "CK"
    }, {
      name: "Costa Rica",
      dial_code: "+506",
      code: "CR"
    }, {
      name: "Croatia",
      dial_code: "+385",
      code: "HR"
    }, {
      name: "Cuba",
      dial_code: "+53",
      code: "CU"
    }, {
      name: "Cyprus",
      dial_code: "+537",
      code: "CY"
    }, {
      name: "Czech Republic",
      dial_code: "+420",
      code: "CZ"
    }, {
      name: "Denmark",
      dial_code: "+45",
      code: "DK"
    }, {
      name: "Djibouti",
      dial_code: "+253",
      code: "DJ"
    }, {
      name: "Dominica",
      dial_code: "+1 767",
      code: "DM"
    }, {
      name: "Dominican Republic",
      dial_code: "+1 849",
      code: "DO"
    }, {
      name: "Ecuador",
      dial_code: "+593",
      code: "EC"
    }, {
      name: "Egypt",
      dial_code: "+20",
      code: "EG"
    }, {
      name: "El Salvador",
      dial_code: "+503",
      code: "SV"
    }, {
      name: "Equatorial Guinea",
      dial_code: "+240",
      code: "GQ"
    }, {
      name: "Eritrea",
      dial_code: "+291",
      code: "ER"
    }, {
      name: "Estonia",
      dial_code: "+372",
      code: "EE"
    }, {
      name: "Ethiopia",
      dial_code: "+251",
      code: "ET"
    }, {
      name: "Faroe Islands",
      dial_code: "+298",
      code: "FO"
    }, {
      name: "Fiji",
      dial_code: "+679",
      code: "FJ"
    }, {
      name: "Finland",
      dial_code: "+358",
      code: "FI"
    }, {
      name: "France",
      dial_code: "+33",
      code: "FR"
    }, {
      name: "French Guiana",
      dial_code: "+594",
      code: "GF"
    }, {
      name: "French Polynesia",
      dial_code: "+689",
      code: "PF"
    }, {
      name: "Gabon",
      dial_code: "+241",
      code: "GA"
    }, {
      name: "Gambia",
      dial_code: "+220",
      code: "GM"
    }, {
      name: "Georgia",
      dial_code: "+995",
      code: "GE"
    }, {
      name: "Germany",
      dial_code: "+49",
      code: "DE"
    }, {
      name: "Ghana",
      dial_code: "+233",
      code: "GH"
    }, {
      name: "Gibraltar",
      dial_code: "+350",
      code: "GI"
    }, {
      name: "Greece",
      dial_code: "+30",
      code: "GR"
    }, {
      name: "Greenland",
      dial_code: "+299",
      code: "GL"
    }, {
      name: "Grenada",
      dial_code: "+1 473",
      code: "GD"
    }, {
      name: "Guadeloupe",
      dial_code: "+590",
      code: "GP"
    }, {
      name: "Guam",
      dial_code: "+1 671",
      code: "GU"
    }, {
      name: "Guatemala",
      dial_code: "+502",
      code: "GT"
    }, {
      name: "Guinea",
      dial_code: "+224",
      code: "GN"
    }, {
      name: "Guinea-Bissau",
      dial_code: "+245",
      code: "GW"
    }, {
      name: "Guyana",
      dial_code: "+595",
      code: "GY"
    }, {
      name: "Haiti",
      dial_code: "+509",
      code: "HT"
    }, {
      name: "Honduras",
      dial_code: "+504",
      code: "HN"
    }, {
      name: "Hungary",
      dial_code: "+36",
      code: "HU"
    }, {
      name: "Iceland",
      dial_code: "+354",
      code: "IS"
    }, {
      name: "Indonesia",
      dial_code: "+62",
      code: "ID"
    }, {
      name: "Iraq",
      dial_code: "+964",
      code: "IQ"
    }, {
      name: "Ireland",
      dial_code: "+353",
      code: "IE"
    }, {
      name: "Israel",
      dial_code: "+972",
      code: "IL"
    }, {
      name: "Italy",
      dial_code: "+39",
      code: "IT"
    }, {
      name: "Jamaica",
      dial_code: "+1 876",
      code: "JM"
    }, {
      name: "Japan",
      dial_code: "+81",
      code: "JP"
    }, {
      name: "Jordan",
      dial_code: "+962",
      code: "JO"
    }, {
      name: "Kazakhstan",
      dial_code: "+7 7",
      code: "KZ"
    }, {
      name: "Kenya",
      dial_code: "+254",
      code: "KE"
    }, {
      name: "Kiribati",
      dial_code: "+686",
      code: "KI"
    }, {
      name: "Kuwait",
      dial_code: "+965",
      code: "KW"
    }, {
      name: "Kyrgyzstan",
      dial_code: "+996",
      code: "KG"
    }, {
      name: "Latvia",
      dial_code: "+371",
      code: "LV"
    }, {
      name: "Lebanon",
      dial_code: "+961",
      code: "LB"
    }, {
      name: "Lesotho",
      dial_code: "+266",
      code: "LS"
    }, {
      name: "Liberia",
      dial_code: "+231",
      code: "LR"
    }, {
      name: "Liechtenstein",
      dial_code: "+423",
      code: "LI"
    }, {
      name: "Lithuania",
      dial_code: "+370",
      code: "LT"
    }, {
      name: "Luxembourg",
      dial_code: "+352",
      code: "LU"
    }, {
      name: "Madagascar",
      dial_code: "+261",
      code: "MG"
    }, {
      name: "Malawi",
      dial_code: "+265",
      code: "MW"
    }, {
      name: "Malaysia",
      dial_code: "+60",
      code: "MY"
    }, {
      name: "Maldives",
      dial_code: "+960",
      code: "MV"
    }, {
      name: "Mali",
      dial_code: "+223",
      code: "ML"
    }, {
      name: "Malta",
      dial_code: "+356",
      code: "MT"
    }, {
      name: "Marshall Islands",
      dial_code: "+692",
      code: "MH"
    }, {
      name: "Martinique",
      dial_code: "+596",
      code: "MQ"
    }, {
      name: "Mauritania",
      dial_code: "+222",
      code: "MR"
    }, {
      name: "Mauritius",
      dial_code: "+230",
      code: "MU"
    }, {
      name: "Mayotte",
      dial_code: "+262",
      code: "YT"
    }, {
      name: "Mexico",
      dial_code: "+52",
      code: "MX"
    }, {
      name: "Monaco",
      dial_code: "+377",
      code: "MC"
    }, {
      name: "Mongolia",
      dial_code: "+976",
      code: "MN"
    }, {
      name: "Montenegro",
      dial_code: "+382",
      code: "ME"
    }, {
      name: "Montserrat",
      dial_code: "+1664",
      code: "MS"
    }, {
      name: "Morocco",
      dial_code: "+212",
      code: "MA"
    }, {
      name: "Myanmar",
      dial_code: "+95",
      code: "MM"
    }, {
      name: "Namibia",
      dial_code: "+264",
      code: "NA"
    }, {
      name: "Nauru",
      dial_code: "+674",
      code: "NR"
    }, {
      name: "Nepal",
      dial_code: "+977",
      code: "NP"
    }, {
      name: "Netherlands",
      dial_code: "+31",
      code: "NL"
    }, {
      name: "Netherlands Antilles",
      dial_code: "+599",
      code: "AN"
    }, {
      name: "New Caledonia",
      dial_code: "+687",
      code: "NC"
    }, {
      name: "New Zealand",
      dial_code: "+64",
      code: "NZ"
    }, {
      name: "Nicaragua",
      dial_code: "+505",
      code: "NI"
    }, {
      name: "Niger",
      dial_code: "+227",
      code: "NE"
    }, {
      name: "Nigeria",
      dial_code: "+234",
      code: "NG"
    }, {
      name: "Niue",
      dial_code: "+683",
      code: "NU"
    }, {
      name: "Norfolk Island",
      dial_code: "+672",
      code: "NF"
    }, {
      name: "Northern Mariana Islands",
      dial_code: "+1 670",
      code: "MP"
    }, {
      name: "Norway",
      dial_code: "+47",
      code: "NO"
    }, {
      name: "Oman",
      dial_code: "+968",
      code: "OM"
    }, {
      name: "Pakistan",
      dial_code: "+92",
      code: "PK"
    }, {
      name: "Palau",
      dial_code: "+680",
      code: "PW"
    }, {
      name: "Panama",
      dial_code: "+507",
      code: "PA"
    }, {
      name: "Papua New Guinea",
      dial_code: "+675",
      code: "PG"
    }, {
      name: "Paraguay",
      dial_code: "+595",
      code: "PY"
    }, {
      name: "Peru",
      dial_code: "+51",
      code: "PE"
    }, {
      name: "Philippines",
      dial_code: "+63",
      code: "PH"
    }, {
      name: "Poland",
      dial_code: "+48",
      code: "PL"
    }, {
      name: "Portugal",
      dial_code: "+351",
      code: "PT"
    }, {
      name: "Puerto Rico",
      dial_code: "+1 939",
      code: "PR"
    }, {
      name: "Qatar",
      dial_code: "+974",
      code: "QA"
    }, {
      name: "Romania",
      dial_code: "+40",
      code: "RO"
    }, {
      name: "Rwanda",
      dial_code: "+250",
      code: "RW"
    }, {
      name: "Samoa",
      dial_code: "+685",
      code: "WS"
    }, {
      name: "San Marino",
      dial_code: "+378",
      code: "SM"
    }, {
      name: "Saudi Arabia",
      dial_code: "+966",
      code: "SA"
    }, {
      name: "Senegal",
      dial_code: "+221",
      code: "SN"
    }, {
      name: "Serbia",
      dial_code: "+381",
      code: "RS"
    }, {
      name: "Seychelles",
      dial_code: "+248",
      code: "SC"
    }, {
      name: "Sierra Leone",
      dial_code: "+232",
      code: "SL"
    }, {
      name: "Singapore",
      dial_code: "+65",
      code: "SG"
    }, {
      name: "Slovakia",
      dial_code: "+421",
      code: "SK"
    }, {
      name: "Slovenia",
      dial_code: "+386",
      code: "SI"
    }, {
      name: "Solomon Islands",
      dial_code: "+677",
      code: "SB"
    }, {
      name: "South Africa",
      dial_code: "+27",
      code: "ZA"
    }, {
      name: "South Georgia and the South Sandwich Islands",
      dial_code: "+500",
      code: "GS"
    }, {
      name: "Spain",
      dial_code: "+34",
      code: "ES"
    }, {
      name: "Sri Lanka",
      dial_code: "+94",
      code: "LK"
    }, {
      name: "Sudan",
      dial_code: "+249",
      code: "SD"
    }, {
      name: "Suriname",
      dial_code: "+597",
      code: "SR"
    }, {
      name: "Swaziland",
      dial_code: "+268",
      code: "SZ"
    }, {
      name: "Sweden",
      dial_code: "+46",
      code: "SE"
    }, {
      name: "Switzerland",
      dial_code: "+41",
      code: "CH"
    }, {
      name: "Tajikistan",
      dial_code: "+992",
      code: "TJ"
    }, {
      name: "Thailand",
      dial_code: "+66",
      code: "TH"
    }, {
      name: "Togo",
      dial_code: "+228",
      code: "TG"
    }, {
      name: "Tokelau",
      dial_code: "+690",
      code: "TK"
    }, {
      name: "Tonga",
      dial_code: "+676",
      code: "TO"
    }, {
      name: "Trinidad and Tobago",
      dial_code: "+1 868",
      code: "TT"
    }, {
      name: "Tunisia",
      dial_code: "+216",
      code: "TN"
    }, {
      name: "Turkey",
      dial_code: "+90",
      code: "TR"
    }, {
      name: "Turkmenistan",
      dial_code: "+993",
      code: "TM"
    }, {
      name: "Turks and Caicos Islands",
      dial_code: "+1 649",
      code: "TC"
    }, {
      name: "Tuvalu",
      dial_code: "+688",
      code: "TV"
    }, {
      name: "Uganda",
      dial_code: "+256",
      code: "UG"
    }, {
      name: "Ukraine",
      dial_code: "+380",
      code: "UA"
    }, {
      name: "United Arab Emirates",
      dial_code: "+971",
      code: "AE"
    }, {
      name: "United Kingdom",
      dial_code: "+44",
      code: "GB"
    }, {
      name: "Uruguay",
      dial_code: "+598",
      code: "UY"
    }, {
      name: "Uzbekistan",
      dial_code: "+998",
      code: "UZ"
    }, {
      name: "Vanuatu",
      dial_code: "+678",
      code: "VU"
    }, {
      name: "Wallis and Futuna",
      dial_code: "+681",
      code: "WF"
    }, {
      name: "Yemen",
      dial_code: "+967",
      code: "YE"
    }, {
      name: "Zambia",
      dial_code: "+260",
      code: "ZM"
    }, {
      name: "Zimbabwe",
      dial_code: "+263",
      code: "ZW"
    }, {
      name: "land Islands",
      dial_code: "",
      code: "AX"
    }, {
      name: "Antarctica",
      dial_code: null,
      code: "AQ"
    }, {
      name: "Bolivia, Plurinational State of",
      dial_code: "+591",
      code: "BO"
    }, {
      name: "Brunei Darussalam",
      dial_code: "+673",
      code: "BN"
    }, {
      name: "Cocos (Keeling) Islands",
      dial_code: "+61",
      code: "CC"
    }, {
      name: "Congo, The Democratic Republic of the",
      dial_code: "+243",
      code: "CD"
    }, {
      name: "Cote d'Ivoire",
      dial_code: "+225",
      code: "CI"
    }, {
      name: "Falkland Islands (Malvinas)",
      dial_code: "+500",
      code: "FK"
    }, {
      name: "Guernsey",
      dial_code: "+44",
      code: "GG"
    }, {
      name: "Holy See (Vatican City State)",
      dial_code: "+379",
      code: "VA"
    }, {
      name: "Hong Kong",
      dial_code: "+852",
      code: "HK"
    }, {
      name: "Iran, Islamic Republic of",
      dial_code: "+98",
      code: "IR"
    }, {
      name: "Isle of Man",
      dial_code: "+44",
      code: "IM"
    }, {
      name: "Jersey",
      dial_code: "+44",
      code: "JE"
    }, {
      name: "Korea, Democratic People's Republic of",
      dial_code: "+850",
      code: "KP"
    }, {
      name: "Korea, Republic of",
      dial_code: "+82",
      code: "KR"
    }, {
      name: "Lao People's Democratic Republic",
      dial_code: "+856",
      code: "LA"
    }, {
      name: "Libyan Arab Jamahiriya",
      dial_code: "+218",
      code: "LY"
    }, {
      name: "Macao",
      dial_code: "+853",
      code: "MO"
    }, {
      name: "Macedonia, The Former Yugoslav Republic of",
      dial_code: "+389",
      code: "MK"
    }, {
      name: "Micronesia, Federated States of",
      dial_code: "+691",
      code: "FM"
    }, {
      name: "Moldova, Republic of",
      dial_code: "+373",
      code: "MD"
    }, {
      name: "Mozambique",
      dial_code: "+258",
      code: "MZ"
    }, {
      name: "Palestinian Territory, Occupied",
      dial_code: "+970",
      code: "PS"
    }, {
      name: "Pitcairn",
      dial_code: "+872",
      code: "PN"
    }, {
      name: "RÃ©union",
      dial_code: "+262",
      code: "RE"
    }, {
      name: "Russia",
      dial_code: "+7",
      code: "RU"
    }, {
      name: "Saint BarthÃ©lemy",
      dial_code: "+590",
      code: "BL"
    }, {
      name: "Saint Helena, Ascension and Tristan Da Cunha",
      dial_code: "+290",
      code: "SH"
    }, {
      name: "Saint Kitts and Nevis",
      dial_code: "+1 869",
      code: "KN"
    }, {
      name: "Saint Lucia",
      dial_code: "+1 758",
      code: "LC"
    }, {
      name: "Saint Martin",
      dial_code: "+590",
      code: "MF"
    }, {
      name: "Saint Pierre and Miquelon",
      dial_code: "+508",
      code: "PM"
    }, {
      name: "Saint Vincent and the Grenadines",
      dial_code: "+1 784",
      code: "VC"
    }, {
      name: "Sao Tome and Principe",
      dial_code: "+239",
      code: "ST"
    }, {
      name: "Somalia",
      dial_code: "+252",
      code: "SO"
    }, {
      name: "Svalbard and Jan Mayen",
      dial_code: "+47",
      code: "SJ"
    }, {
      name: "Syrian Arab Republic",
      dial_code: "+963",
      code: "SY"
    }, {
      name: "Taiwan, Province of China",
      dial_code: "+886",
      code: "TW"
    }, {
      name: "Tanzania, United Republic of",
      dial_code: "+255",
      code: "TZ"
    }, {
      name: "Timor-Leste",
      dial_code: "+670",
      code: "TL"
    }, {
      name: "Venezuela, Bolivarian Republic of",
      dial_code: "+58",
      code: "VE"
    }, {
      name: "Viet Nam",
      dial_code: "+84",
      code: "VN"
    }, {
      name: "Virgin Islands, British",
      dial_code: "+1 284",
      code: "VG"
    }, {
      name: "Virgin Islands, U.S.",
      dial_code: "+1 340",
      code: "VI"
    }
  ];
  
/**********************************************
 *   Enums START
 ***********************************************/
var statusEnum = {
    success: 'success',
    error: 'error'
}

var userTypeEnum = {
  ADMN: 'ADMN',
  OPTR: 'OPTR'
}

var shelfLifeEnum = {
    REG: 'Regular',
    PER: 'Perishable',
    QPR: 'Quickly Perishable'
}

var statesEnum = {}

var shippingEnum = {

}

var adminConsoleTypesEnum = {
    main_admin: 'MAIN_ADMIN',
    client_admin: 'CLIENT_ADMIN'
}

var genderDispEnum = {
    M: 'Male',
    F: 'Female',
    O: 'Others'
}

var feeFrequencyDisplayEnum = {
    MONTLY: 'Monthly',
    QRTRLY: 'Quarterly',
    HFYRLY: 'Half-Yearly',
    ONETIM: 'One Time'
}

var paymentTypesDisplayEnum = {
    IND: 'Domestic',
    FRN: 'International'
}

var orgOrientationDisplayEnum = {
    CHRTBL: 'Charitable',
    SERVCE: 'Service',
    PRTCPR: 'PRTCPR',
    EMPOWR: 'Empowerment'
}

var ordersUnderDeliveryStatusEnum = {
    PSHIPD: "Partially Shipped",
    SUSPND: "Suspended",
    REJCTD: "Rejected",
    DELVRD: "Delivered",
    TRNSIT: "Transit",
    CSHIPD: "Shipped",
    DAMAGD: "Damaged",
    OUTDLV: "Out For Delivery",
    CNCLD: "Cancelled"
}

var orgLevelDisplayEnum = {
    CITY: 'City',
    STAT: 'State',
    NATN: 'National',
    INTR: 'International'
}

var orgRegStructureDisplayEnum = {
    TRST: 'Trust',
    SCTY: 'Society',
    SEC8: 'SEC8'
}

var orgSubStructureDisplayEnum = {
    PRIV: 'Private',
    PUBL: 'Public'
}

var orgFocusAreaCatgsDisplayEnum = {
    education: 'Education',
    empowerment: 'Empowerment',
    healthcare: 'Healthcare'
}

var order_status = {
    NYORD: 'NYORD',
    ORDRD: 'ORDRD',
    SHIPD: 'SHIPD',
    CNCLD: 'CNCLD',
    DLVRD: 'DLVRD',
    TRNST: 'TRNST',
    RTRND: 'RTRND',
    SUSPD: 'SUSPD',
    PACKD: 'PACKD',
    DSPTD: 'DSPTD'
}
var gst_include = {
    1: 'Include',
    0: 'Exclude'
}
var order_display_status = {
    NYORD: 'Pending Payment',
    ORDRD: 'Processing',
    SHIPD: 'Shipping',
    CNCLD: 'Cancelled',
    DLVRD: 'Delivered',
    TRNST: 'TRNST',
    RTRND: 'Returned',
    RPLCD: 'Replaced',
    SUSPD: 'Suspended',
    PACKD: 'Packed',
    DSPTD: 'Dispatched',
    CNCTD: 'Being Processed'
}

var templateSectionsEnum = {
    linkSets: 'Links Set',
    links: 'Links',
    carouselImgs: 'Carousel Images',
    images: 'Images',
    colors: 'Colors',
    fonts: 'Fonts',
    fontSizes: 'Font Sizes',
    options: 'Options',
    inputs: 'Inputs',
    time: 'Time',
    TextArea: 'TextArea'
}

var tmltFieldTypeEnum = {
    mandatory: 'MAND',
    optional: 'OPTL'
}

var tmltInputFieldTypeEnum = {
    text: 'TEXT',
    number: 'NUMBER'
}

var agenciesTypeEnum = {
    DLVRY: 'Delivery'
}
var agencyMode = {
    INTR: 'Internal',
    EXTR: 'External'
}
var agencyCriteriaEnum = {
    STATE: 'State',
    PRCAT: 'Product Category'
}

var avlFontsList = [
    "Lato-Bold",
    "Lato-Semibold",
    "Lato-Medium",
    "Lato-Regular",
    "Lato-Light",

    "Poppins-Bold",
    "Poppins-SemiBold",
    "Poppins-Medium",
    "Poppins-Regular",
    "Poppins-Light",

    "Proxima-Nova-Bold",
    "Proxima-Nova-Semibold",
    "Proxima-Nova-Regular",
    "Proxima-Nova-Thin",

    "OpenSans-Bold",
    "OpenSans-Semibold",
    "OpenSans-Regular",
    "OpenSans-Light",

    "Roboto-Bold",
    "Roboto-Medium",
    "Roboto-Regular",
    "Roboto-Light",

    "Montserrat-Bold",
    "Montserrat-Medium",
    "Montserrat-Regular",
    "Montserrat-Light",

    "Lora-Bold",
    "Lora-Regular",

    "Roboto-Condensed",

    "Niconne-Regular",

    "VarelaRound-Regular"
]

var iconsList = ['FB', 'Twitter', 'Instagram', 'Linkedin', 'Youtube', 'Email', 'Phone', 'Location',
    'Clock', 'AppStore', 'PlayStore'
]

/**********************************************
 *   Enums END
 ***********************************************/



/**********************************************
 *   DateTime Related Options START
 ***********************************************/

var dateformat_type = {
    ServerDateTimeZone: "YYYY-MM-DDTHH:mm:ss.SSSZ",
    ServerDateTime: "YYYY-MM-DD hh:mm:ss",
    ServerDate: "YYYY-MM-DD",
    DisplayDateTime: "DD-MM-YYYY hh:mm A",
    DisplayDate: "DD-MM-YYYY",
    DisplayDate_Small: "dd-mm-yyyy",
    FourDigitTime: "hhmm",
    DisplayTime: "hh:mm A",
    DisplaySmallTime: "h:mma",
    MonthDateYear: "MMM DD, YYYY",
    MonthDate: "MMM DD",
    YearMonth: "MMM YYYY",
    Year: "YYYY",
    DayMonthYear: "D MMM YYYY",
    DayMonthShortYear: "D MMM YY",
    DayMonthQuoteShortYear: "D MMM'YY",
    YearMonthNumber: "YYYY-M",
    DateMonthTime: "Do MMM h:mm A"
}


// Convert date Object from given date string
function getDateFrom(dateString, inputFormat = dateformat_type.ServerDateTime) {

    return moment(dateString, inputFormat)
}

// Convert date string to given date format
function convertDateFormater(dateString, inputFormat = dateformat_type.ServerDateTime, outputFormat = dateformat_type.DisplayDate) {

    return moment(dateString, inputFormat == "default" ? dateformat_type.ServerDateTime : inputFormat).format(outputFormat == "default" ? dateformat_type.DisplayDate : outputFormat)
}

function getDate_from_dateObject(obj_date, isToShow) {
    
    isToShow = (isInvalidString(isToShow)) ? false : isToShow;
    if (isInvalidString(obj_date)) {
        if (isToShow) {
            return '-';
        }
        return '';
    }
    return moment(new Date(obj_date)).format("DD-MM-YYYY");
}

function getDateTime_from_dateObject(obj_date, isToShow) {
    isToShow = (isInvalidString(isToShow)) ? false : isToShow;
    if (isInvalidString(obj_date)) {
        if (isToShow) {
            return '-';
        }
        return '';
    }

    return moment(new Date(obj_date)).format("DD-MM-YYYY, hh:mm A");
}

function fourDigitsToTwelveHrFormate(str) {
    return moment(str, "HHmm").format("h:mm A")
}

function twelveHrToFourDigitsFormate(str) {
    return moment(str, "h:mm A").format("HHmm")
}
/**********************************************
 *   DateTime Related Options END
 ***********************************************/



function isInvalidString(str) {
    //    str = $.trim(str);
    if (str === '' || str == '' || str === null || str == null ||
        typeof str === 'undefined' || str == undefined) {
        return true;
    }
    return false;
}

function getValidData_toDisplay(str) {
    if (isInvalidString(str)) {
        return '-';
    }
    return str;
}



var isValid = true;
function validateTextField(ele) {
  var inputValue = $(ele).val();

  if (inputValue === undefined || inputValue.trim() === "") {
      $(ele).val('').addClass('placeholderred');
      if (isValid) {
          $(ele).focus();
      }
      isValid = false;
      return false;
  }
  return true;
}

function validateSelectField(ele) {
  var selectedValue = $(ele).val();

  if (!selectedValue || selectedValue.trim() === "" || selectedValue === "Select Document Type") {
      // Validation failed
      $(ele).addClass('placeholderred');
      if (isValid) {
          $(ele).focus();
      }
      isValid = false;
      return false;
  }
  return true;
}

function goToPreviousPage() {
    history.back();
}


/**********************************************
 *       String Operations Starting
 *********************************************/

// Truncate string to eclipse (i.e 'Hello...')
// Usage:-  truncate.apply(getValidData_toDisplay(data), [30, true])
function truncate(n, useWordBoundary) {
    if (this.length <= n) { return this; }
    var subString = this.substr(0, n - 1);
    return (useWordBoundary ?
        subString.substr(0, subString.lastIndexOf(' ')) :
        subString) + "&hellip;";
};


// Replace string (i.e 'Hello World' to 'He!!o World')
String.prototype.replaceAt = function(index, replacement) {
    return this.substr(0, index) + replacement + this.substr(index + replacement.length);
}

function getLastIndexPathOf(url) {

    var parts = url.split("/")
    return parts[parts.length - 1]
}
/**********************************************
 *       String Operations Ending
 *********************************************/


/**********************************************
 *       Image Related Starting
 *********************************************/
imageToBase64 = (URL, callback) => {
    let image;
    image = new Image();
    image.crossOrigin = 'Anonymous';
    image.addEventListener('load', function() {
        let canvas = document.createElement('canvas');
        let context = canvas.getContext('2d');
        canvas.width = image.width;
        canvas.height = image.height;
        context.drawImage(image, 0, 0);
        try {
            var base64Str = canvas.toDataURL('image/png')

            callback(base64Str);

        } catch (err) {
            console.error(err)
        }
    });
    image.src = URL;
};
/**********************************************
 *       Image Related Ending
 *********************************************/



/**********************************************
 *       Search Related Functions Starting
 *********************************************/
$(window).keypress(function(e) {
    var key = e.which;

    if (key == 13 && $(document.activeElement).parents('.searchContainer').length == 1) {
        $(document.activeElement).parents('.searchContainer').find('.searchContainerSearchBtn').click();
        return false;
    }
});

$(document).on('click', '.input-group-addon .fa-calendar-times', function() {
    $(this).closest('.input-group').find('.date-field').val('').trigger('change');
    $(this).removeClass('fa-calendar-times').addClass('fa-calendar-alt');
});

// This will prevent fields from typing
$(document).on("cut paste keydown keyup keypress", '.disableTyping, .date-field', function(e) {

    switch (e.keyCode) {

        case 9: // Tab
        case 13: // Enter
        case 37: // Left
        case 38: // Up
        case 39: // Right
        case 40: // Down
            break;

        default:
            e.preventDefault();
            return false;
    }

});
/**********************************************
 *       Search Related Functions Ending
 *********************************************/



/**********************************************
 *       API Related Functions Starting
 *********************************************/
function initAjaxSetUp() {
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'),
            'deviceType': "WEB"
        },
        beforeSend: function(xhr) {
            if (!isInvalidString(localStorage.getItem("sessiontoken"))) {
                xhr.setRequestHeader('sessiontoken', localStorage.getItem("sessiontoken"));
            }
            if (!isInvalidString(localStorage.getItem("organizationId"))) {
                xhr.setRequestHeader('organizationId', localStorage.getItem("organizationId"));
            }
        }
    });
}

// AJAX API CALL ERROR HANDLING
function errorCallBack(data, textStatus, jqXHR) {
    if (data.status === 401) {
        clearUserSession();
        window.location.href = "login";
    } else {
        if (!isInvalidString(data.responseJSON) && !isInvalidString(data.responseJSON.message))
            show_StatusModal(data.responseJSON.message, statusEnum.error)
        else
            show_StatusModal("A System Error occurred. Please try again.", statusEnum.error)
    }
}

function errorHandledCallBack(data, textStatus, jqXHR, errorHandledCallBack) {
    errorCallBack(data, textStatus, jqXHR)
    errorHandledCallBack()
}

function apiResStatus(status) {
    return status == statusEnum.success
}
/**********************************************
 *       API Related Functions Ending
 *********************************************/



/**********************************************
 *       User Session Related Functions Starting
 *********************************************/
function clearUserSession() {
    localStorage.removeItem('organizationId')
    localStorage.removeItem('sessiontoken')
    localStorage.removeItem('adminDetails')

    setCookie('sessiontoken', '', 0);
    setCookie('organizationId', '', 0);
}

function addUserSession(user) {
    localStorage.setItem('organizationId', user.organizationId)
    localStorage.setItem('sessiontoken', user.sessiontoken)
    localStorage.setItem('adminDetails', JSON.stringify(user))

    setCookie('sessiontoken', user.sessiontoken, 30);
    setCookie('organizationId', user.organizationId, 30);
}

function addDeliveryUserSession(user) {
    localStorage.setItem('organizationId', user.organizationId)
    localStorage.setItem('sessiontoken', user.sessiontoken)
    localStorage.setItem('adminDetails', JSON.stringify(user))

    setCookie('sessiontoken', user.sessiontoken, 30);
    setCookie('organizationId', user.organizationId, 30);
}

function addMainUserSession(user) {
    localStorage.setItem('sessiontoken', user.sessiontoken)
    localStorage.setItem('adminDetails', JSON.stringify(user))

    setCookie('sessiontoken', user.sessiontoken, 30);
}



function getReqAPIHeaders() {

    return {
        'deviceType': "WEB",
        'sessiontoken': isInvalidString(localStorage.getItem("sessiontoken")) ? null : localStorage.getItem("sessiontoken"),
        'organizationId': isInvalidString(localStorage.getItem("organizationId")) ? null : localStorage.getItem("organizationId")
    }

}
/**********************************************
 *       User Session Related Functions Ending
 *********************************************/



/**********************************************
 *       Cookies Related Functions Starting
 *********************************************/
function setCookie(cname, cvalue, exdays) {
    var expires = ''
    if (exdays != null) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        expires = "expires=" + d.toUTCString() + ";";
    }
    document.cookie = cname + "=" + cvalue + ";" + expires + "path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
/**********************************************
 *       Cookies Related Functions Ending
 *********************************************/



/**********************************************
 *   Status Dialogue For Success, Error Msgs
 *********************************************/
// function show_StatusModal(message, status) {
//     if (apiResStatus(status)) {
//         $("#successmodal").modal("show")
//         $('.successmassagetext').text(message)
//     } else {
//         $("#errormodal").modal('show')
//         $(".errormassagetext").text(message)
//     }
// }



function show_StatusModal(message, status) {
  if (apiResStatus(status)) {
    $("#successmodal").modal("open");
    $('.successmassagetext').text(message);
  } else {
    $("#errormodal").modal('open');
    $(".errormassagetext").text(message);
  }
}
/**********************************************
 *       Conformation Dialog Callback START
 *********************************************/

function show_conformationModal(payload, callback) {

    $(".conformationmassagetext").text(payload.message)
    $("#conformationmodal").data('fn', callback)
    $('#conformationmodal .conformation_btn_yes').text(payload.yesBtnText ? payload.yesBtnText : 'Yes')
    $('#conformationmodal .conformation_btn_no').text(payload.noBtnText ? payload.noBtnText : 'No')

    $("#conformationmodal").modal('show')
}

// Conformation Dialog Callback Click events
$(document).on("click", "#conformationmodal .conformation_btn_no", function() {
    ($(this).parents('#conformationmodal').data('fn'))(false);
})
$(document).on("click", "#conformationmodal .conformation_btn_yes", function() {
        ($(this).parents('#conformationmodal').data('fn'))(true);
    })
/**********************************************
     *       Conformation Dialog Callback END
*********************************************/



/**********************************************
 *   Form Field Validations START
 *********************************************/

var formSubmit = false;
var emailExpr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
var mobileExpr = /\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})/;
var passwordExpr = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;
var acceptsOnlyAlphabetsExpr = /^[a-zA-Z]+$/;
var acceptsOnlynumbersExpr = /^[0-9]+$/;
var acceptsOnlyAlphabetsandNumExpr = /^[a-zA-Z0-9]+$/;
var acceptsOnlyAlphabetsSpaceDotExpr = /^[a-zA-Z. ]*$/;
var acceptsAlphaNumricWithSpace = /^(?=.*[A-Za-z0-9])[A-Za-z0-9 _]*$/;
var aadharRegularExpr = /^\d{4}\s\d{4}\s\d{4}$/;
var zipcodeExpr = /^[0-9]{6}$/;
var onlyaphaspace = /^(?=.*[A-Za-z])[a-zA-Z\s]+$/;
var orgID = /^[A-Za-z\d]{4,6}$/;
var floatNumbers = /^[+-]?\d+(\.\d+)?$/;
var addressfields = /^[a-zA-Z0-9!@#$&()-/'`.+, _/\"]*$/;

// var urlExpr = /^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_-]+=\w+(&[a-zA-Z0-9_-]+=\w+)*)?$/
var urlExpr = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/
var fbUrlCheck = /^(https?:\/\/)?(www\.)?facebook.com\/[a-zA-Z0-9(\.\?)?]/;


$(document).on("change paste keyup", ".mandatoryLocal, .validateLocal, .placeholderred", function() {
    checkValidForm($(this));
});
$(document).on("change paste keyup keypress keydown", ".noKeyPress", function() {
    return false;
});
$(document).on("change paste keyup keypress keydown", ".numbersOnly", function() {
    // Backspace, tab, enter, end, home, left, right
    // We don't support the del key in Opera because del == . == 46.
    var controlKeys = [8, 9, 13, 35, 36, 37, 39];
    // IE doesn't support indexOf
    var isControlKey = controlKeys.join(",").match(new RegExp(event.which));
    // Some browsers just don't raise events for control keys. Easy.
    // e.g. Safari backspace.
    if (!event.which || // Control keys in most browsers. e.g. Firefox tab is 0
        (48 <= event.which && event.which <= 57) || (96 <= event.which && event.which <= 105) || // Always 1 through 9
        (190 == event.which || 110 == event.which) || (46 == event.which && !($(this).val().includes("."))) || // to allow dot
        isControlKey) { // Opera assigns values for control keys.
        return;
    } else {
        event.preventDefault();
    }
});

function checkViewMode(formEle, forView) {

    if (forView) {
        $(formEle).addClass('viewOnly')

        $(formEle + ' input').each(function() {
            if ($(this).val() == '' && $(this).attr('type') != 'file') {
                $(this).val('-')
            }
        });
        $(formEle + ' textarea').each(function() {
            if ($(this).val() == '') {
                $(this).val('-')
            }
        });
        $(formEle + ' select').each(function() {
            if ($(this).val() == '') {
                $(this).closest('.select-wrapper').find('input.select-dropdown').val('-')
            }
        });
    } else {
        $(formEle).removeClass('viewOnly')
    }

}

function removeViewMode(formEle) {

    $(formEle).removeClass('viewOnly')

    $(formEle + ' input').each(function() {
        if ($(this).val() == '-') {
            $(this).val('')
        }
    });
    $(formEle + ' textarea').each(function() {
        if ($(this).val() == '-') {
            $(this).val('')
        }
    });
    $(formEle + ' select').each(function() {
        if ($(this).val() == '') {
            $(this).val($(this).find("option:first").text())
        }
    });

}

// Check form field is valid or not
function checkValidForm($this) {

    var parentConatiner = $($this).parent();

    if ($($this).data('parent-container') != undefined) {
        parentConatiner = $($this).parents($($this).data('parent-container'));
    }

    if (!formSubmit) {
        // removeError($this, parentConatiner);
        return true;
    }


    var validField = false;

    if ($($this).data('type') == "email") {
        validField = !emailExpr.test($($this).val())
    }
    if ($($this).data('type') == "mobile") {
        validField = !mobileExpr.test($($this).val())
    }
    if ($($this).data('type') == "password") {
        validField = !passwordExpr.test($($this).val())
    }
    if ($($this).data('type') == "onlyalpha") {
        validField = !acceptsOnlyAlphabetsExpr.test($($this).val())
    }
    if ($($this).data('type') == "onlyalphaandnum") {
        validField = !acceptsOnlyAlphabetsandNumExpr.test($($this).val())
    }
    if ($($this).data('type') == "onlynum") {
        validField = !acceptsOnlynumbersExpr.test($($this).val())
    }
    if ($($this).data('type') == "onlyfloatnum") {
        validField = !floatNumbers.test($($this).val())
        if (!validField && !isInvalidString($($this).data('maxvalue')))
            validField = parseFloat($($this).val()) > parseFloat($($this).data('maxvalue'))
    }
    if ($($this).data('type') == "aadhar") {
        validField = !aadharRegularExpr.test($($this).val())
        if (!validField) {
            validField = $($this).val() == "0000 0000 0000";
        }
    }
    if ($($this).data('type') == "zipcode") {
        validField = !zipcodeExpr.test($($this).val())
        if (!validField) {
            validField = $($this).val() == "000000";
        }
    }
    if ($($this).data('type') == "url") {
        validField = !urlExpr.test($($this).val())
    }
    if ($($this).data('type') == "onlyaphaspace") {
        validField = !onlyaphaspace.test($($this).val())
    }
    if ($($this).data('type') == "alphanumwithspace") {
        validField = !acceptsAlphaNumricWithSpace.test($($this).val())
    }
    if ($($this).data('type') == "alphwithspacedot") {
        validField = !acceptsOnlyAlphabetsSpaceDotExpr.test($($this).val())
    }
    if ($($this).data('type') == "fburl") {
        validField = !fbUrlCheck.test($($this).val())
    }
    if ($($this).data('type') == "orgid") {
        validField = !orgID.test($($this).val())
    }
    if ($($this).data('type') == "notacceptzero") {
        validField = (parseInt($($this).val()) <= 0);
    }
    if ($($this).data('type') == "percentage") {
        validField = (parseInt($($this).val()) < 0 || parseInt($($this).val()) > 100);
    }
    if ($($this).data('type') == "checkempty") {
        validField = ($($this).val().trim() == "");
    }
    if ($($this).data('type') == "confirm-password") {
        validField = $($this).val() != $($($this).data('new-password')).val();
    }
    if ($($this).data('type') == "addressfields") {
        validField = !addressfields.test($($this).val())
    }

    if ($($this).hasClass('validateLocal') && $($this).val() === '') {
        removeError($this, parentConatiner);
        return true;
    }

    if (validField || $($this).val() == null || $($this).val() === '' || $($this).val().length == 0 || $($this).val() === 'select') {
        $($this).addClass('placeholderred');
        $($this).siblings().find('button').addClass('placeholderred');

        // if ($($this).data('type') == "password") {
        //   return false;
        // }

        if ($($this).data('label') == undefined) {
            return false;
        }


        var errorMessage = "";

        errorMessage += $($this).data('label');

        if ($($this).val() == null || $($this).val() === '' || $($this).val().length == 0 || $($this).val() === 'select') {
            errorMessage += " required";
        } else {
            if ($($this).data('type') == "password") {
                errorMessage = "Password must contain at least one special, numeric, lower and uppercase alphabetical character. Eg: Strong2@"
            } else if ($($this).data('type') == "confirm-password") {
                errorMessage = "Password and Confirm Password should be match"
            } else {
                errorMessage = "Please enter valid " + errorMessage;
            }
        }

        if (parentConatiner.find('.error_msg').html() != undefined) {
            if (parentConatiner.hasClass('input-group'))
                parentConatiner.parent().find('.error_msg').text(errorMessage);
            else
                parentConatiner.find('.error_msg').text(errorMessage);
        } else {
            if (parentConatiner.hasClass('input-group')) {
                parentConatiner.parent().find('small').remove();
                parentConatiner.parent().append("<small class='error_msg'>" + errorMessage + "</small>")
            } else
                parentConatiner.append("<small class='error_msg'>" + errorMessage + "</small>")
        }
        return false;
    } else {
        removeError($this, parentConatiner);
        return true;
    }
}

// Validate Given Form
function validateForm(formEle) {

    formSubmit = true;

    var isValidForm = true;
    var errorElement = null;

    $(formEle + ' .mandatoryLocal:visible, ' + formEle + ' .validateLocal:visible, ' + formEle + ' select.mandatoryLocal:visible').each(function() {
        if (!checkValidForm($(this))) {
            if (errorElement == null) {
                errorElement = $(this)
            }
            isValidForm = false;
        }
    })

    if (isValidForm) {
        // Valid Data Prepare Payload
    } else {
        $('html, body').animate({
            scrollTop: (errorElement.offset().top - 50)
        }, 500);
    }

    return isValidForm
}

function resetForm(formEle) {

    $(formEle).trigger("reset");
    // $(formEle + ' .multiselect-native-select select').multiselect("clearSelection").multiselect('refresh');
    $(formEle + ' .placeholderred').removeClass('placeholderred')
    $(formEle + ' .error_msg').remove()

}


function removeError($this, parentConatiner) {

    $($this).removeClass('placeholderred');
    $($this).siblings().find('button').removeClass('placeholderred');

    if (parentConatiner.hasClass('input-group') && parentConatiner.parent().find('.error_msg').html() != undefined)
        parentConatiner.parent().find('.error_msg').remove();
    else if (parentConatiner.find('.error_msg').html() != undefined) {
        parentConatiner.find('.error_msg').remove();
    }

    if (parentConatiner.hasClass('input-group') && parentConatiner.parent().find('.error_msg').html() != undefined)
        parentConatiner.parent().find('.error_msg').remove();
    else if (parentConatiner.find('.error_msg').html() != undefined) {
        parentConatiner.find('.error_msg').remove();
    }

}
/**********************************************
 *   Form Field Validations END
 *********************************************/




/**********************************************
 *   DropDown Utility Functions START
 ***********************************************/
function getDropdownsFromAPI(payload, completionCallback) {

    $.ajax({
        type: "Get",
        url: baseUrl + payload.apiUrl,
        dataType: 'json',
        global: false,
        success: function(data) {

            if (payload.withOptions) {
                var html = ''
                if (payload.placeholder != null)
                    html += '<option value="">' + payload.placeholder + '</option>';
                $.each(data, function(index, obj) {
                    html += '<option value="' + obj.id + '">' + obj.title + '</option>';
                });
                completionCallback(html);
            } else {
                completionCallback(data);
            }

        },
        error: function(data, textStatus, jqXHR) {
            errorHandledCallBack(data, textStatus, jqXHR, function() {
                completionCallback(null);
            })
        }
    });
}

function setDropdownsWith(payload, completionCallback) {

    var html = ''
    if (payload.placeholder != null)
        html += '<option value="">' + payload.placeholder + '</option>';
    $.each(payload.data, function(index, obj) {
        html += '<option value="' + obj.id + '">' + obj.title + '</option>';
    });
    completionCallback(html);

}



/**********************************************
 *   DropDown Utility Functions END
 ***********************************************/

//states list


function getStates() {
    if (!isInvalidString(localStorage.getItem("organizationId"))) {
        $.ajax({
            url: baseUrl + 'orders/states',
            type: 'GET',
            contentType: "application/json",
            dataType: 'json',
            success: function(result) {
                if (result.status == 'success') {
                    statesList = result.data

                    statesList.forEach((state) => {
                        statesEnum[state.code] = state.name
                    })
                    console.log(statesList)
                }
            },
            error: function(data, textStatus, jqXHR) {
                // errorCallBack(widgetContainer, data, textStatus, jqXHR)
            }
        });
    }

}



// ****************************************************************** //
// **************        Ajax Spinner Start      **************** //
// ****************************************************************** //

// start the ajac call spinner
jQuery(document).ajaxStart(function () {
  //show ajax indicator
  ajaxindicatorstart('please wait...');
}).ajaxStop(function () {
  //hide ajax indicator
 ajaxindicatorstop();
});


// start ajax call start spinner
function ajaxindicatorstart(text) {
  if (jQuery('body').find('#resultLoading').attr('id') != 'resultLoading') {

      jQuery('body').append('<div id="resultLoading" style="display:none"><div><div class="spinner-border text-primary" style="color: #393381!important;" role="status"></div><div></div></div><div class="bg-t"></div></div>');

  }

  jQuery('#resultLoading').css({
      'width': '100%',
      'height': '100%',
      'position': 'fixed',
      'z-index': '10000000',
      'top': '0',
      'left': '0',
      'right': '0',
      'bottom': '0',
      'margin': 'auto'
  });
  jQuery('.spinner_bg').css({
      'position': 'absolute',
      'left': '50%',
      'top': '50%',
      "width": '40px',
      'transform': 'translate( -50%,-50%)'

  });
  jQuery('.img-spinner').css({
      'width': '120px',
      'height': '120px',
      'transition-property': 'transform',
      'transition-duration': '1s',
      'animation-name': 'rotate',
      'animation-duration': '1s',
      'animation-iteration-count': 'infinite',
      'animation-timing-function': 'linear',
      'margin-top': '5%'

  });
  jQuery('#resultLoading .bg').css({
      'background': '#000000',
      'opacity': '0',
      'width': '100%',
      'height': '100%',
      'position': 'absolute',
      'top': '0'
  });
  jQuery('#resultLoading>div:first').css({
      'width': '90px',
      'height': '90px',
      'text-align': 'center',
      'position': 'fixed',
      'top': '0',
      'left': '0',
      'right': '0',
      'bottom': '0',
      'margin': 'auto',
      'font-size': '16px',
      'z-index': '10',
      'color': '#ffffff',
      'border-radius': '5px',
      'margin-top': '250px',
      //   'background-color': 'rgba(0,0,0,0.5)',
      'color': 'rgb(255, 255, 255)'

  });
  jQuery('#resultLoading .bg').height('100%');
  jQuery('#resultLoading').fadeIn(300);
  jQuery('body').css('cursor', 'wait');
}

// end ajax call spinner
function ajaxindicatorstop() {
  jQuery('#resultLoading .bg').height('100%');
  jQuery('#resultLoading').fadeOut('slow');
  jQuery('body').css('cursor', 'default');
}

// ****************************************************************** //
// **************        Ajax Spinner End        **************** //
// ****************************************************************** //

// AJAX API CALL ERROR HANDLING
function showCartsCountWidget() {
  // var widgetContainer = '.shopping_cart_a'
  alert("it is cart count")
  var cartProcucts = sessionStorage.getItem("cartProcucts");
  if(isInvalidString(cartProcucts)) {
    cartProcucts = []
  } else {
    cartProcucts = JSON.parse(cartProcucts)
  }
  $( '.cart_count').text(cartProcucts.length)
  if(cartProcucts.length > 0) {
      jQuery(widgetContainer).addClass('d-inline');
      jQuery(widgetContainer).css('color: #000');
  } else {
      jQuery(widgetContainer).removeClass('d-inline');
  }
}