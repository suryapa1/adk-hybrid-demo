# Hybrid Multi-Agent Pattern - Complete Guide

## Overview

This guide explains the **hybrid multi-agent pattern** demonstrated in this project, where a main agent can:

1. **Handle tasks directly** (FAQs, policies, greetings)
2. **Delegate to specialized sub-agents** when needed
3. **Handle different response types** (JSON and text) from sub-agents seamlessly

## The Problem This Solves

In real-world applications, you often need an agent that:

- Can answer simple questions immediately (efficiency)
- Can delegate complex tasks to specialists (accuracy)
- Works with different data types and formats (flexibility)
- Provides consistent user experience (quality)

**Traditional approaches have limitations:**

- **All tool-based**: Inefficient for simple queries, unnecessary overhead
- **All direct**: Can't handle specialized tasks requiring structured data
- **Single response type**: Inflexible, can't handle diverse scenarios

## The Hybrid Solution

### Architecture

```
User Query
    ↓
Main Agent (Intelligent Router)
    ↓
Decision Point
    ↓
├─ Direct Response
│  └─ Answer from own knowledge
│     (FAQs, policies, greetings)
│
├─ JSON Sub-Agent
│  ├─ Returns structured data
│  └─ Main agent extracts and formats
│     (order lookup, refund processing)
│
└─ Text Sub-Agent
   ├─ Returns conversational text
   └─ Main agent relays naturally
      (technical support, guidance)
```

### Three Response Patterns

#### Pattern 1: Direct Response

**When:** Query can be answered from main agent's knowledge

**Example:** "What are your store hours?"

**Flow:**
```
User → Main Agent → Direct Answer → User
```

**Benefits:**
- ✅ Fastest response time
- ✅ No tool overhead
- ✅ Efficient for common queries

**Implementation:**
```python
MAIN_AGENT_INSTRUCTION = """
You can directly answer these types of questions WITHOUT using tools:
- Greetings and general conversation
- Store hours: "We're open 24/7 online..."
- Shipping policy: "Free shipping on orders over $50..."
- Payment methods: "We accept Visa, Mastercard..."
"""
```

#### Pattern 2: JSON Sub-Agent

**When:** Need structured data (orders, refunds, database queries)

**Example:** "Check order ORD-2024-001"

**Flow:**
```
User → Main Agent → JSON Tool → Sub-Agent → JSON Response → Main Agent → Formatted Answer → User
```

**Benefits:**
- ✅ Type-safe structured data
- ✅ Consistent format
- ✅ Easy to validate and process
- ✅ Can be stored or logged

**Implementation:**

**Sub-Agent (Returns JSON):**
```python
from pydantic import BaseModel

class OrderInfo(BaseModel):
    order_id: str
    customer_name: str
    status: str
    items: List[OrderItem]
    total_amount: float

order_lookup_agent = LlmAgent(
    name="order_lookup",
    output_schema=OrderInfo  # ← Returns JSON
)
```

**Main Agent (Processes JSON):**
```python
order_lookup_tool = AgentTool(agent=order_lookup_agent)

main_agent = LlmAgent(
    tools=[order_lookup_tool],
    instruction="""
    When you receive JSON from order_lookup:
    - Extract the relevant information
    - Present it in a natural, conversational way
    - Highlight important details like status and tracking
    """
)
```

**Response Transformation:**

**JSON from sub-agent:**
```json
{
  "order_id": "ORD-2024-001",
  "customer_name": "John Doe",
  "status": "delivered",
  "total_amount": 111.97,
  "tracking_number": "TRK-1234567890"
}
```

**Natural presentation by main agent:**
```
Okay, I have the details for order ORD-2024-001:

• Customer Name: John Doe
• Status: Delivered
• Total Amount: $111.97
• Tracking Number: TRK-1234567890

Is there anything else I can help you with?
```

#### Pattern 3: Text Sub-Agent

**When:** Need conversational guidance (troubleshooting, advice, explanations)

