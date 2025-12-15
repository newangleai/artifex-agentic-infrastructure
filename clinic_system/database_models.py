from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class InsuranceType(Enum):
    PARTICULAR = "particular"
    HEALTH_PLAN = "plano_saude"

class AppointmentStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

@dataclass
class InsurancePlan:
    id: int
    name: str
    coverage_percentage: float
    max_consultation_price: float
    acceptance_regions: List[str]
    specialties_covered: List[str]
    
    def covers_specialty(self, specialty: str) -> bool:
        return specialty.lower() in [s.lower() for s in self.specialties_covered]
    
    def accepts_region(self, region: str) -> bool:
        
        return region.lower() in [r.lower() for r in self.acceptance_regions]

@dataclass
class Doctor:
    
    id: int
    name: str
    specialty: str
    crm: str
    clinic_id: int
    accepted_insurance_plans: List[int]
    consultation_price: float
    available_slots: List['Slot'] = field(default_factory=list)
    
    def accepts_insurance_plan(self, plan_id: int) -> bool:
        
        return plan_id in self.accepted_insurance_plans
    
    def has_available_slots(self) -> bool:
        
        return len([s for s in self.available_slots if not s.is_booked]) > 0

@dataclass
class Slot:
    
    id: int
    doctor_id: int
    date: str
    time: str
    is_booked: bool = False
    appointment_id: Optional[int] = None
    
    @property
    def datetime_str(self) -> str:
        
        return f"{self.date} {self.time}"

@dataclass
class Clinic:
    
    id: int
    name: str
    address: str
    city: str
    state: str
    phone: str
    email: str
    doctors: List[Doctor] = field(default_factory=list)
    accepted_insurance_plans: List[int] = field(default_factory=list)
    
    def get_doctor_by_specialty(self, specialty: str) -> List[Doctor]:
        
        return [d for d in self.doctors if d.specialty.lower() == specialty.lower()]
    
    def get_available_doctors_for_plan(self, plan_id: int, specialty: str) -> List[Doctor]:
        
        return [
            d for d in self.get_doctor_by_specialty(specialty)
            if d.accepts_insurance_plan(plan_id) and d.has_available_slots()
        ]

@dataclass
class Patient:
    
    id: int
    name: str
    email: str
    phone: str
    cpf: str
    date_of_birth: str
    address: str
    city: str
    state: str
    insurance_type: InsuranceType
    insurance_plan_id: Optional[int] = None
    preferred_clinic_id: Optional[int] = None
    
    def is_valid(self) -> bool:
        
        required_fields = [self.name, self.email, self.phone, self.cpf]
        return all(required_fields)

@dataclass
class Appointment:
    
    id: int
    patient_id: int
    doctor_id: int
    clinic_id: int
    slot_id: int
    appointment_datetime: str
    insurance_type: InsuranceType
    insurance_plan_id: Optional[int]
    status: AppointmentStatus = AppointmentStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    confirmed_at: Optional[str] = None
    cancelled_at: Optional[str] = None
    cancellation_reason: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        
        return asdict(self)

