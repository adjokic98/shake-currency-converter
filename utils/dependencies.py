from fastapi import Header, HTTPException, Depends
from db.operations import decrement_user_credits

async def get_valid_user(x_api_key: str = Header(..., description="API key")):
    """
    Dependency function to validate the API key and return the user's data.

    Raises an HTTPException with status code 401 if the API key is invalid.
    """
    from db.operations import get_user_by_api_key
    user_data = get_user_by_api_key(x_api_key)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    user_data["api_key"] = x_api_key
    return user_data

async def rate_limit_by_credits(user_data: dict = Depends(get_valid_user)):
    """Rate limits requests based on the user's remaining credits."""
    credits = user_data.get("credits")
    user_email = user_data.get("email")

    if credits is None or credits <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits")

    if user_email:
        decrement_user_credits(user_email)
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User email not found in user data")
