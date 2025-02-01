import unittest
from main2 import MultiAgentSystem
import logging
from datetime import datetime
import json
import os

class TestMultiAgentMathSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = MultiAgentSystem()
        cls.cache_file = "virtual_tools.json"
        cls.operation_counts = {}
        
        # Setup logging
        log_filename = f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )

    def setUp(self):
        logging.info("\n" + "="*50 + "\nStarting new test\n" + "="*50)
        self.initial_cache_state = self._read_cache_state()

    def _read_cache_state(self):
        """Helper to read current cache state"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def track_operation(self, operation):
        """Track operation usage"""
        self.operation_counts[operation] = self.operation_counts.get(operation, 0) + 1
        logging.info(f"Operation {operation} called {self.operation_counts[operation]} times")

    def test_basic_operations(self):
        """Test all basic mathematical operations"""
        test_cases = {
            "SUM": [
                ("What is the sum of 5 and 3?", 8),
                ("What is the sum of 10 and 20?", 30),
                ("What is the sum of 15 and 25?", 40)
            ],
            "PRODUCT": [
                ("What is the product of 4 and 6?", 24),
                ("What is the product of 3 and 5?", 15),
                ("What is the product of 7 and 8?", 56)
            ],
            "QUOTIENT": [
                ("What is 20 divided by 4?", 5),
                ("What is 30 divided by 6?", 5),
                ("What is 100 divided by 25?", 4)
            ],
            "POWER": [
                ("What is 2 to the power of 3?", 8),
                ("What is 3 to the power of 2?", 9),
                ("What is 4 to the power of 2?", 16)
            ],
            "SQRT": [
                ("What is the square root of 16?", 4),
                ("What is the square root of 25?", 5),
                ("What is the square root of 81?", 9)
            ],
            # "AVG": [
            #     ("What is the average of 10 and 20?", 15),
            #     ("What is the average of 15 and 25?", 20),
            #     ("What is the average of 30 and 40?", 35)
            #],
            "MODULO": [
                ("What is the remainder when 17 is divided by 5?", 2),
                ("What is the remainder when 23 is divided by 7?", 2),
                ("What is the remainder when 100 is divided by 30?", 10)
            ],
            "ABS": [
                ("What is the absolute value of -15?", 15),
                ("What is the absolute value of -25?", 25),
                ("What is the absolute value of -30?", 30)
            ]
        }

        for operation, cases in test_cases.items():
            logging.info(f"\nTesting {operation} operations:")
            for question, expected in cases:
                logging.info(f"\nTesting: {question}")
                self.track_operation(operation)
                
                result = self.system.solve(question, expected)
                logging.info(f"Result: {result}")
                
                if 'error' in result:
                    logging.error(f"Operation failed: {result['error']}")
                    self.fail(f"Operation {operation} failed for input: {question}")
                else:
                    self.assertEqual(result['result'], expected, 
                                   f"Expected {expected} but got {result['result']} for {question}")

    def test_caching_behavior(self):
        """Test if caching works by verifying cache file operations and cache usage"""
        logging.info("\nTesting caching behavior...")
        
        test_cases = [
            ("What is the sum of 5 and 3?", 8),
            ("What is the product of 4 and 6?", 24),
            ("What is the square root of 16?", 4)
        ]

        for question, expected in test_cases:
            logging.info(f"\nTesting cache for: {question}")
            
            # Check if problem already exists in cache
            initial_exists = self.system.virtual_tool_cache.exists(question)
            logging.info(f"Problem initially in cache: {initial_exists}")

            # First execution
            logging.info("Executing first time...")
            result1 = self.system.solve(question, expected)
            
            # Verify problem was added to cache if it wasn't there
            self.assertTrue(
                self.system.virtual_tool_cache.exists(question),
                f"Problem should have been added to cache: {question}"
            )

            # Second execution - should use cache
            logging.info("Executing second time (should use cache)...")
            before_cache = self._read_cache_state()
            result2 = self.system.solve(question, expected)
            after_cache = self._read_cache_state()
            
            # Cache content shouldn't change on second execution
            self.assertEqual(
                before_cache,
                after_cache,
                "Cache state changed during cached execution"
            )
            
            # Results should be consistent
            self.assertEqual(
                result1,
                result2,
                f"Cached result different from original for: {question}"
            )

    def test_error_handling(self):
        """Test system's error handling capabilities"""
        error_cases = [
            ("What is 10 divided by 0?", None),  # Division by zero
            ("What is the square root of -16?", None),  # Negative square root
            ("What is the product of 999999999999 and 999999999999?", None)  # Overflow
        ]

        for question, _ in error_cases:
            logging.info(f"\nTesting error case: {question}")
            result = self.system.solve(question, None)
            
            if 'error' in result:
                logging.info(f"Error handled correctly for: {question}")
            else:
                logging.warning(f"Expected error but got result: {result}")

    def test_cache_persistence(self):
        """Test if cache persists between system instances"""
        test_problem = "What is the sum of 100 and 200?"
        expected = 300
        
        # First system instance
        system1 = MultiAgentSystem()
        result1 = system1.solve(test_problem, expected)
        
        # Create new system instance
        system2 = MultiAgentSystem()
        self.assertTrue(
            system2.virtual_tool_cache.exists(test_problem),
            "Cache should persist between system instances"
        )
        
        result2 = system2.solve(test_problem, expected)
        self.assertEqual(
            result1,
            result2,
            "Results should be consistent between system instances"
        )

    def tearDown(self):
        logging.info("\nTest completed")

    @classmethod
    def tearDownClass(cls):
        logging.info("\n" + "="*50 + "\nTest Suite Summary\n" + "="*50)
        logging.info("Operation counts:")
        for op, count in cls.operation_counts.items():
            logging.info(f"{op}: {count} times")

if __name__ == '__main__':
    unittest.main(verbosity=2)