from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.tag import Tag
from app.ai.embedding import generate_embedding
from app.ai.vector_db.index_manager import faiss_store
from app.ai.text_builder import build_profile_text
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate
from typing import List, Optional

class ProfileService:
    @staticmethod
    def _attach_tags(db: Session, profile: Profile, tag_names: List[str]):
        profile.tags.clear()
        if not tag_names:
            return
            
        # Fetch all existing tags in one query
        existing_tags = db.query(Tag).filter(Tag.name.in_(tag_names)).all()
        tag_dict = {t.name: t for t in existing_tags}
        
        for name in tag_names:
            if name in tag_dict:
                profile.tags.append(tag_dict[name])
            else:
                new_tag = Tag(name=name)
                db.add(new_tag)
                profile.tags.append(new_tag)

    @staticmethod
    def index_profile(profile: Profile):
        """Builds text, generates embedding, and adds to persistent FAISS."""
        text = build_profile_text(profile)
        embedding = generate_embedding(text)
        faiss_store.add(profile.id, embedding)
        return str(profile.id)

    @staticmethod
    def create_profile(db: Session, user_id: str, data: ProfileCreate):
        existing = db.query(Profile).filter(Profile.user_id == user_id).first()
        if existing:
            raise Exception("Profile already exists")
        
        profile = Profile(
            user_id=user_id,
            full_name=data.full_name,
            bio=data.bio,
            location=data.location,
            institution=data.institution,
            primary_field=data.primary_field,
        )
        db.add(profile)
        # Flush to get the ID but don't commit yet
        db.flush()

        ProfileService._attach_tags(db, profile, data.tags)
        
        # Sync with AI Search Engine before final commit
        # (Assuming indexing is idempotent or we can rollback if needed)
        embedding_id = ProfileService.index_profile(profile)
        profile.embedding_id = embedding_id
        
        db.commit()
        db.refresh(profile)
        
        return profile

    @staticmethod
    def update_profile(db: Session, user_id: str, data: ProfileUpdate):
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise Exception("Profile not found")
        
        for field, value in data.dict(exclude_unset=True).items():
            if field != "tags":
                setattr(profile, field, value)
        
        if data.tags is not None:
            ProfileService._attach_tags(db, profile, data.tags)
        
        db.commit()
        db.refresh(profile)

        # Re-sync with AI Search Engine
        ProfileService.index_profile(profile)

        return profile

    @staticmethod
    def get_my_profile(db: Session, user_id: str):
        return db.query(Profile).filter(Profile.user_id == user_id).first()

    @staticmethod
    def get_profile_by_user(db: Session, user_id: str):
        return db.query(Profile).filter(Profile.user_id == user_id).first()

    @staticmethod
    def search_profiles(
        db: Session,
        field: Optional[str] = None,
        tags: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 10
    ):
        query = db.query(Profile)
        if field:
            query = query.filter(Profile.primary_field.ilike(f"%{field}%"))
        if tags:
            query = query.join(Profile.tags).filter(Tag.name.in_(tags))
        
        results = query.offset(skip).limit(limit).all()
        return results

profile_service = ProfileService()
