from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId

import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone


# ============================================================
# APP
# ============================================================

app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# MONGODB
# ============================================================

URL = "mongodb://127.0.0.1:27017"

client = MongoClient(URL)

db = client["richest_tickets_db"]

ticket_collection = db["tickets"]
user_collection = db["users"]


# ============================================================
# SECURITY
# ============================================================

password_hash = PasswordHash.recommended()

SECRET_KEY = "ITServiceDeskSecurityKey-ChangeThis"

ALGORITHM = "HS256"

TOKEN_EXPIRE_MINS = 30


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# ============================================================
# USER SCHEMA
# ============================================================

class UserCreate(BaseModel):

    username: str
    password: str
    name: str
    email: str
    phone: str
    department: str
    role: int


class UserUpdate(BaseModel):

    username: str
    name: str
    email: str
    phone: str
    department: str
    role: int


class UserResponse(BaseModel):

    id: str
    username: str
    name: str
    email: str
    phone: str
    department: str
    role: int


# ============================================================
# LOGIN SCHEMA
# ============================================================

class LoginData(BaseModel):

    username: str
    password: str


# ============================================================
# TOKEN RESPONSE
# ============================================================

class TokenResponse(BaseModel):

    access_token: str
    token_type: str


# ============================================================
# TICKET SCHEMA
# ============================================================

class TicketCreate(BaseModel):

    title: str
    description: str
    category: str
    status: str


class TicketResponse(TicketCreate):

    id: str


# ============================================================
# USER HELPER
# ============================================================

def user_helper(user):

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "department": user["department"],
        "role": user["role"]
    }


# ============================================================
# TICKET HELPER
# ============================================================

def ticket_helper(ticket):

    return {
        "id": str(ticket["_id"]),
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "status": ticket["status"]
    }


# ============================================================
# CREATE JWT TOKEN
# ============================================================

def create_token(username: str, role: int):

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=TOKEN_EXPIRE_MINS)
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        role = payload.get("role")

        if username is None or role is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = user_collection.find_one({
        "username": username
    })

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ============================================================
# ROLE CHECK
#
# 1 = Employee
# 2 = Support Engineer
# 3 = Team Lead
# 4 = Admin
# ============================================================

def require_roles(*allowed_roles):

    def check_role(
        current_user=Depends(get_current_user)
    ):

        if current_user["role"] not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return check_role


# ============================================================
# ============================================================
# USER APIs
# ============================================================
# ============================================================


# ============================================================
# CREATE USER
# ============================================================

@app.post(
    "/users",
    status_code=201,
    response_model=UserResponse
)
def create_user(user: UserCreate):

    # Check username
    existing_user = user_collection.find_one({
        "username": user.username
    })

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    # Hash password
    hashed_password = password_hash.hash(
        user.password
    )

    # Save user
    user_data = {

        "username": user.username,

        "password": hashed_password,

        "name": user.name,

        "email": user.email,

        "phone": user.phone,

        "department": user.department,

        "role": user.role
    }

    result = user_collection.insert_one(
        user_data
    )

    new_user = user_collection.find_one({
        "_id": result.inserted_id
    })

    return user_helper(new_user)


# ============================================================
# READ ALL USERS
# ============================================================

@app.get(
    "/users",
    response_model=list[UserResponse]
)
def read_all_users(
    current_user=Depends(
        require_roles(2, 3, 4)
    )
):

    users = user_collection.find()

    result = [
        user_helper(user)
        for user in users
    ]

    return result


# ============================================================
# READ USER BY ID
# ============================================================

