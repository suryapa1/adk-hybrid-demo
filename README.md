# ADK Hybrid Multi-Agent Demo - Customer Support System

## Overview

This demo showcases a **hybrid multi-agent architecture** where:

1. **Main agent** can handle tasks directly (FAQs, policies, greetings)
2. **Main agent** delegates to specialized sub-agents when needed
3. **Different sub-agents return different response types**:
   - Some return **structured JSON** (order lookup, refund processor)
   - Some return **plain text** (tech support)
4. **Main agent handles both response types** seamlessly

## Use Case: Customer Support Agent

A realistic e-commerce customer support system that demonstrates production-ready patterns.

## Architecture

```
Customer Query
    ↓
Main Agent (customer_support)
    ↓
Decision: Can I handle this directly?
    ↓
├─ YES → Answer directly (FAQs, policies, greetings)
│
└─ NO → Delegate to sub-agent
        ↓
        ├─ order_lookup (Returns JSON)
        │   - OrderInfo schema
        │   - Status, items, tracking
        │
        ├─ refund_processor (Returns JSON)
        │   - RefundResult schema
        │   - Approval, amount, reason
        │
        └─ tech_support (Returns Text)
            - Conversational guidance
            - Troubleshooting steps
```

## Agent Capabilities

### Main Agent (Direct Capabilities)

Can answer WITHOUT using sub-agents:
- ✅ Greetings and small talk
- ✅ Store hours
- ✅ Shipping policy
- ✅ Return policy  
- ✅ Payment methods
- ✅ General FAQs
- ✅ Thank you / goodbye

### Sub-Agent 1: Order Lookup (JSON)

**Returns:** Structured `OrderInfo` JSON

**Capabilities:**
- Look up order by ID or customer name
- Return order status, items, total
- Provide tracking information

**Example Response:**
```json
{
  "order_id": "ORD-2024-001",
  "customer_name": "John Doe",
  "status": "delivered",
  "items": [...],
  "total_amount": 111.97,
  "tracking_number": "TRK-1234567890"
}
```

### Sub-Agent 2: Refund Processor (JSON)

**Returns:** Structured `RefundResult` JSON

**Capabilities:**
- Process refund requests
- Apply refund policy rules
- Generate refund decision

**Example Response:**
```json
{
  "refund_id": "REF-2024-001",
  "status": "approved",
  "refund_amount": 111.97,
  "reason": "Within 30-day return window",
  "processing_time": "3-5 business days"
}
```

### Sub-Agent 3: Tech Support (Plain Text)

**Returns:** Conversational text response

**Capabilities:**
- Troubleshoot product issues
- Provide step-by-step guidance
- Offer technical solutions

**Example Response:**
```
I can help you with your wireless headphones pairing issue! 
Here's what to try:

1. Reset your headphones by holding the power button for 10 seconds
2. Put them in pairing mode (LED should flash blue)
3. On your device, forget the previous Bluetooth connection
4. Search for new devices and select your headphones

Let me know if this works!
```

## How Main Agent Handles Different Response Types

### Handling JSON Responses

When `order_lookup` or `refund_processor` returns JSON:

```python
# Main agent receives structured data
order_info = {
    "order_id": "ORD-2024-001",
    "status": "delivered",
    "tracking_number": "TRK-1234567890"
}

# Main agent extracts and presents naturally
"Great news! Your order ORD-2024-001 has been delivered. 
You can track it with TRK-1234567890."
```

### Handling Text Responses

When `tech_support` returns text:

```python
# Main agent receives conversational text
tech_response = "Try resetting by holding power for 10 seconds..."

# Main agent relays it naturally
"Here's what our tech specialist recommends:
Try resetting by holding power for 10 seconds..."
```

## Project Structure

```
adk-hybrid-demo/
├── customer_support/
│   ├── __init__.py
│   ├── agent.py                      # Main hybrid agent
│   ├── schemas.py                    # Pydantic models
│   └── sub_agents/
│       ├── __init__.py
│       ├── order_lookup/
│       │   ├── __init__.py
│       │   └── agent.py              # Returns JSON
│       ├── refund_processor/
│       │   ├── __init__.py
│       │   └── agent.py              # Returns JSON
│       └── tech_support/
│           ├── __init__.py
│           └── agent.py              # Returns text
├── pyproject.toml
├── .env
└── README.md
```

## Setup

### Prerequisites
- Python 3.11+
- Poetry
- Google Gemini API key (already configured)

### Installation

```bash
cd adk-hybrid-demo
poetry install
```

## Running the Demo

### ADK Web UI (Recommended)

```bash
poetry run adk web --host 0.0.0.0 --port 8002
```

Then open your browser to the provided URL.

## Test Queries

### Direct Responses (No Sub-Agent)

1. **"Hello, how are you?"**
   - Main agent responds directly with greeting

2. **"What are your store hours?"**
   - Main agent responds: "We're open 24/7 online..."

3. **"What's your shipping policy?"**
   - Main agent responds: "Free shipping on orders over $50..."

4. **"What payment methods do you accept?"**
   - Main agent responds: "We accept Visa, Mastercard..."

### Order Lookup (JSON Sub-Agent)

5. **"Check order ORD-2024-001"**
   - Delegates to order_lookup
   - Receives JSON
   - Presents: "Your order has been delivered..."

6. **"Where is my order ORD-2024-002?"**
   - Delegates to order_lookup
   - Receives JSON with tracking
   - Presents: "Your order is shipped, tracking: TRK-..."

