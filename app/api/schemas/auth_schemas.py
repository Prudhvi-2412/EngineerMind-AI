from pydantic import BaseModel, EmailStr, Field


class RegisterOrgRequest(BaseModel):
    org_name: str = Field(..., min_length=2, max_length=100, example="Acme Engineering")
    org_slug: str = Field(..., min_length=2, max_length=50, pattern="^[a-z0-9-]+$", example="acme-eng")
    admin_email: EmailStr = Field(..., example="admin@acme.com")
    admin_name: str = Field(..., min_length=2, max_length=100, example="Jane Doe")
    password: str = Field(..., min_length=8, max_length=100, example="P@ssw0rd123!")


class LoginRequest(BaseModel):
    org_slug: str = Field(..., example="acme-eng")
    email: EmailStr = Field(..., example="admin@acme.com")
    password: str = Field(..., example="P@ssw0rd123!")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
