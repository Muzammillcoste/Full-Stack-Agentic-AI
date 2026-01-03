from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User (BaseModel):
    name: str
    age: int
    address: Address
    email: Optional[str] = None
    created_at: datetime = datetime.now()

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')})


# Example usage

if __name__ == "__main__":
    user1 = User(name="John Doe", age=30, address=Address(street="123 Main St", city="Anytown", zip_code="12345",email='exam@.com'))
    print(user1)
    print('--- Serialized Outputs ---')
    print(user1.model_dump())
    print('--- JSON Output ---')
    print(user1.model_dump_json())
