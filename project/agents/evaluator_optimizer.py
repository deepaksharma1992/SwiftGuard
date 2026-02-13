"""
Evaluator-Optimizer Pattern for SWIFT Message Validation

This module implements iterative validation and correction of SWIFT messages.
The evaluator identifies issues, and the optimizer corrects them.
"""

from typing import Dict, List, Any, Tuple
from agents.workflow_agents.base_agents import SwiftCorrectionAgent
from config import Config
from agents.workflow_agents.base_agents import EvaluatorAgent


class EvaluatorOptimizerPattern:
    """
    Implements the evaluator-optimizer pattern for SWIFT message processing.

    This pattern:
    1. Evaluates messages for compliance with SWIFT standards
    2. Optimizes (corrects) any identified issues
    3. Re-evaluates to ensure corrections are valid
    4. Repeats up to MAX_ITERATIONS times
    """

    def __init__(self):
        """Initialize the evaluator-optimizer pattern."""
        self.config = Config()
        self.MAX_ITERATIONS = 3
        self.correction_agent = SwiftCorrectionAgent()
        self.evaluator_agent = EvaluatorAgent()

        # SWIFT validation rules
        self.SWIFT_STANDARDS = {
            "max_reference_length": 16,
            "max_amount": 999999999.99,
            "min_amount": 0.01,
            "required_fields": [
                "message_type", "reference", "amount",
                "sender_bic", "receiver_bic"
            ],
            "valid_message_types": ["MT103", "MT202"],
            "valid_currencies": ["USD", "EUR", "GBP", "JPY", "CHF"]
        }

    def evaluate_message(self, message: Dict) -> Tuple[bool, List[str]]:
        """
        Evaluate a SWIFT message for compliance with standards.

        Args:
            message: SWIFT message to evaluate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        result = self.evaluator_agent.evaluate(message)
        return result["is_valid"], result.get("errors", [])


    def _validate_bic(self, bic: str) -> bool:
        """
        Validate a BIC (Bank Identifier Code) format.

        BIC format: 8 or 11 characters
        - 4 letters: Bank code
        - 2 letters: Country code
        - 2 letters/digits: Location code
        - 3 letters/digits: Branch code (optional)

        Args:
            bic: BIC code to validate

        Returns:
            True if valid, False otherwise
        """
        if not bic:
            return False

        # BIC must be 8 or 11 characters
        if len(bic) not in [8, 11]:
            return False

        # First 4 characters must be letters (bank code)
        if not bic[:4].isalpha():
            return False

        # Characters 5-6 must be letters (country code)
        if not bic[4:6].isalpha():
            return False

        # Characters 7-8 must be alphanumeric (location code)
        if not bic[6:8].isalnum():
            return False

        # If 11 characters, last 3 must be alphanumeric (branch code)
        if len(bic) == 11 and not bic[8:11].isalnum():
            return False

        return True

    def optimize_message(self, message: Dict, errors: List[str]) -> Dict:
        """
        Optimize (correct) a SWIFT message based on identified errors.

        NOTE: This method uses the SwiftCorrectionAgent that You implement
        in base_agents.py (TODOs 7-9).

        Args:
            message: SWIFT message to optimize
            errors: List of errors to correct

        Returns:
            Optimized message
        """
        try:
            corrected_message = self.correction_agent.respond(message, errors)
            if isinstance(corrected_message, dict):
                message.update(corrected_message)
        except Exception as e:
            print(f"Error during optimization: {e}")

        if "amount" in message and isinstance(message["amount"], str):
            parts = message["amount"].split()
            if len(parts) == 1:
                # Assume USD if currency missing
                message["amount"] = f"{parts[0]} USD"

        return message

    def process_with_evaluator_optimizer(self, messages: List[Dict]) -> List[Dict]:
        """
        Process messages through the evaluator-optimizer pattern.

        Args:
            messages: List of SWIFT messages to process

        Returns:
            List of validated and optimized messages
        """
        print("=" * 60)
        print("EVALUATOR-OPTIMIZER PATTERN PROCESSING")
        print("=" * 60)

        optimized_messages = []

        for i, message in enumerate(messages):
            if hasattr(message, "model_dump"):
                message = message.model_dump()
            # print(f"{i=}, {message=}")
            print(f"\nProcessing message {i+1}/{len(messages)}: {message.get('message_id', 'Unknown')}")

            # Iterative evaluation and optimization
            for iteration in range(self.MAX_ITERATIONS):
                is_valid, errors = self.evaluate_message(message)

                if is_valid:
                    print(f"  ✓ Message valid after {iteration} iteration(s)")
                    message['validation_status'] = 'VALID'
                    message['validation_errors'] = []
                    break
                else:
                    print(f"  Iteration {iteration + 1}: Found {len(errors)} error(s)")
                    for error in errors[:3]:  # Show first 3 errors
                        print(f"    - {error}")

                    if iteration < self.MAX_ITERATIONS - 1:
                        # Attempt to optimize
                        print(f"  Attempting optimization...")
                        message = self.optimize_message(message, errors)
                    else:
                        # Max iterations reached
                        print(f"  ✗ Max iterations reached. Message still has errors.")
                        message['validation_status'] = 'INVALID'
                        message['validation_errors'] = errors

            optimized_messages.append(message)

        # Print summary
        valid_count = sum(1 for m in optimized_messages if m.get('validation_status') == 'VALID')
        print(f"\n{'=' * 60}")
        print(f"EVALUATOR-OPTIMIZER SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total messages processed: {len(optimized_messages)}")
        print(f"Valid messages: {valid_count}")
        print(f"Invalid messages: {len(optimized_messages) - valid_count}")

        return optimized_messages

    def test_pattern(self):
        """
        Test the evaluator-optimizer pattern with sample messages.
        You can use this to verify the pattern works with your implementations.
        """
        test_messages = [
            {
                'message_id': 'VALID001',
                'message_type': 'MT103',
                'reference': 'REF123456',
                'amount': '5000.00 USD',
                'sender_bic': 'CHASUS33XXX',
                'receiver_bic': 'DEUTDEFFXXX',
                'remittance_info': 'Invoice payment'
            },
            {
                'message_id': 'INVALID001',
                'message_type': 'MT999',  # Invalid type
                'reference': 'THIS_REFERENCE_IS_WAY_TOO_LONG_12345',  # Too long
                'amount': '9999999999.99 USD',  # Too large
                'sender_bic': 'INVALID',  # Invalid BIC
                'receiver_bic': 'INVALID',  # Invalid BIC
                'remittance_info': 'Test invalid message'
            },
            {
                'message_id': 'FIXABLE001',
                'message_type': 'MT103',
                'reference': 'REF_NEEDS_FIX_123456789',  # Slightly too long
                'amount': '0.001 USD',  # Too small
                'sender_bic': 'TEST1234',  # Invalid format
                'receiver_bic': 'BARCGB22XXX',
                'remittance_info': 'Should be fixable'
            }
        ]

        print("Testing Evaluator-Optimizer Pattern\n")
        results = self.process_with_evaluator_optimizer(test_messages)

        print("\nTest Results:")
        for msg in results:
            print(f"\n{msg.get('message_id')}:")
            print(f"  Status: {msg.get('validation_status')}")
            if msg.get('validation_errors'):
                print(f"  Remaining errors: {len(msg.get('validation_errors'))}")

        return results


if __name__ == "__main__":
    # Test the evaluator-optimizer pattern
    pattern = EvaluatorOptimizerPattern()
    pattern.test_pattern()