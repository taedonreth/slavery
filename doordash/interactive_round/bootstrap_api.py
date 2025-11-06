import logging
from dataclasses import dataclass
from typing import Optional
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Data Classes
@dataclass
class Address:
    """Represents a user's address"""

    line1: str
    city: str
    zip: str

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.zip}"


@dataclass
class Consumer:
    """Represents a consumer from ConsumerService"""

    id: str
    name: str


@dataclass
class PaymentInfo:
    """Represents payment information from PaymentService"""

    defaultMethod: str
    giftCardBalance: float


@dataclass
class UserProfile:
    """Aggregated user profile response"""

    consumerId: str
    name: str
    defaultPaymentMethod: Optional[str] = None
    giftCardBalance: Optional[float] = None
    address: Optional[Address] = None

    def to_dict(self):
        """Convert to dictionary for JSON-like output"""
        return {
            "consumerId": self.consumerId,
            "name": self.name,
            "defaultPaymentMethod": self.defaultPaymentMethod,
            "giftCardBalance": self.giftCardBalance,
            "address": str(self.address) if self.address else None,
        }


# Custom Exceptions
class UserNotFoundException(Exception):
    """Raised when user is not found in ConsumerService"""

    pass


class ServiceException(Exception):
    """Base exception for service failures"""

    pass


# Mock Services (These would be actual service clients in production)
class ConsumerService:
    """Service to fetch consumer information"""

    def __init__(self):
        # Mock data store
        self.consumers = {
            "user123": Consumer(id="123", name="Alice"),
            "user456": Consumer(id="456", name="Bob"),
            "user789": Consumer(id="789", name="Charlie"),
        }

    def getConsumer(self, userId: str) -> Consumer:
        """
        Fetches consumer data by userId
        Raises UserNotFoundException if user doesn't exist
        """
        logger.info(f"ConsumerService: Fetching consumer for userId={userId}")

        if userId not in self.consumers:
            logger.error(f"ConsumerService: User not found for userId={userId}")
            raise UserNotFoundException(f"User with userId={userId} not found")

        # Simulate occasional service failure (uncomment to test)
        # import random
        # if random.random() < 0.1:
        #     raise ServiceException("ConsumerService temporarily unavailable")

        consumer = self.consumers[userId]
        logger.info(
            f"ConsumerService: Successfully retrieved consumer id={consumer.id}"
        )
        return consumer


class PaymentService:
    """Service to fetch payment information"""

    def __init__(self):
        # Mock payment data
        self.payments = {
            "123": PaymentInfo(defaultMethod="Credit Card", giftCardBalance=50.0),
            "456": PaymentInfo(defaultMethod="Debit Card", giftCardBalance=25.5),
            "789": PaymentInfo(defaultMethod="PayPal", giftCardBalance=0.0),
        }

    def getPaymentInfo(self, consumerId: str) -> PaymentInfo:
        """
        Fetches payment information by consumerId
        May raise ServiceException on failure
        """
        logger.info(
            f"PaymentService: Fetching payment info for consumerId={consumerId}"
        )

        # Simulate occasional service failure (uncomment to test)
        # import random
        # if random.random() < 0.2:
        #     raise ServiceException("PaymentService temporarily unavailable")

        if consumerId not in self.payments:
            logger.warning(
                f"PaymentService: No payment info found for consumerId={consumerId}"
            )
            raise ServiceException(
                f"Payment info not found for consumerId={consumerId}"
            )

        payment_info = self.payments[consumerId]
        logger.info(f"PaymentService: Successfully retrieved payment info")
        return payment_info


