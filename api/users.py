from utils.dependencies import get_valid_user
from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserSignupResponse, UserCreditsResponse, UserSignupRequest
from services.auth import AuthService
from db.operations import create_user, get_user_by_email, get_user_credits
from utils.consts import INITIAL_CREDITS

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=UserSignupResponse)
async def signup(signup_request: UserSignupRequest):
    """Registers a new user with an email and provides an API key with initial credits."""
    email = signup_request.email.lower()  # Ensure emails are case-insensitive

    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    api_key = AuthService.generate_api_key()
    create_user(email=email, api_key=api_key, initial_credits=INITIAL_CREDITS)
    return {"api_key": api_key, "credits": INITIAL_CREDITS}

@router.get("/credits", response_model=UserCreditsResponse)
async def get_user_credits_endpoint(user: dict = Depends(get_valid_user)):
    """
    Retrieves the remaining credits for the logged-in user.
    Requires a valid API key in the X-API-Key header.
    """
    credits = user.get("credits")
    if credits is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"credits": credits}