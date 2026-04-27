from sqlalchemy.orm import Session
from app.models.skill import Skill, UserSkill
from typing import List, Dict, Any

class GraphRecommendation:
    @staticmethod
    def get_related_skills(db: Session, skill_name: str) -> List[str]:
        """
        Finds skills that are often held by users who also have the target skill.
        (Co-occurrence analysis)
        """
        target_skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not target_skill:
            return []
            
        # Get users who have this skill
        user_ids = [us.user_id for us in db.query(UserSkill).filter(UserSkill.skill_id == target_skill.id).all()]
        
        # Get other skills held by these users
        related_skills = db.query(Skill.name).join(UserSkill).filter(
            UserSkill.user_id.in_(user_ids),
            Skill.id != target_skill.id
        ).all()
        
        # Count occurrences (Basic graph proximity)
        skill_counts = {}
        for (s_name,) in related_skills:
            skill_counts[s_name] = skill_counts.get(s_name, 0) + 1
            
        # Return top 5 related skills
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_skills[:5]]

graph_rec = GraphRecommendation()
