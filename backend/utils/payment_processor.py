import stripe
from flask import current_app

def process_payment(user_id, amount, currency, payment_method, card_token=None):
    """
    Process a payment using Stripe
    """
    try:
        # Set Stripe API key
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        
        # Create payment intent
        if card_token:
            # Create customer and charge
            customer = stripe.Customer.create(
                source=card_token,
                description=f"Customer for user {user_id}"
            )
            
            charge = stripe.Charge.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                customer=customer.id,
                description=f"Payment from user {user_id}"
            )
        else:
            # Use payment method
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency.lower(),
                payment_method=payment_method,
                confirmation_method='manual',
                confirm=True
            )
        
        return {
            "success": True,
            "message": "Payment processed successfully",
            "transaction_id": charge.id if card_token else intent.id
        }
        
    except stripe.error.CardError as e:
        return {
            "success": False,
            "message": f"Card error: {e.error.message}"
        }
    except stripe.error.RateLimitError as e:
        return {
            "success": False,
            "message": "Too many requests. Please try again later."
        }
    except stripe.error.InvalidRequestError as e:
        return {
            "success": False,
            "message": f"Invalid request: {e.error.message}"
        }
    except stripe.error.AuthenticationError as e:
        return {
            "success": False,
            "message": "Authentication error. Please contact support."
        }
    except stripe.error.APIConnectionError as e:
        return {
            "success": False,
            "message": "Network error. Please check your connection and try again."
        }
    except stripe.error.StripeError as e:
        return {
            "success": False,
            "message": f"Payment error: {e.error.message}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }
