from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.models.user import User, Role
from app.models.organization import Organization, OrganizationMember, OrgRole
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user
from app.services.ledger_service import LedgerService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=APIResponse[UserResponse])
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        phone_number=user_in.phone_number,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.flush()

    # Assign requested role
    role = db.query(Role).filter(Role.name == user_in.role_name.upper()).first()
    if not role:
        role = db.query(Role).filter(Role.name == "TENANT").first()
    if role:
        user.roles.append(role)

    # Auto-create or attach default organization
    default_org = db.query(Organization).first()
    if not default_org:
        default_org = Organization(
            name="Apex Property Management",
            slug="apex-pm",
            email="contact@apexpm.com"
        )
        db.add(default_org)
        db.flush()
        LedgerService.ensure_default_chart_of_accounts(db, default_org.id)

    org_member = OrganizationMember(
        organization_id=default_org.id,
        user_id=user.id,
        role=OrgRole.TENANT if user_in.role_name.upper() == "TENANT" else OrgRole.MANAGER
    )
    db.add(org_member)
    user.current_org_id = default_org.id

    db.commit()
    db.refresh(user)

    return APIResponse(
        success=True,
        message="User registered successfully.",
        data=UserResponse.model_validate(user)
    )

@router.post("/login", response_model=APIResponse[TokenResponse])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is inactive.")

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    user_resp = UserResponse.model_validate(user)
    token_resp = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=user_resp
    )

    return APIResponse(
        success=True,
        message="Login successful",
        data=token_resp
    )

@router.get("/me", response_model=APIResponse[UserResponse])
def get_me(current_user: User = Depends(get_current_user)):
    return APIResponse(
        success=True,
        message="Current user profile fetched",
        data=UserResponse.model_validate(current_user)
    )

@router.get("/oauth/{provider}/url", response_model=APIResponse[dict])
def get_oauth_url(provider: str):
    """Returns the authorization redirect URL for Google, Microsoft, Facebook, or LinkedIn."""
    from app.services.oauth_service import OAuthService
    auth_url = OAuthService.get_authorization_url(provider)
    return APIResponse(success=True, data={"provider": provider, "authorization_url": auth_url})

@router.get("/oauth/{provider}/callback", response_model=APIResponse[TokenResponse])
def oauth_callback(provider: str, code: str = "mock_code_123", role: str = "TENANT", db: Session = Depends(get_db)):
    """Handles OAuth callback, provisions/authenticates user, and issues JWT tokens."""
    from app.services.oauth_service import OAuthService
    user, access_token, refresh_token = OAuthService.process_oauth_login(provider, code, db, default_role=role)

    user_resp = UserResponse.model_validate(user)
    token_resp = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=user_resp
    )
    return APIResponse(success=True, message=f"Authenticated via {provider.capitalize()} OAuth", data=token_resp)
