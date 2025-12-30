import json

def lambda_handler(event, context):
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
        
    user_text = body.get('message', '').lower()
    
    response_data = {
        "message": "I didn't catch that. Contact admin for help.",
        "action": None
    }

    # --- KNOWLEDGE BASE (30+ B2B Keywords) ---
    keywords = {
        # Navigation Triggers (SPA)
        "marketplace": {"msg": "Opening the Wholesale Marketplace...", "act": "marketplace"},
        "supplier":    {"msg": "Here is our list of verified manufacturers.", "act": "suppliers"},
        "rfq":         {"msg": "Opening the Bulk Request for Quote form.", "act": "rfq"},
        "quote":       {"msg": "Please fill out the RFQ form for custom pricing.", "act": "rfq"},
        "login":       {"msg": "Redirecting to Partner Login...", "act": "login"},
        "register":    {"msg": "New partners can register via the Login page.", "act": "login"},

        # Business Logic
        "moq":         {"msg": "Standard MOQ is 50 units. Custom runs require 500 units.", "act": None},
        "price":       {"msg": "Login to see Tier-1 wholesale pricing.", "act": "login"},
        "bulk":        {"msg": "Orders >1000 units get a 15% volume discount.", "act": None},
        "shipping":    {"msg": "We ship FOB and EXW via Maersk or DHL.", "act": None},
        "track":       {"msg": "Enter your PO Number in the chat to track.", "act": None},
        "invoice":     {"msg": "Invoices are emailed automatically upon dispatch.", "act": None},
        "payment":     {"msg": "We accept Net-30, LC, and TT.", "act": None},
        "credit":      {"msg": "Apply for a credit line in your dashboard.", "act": None},
        "catalog":     {"msg": "The Q4 Catalog is available in the 'Resources' tab.", "act": None},
        "return":      {"msg": "RMA requests are valid for 14 days post-delivery.", "act": None},
        "lead time":   {"msg": "Current manufacturing lead time is 14 days.", "act": None},
        "sample":      {"msg": "Paid samples are available. Contact sales.", "act": None},
        "stock":       {"msg": "Live inventory is updated every 4 hours.", "act": None},
        "warranty":    {"msg": "Industrial parts carry a 1-year manufacturer warranty.", "act": None},
        "customs":     {"msg": "Buyer is responsible for import duties.", "act": None},
        
        # Greetings
        "hello":       {"msg": "Welcome to B2B Hub. How can I assist?", "act": None},
        "hi":          {"msg": "Hello! Need help with sourcing?", "act": None},
        "help":        {"msg": "I can navigate you or answer questions about MOQ/Shipping.", "act": None}
    }

    match_found = False
    for key, data in keywords.items():
        if key in user_text:
            response_data["message"] = data["msg"]
            response_data["action"] = data["act"]
            match_found = True
            break
            
    if not match_found:
        response_data["message"] = "I can't help with that specific query. Please contact support@b2bhub.com."

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(response_data)
    }