**Example:** "My wireless headphones won't pair"

**Flow:**
```
User → Main Agent → Text Tool → Sub-Agent → Text Response → Main Agent → Relayed Answer → User
```

**Benefits:**
- ✅ Natural conversational flow
- ✅ Flexible formatting
- ✅ Can include examples and steps
- ✅ More human-like interaction

**Implementation:**

**Sub-Agent (Returns Text):**
```python
tech_support_agent = LlmAgent(
    name="tech_support",
    # ← NO output_schema = returns text
    instruction="""
    Provide conversational, helpful technical guidance.
    You do NOT return JSON - just natural, friendly text responses.
    """
)
```

**Main Agent (Relays Text):**
```python
tech_support_tool = AgentTool(agent=tech_support_agent)

main_agent = LlmAgent(
    tools=[tech_support_tool],
    instruction="""
    When you receive text from tech_support:
    - Simply relay the technical guidance to the customer
    - The response is already formatted naturally
    - Add any additional empathy or support as needed
    """
)
```

**Response Flow:**

**Text from sub-agent:**
```
I can help you with your wireless headphones pairing issue! 

First, try resetting your headphones by holding the power button 
for 10 seconds. After the reset, put them in pairing mode and 
search for them on your device.

Let me know if this works!
```

**Relayed by main agent:**
```
Okay, I can help with that! Let's get those headphones paired.

First, have you tried resetting the headphones? Usually, you can 
do this by holding down the power button for about 10 seconds. 
After the reset, try pairing them with your device again.

Let me know if that works, or if you've already tried that!

Is there anything else I can help you with?
```

## Implementation Details

### Main Agent Configuration

```python
MAIN_AGENT_INSTRUCTION = """
You are a Customer Support Agent. You can handle various inquiries.

**Your Direct Capabilities:**
[List what you can answer directly]

**When to Use Tools:**

1. order_lookup - Use when customer asks about orders
   Returns: STRUCTURED JSON
   Handle: Extract and present naturally

2. refund_processor - Use when customer asks about refunds
   Returns: STRUCTURED JSON
   Handle: Extract status, amount, reason

3. tech_support - Use when customer has technical issues
   Returns: PLAIN TEXT
   Handle: Relay the guidance conversationally

**Guidelines:**
- Try to answer directly if you can
- Only use tools when you need specialized information
- When tools return JSON, extract and present data naturally
- When tools return text, relay it conversationally
- Always be friendly and helpful
"""
```

### Tool Wrapping

```python
from google.adk.tools import AgentTool

# Wrap each sub-agent as a tool
order_lookup_tool = AgentTool(agent=order_lookup_agent)
refund_processor_tool = AgentTool(agent=refund_processor_agent)
tech_support_tool = AgentTool(agent=tech_support_agent)

# Main agent with all tools
customer_support_agent = LlmAgent(
    name="customer_support",
    tools=[
        order_lookup_tool,
        refund_processor_tool,
        tech_support_tool
    ],
    instruction=MAIN_AGENT_INSTRUCTION
)
```

## Decision Making Logic

### How Main Agent Decides

The main agent uses its instruction and context to decide:

1. **Can I answer this directly?**
   - Check if query matches direct capabilities
   - If yes: Answer immediately
   - If no: Continue to step 2

2. **Which tool do I need?**
   - Analyze query intent
   - Match to tool descriptions
   - Select appropriate tool

3. **How do I handle the response?**
   - Check response type (JSON or text)
   - Apply appropriate processing
   - Format for user

### Example Decision Trees

**Query: "What are your store hours?"**
```
Can I answer directly? YES
└─ Answer: "We're open 24/7 online..."
```

**Query: "Check order ORD-2024-001"**
```
Can I answer directly? NO
Need tool? YES
Which tool? order_lookup (needs order data)
Response type? JSON
└─ Call tool → Extract JSON → Format → Present
```

**Query: "My keyboard keys are sticking"**
```
Can I answer directly? NO
Need tool? YES
Which tool? tech_support (technical issue)
Response type? Text
└─ Call tool → Relay text → Add empathy
```