class AddressService:
    """Service to fetch user address"""

    def __init__(self):
        # Mock address data
        self.addresses = {
            "123": Address(line1="123 Main St", city="Anytown", zip="12345"),
            "456": Address(line1="456 Oak Ave", city="Springfield", zip="67890"),
            "789": Address(line1="789 Pine Rd", city="Metropolis", zip="11111"),
        }

    def getAddress(self, consumerId: str) -> Address:
        """
        Fetches address by consumerId
        May raise ServiceException on failure
        """
        logger.info(f"AddressService: Fetching address for consumerId={consumerId}")

        # Simulate occasional service failure (uncomment to test)
        # import random
        # if random.random() < 0.2:
        #     raise ServiceException("AddressService temporarily unavailable")

        if consumerId not in self.addresses:
            logger.warning(
                f"AddressService: No address found for consumerId={consumerId}"
            )
            raise ServiceException(f"Address not found for consumerId={consumerId}")

        address = self.addresses[consumerId]
        logger.info(f"AddressService: Successfully retrieved address")
        return address


# Main Bootstrap Service
class BootstrapService:
    """
    Aggregates user data from multiple services.
    Handles partial failures gracefully.
    """

    def __init__(self, consumer_service, payment_service, address_service):
        """
        Args:
            consumer_service: Instance of ConsumerService
            payment_service: Instance of PaymentService
            address_service: Instance of AddressService
        """
        self.consumer_service = consumer_service
        self.payment_service = payment_service
        self.address_service = address_service

    def getUserProfile(self, userId: str) -> Optional[UserProfile]:
        """
        Retrieves and aggregates user profile from multiple services.

        Args:
            userId: The user identifier

        Returns:
            UserProfile with aggregated data, or None if user not found

        Raises:
            UserNotFoundException: If userId is invalid
        """
        logger.info(f"Fetching user profile for userId: {userId}")

        # Step 1: Get consumer info - CRITICAL, must succeed
        try:
            consumer = self.consumer_service.getConsumer(userId)
            logger.info(f"Retrieved consumer: {consumer.id}")
        except Exception as e:
            logger.error(f"Failed to get consumer for userId {userId}: {e}")
            raise UserNotFoundException(f"User {userId} not found") from e

        # Initialize profile with consumer data
        profile = UserProfile(consumerId=consumer.id, name=consumer.name)

        # Step 2: Get payment info - NON-CRITICAL, fail gracefully
        try:
            payment_info = self.payment_service.getPaymentInfo(consumer.id)
            profile.defaultPaymentMethod = payment_info.defaultMethod
            profile.giftCardBalance = payment_info.giftCardBalance
            logger.info(f"Retrieved payment info for consumer {consumer.id}")
        except Exception as e:
            logger.warning(
                f"Failed to get payment info for consumer {consumer.id}: {e}"
            )
            # Leave defaultPaymentMethod and giftCardBalance as None

        # Step 3: Get address - NON-CRITICAL, fail gracefully
        try:
            address = self.address_service.getAddress(consumer.id)
            profile.address = address
            logger.info(f"Retrieved address for consumer {consumer.id}")
        except Exception as e:
            logger.warning(f"Failed to get address for consumer {consumer.id}: {e}")
            # Leave address as None

        logger.info(f"Successfully built profile for consumer {consumer.id}")
        return profile


