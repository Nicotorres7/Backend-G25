from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.models.offer import Offer
from app.models.application import Application, ApplicationStatus


def seed_if_empty(db: Session):
    if db.query(Offer).first():
        return

    # Create a staff user if none exists
    staff = db.query(User).first()
    if not staff:
        staff = User(
            name="Juan Pérez",
            email="juan.perez@uniandes.edu.co",
            password_hash=hash_password("123456"),
            department="Ingeniería",
            language="es",
            is_dark_mode=False,
        )
        db.add(staff)
        db.commit()
        db.refresh(staff)

    now = datetime.now()

    offer1 = Offer(
        staff_id=staff.id,
        title="Apoyo Biblioteca",
        description="Apoyo en tareas operativas y atención básica durante eventos universitarios.",
        requirements="Estudiante activo\nDisponibilidad fines de semana\nBuena presentación personal",
        category="Administrativo",
        value_cop=80000,
        date_time=now + timedelta(days=2),
        deadline=now + timedelta(days=1),
        duration_hours=4,
        is_on_site=True,
        location="Biblioteca General, Edificio ML, Piso 1",
    )
    offer2 = Offer(
        staff_id=staff.id,
        title="Asistente Laboratorio Física",
        description="Ayuda con inventario y preparación de materiales para prácticas de física.",
        requirements="Curso Física I aprobado\nManejo de equipos de laboratorio\nCuidado y precisión",
        category="Académico",
        value_cop=120000,
        date_time=now + timedelta(days=5),
        deadline=now + timedelta(days=3),
        duration_hours=6,
        is_on_site=True,
        location="Edificio Mario Laserna, Lab 102",
    )
    db.add_all([offer1, offer2])
    db.commit()
    db.refresh(offer1)
    db.refresh(offer2)

    apps = [
        Application(
            offer_id=offer1.id,
            offer_title=offer1.title,
            student_name="Ana Gómez",
            student_email="ana.gomez@uniandes.edu.co",
            applicant_name="Ana Gómez",
            career="Administración de Empresas",
            semester=6,
            gpa=4.2,
            availability="part_time",
            motivation_letter="Me interesa apoyar la biblioteca y mejorar mis habilidades organizativas.",
            status=ApplicationStatus.pending,
        ),
        Application(
            offer_id=offer1.id,
            offer_title=offer1.title,
            student_name="Mateo Ríos",
            student_email="mateo.rios@uniandes.edu.co",
            applicant_name="Mateo Ríos",
            career="Ingeniería Industrial",
            semester=4,
            gpa=3.8,
            availability="flexible",
            motivation_letter="Busco experiencia laboral y contribuir al ambiente universitario.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer2.id,
            offer_title=offer2.title,
            student_name="Laura Díaz",
            student_email="laura.diaz@uniandes.edu.co",
            applicant_name="Laura Díaz",
            career="Física",
            semester=8,
            gpa=4.7,
            availability="full_time",
            motivation_letter="Tengo experiencia en laboratorio y deseo apoyar a estudiantes de semestres menores.",
            status=ApplicationStatus.rejected,
        ),
        Application(
            offer_id=offer2.id,
            offer_title=offer2.title,
            student_name="Carlos Herrera",
            student_email="carlos.herrera@uniandes.edu.co",
            applicant_name="Carlos Herrera",
            career="Ingeniería Eléctrica",
            semester=5,
            gpa=3.5,
            availability="part_time",
            motivation_letter="Quiero poner en práctica los conocimientos de física que he adquirido.",
            status=ApplicationStatus.pending,
        ),
    ]
    db.add_all(apps)
    db.commit()
