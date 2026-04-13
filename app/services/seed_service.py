from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.application import Application, ApplicationStatus
from app.models.offer import Offer
from app.models.user import User


STAFF_PASSWORD = "amogrupo25"

STAFF_SEED = [
    {
        "name": "Carlos Andres Escobar",
        "email": "ca.escobar2434@uniandes.edu.co",
        "department": "Ingenieria",
        "language": "es",
        "is_dark_mode": False,
    },
    {
        "name": "Laura Martinez",
        "email": "laura.martinez.staff@uniandes.edu.co",
        "department": "Administracion",
        "language": "es",
        "is_dark_mode": True,
    },
    {
        "name": "Felipe Rojas",
        "email": "felipe.rojas.staff@uniandes.edu.co",
        "department": "Fisica",
        "language": "es",
        "is_dark_mode": False,
    },
    {
        "name": "Natalia Gomez",
        "email": "natalia.gomez.staff@uniandes.edu.co",
        "department": "Diseno",
        "language": "es",
        "is_dark_mode": True,
    },
    {
        "name": "Santiago Cardenas",
        "email": "santiago.cardenas.staff@uniandes.edu.co",
        "department": "Deportes",
        "language": "es",
        "is_dark_mode": False,
    },
    {
        "name": "Daniela Prieto",
        "email": "daniela.prieto.staff@uniandes.edu.co",
        "department": "Historia",
        "language": "es",
        "is_dark_mode": True,
    },
    {
        "name": "Miguel Parra",
        "email": "miguel.parra.staff@uniandes.edu.co",
        "department": "Economia",
        "language": "es",
        "is_dark_mode": False,
    },
    {
        "name": "Juliana Beltran",
        "email": "juliana.beltran.staff@uniandes.edu.co",
        "department": "Arquitectura",
        "language": "es",
        "is_dark_mode": True,
    },
    {
        "name": "Tomas Molina",
        "email": "tomas.molina.staff@uniandes.edu.co",
        "department": "Derecho",
        "language": "es",
        "is_dark_mode": False,
    },
    {
        "name": "Maria Fernanda Ruiz",
        "email": "maria.ruiz.staff@uniandes.edu.co",
        "department": "Medicina",
        "language": "es",
        "is_dark_mode": True,
    },
]

OFFER_TEMPLATES = [
    {
        "title": "Apoyo Administrativo",
        "description": "Apoyo operativo y organizacion de documentos para actividades internas.",
        "requirements": "Estudiante activo\nBuena organizacion\nAtencion al detalle",
        "category": "Administrativo",
        "value_cop": 85000,
        "duration_hours": 4,
        "is_on_site": True,
        "location": "Edificio SD, piso 2",
    },
    {
        "title": "Monitor Academico",
        "description": "Acompanamiento a estudiantes en sesiones de apoyo academico.",
        "requirements": "Promedio mayor a 3.8\nBuenas habilidades de comunicacion\nPuntualidad",
        "category": "Academico",
        "value_cop": 110000,
        "duration_hours": 3,
        "is_on_site": True,
        "location": "Edificio W, salon 301",
    },
    {
        "title": "Apoyo de Investigacion",
        "description": "Soporte en recoleccion y organizacion de informacion para proyectos.",
        "requirements": "Manejo de hojas de calculo\nCapacidad analitica\nResponsabilidad",
        "category": "Investigacion",
        "value_cop": 125000,
        "duration_hours": 5,
        "is_on_site": False,
        "location": "Remoto",
    },
    {
        "title": "Asistente de Eventos",
        "description": "Apoyo logistico en jornadas, talleres y eventos institucionales.",
        "requirements": "Trabajo en equipo\nDisponibilidad entre semana\nActitud de servicio",
        "category": "Administrativo",
        "value_cop": 90000,
        "duration_hours": 6,
        "is_on_site": True,
        "location": "Centro Civico, lobby principal",
    },
    {
        "title": "Auxiliar de Laboratorio",
        "description": "Preparacion de materiales y acompanamiento en practicas guiadas.",
        "requirements": "Experiencia previa o curso relacionado\nCuidado del material\nSeguimiento de instrucciones",
        "category": "Academico",
        "value_cop": 130000,
        "duration_hours": 4,
        "is_on_site": True,
        "location": "Edificio ML, laboratorio 102",
    },
    {
        "title": "Apoyo de Biblioteca",
        "description": "Organizacion de material bibliografico y orientacion basica a usuarios.",
        "requirements": "Orden\nBuen trato al usuario\nResponsabilidad",
        "category": "Administrativo",
        "value_cop": 80000,
        "duration_hours": 4,
        "is_on_site": True,
        "location": "Biblioteca General",
    },
    {
        "title": "Asistente de Comunicaciones",
        "description": "Creacion de piezas, apoyo en contenido y cubrimiento de actividades.",
        "requirements": "Canva o Figma\nRedaccion clara\nCreatividad",
        "category": "Investigacion",
        "value_cop": 115000,
        "duration_hours": 5,
        "is_on_site": False,
        "location": "Remoto",
    },
    {
        "title": "Auxiliar de Bienestar",
        "description": "Apoyo en jornadas estudiantiles, inscripciones y logistica de bienestar.",
        "requirements": "Servicio al cliente\nDisponibilidad diurna\nTrabajo colaborativo",
        "category": "Administrativo",
        "value_cop": 95000,
        "duration_hours": 6,
        "is_on_site": True,
        "location": "Centro de Bienestar",
    },
]

