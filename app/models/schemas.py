from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime
from enum import Enum


class KeyType(str, Enum):
    CPF   = "CPF"
    CNPJ  = "CNPJ"
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    EVP   = "EVP"


# ==============================================================================
# REQUESTS
# ==============================================================================

class PixKeyRequest(BaseModel):
    key_type:       KeyType = Field(..., description="Tipo da chave PIX: CPF, CNPJ, PHONE, EMAIL ou EVP")
    key_value:      str     = Field(..., description="Valor da chave PIX")
    amount:         str     = Field("0.01", description="Valor em BRL (ex: '10.00')")
    payment_method: str     = Field("WALLET", description="Método de pagamento: WALLET ou ID do cartão")

    class Config:
        json_schema_extra = {
            "example": {
                "key_type":       "CPF",
                "key_value":      "55537568802",
                "amount":         "10.00",
                "payment_method": "WALLET",
            }
        }


class PixContactRequest(BaseModel):
    person_id:      str = Field(..., description="personId do contato RecargaPay")
    account_id:     str = Field(..., description="accountId do contato RecargaPay")
    amount:         str = Field("0.01", description="Valor em BRL")
    payment_method: str = Field("WALLET", description="Método de pagamento")

    class Config:
        json_schema_extra = {
            "example": {
                "person_id":      "01a044eb-02f1-72c4-aa94-b7a5c1b3d00b",
                "account_id":     "01a044eb-02f1-789c-9973-c02404f22608",
                "amount":         "0.01",
                "payment_method": "WALLET",
            }
        }


class RenewTokenRequest(BaseModel):
    force: bool = Field(False, description="Forçar renovação mesmo se o token ainda for válido")


# ==============================================================================
# RESPONSES
# ==============================================================================

class ReceiverOwner(BaseModel):
    name:          Optional[str] = None
    taxIdNumber:   Optional[str] = None

class ReceiverAccount(BaseModel):
    participantName: Optional[str] = None
    branch:          Optional[str] = None
    accountNumber:   Optional[str] = None
    accountType:     Optional[str] = None

class ReceiverInfo(BaseModel):
    owner:   Optional[ReceiverOwner]   = None
    account: Optional[ReceiverAccount] = None

class PixResponse(BaseModel):
    success:        bool
    pix_id:         str
    cart_id:        str
    run_id:         str
    amount:         str
    payment_method: str
    receiver:       Optional[Dict[str, Any]] = None
    result:         Optional[Dict[str, Any]] = None
    timestamp:      str
    key_type:       Optional[str] = None
    key_value:      Optional[str] = None
    person_id:      Optional[str] = None
    account_id:     Optional[str] = None


class TokenStatus(BaseModel):
    component:  str
    status:     str
    valid:      bool
    expires_in: Optional[str] = None
    auto_renew: bool


class StatusResponse(BaseModel):
    healthy:       bool
    bearer_token:  str
    bearer_valid:  bool
    expires_in_h:  float
    login_count:   int
    last_login:    Optional[str]
    tokens:        List[TokenStatus]
    timestamp:     str


class RenewResponse(BaseModel):
    success:      bool
    new_token:    str
    expires_in_h: float
    timestamp:    str


class ErrorResponse(BaseModel):
    error:      bool = True
    code:       str
    title:      str
    message:    str
    status_code: int


class TransactionRecord(BaseModel):
    id:             str
    type:           str   # "key" | "contact"
    key_type:       Optional[str] = None
    key_value:      Optional[str] = None
    person_id:      Optional[str] = None
    account_id:     Optional[str] = None
    amount:         str
    payment_method: str
    receiver_name:  Optional[str] = None
    receiver_bank:  Optional[str] = None
    status:         str
    pix_id:         str
    cart_id:        str
    run_id:         str
    timestamp:      str


class HistoryResponse(BaseModel):
    total:        int
    transactions: List[TransactionRecord]


class IntegrityHashResponse(BaseModel):
    key_value:      str
    integrity_hash: str
