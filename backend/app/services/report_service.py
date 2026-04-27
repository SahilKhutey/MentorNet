from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from sqlalchemy.orm import Session
from app.services.export_service import export_service

class ReportService:
    @staticmethod
    def generate_academic_report_pdf(db: Session, user_id: str):
        """
        Generates a professional PDF report summarizing the user's academic engagement and mentorship history.
        """
        # 1. Gather comprehensive user data
        data = export_service.generate_user_data_export(db, user_id)
        
        # 2. Create PDF in memory
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Header Styling
        c.setFillColorRGB(0.1, 0.2, 0.4) # Dark Blue
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, height - 60, "Academic Performance Report")
        
        c.setFillColorRGB(0.3, 0.3, 0.3) # Gray
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 80, f"MentorNet AI Platform | Verified Student Record")
        c.line(50, height - 90, width - 50, height - 90)
        
        # User Context
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 120, "Student Information")
        c.setFont("Helvetica", 12)
        c.drawString(60, height - 140, f"Name: {data['account']['name']}")
        c.drawString(60, height - 155, f"Email: {data['account']['email']}")
        c.drawString(60, height - 170, f"Academic Field: {data['profile']['primary_field']}")
        
        # Engagement Metrics
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 210, "Platform Engagement")
        
        # Create a simple box for stats
        c.rect(50, height - 280, width - 100, 60, stroke=1, fill=0)
        c.setFont("Helvetica", 11)
        c.drawString(70, height - 235, f"• Total Mentorship Bookings: {data['activity']['bookings_count']}")
        c.drawString(70, height - 250, f"• Verified Sessions Completed: {data['activity']['sessions_completed']}")
        c.drawString(70, height - 265, f"• Roadmap Milestones Active: {data['activity']['roadmaps_active']}")
        
        # Expertise Tags
        if data['profile']['expertise']:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 310, "Skills & Expertise")
            c.setFont("Helvetica", 11)
            tags_str = ", ".join(data['profile']['expertise'])
            c.drawString(60, height - 330, f"{tags_str}")

        # Notifications / Recent Activity
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 370, "Recent Platform Activity")
        y_offset = height - 390
        for i, n in enumerate(data['notifications'][:5]): # Top 5
            c.setFont("Helvetica", 10)
            c.drawString(60, y_offset, f"• {n['title']} ({n['created_at'][:10]})")
            y_offset -= 15

        # Footer
        c.line(50, 50, width - 50, 50)
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(50, 40, "This report is an automated generation from the MentorNet AI platform. Information is verified based on platform interactions.")
        
        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer

report_service = ReportService()