class DatabaseService:
    
    
    def __init__(self):
        
        self.clinics: Dict[int, Clinic] = {}
        self.doctors: Dict[int, Doctor] = {}
        self.patients: Dict[int, Patient] = {}
        self.appointments: Dict[int, Appointment] = {}
        self.insurance_plans: Dict[int, InsurancePlan] = {}
        self.slots: Dict[int, Slot] = {}
        
        self._init_sample_data()
    
    def _init_sample_data(self):
        
        

        self.insurance_plans[1] = InsurancePlan(
            id=1,
            name="Unimed",
            coverage_percentage=80,
            max_consultation_price=500,
            acceptance_regions=["São Paulo", "Rio de Janeiro"],
            specialties_covered=["Cardiologia", "Oftalmologia", "Pediatria"]
        )
        
        self.insurance_plans[2] = InsurancePlan(
            id=2,
            name="Amil",
            coverage_percentage=85,
            max_consultation_price=600,
            acceptance_regions=["São Paulo", "Brasília"],
            specialties_covered=["Cardiologia", "Dermatologia", "Oftalmologia"]
        )
        
        self.insurance_plans[3] = InsurancePlan(
            id=3,
            name="Bradesco Saúde",
            coverage_percentage=75,
            max_consultation_price=400,
            acceptance_regions=["São Paulo", "Belo Horizonte"],
            specialties_covered=["Cardiologia", "Pediatria", "Dermatologia"]
        )
        

        clinic1 = Clinic(
            id=1,
            name="Clínica Cardio Center",
            address="Av. Paulista 1000",
            city="São Paulo",
            state="SP",
            phone="(11) 3000-0001",
            email="cardio@clinic.com",
            accepted_insurance_plans=[1, 2, 3]
        )
        
        clinic2 = Clinic(
            id=2,
            name="Clínica Oftalmológica Vision",
            address="Rua Augusta 500",
            city="São Paulo",
            state="SP",
            phone="(11) 3000-0002",
            email="vision@clinic.com",
            accepted_insurance_plans=[1, 2]
        )
        
        self.clinics[1] = clinic1
        self.clinics[2] = clinic2
        

        doctor1 = Doctor(
            id=1,
            name="Dr. Carlos Santos",
            specialty="Cardiologia",
            crm="12345",
            clinic_id=1,
            accepted_insurance_plans=[1, 2, 3],
            consultation_price=350
        )
        
        doctor2 = Doctor(
            id=2,
            name="Dra. Marina Silva",
            specialty="Pediatria",
            crm="12346",
            clinic_id=1,
            accepted_insurance_plans=[1, 3],
            consultation_price=250
        )
        

        doctor3 = Doctor(
            id=3,
            name="Dr. Roberto Costa",
            specialty="Oftalmologia",
            crm="12347",
            clinic_id=2,
            accepted_insurance_plans=[1, 2],
            consultation_price=300
        )
        
        self.doctors[1] = doctor1
        self.doctors[2] = doctor2
        self.doctors[3] = doctor3
        
        clinic1.doctors = [doctor1, doctor2]
        clinic2.doctors = [doctor3]
        

        slots = [
            Slot(id=1, doctor_id=1, date="2025-12-15", time="14:00"),
            Slot(id=2, doctor_id=1, date="2025-12-15", time="14:30"),
            Slot(id=3, doctor_id=1, date="2025-12-15", time="15:00"),
            Slot(id=4, doctor_id=2, date="2025-12-16", time="10:00"),
            Slot(id=5, doctor_id=2, date="2025-12-16", time="10:30"),
            Slot(id=6, doctor_id=3, date="2025-12-17", time="16:00"),
            Slot(id=7, doctor_id=3, date="2025-12-17", time="16:30"),
        ]
        
        for slot in slots:
            self.slots[slot.id] = slot
            self.doctors[slot.doctor_id].available_slots.append(slot)
    

    
    def search_clinics(self, specialty: Optional[str] = None, 
                      city: Optional[str] = None) -> List[Clinic]:
        
        results = list(self.clinics.values())
        
        if specialty:
            results = [
                c for c in results 
                if any(d.specialty.lower() == specialty.lower() for d in c.doctors)
            ]
        
        if city:
            results = [c for c in results if c.city.lower() == city.lower()]
        
        return results
    
    def get_clinic_by_id(self, clinic_id: int) -> Optional[Clinic]:
        
        return self.clinics.get(clinic_id)
    

    
    def get_doctors_by_specialty_and_plan(self, specialty: str, 
                                         plan_id: Optional[int] = None,
                                         city: Optional[str] = None) -> List[Dict]:
        
        doctors = []
        
        for doctor in self.doctors.values():
            if doctor.specialty.lower() != specialty.lower():
                continue
            
            if plan_id and not doctor.accepts_insurance_plan(plan_id):
                continue
            
            clinic = self.clinics.get(doctor.clinic_id)
            if city and clinic and clinic.city.lower() != city.lower():
                continue
            
            if not doctor.has_available_slots():
                continue
            
            clinic_info = {
                "doctor_id": doctor.id,
                "doctor_name": doctor.name,
                "specialty": doctor.specialty,
                "clinic_id": doctor.clinic_id,
                "clinic_name": clinic.name if clinic else "Unknown",
                "consultation_price": doctor.consultation_price,
                "available_slots": len([s for s in doctor.available_slots if not s.is_booked])
            }
            doctors.append(clinic_info)
        
        return doctors
    
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Doctor]:
        
        return self.doctors.get(doctor_id)
    

    
    def get_available_slots(self, doctor_id: int, 
                           date: Optional[str] = None) -> List[Dict]:
        
        doctor = self.doctors.get(doctor_id)
        if not doctor:
            return []
        
        available = [s for s in doctor.available_slots if not s.is_booked]
        
        if date:
            available = [s for s in available if s.date == date]
        
        return [
            {
                "slot_id": s.id,
                "doctor_id": s.doctor_id,
                "date": s.date,
                "time": s.time,
                "datetime": s.datetime_str
            }
            for s in available
        ]
    
    def get_slot_by_id(self, slot_id: int) -> Optional[Slot]:
        
        return self.slots.get(slot_id)
    
    def book_slot(self, slot_id: int, appointment_id: int) -> bool:
        
        slot = self.slots.get(slot_id)
        if not slot or slot.is_booked:
            return False
        
        slot.is_booked = True
        slot.appointment_id = appointment_id
        return True
    

    
    def create_or_get_patient(self, **patient_data) -> Patient:
        
        cpf = patient_data.get('cpf')
        
        for patient in self.patients.values():
            if patient.cpf == cpf:
                return patient
        
        patient_id = max(self.patients.keys()) + 1 if self.patients else 1
        
        insurance_plan_id = None
        if patient_data.get('insurance_type') == InsuranceType.HEALTH_PLAN:
            insurance_plan_id = patient_data.get('insurance_plan_id')
        
        patient = Patient(
            id=patient_id,
            name=patient_data.get('name'),
            email=patient_data.get('email'),
            phone=patient_data.get('phone'),
            cpf=cpf,
            date_of_birth=patient_data.get('date_of_birth', ''),
            address=patient_data.get('address', ''),
            city=patient_data.get('city', ''),
            state=patient_data.get('state', ''),
            insurance_type=patient_data.get('insurance_type', InsuranceType.PARTICULAR),
            insurance_plan_id=insurance_plan_id
        )
        
        self.patients[patient_id] = patient
        return patient
    
    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        
        return self.patients.get(patient_id)
    

    
    def create_appointment(self, **appointment_data) -> Optional[Appointment]:
        
        appointment_id = max(self.appointments.keys()) + 1 if self.appointments else 1
        
        appointment = Appointment(
            id=appointment_id,
            patient_id=appointment_data.get('patient_id'),
            doctor_id=appointment_data.get('doctor_id'),
            clinic_id=appointment_data.get('clinic_id'),
            slot_id=appointment_data.get('slot_id'),
            appointment_datetime=appointment_data.get('appointment_datetime'),
            insurance_type=appointment_data.get('insurance_type', InsuranceType.PARTICULAR),
            insurance_plan_id=appointment_data.get('insurance_plan_id'),
            notes=appointment_data.get('notes')
        )
        
        self.appointments[appointment_id] = appointment
        return appointment
    
    def confirm_appointment(self, appointment_id: int) -> bool:
        
        appointment = self.appointments.get(appointment_id)
        if not appointment:
            return False
        
        appointment.status = AppointmentStatus.CONFIRMED
        appointment.confirmed_at = datetime.now().isoformat()
        return True
    
    def cancel_appointment(self, appointment_id: int, reason: str = "") -> bool:
        
        appointment = self.appointments.get(appointment_id)
        if not appointment:
            return False
        
        appointment.status = AppointmentStatus.CANCELLED
        appointment.cancelled_at = datetime.now().isoformat()
        appointment.cancellation_reason = reason
        

        slot = self.slots.get(appointment.slot_id)
        if slot:
            slot.is_booked = False
            slot.appointment_id = None
        
        return True
    
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        
        return self.appointments.get(appointment_id)
    
    def get_appointments_by_patient(self, patient_id: int) -> List[Appointment]:
        
        return [a for a in self.appointments.values() if a.patient_id == patient_id]
    
    def get_appointments_by_clinic(self, clinic_id: int) -> List[Appointment]:
        
        return [a for a in self.appointments.values() if a.clinic_id == clinic_id]
    

    
    def get_insurance_plan_by_id(self, plan_id: int) -> Optional[InsurancePlan]:
        
        return self.insurance_plans.get(plan_id)
    
    def get_insurance_plans_by_region(self, region: str) -> List[InsurancePlan]:
        
        return [
            p for p in self.insurance_plans.values()
            if p.accepts_region(region)
        ]
    
    def validate_insurance_coverage(self, plan_id: int, specialty: str,
                                   consultation_price: float) -> bool:
        
        plan = self.insurance_plans.get(plan_id)
        if not plan:
            return False
        
        return (
            plan.covers_specialty(specialty) and
            consultation_price <= plan.max_consultation_price
        )

db_service = DatabaseService()

def get_db() -> DatabaseService:
    
    return db_service
