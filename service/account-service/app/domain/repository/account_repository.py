"""
Account Repository - 순수한 데이터 접근 로직
"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("account-repository")

class AccountRepository:
    def __init__(self, engine):
        self.engine = engine
    
    def create_user(self, user_data: dict) -> bool:
        """사용자 생성(해시된 비밀번호)"""
        try:
            with self.engine.connect() as conn:
                logger.info(f"Executing SQL with data: {user_data}")
                logger.info(f"Executing SQL with cleaned data: {user_data}")
                conn.execute(
                    text("""
                    INSERT INTO auth (
                        user_id, user_pw, industry, bs_num, company_id,
                        company_add, company_country, manager_dept,
                        manager_name, manager_email, manager_phone
                    ) VALUES (
                        :user_id, :user_pw, :industry, :bs_num, :company_id,
                        :company_add, :company_country, :manager_dept,
                        :manager_name, :manager_email, :manager_phone
                    )
                """),
                    user_data
                )
                conn.commit()
            return True
        except IntegrityError:
            logger.warning(f"User already exists: {user_data['user_id']}")
            return False
        except SQLAlchemyError as e:
            logger.error(f"Database error during user creation: {e}")
            raise
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자 조회"""
        try:
            with self.engine.connect() as conn:
                row = conn.execute(
                    text("""SELECT user_id, company_id, user_pw
                            FROM auth WHERE user_id = :user_id"""),
                    {"user_id": user_id},
                ).fetchone()
            
            if row:
                return {
                    "user_id": row.user_id,
                    "company_id": row.company_id,
                    "user_pw": row.user_pw
                }
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error during user retrieval: {e}")
            raise
    
    def get_user_count(self) -> int:
        """사용자 수 조회"""
        try:
            with self.engine.connect() as conn:
                count = conn.execute(text("SELECT COUNT(*) FROM auth")).scalar()
            return count
        except SQLAlchemyError as e:
            logger.error(f"Database error during count retrieval: {e}")
            raise
