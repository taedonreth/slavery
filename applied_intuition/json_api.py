"""
Product Analysis API Client

This module provides functionality to analyze product data from a JSON API endpoint.
It finds the most expensive product and the most recently added product from the dataset.

Problem Statement:
-----------------
Analyze a dataset of products from a remote API endpoint. The data is a JSON array 
of objects containing product_id, price, and timestamp. The program must:
1. Download and parse JSON data from a URL
2. Find the product with the highest price
3. Find the most recently added product (by timestamp)
4. Handle errors comprehensively (network failures, malformed URLs, invalid JSON)
5. Scale to handle large datasets or paginated APIs

Usage:
------
    analyze_products("https://api.example.com/products")
"""

import json
from datetime import datetime

import requests

def analyze_products(url: str):
    """
    Downloads and analyzes product data from a given URL.

    Finds and prints the product with the highest price and the most
    recently added product based on its timestamp.

    Args:
        url: The URL of the JSON API endpoint.

    Returns:
        None. Prints results to stdout.

    Raises:
        Catches and handles all exceptions, printing error messages instead.
    """
    try:
        # Perform HTTP GET request with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse JSON data
        products = response.json()

        # Validate data structure
        if not isinstance(products, list) or not products:
            print("No products found or data is not a list.")
            return

        # Initialize tracking variables
        highest_price_product = None
        most_recent_product = None
        latest_timestamp = datetime.min

        # Process each product
        for product in products:
            try:
                # Price analysis
                if (highest_price_product is None or 
                    product['price'] > highest_price_product['price']):
                    highest_price_product = product

                # Recency analysis
                current_timestamp = datetime.fromisoformat(
                    product['timestamp'].replace('Z', '+00:00')
                )
                if (most_recent_product is None or 
                    current_timestamp > latest_timestamp):
                    latest_timestamp = current_timestamp
                    most_recent_product = product

            except (KeyError, TypeError) as e:
                print(f"Skipping malformed product: {product}. Error: {e}")
                continue

        # Display results
        _display_results(highest_price_product, most_recent_product)

    except requests.exceptions.MissingSchema:
        print(f"Error: Invalid URL '{url}'. Please include 'http://' or 'https://'.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Check your network connection.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP request failed with status code {e.response.status_code}.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. The response may not be valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def _display_results(highest_price_product, most_recent_product):
    """Display analysis results."""
    print("\n" + "=" * 50)
    print("ANALYSIS RESULTS")
    print("=" * 50)
    
    if highest_price_product:
        print("\nMost Expensive Product:")
        print(f"  ID: {highest_price_product['product_id']}")
        print(f"  Price: ${highest_price_product['price']:.2f}")
    else:
        print("\nCould not determine the most expensive product.")

    if most_recent_product:
        print("\nMost Recent Product:")
        print(f"  ID: {most_recent_product['product_id']}")
        print(f"  Timestamp: {most_recent_product['timestamp']}")
    else:
        print("\nCould not determine the most recent product.")
    
    print("=" * 50 + "\n")


if __name__ == '__main__':
    # Example usage with mock API endpoint
    mock_api_url = "https://api.jsonserve.com/q3i8aP"
    analyze_products(mock_api_url)


# =============================================================================
# IMPLEMENTATION NOTES: ERROR HANDLING & SCALING
# =============================================================================

"""
ERROR HANDLING STRATEGY
-----------------------

1. Network Failures
   Problem: Temporary network glitches, timeouts, server-side issues
   Solution: 
   - Implement retry mechanism with exponential backoff
   - Prevents failure on transient issues
   - Increases delays between retry attempts

2. URL & HTTP Status Validation
   Problem: Malformed URLs or error status codes (404, 503, etc.)
   Solution:
   - Catch invalid URL exceptions for clear feedback
   - Retry server errors (5xx) with exponential backoff
   - Fail immediately on client errors (4xx) - retrying won't help

3. Invalid Data Handling
   Problem: Non-JSON responses or missing required fields (price, timestamp)
   Solution:
   - Use schema validation (e.g., Pydantic) to confirm data structure
   - Wrap individual item processing in try-except blocks
   - Skip malformed records without crashing entire program
   - Implement centralized logging for debugging and monitoring


SCALING STRATEGY
----------------

1. Large JSON Files (Memory Constraints)
   Problem: Entire file doesn't fit in memory
   Solution: Use streaming approach
   - Download in chunks: requests.get(url, stream=True)
   - Parse incrementally with streaming JSON parser (ijson)
   - Process one product at a time
   - Maintains constant, low memory usage

2. Paginated APIs (Multiple Requests)
   Problem: Data split across multiple pages
   Solution: Implement pagination loop
   - Make initial request to first page
   - Check response for pagination indicators:
     * next_page_url
     * page count metadata
     * cursor tokens
   - Loop until no more data available
   - Add delays (time.sleep) between requests to respect rate limits

3. Best Practices
   - Implement request throttling
   - Use connection pooling for multiple requests
   - Add proper logging and monitoring
   - Consider async/await for concurrent requests
   - Cache results when appropriate
"""