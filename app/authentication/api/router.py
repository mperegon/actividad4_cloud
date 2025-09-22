from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel
from app.authentication.dependency_injection.domain.register_controller import RegisterControllers
from app.authentication.dependency_injection.domain.login_controller import LoginControllers
from app.authentication.dependency_injection.domain.logout_controller import LogoutControllers
from app.authentication.dependency_injection.domain.introspect_controller import IntrospectControllers
from app.authentication.domain.persistences.exceptions import TokenNotFoundException, UsernameAlreadyTakenException, WrongPasswordException, UserNotFoundException


#Creamos el enrutador con su prefijo y etiquetas
router = APIRouter(tags=["Authentication"])

class RegisterInput(BaseModel):
    username: str
    password: str
    mail: str
    year_of_birth: int

class RegisterOutput(BaseModel):
    username: str
    mail: str
    year_of_birth: int


#--------------------------
#register
#--------------------------
@router.post("/register", response_model=RegisterOutput, summary="Register a new user", description="Create a new user account with username, email, password and birth year")


async def register(input: RegisterInput = Body()) -> RegisterOutput:
    register_controller = RegisterControllers.carlemany()
    try:
        user_bo = await register_controller(
            username=input.username,
            password=input.password,
            mail=input.mail,
            year_of_birth=input.year_of_birth,
        )
    except UsernameAlreadyTakenException:
        raise HTTPException(status_code=409, detail="Username already taken")
    
    return RegisterOutput(
        username=user_bo.username,
        mail=user_bo.mail,
        year_of_birth=user_bo.year_of_birth
    )
    



class LoginInput(BaseModel):
    username: str
    password: str

#--------------------------
#login
#--------------------------
@router.post("/login", summary="User login", description="Authenticate user and return auth token")
async def login(input: LoginInput = Body()) -> dict[str, str]:
    login_controller = LoginControllers.carlemany()
    try:
        token = await login_controller(
            username=input.username,
            password=input.password
        )
    except WrongPasswordException:
        raise HTTPException(
            status_code=403,
            detail="Wrong password"
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=404 ,
            detail="User not found"
        )
    return {"auth": token}




#--------------------------
#logout
#--------------------------
@router.delete("/logout", summary="User logout", description="Invalidate auth token and log out user")
async def logout(auth: str = Header(description="Authentication token")) -> dict[str, str]:
    LogoutController = LogoutControllers.carlemany()
    try:
        await LogoutController(token=auth)
    except TokenNotFoundException:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    return {"status": "bye"}



class IntrospectOutput(BaseModel):
    username: str
    mail: str
    year_of_birth: int
    external_id: int

#--------------------------
#Introspect
#--------------------------
@router.get("/introspect", response_model=IntrospectOutput, summary="Get user info", description="Get current user information from auth token")
async def introspect(auth: str = Header(description="Authentication token")) -> IntrospectOutput:
    introspect_controller = IntrospectControllers.carlemany()
    try:
        user_bo = await introspect_controller(token=auth)
    except TokenNotFoundException:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    return IntrospectOutput(
        username=user_bo.username,
        mail=user_bo.mail,
        year_of_birth=user_bo.year_of_birth,
        external_id=user_bo.external_id
    )