@app.get(
    "/users/{id}",
    response_model=UserResponse
)
def read_user_by_id(
    id: str,
    current_user=Depends(
        require_roles(2, 3, 4)
    )
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    user = user_collection.find_one({
        "_id": ObjectId(id)
    })

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_helper(user)


# ============================================================
# UPDATE USER
# ============================================================

@app.put(
    "/users/{id}",
    response_model=UserResponse
)
def update_user(
    id: str,
    user: UserUpdate,
    current_user=Depends(
        require_roles(3, 4)
    )
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    # Check if another user has same username
    existing_user = user_collection.find_one({
        "username": user.username,
        "_id": {
            "$ne": ObjectId(id)
        }
    })

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    result = user_collection.update_one(

        {
            "_id": ObjectId(id)
        },

        {
            "$set": {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "department": user.department,
                "role": user.role
            }
        }
    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    updated_user = user_collection.find_one({
        "_id": ObjectId(id)
    })

    return user_helper(updated_user)


# ============================================================
# DELETE USER
# ============================================================

@app.delete("/users/{id}")
def delete_user(
    id: str,
    current_user=Depends(
        require_roles(4)
    )
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    result = user_collection.delete_one({
        "_id": ObjectId(id)
    })

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }


# ============================================================
# ============================================================
# LOGIN
# ============================================================
# ============================================================

@app.post(
    "/login",
    response_model=TokenResponse
)
def login(payload: LoginData):

    # Find user using username
    user = user_collection.find_one({
        "username": payload.username
    })

    # Username doesn't exist
    if not user:

        raise HTTPException(
            status_code=401,
            detail="Wrong username or password"
        )

    # Check password
    password_correct = password_hash.verify(
        payload.password,
        user["password"]
    )

    if not password_correct:

        raise HTTPException(
            status_code=401,
            detail="Wrong username or password"
        )

    # Create JWT token
    token = create_token(
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ============================================================
# ============================================================
# TICKET APIs
# ============================================================
# ============================================================


# ============================================================
# CREATE TICKET
# ============================================================

@app.post(
    "/tickets",
    status_code=201,
    response_model=TicketResponse
)
def create_ticket(
    payload: TicketCreate,
    current_user=Depends(
        require_roles(1, 2, 3, 4)
    )
):

    ticket_data = payload.model_dump()

    result = ticket_collection.insert_one(
        ticket_data
    )

    new_ticket = ticket_collection.find_one({
        "_id": result.inserted_id
    })

    return ticket_helper(new_ticket)


# ============================================================
# READ ALL TICKETS
# ============================================================

@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def read_all_tickets(
    current_user=Depends(
        require_roles(1, 2, 3, 4)
    )
):

    tickets_result = ticket_collection.find()

    tickets = [
        ticket_helper(ticket)
        for ticket in tickets_result
    ]

    return tickets


# ============================================================
# READ TICKET BY ID
# ============================================================

@app.get(
    "/tickets/{id}",
    response_model=TicketResponse
)
def read_ticket_by_id(
    id: str,
    current_user=Depends(
        require_roles(1, 2, 3, 4)
    )
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid ticket ID format"
        )

    ticket = ticket_collection.find_one({
        "_id": ObjectId(id)
    })

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket_helper(ticket)


# ============================================================
# UPDATE TICKET
# ============================================================

@app.put(
    "/tickets/{id}",
    response_model=TicketResponse
)
def update_ticket(
    id: str,
    payload: TicketCreate,
    current_user=Depends(
        require_roles(2, 3, 4)
    )
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid ticket ID format"
        )

    result = ticket_collection.update_one(

        {
            "_id": ObjectId(id)
        },

        {
            "$set": payload.model_dump()
        }
    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    updated_ticket = ticket_collection.find_one({
        "_id": ObjectId(id)
    })

    return ticket_helper(updated_ticket)


# ============================================================
# DELETE TICKET
# ============================================================

@app.delete("/tickets/{id}")
def delete_ticket(
    id: str,
    current_user=Depends(
        require_roles(4)
    )
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid ticket ID format"
        )

    result = ticket_collection.delete_one({
        "_id": ObjectId(id)
    })

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return {
        "message": "Ticket deleted successfully"
    }
