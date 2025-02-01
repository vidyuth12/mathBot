import unittest
from main2 import MultiAgentSystem
import logging
from datetime import datetime
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class TestMultiAgentMathSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = MultiAgentSystem()
        cls.cache_hits = 0
        cls.error_corrections = 0
        cls.operation_counts = {}

    def setUp(self):
        logging.info("\n" + "="*50 + "\nStarting new test\n" + "="*50)

    def track_operation(self, operation):
        self.operation_counts[operation] = self.operation_counts.get(operation, 0) + 1
        logging.info(f"Operation {operation} called {self.operation_counts[operation]} times")

    def test_basic_operations(self):
        """Test all basic operations multiple times"""
        test_cases = [
            # SUM tests
            ("What is the sum of 5 and 3?", 8),
            ("What is the sum of 10 and 20?", 30),
            ("What is the sum of 15 and 25?", 40),
            
            # PRODUCT tests
            ("What is the product of 4 and 6?", 24),
            ("What is the product of 3 and 5?", 15),
            ("What is the product of 7 and 8?", 56),
            
            # QUOTIENT tests
            ("What is 20 divided by 4?", 5),
            ("What is 30 divided by 6?", 5),
            ("What is 100 divided by 25?", 4),
            
            # POWER tests
            ("What is 2 to the power of 3?", 8),
            ("What is 3 to the power of 2?", 9),
            ("What is 4 to the power of 2?", 16),
            
            # SQRT tests
            ("What is the square root of 16?", 4),
            ("What is the square root of 25?", 5),
            ("What is the square root of 81?", 9),
            
            # AVG test cases to try
            # ("What is the average of 10 and 20?", 15),
            # ("What is the average of 15 and 25?", 20),
            # ("What is the average of 30 and 40?", 35),

            # MODULO test cases that should work
            ("What is the remainder when 17 is divided by 5?", 2),
            ("What is the remainder when 23 is divided by 7?", 2),
            ("What is the remainder when 100 is divided by 30?", 10),

            # ABS test cases that should work
            ("What is the absolute value of -15?", 15),
            ("What is the absolute value of -25?", 25),
            ("What is the absolute value of -30?", 30)
        ]

        for question, expected in test_cases:
            logging.info(f"\nTesting: {question}")
            operation = question.split()[3].upper()  # Extract operation from question
            self.track_operation(operation)
            
            result = self.system.solve(question, expected)
            logging.info(f"Result: {result}")
            
            self.assertIn('result', result, f"Failed to get result for: {question}")
            self.assertEqual(result['result'], expected, 
                           f"Expected {expected} but got {result['result']} for {question}")

    def test_caching_behavior(self):
        """Test if caching works by repeating the same operations"""
        logging.info("\nTesting caching behavior...")
        
        # Test cases to repeat
        repeat_cases = [
            ("What is the sum of 5 and 3?", 8),
            ("What is the product of 4 and 6?", 24),
            ("What is the square root of 16?", 4)
        ]

        for question, expected in repeat_cases:
            # First execution
            logging.info(f"\nFirst execution of: {question}")
            result1 = self.system.solve(question, expected)
            
            # Second execution (should use cache)
            logging.info(f"Second execution of: {question}")
            result2 = self.system.solve(question, expected)
            
            # Verify results are the same
            self.assertEqual(result1['result'], result2['result'], 
                           f"Cached result different from original for: {question}")
            
            # Check if cache was actually used (this requires checking logs)
            if "Using cached virtual tool" in logging.getLogger().handlers[0].baseFilename:
                self.cache_hits += 1
                logging.info(f"Cache hit confirmed for: {question}")

    def test_error_correction(self):
        """Test error correction by introducing potentially problematic cases"""
        logging.info("\nTesting error correction behavior...")
        
        edge_cases = [
            # Division by zero (should trigger error correction)
            ("What is 10 divided by 0?", None),
            # Very large numbers (might trigger precision errors)
            ("What is the product of 999999999 and 999999999?", 999999998000000001),
            # Negative square root
            ("What is the square root of -16?", None)
        ]

        for question, expected in edge_cases:
            logging.info(f"\nTesting edge case: {question}")
            result = self.system.solve(question, expected)
            
            if 'error' in result:
                logging.info(f"Error correction triggered for: {question}")
                self.error_corrections += 1
            else:
                logging.info(f"Operation completed successfully: {result}")

    def tearDown(self):
        logging.info("\nTest completed")

    @classmethod
    def tearDownClass(cls):
        logging.info("\n" + "="*50 + "\nTest Suite Summary\n" + "="*50)
        logging.info(f"Total cache hits: {cls.cache_hits}")
        logging.info(f"Total error corrections: {cls.error_corrections}")
        logging.info("Operation counts:")
        for op, count in cls.operation_counts.items():
            logging.info(f"{op}: {count} times")

if __name__ == '__main__':
    unittest.main(verbosity=2)