## Benefits of Hybrid Pattern

### 1. Efficiency
- **Fast responses** for simple queries (no tool overhead)
- **Specialized processing** only when needed
- **Reduced API calls** and costs

### 2. Flexibility
- **Multiple response types** (JSON, text, direct)
- **Easy to extend** (add new tools or capabilities)
- **Adaptable** to different scenarios

### 3. Maintainability
- **Clear separation** of concerns
- **Independent sub-agents** (easy to test)
- **Modular architecture** (easy to modify)

### 4. User Experience
- **Consistent tone** across all responses
- **Natural conversation** flow
- **Appropriate detail** level for each query type

### 5. Scalability
- **Add new sub-agents** without changing main agent code
- **Update sub-agents** independently
- **Parallel development** possible

## When to Use Each Pattern

### Use Direct Response When:
✅ Information is in main agent's instruction  
✅ Query is common and simple  
✅ No external data needed  
✅ Speed is critical  

**Examples:**
- Store policies
- Business hours
- Payment methods
- Greetings and farewells

### Use JSON Sub-Agent When:
✅ Need structured, validated data  
✅ Data comes from database or API  
✅ Multiple fields to present  
✅ Data might be logged or stored  

**Examples:**
- Order lookups
- Account information
- Transaction history
- Inventory queries
- Refund processing

### Use Text Sub-Agent When:
✅ Need conversational guidance  
✅ Response varies significantly  
✅ Multiple steps or examples needed  
✅ Human-like interaction important  

**Examples:**
- Technical troubleshooting
- How-to guides
- Recommendations
- Explanations
- Creative content

## Best Practices

### 1. Clear Instructions

**DO:**
```python
instruction = """
Use order_lookup when customer asks about:
- Order status
- Tracking information
- Order details

This tool returns STRUCTURED JSON. Extract and present naturally.
"""
```

**DON'T:**
```python
instruction = "Use order_lookup for orders."  # Too vague
```

### 2. Appropriate Tool Selection

**DO:**
- One tool per specialized function
- Clear, distinct purposes
- Descriptive names

**DON'T:**
- One tool for everything
- Overlapping functionality
- Generic names

### 3. Response Handling

**DO:**
```python
# For JSON: Extract and format
"Your order ORD-001 has been delivered. Tracking: TRK-123"

# For text: Relay naturally
"Here's what our tech specialist recommends: [guidance]"
```

**DON'T:**
```python
# For JSON: Don't dump raw JSON
"Here's your order: {\"order_id\": \"ORD-001\", ...}"

# For text: Don't add unnecessary wrapper
"The tech support agent says: [exact copy]"
```

### 4. Error Handling

**DO:**
```python
instruction = """
If a tool fails:
1. Apologize to the customer
2. Offer alternative help
3. Provide fallback information
"""
```

**DON'T:**
- Expose error messages to users
- Give up after first failure
- Blame the tool or system

### 5. Consistent Tone

**DO:**
```python
instruction = """
Always:
- Be friendly and professional
- Use conversational language
- End with "Is there anything else I can help you with?"
"""
```

**DON'T:**
- Switch tone between direct and tool responses
- Be overly formal or robotic
- Forget to close the conversation

## Testing Strategy

### Test All Three Patterns

1. **Direct Response Tests**
   ```
   - "What are your store hours?"
   - "What payment methods do you accept?"
   - "Hello, how are you?"
   ```

2. **JSON Sub-Agent Tests**
   ```
   - "Check order ORD-2024-001"
   - "I want a refund for order ORD-2024-002"
   - "What's the status of my order?"
   ```

3. **Text Sub-Agent Tests**
   ```
   - "My wireless headphones won't pair"
   - "How do I fix a wobbly laptop stand?"
   - "My keyboard keys are sticking"
   ```

### Verify Response Quality

