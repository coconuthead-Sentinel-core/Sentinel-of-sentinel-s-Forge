"""
Stripe Billing Integration for Sentinel Forge.

Provides subscription management, checkout session creation,
webhook handling, and billing portal access.

Requires: pip install stripe
"""
import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from ..core.config import settings
from ..core.auth import UserRecord, get_current_user, update_user_subscription

logger = logging.getLogger(__name__)

billing_router = APIRouter(prefix="/billing", tags=["billing"])

# Lazy-load stripe to avoid import errors if not installed
_stripe = None


def _get_stripe():
    global _stripe
    if _stripe is None:
        try:
            import stripe
            _stripe = stripe
            if settings.STRIPE_SECRET_KEY:
                _stripe.api_key = settings.STRIPE_SECRET_KEY
            else:
                logger.warning("STRIPE_SECRET_KEY not configured — billing endpoints will return mock responses")
        except ImportError:
            logger.warning("stripe package not installed — billing endpoints will return mock responses")
    return _stripe


# --- Schemas ---

class CreateCheckoutRequest(BaseModel):
    plan: str = Field(..., pattern="^(starter|pro|enterprise)$")
    success_url: str = Field(default="https://your-domain.com/billing/success")
    cancel_url: str = Field(default="https://your-domain.com/billing/cancel")


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class SubscriptionStatus(BaseModel):
    tier: str
    status: str
    current_period_end: Optional[str] = None
    cancel_at_period_end: bool = False
    stripe_customer_id: str = ""


class BillingPortalResponse(BaseModel):
    portal_url: str


# --- Plan ID Mapping ---

def _get_price_id(plan: str) -> str:
    mapping = {
        "starter": settings.STRIPE_PRICE_ID_STARTER,
        "pro": settings.STRIPE_PRICE_ID_PRO,
        "enterprise": settings.STRIPE_PRICE_ID_ENTERPRISE,
    }
    price_id = mapping.get(plan, "")
    if not price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No Stripe price ID configured for plan: {plan}",
        )
    return price_id


# --- Routes ---

@billing_router.get("/plans")
async def list_plans():
    """Return available subscription plans."""
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "description": "For individuals and small projects",
                "features": [
                    "1,000 API calls/month",
                    "Basic cognitive processing",
                    "Community support",
                ],
                "price_monthly": 29,
                "price_annual": 290,
            },
            {
                "id": "pro",
                "name": "Pro",
                "description": "For teams and growing businesses",
                "features": [
                    "25,000 API calls/month",
                    "Advanced cognitive pipelines",
                    "Priority support",
                    "Custom symbolic rules",
                    "Webhook integrations",
                ],
                "price_monthly": 99,
                "price_annual": 990,
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "description": "For organizations with custom needs",
                "features": [
                    "Unlimited API calls",
                    "Full cognitive suite",
                    "Dedicated support",
                    "Custom AI model deployment",
                    "SLA guarantee",
                    "SSO / SAML",
                ],
                "price_monthly": 499,
                "price_annual": 4990,
            },
        ]
    }


@billing_router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    req: CreateCheckoutRequest,
    user: UserRecord = Depends(get_current_user),
):
    """Create a Stripe Checkout session for the selected plan."""
    stripe = _get_stripe()
    if not stripe or not settings.STRIPE_SECRET_KEY:
        # Mock response for development
        return CheckoutResponse(
            checkout_url=f"https://checkout.stripe.com/mock?plan={req.plan}",
            session_id="mock_session_" + user.id[:8],
        )

    price_id = _get_price_id(req.plan)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=req.success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=req.cancel_url,
            client_reference_id=user.id,
            customer_email=user.email,
            metadata={"user_id": user.id, "plan": req.plan},
        )
        return CheckoutResponse(
            checkout_url=session.url,
            session_id=session.id,
        )
    except Exception as e:
        logger.error("Stripe checkout error: %s", e)
        raise HTTPException(status_code=502, detail="Payment service error")


@billing_router.get("/subscription", response_model=SubscriptionStatus)
async def get_subscription(user: UserRecord = Depends(get_current_user)):
    """Get the current user's subscription status."""
    return SubscriptionStatus(
        tier=user.subscription_tier,
        status="active" if user.subscription_tier != "free" else "none",
        stripe_customer_id=user.stripe_customer_id,
    )


@billing_router.post("/portal", response_model=BillingPortalResponse)
async def billing_portal(user: UserRecord = Depends(get_current_user)):
    """Create a Stripe Billing Portal session for subscription management."""
    stripe = _get_stripe()
    if not stripe or not settings.STRIPE_SECRET_KEY or not user.stripe_customer_id:
        return BillingPortalResponse(
            portal_url="https://billing.stripe.com/mock/portal",
        )

    try:
        session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=settings.CORS_ORIGINS.split(",")[0] if settings.CORS_ORIGINS else "https://your-domain.com",
        )
        return BillingPortalResponse(portal_url=session.url)
    except Exception as e:
        logger.error("Stripe portal error: %s", e)
        raise HTTPException(status_code=502, detail="Billing portal error")


@billing_router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events (subscription changes, payments, etc.)."""
    stripe = _get_stripe()
    if not stripe or not settings.STRIPE_SECRET_KEY:
        return {"status": "ignored", "reason": "stripe not configured"}

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {e}")

    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})

    logger.info("Stripe webhook: %s", event_type)

    if event_type == "checkout.session.completed":
        user_id = data.get("client_reference_id") or data.get("metadata", {}).get("user_id")
        plan = data.get("metadata", {}).get("plan", "starter")
        customer_id = data.get("customer", "")
        if user_id:
            update_user_subscription(user_id, plan, customer_id)
            logger.info("Subscription activated: user=%s plan=%s", user_id, plan)

    elif event_type == "customer.subscription.updated":
        customer_id = data.get("customer", "")
        status_val = data.get("status", "")
        logger.info("Subscription updated: customer=%s status=%s", customer_id, status_val)

    elif event_type == "customer.subscription.deleted":
        customer_id = data.get("customer", "")
        logger.info("Subscription cancelled: customer=%s", customer_id)
        # Find user by stripe customer ID and downgrade
        # In production, query Cosmos DB by stripe_customer_id

    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer", "")
        logger.warning("Payment failed: customer=%s", customer_id)

    return {"status": "ok", "event": event_type}