# Test Suite
def test_bootstrap_service():
    """Test cases for BootstrapService"""

    print("=" * 80)
    print("BOOTSTRAP SERVICE TEST SUITE")
    print("=" * 80)

    # Initialize services
    consumer_service = ConsumerService()
    payment_service = PaymentService()
    address_service = AddressService()
    bootstrap_service = BootstrapService(
        consumer_service, payment_service, address_service
    )

    # Test Case 1: Happy Path - All services succeed
    print("\n[TEST 1] Happy Path - All services return data")
    print("-" * 80)
    try:
        profile = bootstrap_service.getUserProfile("user123")
        assert profile is not None, "Profile should not be None"
        assert (
            profile.consumerId == "123"
        ), f"Expected consumerId='123', got '{profile.consumerId}'"
        assert profile.name == "Alice", f"Expected name='Alice', got '{profile.name}'"
        assert (
            profile.defaultPaymentMethod == "Credit Card"
        ), f"Expected 'Credit Card', got '{profile.defaultPaymentMethod}'"
        assert (
            profile.giftCardBalance == 50.0
        ), f"Expected balance=50.0, got {profile.giftCardBalance}"
        assert profile.address is not None, "Address should not be None"
        print(f"✓ SUCCESS: {profile.to_dict()}")
    except AssertionError as e:
        print(f"✗ FAILED: {str(e)}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

    # Test Case 2: User Not Found
    print("\n[TEST 2] User Not Found - Invalid userId")
    print("-" * 80)
    try:
        profile = bootstrap_service.getUserProfile("invalid_user")
        print(f"✗ FAILED: Should have raised UserNotFoundException")
    except UserNotFoundException as e:
        print(f"✓ SUCCESS: Correctly raised UserNotFoundException - {str(e)}")
    except Exception as e:
        print(f"✗ ERROR: Unexpected exception - {str(e)}")

    # Test Case 3: Payment Service Failure (Graceful Degradation)
    print("\n[TEST 3] Graceful Degradation - Payment Service Fails")
    print("-" * 80)

    # Create a custom payment service that always fails
    class FailingPaymentService(PaymentService):
        def getPaymentInfo(self, consumerId: str) -> PaymentInfo:
            raise ServiceException("Payment service is down")

    failing_bootstrap = BootstrapService(
        consumer_service, FailingPaymentService(), address_service
    )

    try:
        profile = failing_bootstrap.getUserProfile("user123")
        assert profile is not None, "Profile should not be None"
        assert profile.consumerId == "123", "Should have consumer data"
        assert profile.name == "Alice", "Should have consumer name"
        assert profile.defaultPaymentMethod is None, "Payment method should be None"
        assert profile.giftCardBalance is None, "Gift card balance should be None"
        assert profile.address is not None, "Should still have address"
        print(f"✓ SUCCESS: Partial profile returned - {profile.to_dict()}")
    except AssertionError as e:
        print(f"✗ FAILED: {str(e)}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

    # Test Case 4: Address Service Failure (Graceful Degradation)
    print("\n[TEST 4] Graceful Degradation - Address Service Fails")
    print("-" * 80)

    class FailingAddressService(AddressService):
        def getAddress(self, consumerId: str) -> Address:
            raise ServiceException("Address service is down")

    failing_bootstrap2 = BootstrapService(
        consumer_service, payment_service, FailingAddressService()
    )

    try:
        profile = failing_bootstrap2.getUserProfile("user456")
        assert profile is not None, "Profile should not be None"
        assert profile.consumerId == "456", "Should have consumer data"
        assert profile.name == "Bob", "Should have consumer name"
        assert (
            profile.defaultPaymentMethod == "Debit Card"
        ), "Should have payment method"
        assert profile.giftCardBalance == 25.5, "Should have gift card balance"
        assert profile.address is None, "Address should be None"
        print(f"✓ SUCCESS: Partial profile returned - {profile.to_dict()}")
    except AssertionError as e:
        print(f"✗ FAILED: {str(e)}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

    # Test Case 5: Multiple Service Failures (Both Payment and Address)
    print("\n[TEST 5] Multiple Failures - Both Payment and Address Services Fail")
    print("-" * 80)

    failing_bootstrap3 = BootstrapService(
        consumer_service, FailingPaymentService(), FailingAddressService()
    )

    try:
        profile = failing_bootstrap3.getUserProfile("user789")
        assert profile is not None, "Profile should not be None"
        assert profile.consumerId == "789", "Should have consumer data"
        assert profile.name == "Charlie", "Should have consumer name"
        assert profile.defaultPaymentMethod is None, "Payment method should be None"
        assert profile.giftCardBalance is None, "Gift card balance should be None"
        assert profile.address is None, "Address should be None"
        print(
            f"✓ SUCCESS: Minimal profile returned (consumer data only) - {profile.to_dict()}"
        )
    except AssertionError as e:
        print(f"✗ FAILED: {str(e)}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETED")
    print("=" * 80)


# Main execution
if __name__ == "__main__":
    test_bootstrap_service()