CAREERS = [
    "Ingenieria de Sistemas",
    "Ingenieria Industrial",
    "Administracion",
    "Economia",
    "Derecho",
    "Diseno",
    "Matematicas",
    "Fisica",
    "Medicina",
    "Historia",
]

FIRST_NAMES = [
    "Ana",
    "Mateo",
    "Sofia",
    "Diego",
    "Valeria",
    "Juan",
    "Camila",
    "Andres",
    "Paula",
    "Nicolas",
]

LAST_NAMES = [
    "Garcia",
    "Lopez",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Gomez",
    "Diaz",
    "Castro",
    "Rojas",
    "Vargas",
]

AVAILABILITIES = ["part_time", "flexible", "full_time"]
APPLICATION_STATUSES = [
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.accepted,
    ApplicationStatus.rejected,
]


def _build_staff_users() -> list[User]:
    users: list[User] = []
    for staff_data in STAFF_SEED:
        users.append(
            User(
                name=staff_data["name"],
                email=staff_data["email"],
                password_hash=hash_password(STAFF_PASSWORD),
                department=staff_data["department"],
                role="staff",
                language=staff_data["language"],
                is_dark_mode=staff_data["is_dark_mode"],
            )
        )
    return users


def _build_offers(staff_users: list[User]) -> list[Offer]:
    now = datetime.now().replace(second=0, microsecond=0)
    offers: list[Offer] = []

    for staff_index, staff in enumerate(staff_users):
        for template_index, template in enumerate(OFFER_TEMPLATES):
            date_time = now + timedelta(days=2 + (staff_index * 4) + template_index)
            offers.append(
                Offer(
                    staff_id=staff.id,
                    title=f'{template["title"]} {staff_index + 1}-{template_index + 1}',
                    description=f'{template["description"]} Responsable: {staff.name}.',
                    requirements=template["requirements"],
                    category=template["category"],
                    value_cop=template["value_cop"] + (staff_index * 5000),
                    date_time=date_time,
                    deadline=date_time - timedelta(days=1),
                    duration_hours=template["duration_hours"],
                    is_on_site=template["is_on_site"],
                    location=template["location"],
                )
            )

    return offers


def _build_applicant_name(index: int) -> str:
    first = FIRST_NAMES[index % len(FIRST_NAMES)]
    last = LAST_NAMES[(index // len(FIRST_NAMES)) % len(LAST_NAMES)]
    return f"{first} {last} {index + 1}"


def _build_student_email(index: int) -> str:
    return f"applicant{index + 1:02d}@uniandes.edu.co"


def _build_pending_applications(offers: list[Offer]) -> list[Application]:
    applications: list[Application] = []

    for offer_index, offer in enumerate(offers):
        for offset, status in enumerate(APPLICATION_STATUSES):
            applicant_index = (offer_index * len(APPLICATION_STATUSES)) + offset
            applications.append(
                Application(
                    offer_id=offer.id,
                    offer_title=offer.title,
                    student_name=_build_applicant_name(applicant_index),
                    student_email=_build_student_email(applicant_index),
                    applicant_name=_build_applicant_name(applicant_index),
                    career=CAREERS[applicant_index % len(CAREERS)],
                    semester=(applicant_index % 8) + 2,
                    gpa=round(3.2 + ((applicant_index % 15) * 0.1), 2),
                    availability=AVAILABILITIES[applicant_index % len(AVAILABILITIES)],
                    motivation_letter=(
                        f"Quiero aplicar a {offer.title} para ganar experiencia "
                        "y apoyar a la Universidad de los Andes."
                    ),
                    status=status,
                )
            )

    return applications


def seed_if_empty(db: Session):
    if db.query(Offer).first():
        return

    staff_users = _build_staff_users()
    db.add_all(staff_users)
    db.commit()

    for staff in staff_users:
        db.refresh(staff)

    offers = _build_offers(staff_users)
    db.add_all(offers)
    db.commit()

    for offer in offers:
        db.refresh(offer)

    applications = _build_pending_applications(offers)
    db.bulk_save_objects(applications)
    db.commit()
