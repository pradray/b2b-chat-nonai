import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def lambda_handler(event, context):
    # 1. Parse Input
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
        
    user_text = body.get('message', '').lower()
    
    # --- STEP 1: DEFINE INTENTS (Synonym Mapping) ---
    # Mapping the user's potential inputs (including synonyms) to a specific Intent ID.
    intent_map = {
        # Navigation
        "NAV_MARKETPLACE": ["marketplace", "market", "browse", "products", "items"],
        "NAV_SUPPLIER":    ["supplier", "suppliers", "vendor", "manufacturer", "factory"],
        "NAV_RFQ":         ["rfq", "request for quote", "bulk quote", "estimate"],
        "NAV_QUOTE":       ["quote", "pricing", "cost estimation"], 
        "NAV_LOGIN":       ["login", "sign in", "log in", "credentials"],
        "NAV_REGISTER":    ["register", "signup", "sign up", "join", "create account"],

        # Business Logic (15 core B2B keywords)
        "INFO_MOQ":        ["moq", "minimum order", "min qty", "smallest order"],
        "INFO_PRICE":      ["price", "cost", "rates", "pricing", "how much"],
        "INFO_BULK":       ["bulk", "volume discount", "large order", "wholesale"],
        "INFO_SHIPPING":   ["shipping", "freight", "transport", "delivery", "logistics"],
        "INFO_TRACK":      ["track", "tracking", "status", "shipment"],
        "INFO_INVOICE":    ["invoice", "bill", "receipt", "commercial invoice"],
        "INFO_PAYMENT":    ["payment", "pay", "bank details", "wire transfer"],
        "INFO_CREDIT":     ["credit", "payment terms", "net 30", "credit line"],
        "INFO_CATALOG":    ["catalog", "brochure", "pdf", "product list"],
        "INFO_RETURN":     ["return", "refund", "rma", "exchange", "damaged"],
        "INFO_LEADTIME":   ["lead time", "how long", "turnaround", "wait time"],
        "INFO_SAMPLE":     ["sample", "prototype", "test unit"],
        "INFO_STOCK":      ["stock", "inventory", "available", "quantity on hand"],
        "INFO_WARRANTY":   ["warranty", "guarantee", "repair"],
        "INFO_CUSTOMS":    ["customs", "duty", "tax", "tariffs", "import"],

        # Greetings & Help
        "GREETING":        ["hello", "hi", "hey", "greetings", "good morning"],
        "HELP":            ["help", "support", "assist", "stuck", "what can you do"]
    }

    # --- STEP 2: DEFINED RESPONSES ---
    response_map = {
        # Navigation
        "NAV_MARKETPLACE": {"msg": "Opening the Wholesale Marketplace...", "act": "marketplace"},
        "NAV_SUPPLIER":    {"msg": "Here is our list of verified manufacturers.", "act": "suppliers"},
        "NAV_RFQ":         {"msg": "Opening the Bulk Request for Quote form.", "act": "rfq"},
        "NAV_QUOTE":       {"msg": "Please fill out the RFQ form for custom pricing.", "act": "rfq"},
        "NAV_LOGIN":       {"msg": "Redirecting to Partner Login...", "act": "login"},
        "NAV_REGISTER":    {"msg": "New partners can register via the Login page.", "act": "login"},

        # Business Logic
        "INFO_MOQ":        {"msg": "Standard MOQ is 50 units. Custom runs require 500 units.", "act": None},
        "INFO_PRICE":      {"msg": "Login to see Tier-1 wholesale pricing.", "act": "login"},
        "INFO_BULK":       {"msg": "Orders >1000 units get a 15% volume discount.", "act": None},
        "INFO_SHIPPING":   {"msg": "We ship FOB and EXW via Maersk or DHL.", "act": None},
        "INFO_TRACK":      {"msg": "Enter your PO Number in the chat to track.", "act": None},
        "INFO_INVOICE":    {"msg": "Invoices are emailed automatically upon dispatch.", "act": None},
        "INFO_PAYMENT":    {"msg": "We accept Net-30, LC, and TT.", "act": None},
        "INFO_CREDIT":     {"msg": "Apply for a credit line in your dashboard.", "act": None},
        "INFO_CATALOG":    {"msg": "The Q4 Catalog is available in the 'Resources' tab.", "act": None},
        "INFO_RETURN":     {"msg": "RMA requests are valid for 14 days post-delivery.", "act": None},
        "INFO_LEADTIME":   {"msg": "Current manufacturing lead time is 14 days.", "act": None},
        "INFO_SAMPLE":     {"msg": "Paid samples are available. Contact sales.", "act": None},
        "INFO_STOCK":      {"msg": "Live inventory is updated every 4 hours.", "act": None},
        "INFO_WARRANTY":   {"msg": "Industrial parts carry a 1-year manufacturer warranty.", "act": None},
        "INFO_CUSTOMS":    {"msg": "Buyer is responsible for import duties.", "act": None},

        # Greetings & Help
        "GREETING":        {"msg": "Welcome to B2B Hub. How can I assist?", "act": None},
        "HELP":            {"msg": "I can navigate you or answer questions about MOQ/Shipping.", "act": None}
    }

    # --- STEP 3: DETECT INTENT (Fuzzy Logic) ---
    detected_intent = None
    highest_score = 0
    
    # Check user input against all synonyms in the intent_map
    for intent, phrases in intent_map.items():
        # process.extractOne finds the best match in the list of synonyms
        best_match, score = process.extractOne(user_text, phrases, scorer=fuzz.partial_ratio)
        
        if score > highest_score:
            highest_score = score
            detected_intent = intent

    # --- STEP 4: GENERATE RESPONSE ---
    # Use a threshold (e.g., 75) to avoid false positives on random text
    if detected_intent and highest_score >= 75:
        data = response_map[detected_intent]
        response_data = {
            "message": data["msg"],
            "action": data["act"],
            "debug_intent": detected_intent
        }
    else:
        # Fallback for unrecognized inputs
        response_data = {
            "message": "I'm not sure about that. Please contact admin for advanced queries.",
            "action": None
        }

    # --- STEP 5: RETURN RESPONSE ---
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(response_data)
    }