def translate(field, val, default = "Invalid code"):
    try:
        ret = globals()[field].get(val,default)
        print "Translated %s-'%s' to '%s'"%(field,val,ret)
        return "%s (%s)"%(val,ret)
    except KeyError:
        print "Attempt to translate unknown field '%s'. Returning as is."%field
        return val

action_key = { "00":"Published for Opposition",
               "10":"Principal Register",
               "15":"Principal Register - Published Intent to Use",
               "20":"Supplemental Register",
               "30":"Section 12(c)",
               "41":"1st Renewal",
               "42":"2nd Renewal",
               "43":"3rd Renewal",
               "44":"4th Renewal",
               "45":"5th Renewal",
               "46":"6th Renewal",
               "51":"Cancelled Sec. 7(d) - Entire Registration",
               "52":"Cancelled Sec. 7(d) - Less than Total Classes",
               "53":"Cancelled Sec. 8 - Entire Registration",
               "54":"Cancelled Sec. 8 - Less than Total Classes",
               "61":"Cancelled Sec. 37 - Entire Registration",
               "62":"Cancelled Sec. 37 - Less than Total Classes",
               "63":"Cancelled Sec. 18 - Entire Registration",
               "64":"Cancelled Sec. 18 - Less than Total Classes",
               "65":"Cancelled Sec. 24 - Entire Registration",
               "66":"Cancelled Sec. 24 - Less than Total Classes",
               "67":"Inadvertently Issued Registration Number",
               "70":"Amended",
               "71":"Restricted",
               "80":"Corrected",
               "90":"New Certificate",
               "IB":"Used as a basis for filing a Madrid International Request",
               "NA":"New application filed", # Modified
               "TX":"Application modified" # Modified
               } 
