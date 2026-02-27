# agents/shared/models.py

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class InsuranceType(Enum):
    PARTICULAR = "particular"
    HEALTH_PLAN = "plano_saude"


class AppointmentStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class InsurancePlan:
    id: int
    name: str
    coverage_percentage: float
    specialties_covered: List[str]


@dataclass
class Doctor:
    id: int
    name: str
    specialty: str
    crm: str
    clinic_id: int
    consultation_price: float
    available_slots: List[Dict] = field(default_factory=list)


@dataclass
class Clinic:
    id: int
    name: str
    address: str
    city: str
    phone: str
