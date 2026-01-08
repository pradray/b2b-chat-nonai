# ============================================
# KNOWLEDGE BASE (Data Layer)
# ============================================

# Intent definitions with synonyms
INTENT_MAP = {
    # Navigation
    "NAV_MARKETPLACE": ["marketplace", "market", "browse", "products", "items", "shop"],
    "NAV_SUPPLIER":    ["supplier", "suppliers", "vendor", "manufacturer", "factory", "vendors"],
    "NAV_RFQ":         ["rfq", "request for quote", "bulk quote", "estimate", "quotation"],
    "NAV_QUOTE":       ["quote", "pricing", "cost estimation", "price quote"], 
    "NAV_LOGIN":       ["login", "sign in", "log in", "credentials", "account"],
    "NAV_REGISTER":    ["register", "signup", "sign up", "join", "create account", "new account"],

    # Business Logic
    "INFO_MOQ":        ["moq", "minimum order", "min qty", "smallest order", "minimum quantity"],
    "INFO_PRICE":      ["price", "cost", "rates", "pricing", "how much", "what does it cost"],
    "INFO_BULK":       ["bulk", "volume discount", "large order", "wholesale", "bulk discount"],
    "INFO_SHIPPING":   ["shipping", "freight", "transport", "delivery", "logistics", "ship"],
    "INFO_TRACK":      ["track", "tracking", "status", "shipment", "where is my order"],
    "INFO_INVOICE":    ["invoice", "bill", "receipt", "commercial invoice", "billing"],
    "INFO_PAYMENT":    ["payment", "pay", "bank details", "wire transfer", "payment methods"],
    "INFO_CREDIT":     ["credit", "payment terms", "net 30", "credit line", "credit terms"],
    "INFO_CATALOG":    ["catalog", "brochure", "pdf", "product list", "catalogue"],
    "INFO_RETURN":     ["return", "refund", "rma", "exchange", "damaged", "return policy"],
    "INFO_LEADTIME":   ["lead time", "how long", "turnaround", "wait time", "delivery time"],
    "INFO_SAMPLE":     ["sample", "prototype", "test unit", "samples"],
    "INFO_STOCK":      ["stock", "inventory", "available", "quantity on hand", "in stock"],
    "INFO_WARRANTY":   ["warranty", "guarantee", "repair", "warranty policy"],
    "INFO_CUSTOMS":    ["customs", "duty", "tax", "tariffs", "import", "duties"],

    # Greetings & Help
    "GREETING":        ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"],
    "HELP":            ["help", "support", "assist", "stuck", "what can you do", "options"]
}

# Response definitions
RESPONSE_MAP = {
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
    "GREETING":        {"msg": "Welcome to B2B Hub! I can help with orders, shipping, pricing, and navigation. What do you need?", "act": None},
    "HELP":            {"msg": "I can help you with: MOQ info, Pricing, Shipping, Tracking, and Navigation. Try asking about any of these!", "act": None}
}

FALLBACK_RESPONSE = {
    "msg": "I'm not sure about that. Contact admin for advanced queries.",
    "act": None
}