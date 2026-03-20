from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.models.offer import Offer
from app.models.application import Application, ApplicationStatus


def seed_if_empty(db: Session):
    if db.query(Offer).first():
        return

    # ── Staff user ────────────────────────────────────────────────
    staff = db.query(User).first()
    if not staff:
        staff = User(
            name="Juan Pérez",
            email="juan.perez@uniandes.edu.co",
            password_hash=hash_password("123456"),
            department="Ingeniería",
            role="staff",
            language="es",
            is_dark_mode=False,
        )
        db.add(staff)
        db.commit()
        db.refresh(staff)

    now = datetime.now()

    # ── Offers (5 total, varied categories) ───────────────────────
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
    offer3 = Offer(
        staff_id=staff.id,
        title="Monitor Cálculo Integral",
        description="Acompañamiento académico a estudiantes de Cálculo Integral en sesiones de tutoría.",
        requirements="Cálculo Integral aprobado con nota >= 4.0\nHabilidades pedagógicas\nPaciencia",
        category="Académico",
        value_cop=100000,
        date_time=now + timedelta(days=7),
        deadline=now + timedelta(days=5),
        duration_hours=3,
        is_on_site=True,
        location="Edificio W, Salón 301",
    )
    offer4 = Offer(
        staff_id=staff.id,
        title="Diseñador Redes Sociales",
        description="Creación de contenido visual para las redes sociales de Bienestar Universitario.",
        requirements="Manejo de Canva o Figma\nCreatividad\nDisponibilidad 10 hrs/semana",
        category="Comunicaciones",
        value_cop=150000,
        date_time=now + timedelta(days=10),
        deadline=now + timedelta(days=8),
        duration_hours=10,
        is_on_site=False,
        location="Remoto",
    )
    offer5 = Offer(
        staff_id=staff.id,
        title="Auxiliar Deportivo",
        description="Apoyo logístico en eventos deportivos y torneos internos de la universidad.",
        requirements="Interés en deportes\nDisponibilidad sábados\nTrabajo en equipo",
        category="Deporte",
        value_cop=70000,
        date_time=now + timedelta(days=3),
        deadline=now + timedelta(days=2),
        duration_hours=5,
        is_on_site=True,
        location="Centro Deportivo Uniandes",
    )

    db.add_all([offer1, offer2, offer3, offer4, offer5])
    db.commit()
    for o in [offer1, offer2, offer3, offer4, offer5]:
        db.refresh(o)

    # ── Seed student — used to test GET /applications/my ──────────
    student = User(
        name="Juan Perez",
        email="juan.perez.student@uniandes.edu.co",
        password_hash=hash_password("123456"),
        department="Ingeniería",
        role="student",
        language="es",
        is_dark_mode=False,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    # ── Applications (15 total + 3 for seed student) ──────────────
    apps = [
        # Offer 1: Apoyo Biblioteca — 4 apps
        Application(
            offer_id=offer1.id, offer_title=offer1.title,
            student_name="Ana Gómez", student_email="ana.gomez@uniandes.edu.co",
            applicant_name="Ana Gómez", career="Administración de Empresas",
            semester=6, gpa=4.2, availability="part_time",
            motivation_letter="Me interesa apoyar la biblioteca y mejorar mis habilidades organizativas.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer1.id, offer_title=offer1.title,
            student_name="Mateo Ríos", student_email="mateo.rios@uniandes.edu.co",
            applicant_name="Mateo Ríos", career="Ingeniería Industrial",
            semester=4, gpa=3.8, availability="flexible",
            motivation_letter="Busco experiencia laboral y contribuir al ambiente universitario.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer1.id, offer_title=offer1.title,
            student_name="Sofía Mendoza", student_email="sofia.mendoza@uniandes.edu.co",
            applicant_name="Sofía Mendoza", career="Literatura",
            semester=7, gpa=4.5, availability="full_time",
            motivation_letter="Amo los libros y quiero aportar a la comunidad lectora.",
            status=ApplicationStatus.rejected,
        ),
        Application(
            offer_id=offer1.id, offer_title=offer1.title,
            student_name="Diego Vargas", student_email="diego.vargas@uniandes.edu.co",
            applicant_name="Diego Vargas", career="Derecho",
            semester=3, gpa=3.6, availability="part_time",
            motivation_letter="Necesito la experiencia laboral para mi hoja de vida.",
            status=ApplicationStatus.pending,
        ),

        # Offer 2: Lab Física — 3 apps
        Application(
            offer_id=offer2.id, offer_title=offer2.title,
            student_name="Laura Díaz", student_email="laura.diaz@uniandes.edu.co",
            applicant_name="Laura Díaz", career="Física",
            semester=8, gpa=4.7, availability="full_time",
            motivation_letter="Tengo experiencia en laboratorio y deseo apoyar a estudiantes de semestres menores.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer2.id, offer_title=offer2.title,
            student_name="Carlos Herrera", student_email="carlos.herrera@uniandes.edu.co",
            applicant_name="Carlos Herrera", career="Ingeniería Eléctrica",
            semester=5, gpa=3.5, availability="part_time",
            motivation_letter="Quiero poner en práctica los conocimientos de física que he adquirido.",
            status=ApplicationStatus.rejected,
        ),
        Application(
            offer_id=offer2.id, offer_title=offer2.title,
            student_name="Valentina Castro", student_email="valentina.castro@uniandes.edu.co",
            applicant_name="Valentina Castro", career="Ingeniería Mecánica",
            semester=6, gpa=4.0, availability="flexible",
            motivation_letter="Me apasiona la física aplicada y quiero experiencia en laboratorio.",
            status=ApplicationStatus.pending,
        ),

        # Offer 3: Monitor Cálculo — 3 apps
        Application(
            offer_id=offer3.id, offer_title=offer3.title,
            student_name="Andrés Morales", student_email="andres.morales@uniandes.edu.co",
            applicant_name="Andrés Morales", career="Matemáticas",
            semester=7, gpa=4.8, availability="part_time",
            motivation_letter="He sido monitor antes y quiero seguir ayudando a otros estudiantes.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer3.id, offer_title=offer3.title,
            student_name="Camila Torres", student_email="camila.torres@uniandes.edu.co",
            applicant_name="Camila Torres", career="Ingeniería de Sistemas",
            semester=5, gpa=4.3, availability="flexible",
            motivation_letter="Cálculo es mi materia favorita y me gustaría compartir ese conocimiento.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer3.id, offer_title=offer3.title,
            student_name="Julián Ospina", student_email="julian.ospina@uniandes.edu.co",
            applicant_name="Julián Ospina", career="Ingeniería Civil",
            semester=4, gpa=3.9, availability="full_time",
            motivation_letter="Quiero reforzar mis conocimientos de cálculo ayudando a otros.",
            status=ApplicationStatus.pending,
        ),

        # Offer 4: Diseñador Redes — 3 apps
        Application(
            offer_id=offer4.id, offer_title=offer4.title,
            student_name="Isabella Ruiz", student_email="isabella.ruiz@uniandes.edu.co",
            applicant_name="Isabella Ruiz", career="Diseño",
            semester=6, gpa=4.1, availability="flexible",
            motivation_letter="Tengo portafolio de diseño y experiencia con Figma y redes sociales.",
            status=ApplicationStatus.rejected,
        ),
        Application(
            offer_id=offer4.id, offer_title=offer4.title,
            student_name="Nicolás Peña", student_email="nicolas.pena@uniandes.edu.co",
            applicant_name="Nicolás Peña", career="Comunicación Social",
            semester=3, gpa=3.4, availability="part_time",
            motivation_letter="Me encanta crear contenido y tengo experiencia con Canva.",
            status=ApplicationStatus.rejected,
        ),
        Application(
            offer_id=offer4.id, offer_title=offer4.title,
            student_name="Mariana López", student_email="mariana.lopez@uniandes.edu.co",
            applicant_name="Mariana López", career="Arte",
            semester=8, gpa=4.6, availability="full_time",
            motivation_letter="El diseño digital es mi especialidad, puedo aportar mucho.",
            status=ApplicationStatus.pending,
        ),

        # Offer 5: Auxiliar Deportivo — 2 apps
        Application(
            offer_id=offer5.id, offer_title=offer5.title,
            student_name="Santiago Mejía", student_email="santiago.mejia@uniandes.edu.co",
            applicant_name="Santiago Mejía", career="Ingeniería de Sistemas",
            semester=2, gpa=3.7, availability="flexible",
            motivation_letter="Practico fútbol y voleibol, me encantaría ayudar en los torneos.",
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer5.id, offer_title=offer5.title,
            student_name="Paula Sánchez", student_email="paula.sanchez@uniandes.edu.co",
            applicant_name="Paula Sánchez", career="Medicina",
            semester=4, gpa=4.4, availability="part_time",
            motivation_letter="Me interesa el deporte y puedo ayudar con primeros auxilios si se necesita.",
            status=ApplicationStatus.pending,
        ),

        # Seed student applications — covers all 3 statuses for MyApplicationsScreen testing
        Application(
            offer_id=offer1.id,
            student_name=student.name,
            student_email=student.email,
            status=ApplicationStatus.accepted,
        ),
        Application(
            offer_id=offer2.id,
            student_name=student.name,
            student_email=student.email,
            status=ApplicationStatus.pending,
        ),
        Application(
            offer_id=offer3.id,
            student_name=student.name,
            student_email=student.email,
            status=ApplicationStatus.rejected,
        ),
    ]

    db.add_all(apps)
    db.commit()