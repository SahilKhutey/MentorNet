import uuid

class MeetingService:
    @staticmethod
    def generate_room_link(booking_id: str):
        """
        Generates a secure, unique meeting room link for a mentorship session.
        In production, this could integrate with Zoom, Google Meet, or Jitsi.
        """
        room_id = str(uuid.uuid4())
        return f"https://meet.mentornet.ai/{room_id}?booking={booking_id}"

    @staticmethod
    def get_join_instructions():
        return "Ensure your camera and microphone are enabled. You are entering a secure MentorNet research environment."

meeting_service = MeetingService()