- ✅ Direct responses are accurate
- ✅ JSON data is extracted correctly
- ✅ Text responses are relayed naturally
- ✅ Tone is consistent across all patterns
- ✅ All responses end appropriately

### Check Tool Selection

- ✅ Main agent chooses correct tool
- ✅ No unnecessary tool calls
- ✅ Appropriate fallback behavior
- ✅ Error handling works

## Extending the Pattern

### Adding New Direct Capabilities

1. Update main agent instruction
2. Add examples and guidelines
3. Test with sample queries

**No code changes needed!**

### Adding New JSON Sub-Agent

1. Define Pydantic schema
2. Create sub-agent with `output_schema`
3. Wrap as `AgentTool`
4. Add to main agent's tools list
5. Update main agent instruction

```python
# 1. Define schema
class NewDataSchema(BaseModel):
    field1: str
    field2: int

# 2. Create sub-agent
new_agent = LlmAgent(
    name="new_agent",
    output_schema=NewDataSchema
)

# 3. Wrap as tool
new_tool = AgentTool(agent=new_agent)

# 4. Add to main agent
main_agent = LlmAgent(
    tools=[..., new_tool]
)

# 5. Update instruction
instruction += """
Use new_agent when customer asks about X.
Returns: STRUCTURED JSON
Handle: Extract and present naturally
"""
```

### Adding New Text Sub-Agent

Same process as JSON, but **without** `output_schema`:

```python
new_text_agent = LlmAgent(
    name="new_text_agent"
    # ← No output_schema
)
```

## Production Considerations

### Performance

- **Cache** common direct responses
- **Optimize** tool selection logic
- **Monitor** response times
- **Set timeouts** for tool calls

### Monitoring

- **Track** which pattern is used most
- **Log** tool invocations
- **Measure** user satisfaction
- **Identify** failure patterns

### Security

- **Validate** user inputs
- **Sanitize** tool responses
- **Implement** rate limiting
- **Add** authentication

### Cost Optimization

- **Maximize** direct responses (cheapest)
- **Minimize** unnecessary tool calls
- **Use** appropriate models per agent
- **Cache** expensive operations

## Comparison with Other Patterns

| Pattern | Hybrid | All Tool-Based | All Direct | Session State |
|---------|--------|----------------|------------|---------------|
| **Efficiency** | High | Medium | High | Medium |
| **Flexibility** | High | High | Low | Medium |
| **Complexity** | Medium | High | Low | Medium |
| **Maintenance** | Easy | Medium | Easy | Easy |
| **Scalability** | High | High | Low | Medium |
| **Best For** | Production | Complex workflows | Simple FAQs | Pipelines |

## Real-World Use Cases

### Customer Support (This Demo)
- Direct: FAQs, policies
- JSON: Orders, refunds
- Text: Technical support

### E-commerce Assistant
- Direct: Product categories, shipping info
- JSON: Product details, inventory
- Text: Recommendations, styling advice

### IT Help Desk
- Direct: Password reset links, office hours
- JSON: Ticket status, system status
- Text: Troubleshooting, how-to guides

### Financial Advisor
- Direct: Market hours, account types
- JSON: Account balance, transaction history
- Text: Investment advice, explanations

### Travel Agent
- Direct: Baggage policies, check-in times
- JSON: Flight status, booking details
- Text: Destination recommendations, tips

## Conclusion

The hybrid multi-agent pattern provides:

✅ **Efficiency** - Direct responses when possible  
✅ **Flexibility** - Multiple response types  
✅ **Scalability** - Easy to extend  
✅ **Quality** - Consistent user experience  
✅ **Maintainability** - Clear architecture  

**Perfect for production systems** that need to:
- Handle diverse query types
- Provide fast responses
- Maintain high quality
- Scale easily
- Adapt to changing requirements

This pattern combines the best of all approaches:
- **Speed** of direct responses
- **Structure** of JSON tools
- **Naturalness** of text tools
- **Intelligence** of routing logic

**Result:** A production-ready, user-friendly, efficient multi-agent system! 🚀
