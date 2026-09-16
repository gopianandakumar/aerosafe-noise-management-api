import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "AeroSafe – Noise Management API | System Architecture & Interview Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, footer_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY – ENGINEERING SPECIFICATION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)
        
        self.restoreState()

def create_aerosafe_pdf(output_filename="AeroSafe_Architecture_Doc.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom palette
    primary = colors.HexColor("#0F172A")
    secondary = colors.HexColor("#2563EB")
    body_color = colors.HexColor("#334155")
    code_bg = colors.HexColor("#F1F5F9")
    callout_bg = colors.HexColor("#EFF6FF")
    callout_border = colors.HexColor("#3B82F6")

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=18
    )
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body_color,
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )
    qa_style = ParagraphStyle(
        'QAStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    def code_box(code_text):
        p = Paragraph(code_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), code_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        return t

    def callout_box(title, text):
        content = [
            Paragraph(f"<b>{title}</b>", ParagraphStyle('QATitle', parent=qa_style, fontName='Helvetica-Bold')),
            Spacer(1, 3),
            Paragraph(text, qa_style)
        ]
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), callout_bg),
            ('BOX', (0, 0), (-1, -1), 1, callout_border),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    # Document Header
    story.append(Paragraph("AeroSafe – Noise Management API", title_style))
    story.append(Paragraph("System Architecture, Domain Workflows, and Technical Interview Blueprint", subtitle_style))
    story.append(Spacer(1, 6))

    # Section 1: Overview & Stack
    story.append(Paragraph("1. System Overview & Technology Stack", h1_style))
    story.append(Paragraph(
        "AeroSafe is a modular airport operations backend inspired by industrial aerodrome compliance and monitoring systems. "
        "It manages core airport entities, monitors auditory emission thresholds, automatically dispatches compliance audits, "
        "and exposes a sandboxed LLM interface for equipment telemetry interrogation.",
        body_style
    ))
    
    stack_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Technology Choice & Justification</b>", body_style)],
        [Paragraph("Core Backend", body_style), Paragraph("Python, Django, Django REST Framework (DRF)", body_style)],
        [Paragraph("Database", body_style), Paragraph("SQLite (Dev) / PostgreSQL (Target Production)", body_style)],
        [Paragraph("Auth & Access", body_style), Paragraph("JWT (djangorestframework-simplejwt) + Django Groups (RBAC)", body_style)],
        [Paragraph("Documentation", body_style), Paragraph("drf-spectacular (OpenAPI 3.0 / Swagger / ReDoc)", body_style)],
        [Paragraph("Query Optimization", body_style), Paragraph("django-filter, select_related, prefetch_related, Composite Indexes", body_style)],
        [Paragraph("Local AI/LLM", body_style), Paragraph("Ollama orchestrating Llama 3.2 3B via decoupled Service Layer", body_style)],
        [Paragraph("Async & Cache", body_style), Paragraph("Celery + Redis (Architectural Roadmap)", body_style)]
    ]
    t_stack = Table(stack_data, colWidths=[130, 374])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
        ('LINEBELOW', (0, 0), (-1, 0), 1, primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 10))

    # Section 2: Domain Flow
    story.append(Paragraph("2. Operational Business Workflow", h1_style))
    story.append(Paragraph(
        "The application models physical aerodrome operations via an event-driven entity chain:",
        body_style
    ))
    story.append(Paragraph("• <b>Noise Sensor Telemetry:</b> Station records acoustic levels (e.g., 82.50 dB on Runway 12).", bullet_style))
    story.append(Paragraph("• <b>Threshold Breach:</b> NoiseLog record is persisted with OPEN state.", bullet_style))
    story.append(Paragraph("• <b>Inspection Trigger:</b> Operations staff logs a mandatory Noise Compliance Inspection against the incident.", bullet_style))
    story.append(Paragraph("• <b>Maintenance Action:</b> Inspection findings produce an actionable Work Order assigned to technical personnel.", bullet_style))
    story.append(Paragraph("• <b>Resolution:</b> Field engineering verifies sensor calibration or acoustic barriers and closes the loop.", bullet_style))
    story.append(Spacer(1, 10))

    # Section 3: Data Architecture
    story.append(Paragraph("3. Data Architecture & Integrity Decisions", h1_style))
    
    story.append(Paragraph("Referential Integrity & Deletion Rules", h2_style))
    story.append(Paragraph(
        "• <b>Asset Deletion (SET_NULL):</b> <code>on_delete=models.SET_NULL</code> ensures historical acoustic telemetry logs survive device decommissions.<br/>"
        "• <b>Audit Trail (PROTECT):</b> <code>reported_by</code> references the User model via <code>on_delete=models.PROTECT</code>, legally shielding historical compliance data from dangling author IDs.",
        body_style
    ))

    story.append(Paragraph("Indexing Strategy", h2_style))
    story.append(Paragraph(
        "Composite index on <code>['airport', 'status']</code> and a single index on <code>['asset_type']</code> enable high-performance filtering across large IoT operational datasets without sequential table scans.",
        body_style
    ))

    story.append(Paragraph("Server-Enforced User Attribution", h2_style))
    story.append(Paragraph(
        "Client payloads cannot specify <code>reported_by</code>. Identity is strictly derived server-side via <code>perform_create(self, serializer)</code> using <code>self.request.user</code> extracted from validated JWT claims.",
        body_style
    ))
    story.append(code_box(
        "def perform_create(self, serializer):\n"
        "    serializer.save(reported_by=self.request.user)"
    ))
    story.append(Spacer(1, 10))

    # Section 4: Query Optimization
    story.append(Paragraph("4. Query Optimization & ORM Hygiene", h1_style))
    story.append(Paragraph(
        "To systematically prevent N+1 database queries across nested API views, QuerySets explicitly declare join semantics:",
        body_style
    ))
    story.append(Paragraph("• <b>select_related:</b> Applied to direct foreign keys (<code>airport</code>, <code>asset</code>, <code>reported_by</code>) utilizing single SQL INNER/LEFT JOINs.", bullet_style))
    story.append(Paragraph("• <b>prefetch_related:</b> Applied to reverse foreign keys (<code>inspections</code>) to batch child collection queries in Python memory.", bullet_style))
    story.append(code_box(
        "queryset = (\n"
        "    NoiseLog.objects\n"
        "    .select_related('airport', 'asset', 'reported_by')\n"
        "    .prefetch_related('inspections')\n"
        ")"
    ))
    story.append(Spacer(1, 10))

    # Section 5: Security & RBAC
    story.append(Paragraph("5. Security, Authentication & RBAC", h1_style))
    story.append(Paragraph(
        "Stateless authentication is handled via short-lived JWT access tokens (30 min) and refresh tokens (24 h). "
        "Authorization separates authenticated state from permissions using custom DRF permission classes tied to Django Groups.",
        body_style
    ))
    story.append(code_box(
        "class IsOperationsUser(BasePermission):\n"
        "    def has_permission(self, request, view):\n"
        "        return bool(\n"
        "            request.user and request.user.is_authenticated and\n"
        "            (request.user.is_superuser or request.user.groups.filter(name='Operations').exists())\n"
        "        )"
    ))
    story.append(Spacer(1, 10))

    # Section 6: AI/LLM Integration
    story.append(Paragraph("6. AI / LLM Integration Pattern", h1_style))
    story.append(Paragraph(
        "Rather than coupling AI queries directly to ViewSets, the architecture enforces a strict Service Layer (<code>llm/services.py</code>). "
        "The service constructs context from the verified Asset model, injects guardrail system prompts ('Use only provided data; do not hallucinate'), "
        "and queries Ollama running Llama 3.2 3B. This abstraction allows swapping local Ollama for AWS Bedrock without altering the REST interface.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Section 7: Interview Answers Cheatsheet
    story.append(Paragraph("7. Architectural Interview Cheatsheet", h1_style))
    
    qa_pairs = [
        ("Q: Why select_related vs. prefetch_related?",
         "select_related performs SQL joins for single-valued relationships (ForeignKey, OneToOne). prefetch_related executes a separate batch query for multi-valued relationships (reverse FK, ManyToMany) and joins them in memory, avoiding N+1 bottlenecks."),
        ("Q: Why enforce server-side attribution for reported_by?",
         "Accepting user IDs from client JSON violates trust boundaries and invites identity spoofing. We extract and assign request.user securely from the cryptographically verified JWT."),
        ("Q: Why separate LLM calls into a Service Layer?",
         "To keep ViewSets focused solely on HTTP request/response validation. The service layer decouples the LLM provider, making unit testing simpler and enabling seamless migration to enterprise cloud providers like AWS Bedrock.")
    ]

    for q, a in qa_pairs:
        story.append(KeepTogether([
            callout_box(q, a),
            Spacer(1, 6)
        ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated successfully: {output_filename}")

if __name__ == "__main__":
    create_aerosafe_pdf()