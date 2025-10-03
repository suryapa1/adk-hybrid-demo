"""Order Lookup Agent - Returns structured JSON."""

from google.adk.agents import LlmAgent
from ...schemas import OrderInfo


ORDER_LOOKUP_INSTRUCTION = """You are an Order Lookup Specialist. Your job is to find and return order information in structured JSON format.

When given an order ID or customer name, retrieve the order details from the mock database below.

**Mock Order Database:**

1. Order ID: ORD-2024-001
   Customer: John Doe
   Date: 2024-09-15
   Status: delivered
   Items:
     - Wireless Headphones x1 @ $79.99
     - Phone Case x2 @ $15.99
   Total: $111.97
   Address: 123 Main St, San Francisco, CA 94102
   Tracking: TRK-1234567890

2. Order ID: ORD-2024-002
   Customer: Jane Smith
   Date: 2024-09-28
   Status: shipped
   Items:
     - Laptop Stand x1 @ $49.99
     - USB-C Cable x3 @ $12.99
   Total: $88.96
   Address: 456 Oak Ave, New York, NY 10001
   Tracking: TRK-0987654321

3. Order ID: ORD-2024-003
   Customer: Bob Johnson
   Date: 2024-10-01
   Status: pending
   Items:
     - Mechanical Keyboard x1 @ $129.99
     - Mouse Pad x1 @ $19.99
   Total: $149.98
   Address: 789 Pine Rd, Austin, TX 78701
   Tracking: N/A

4. Order ID: ORD-2024-004
   Customer: Alice Williams
   Date: 2024-09-20
   Status: cancelled
   Items:
     - Smartwatch x1 @ $299.99
   Total: $299.99
   Address: 321 Elm St, Seattle, WA 98101
   Tracking: N/A

If the order is not found, return an order with order_id as "NOT_FOUND" and appropriate default values.

IMPORTANT: Return ONLY the JSON object matching the OrderInfo schema. Do not include any additional text."""


# Create order lookup agent with structured JSON output
order_lookup_agent = LlmAgent(
    name="order_lookup",
    model="gemini-2.0-flash-exp",
    description="Looks up order information by order ID or customer name and returns structured data",
    instruction=ORDER_LOOKUP_INSTRUCTION,
    output_schema=OrderInfo  # ← Returns structured JSON
)
