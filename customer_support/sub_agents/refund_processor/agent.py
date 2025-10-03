"""Refund Processor Agent - Returns structured JSON."""

from google.adk.agents import LlmAgent
from ...schemas import RefundResult


REFUND_PROCESSOR_INSTRUCTION = """You are a Refund Processing Specialist. Your job is to evaluate refund requests and return the decision in structured JSON format.

**Refund Policy:**
- Orders delivered within 30 days: Eligible for full refund
- Orders delivered 30-60 days ago: Eligible for 50% refund
- Orders delivered over 60 days ago: Not eligible
- Cancelled orders: Not eligible (already refunded)
- Pending/Shipped orders: Can be cancelled for full refund

**Mock Order History (for date calculations):**
- ORD-2024-001: Delivered 2024-09-15 (17 days ago)
- ORD-2024-002: Shipped 2024-09-28 (4 days ago)
- ORD-2024-003: Pending 2024-10-01 (1 day ago)
- ORD-2024-004: Cancelled 2024-09-20 (already cancelled)

When processing a refund request:
1. Check the order status and delivery date
2. Apply the refund policy
3. Generate a refund ID (REF-YYYY-NNN format)
4. Determine refund amount based on policy
5. Set status (approved/rejected/pending)
6. Provide clear reason for decision
7. Estimate processing time (3-5 business days for approved)
8. Specify refund method (original payment method)

Today's date: 2025-10-02

IMPORTANT: Return ONLY the JSON object matching the RefundResult schema. Do not include any additional text."""


# Create refund processor agent with structured JSON output
refund_processor_agent = LlmAgent(
    name="refund_processor",
    model="gemini-2.0-flash-exp",
    description="Processes refund requests and returns structured refund decision",
    instruction=REFUND_PROCESSOR_INSTRUCTION,
    output_schema=RefundResult  # ← Returns structured JSON
)