7. **"What's the status of order ORD-2024-003?"**
   - Delegates to order_lookup
   - Receives JSON
   - Presents: "Your order is pending..."

### Refund Processing (JSON Sub-Agent)

8. **"I want a refund for order ORD-2024-001"**
   - Delegates to refund_processor
   - Receives JSON with decision
   - Presents: "Your refund has been approved..."

9. **"Can I return order ORD-2024-004?"**
   - Delegates to refund_processor
   - Receives JSON with rejection
   - Presents: "This order was already cancelled..."

### Technical Support (Text Sub-Agent)

10. **"My wireless headphones won't pair"**
    - Delegates to tech_support
    - Receives conversational text
    - Presents: "Here's how to fix that..."

11. **"My keyboard keys are sticking"**
    - Delegates to tech_support
    - Receives troubleshooting steps
    - Presents: "Try these steps..."

12. **"My laptop stand is wobbly"**
    - Delegates to tech_support
    - Receives technical guidance
    - Presents: "Let's fix that..."

## Mock Data

### Orders
- **ORD-2024-001** - John Doe, delivered, $111.97
- **ORD-2024-002** - Jane Smith, shipped, $88.96
- **ORD-2024-003** - Bob Johnson, pending, $149.98
- **ORD-2024-004** - Alice Williams, cancelled, $299.99

### Products
- Wireless Headphones
- Laptop Stand
- Mechanical Keyboard
- Smartwatch
- Phone Case
- USB-C Cable
- Mouse Pad

## Key Features Demonstrated

### 1. Hybrid Decision Making
- Main agent decides: handle directly or delegate
- Intelligent routing based on query type
- No unnecessary tool calls

### 2. Mixed Response Types
- JSON from order_lookup and refund_processor
- Text from tech_support
- Main agent handles both seamlessly

### 3. Natural Presentation
- Extracts data from JSON responses
- Relays text responses naturally
- Always conversational and friendly

### 4. Production-Ready Patterns
- Clear separation of concerns
- Reusable sub-agents
- Structured schemas
- Error handling

## Code Patterns

### Sub-Agent with JSON Output

```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel

class MySchema(BaseModel):
    field1: str
    field2: int

agent = LlmAgent(
    name="my_agent",
    output_schema=MySchema  # ← Returns JSON
)
```

### Sub-Agent with Text Output

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="my_agent"
    # ← No output_schema = returns text
)
```

### Main Agent with Multiple Tools

```python
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

tool1 = AgentTool(agent=json_agent)
tool2 = AgentTool(agent=text_agent)

main_agent = LlmAgent(
    name="main",
    tools=[tool1, tool2],
    instruction="Use tool1 for X, tool2 for Y, answer directly for Z"
)
```

## Observability

### In ADK Web UI

**Trace Tab:**
- See when main agent answers directly
- See when tools are invoked
- See tool responses (JSON or text)

**Events Tab:**
- Detailed execution log
- LLM calls
- Tool invocations

**State Tab:**
- Session state
- Tool results

## Benefits of Hybrid Approach

### 1. Efficiency
- No tool overhead for simple queries
- Only delegate when necessary
- Faster responses for FAQs

### 2. Flexibility
- Main agent adapts to query type
- Can handle diverse scenarios
- Easy to add new capabilities

### 3. Scalability
- Add new sub-agents easily
- Sub-agents are independent
- Clear responsibility boundaries

### 4. User Experience
- Consistent conversational tone
- Natural responses regardless of source
- Seamless integration of different data types

## When to Use This Pattern

✅ **Perfect For:**
- Customer support systems
- Multi-capability assistants
- Systems with both simple and complex queries
- Applications needing structured and unstructured responses

❌ **Not Ideal For:**
- Simple single-purpose agents
- Fixed sequential workflows
- Systems where all queries need same processing

## Extending the Demo

### Add New Sub-Agent

1. Create new agent file
2. Define output schema (or leave blank for text)
3. Wrap as AgentTool
4. Add to main agent's tools list
5. Update main agent instruction

### Add New Direct Capability

1. Update main agent instruction
2. Add examples and guidelines
3. No code changes needed!

### Connect to Real Services

1. Replace mock data with API calls
2. Add database queries
3. Integrate with external systems
4. Add authentication

## Production Considerations

### Error Handling
- Main agent handles tool failures gracefully
- Fallback to direct responses
- Clear error messages to users

### Performance
- Cache common queries
- Optimize tool selection logic
- Monitor response times

### Security
- Validate user inputs
- Sanitize tool responses
- Implement rate limiting
- Add authentication

### Monitoring
- Track tool usage patterns
- Monitor response quality
- Log errors and failures
- Analyze user satisfaction

## Deployment

### Cloud Run
```bash
# Build Docker image
docker build -t customer-support-agent .

# Deploy to Cloud Run
gcloud run deploy customer-support \
  --image customer-support-agent \
  --platform managed
```

### Google Agent Engine
- Recommended for production
- Built-in scaling
- Integrated monitoring
- Easy deployment

## Conclusion

This demo shows a **production-ready hybrid pattern** where:

✅ Main agent has direct capabilities  
✅ Main agent delegates to specialists when needed  
✅ Sub-agents return different types (JSON and text)  
✅ Main agent handles all response types seamlessly  
✅ Natural, conversational user experience  
✅ Efficient, flexible, scalable architecture  

Perfect for real-world customer support and multi-capability agent systems!
