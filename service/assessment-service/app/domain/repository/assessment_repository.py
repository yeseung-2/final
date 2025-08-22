from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import List, Dict, Any, Optional
from ..model.assessment_model import KesgItem

logger = logging.getLogger("assessment-repository")

class AssessmentRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
    
    def get_kesg_items(self) -> List[KesgItem]:
        """kesg 테이블에서 모든 데이터 조회"""
        try:
            with self.engine.connect() as conn:
                query = text("SELECT id, item_name, question_type, levels_json, choices_json FROM kesg ORDER BY id")
                result = conn.execute(query)
                
                items = []
                for row in result:
                    # question_type에 따라 적절한 choices 데이터 설정
                    choices_data = None
                    if row.question_type in ['three_level', 'five_level']:
                        choices_data = row.levels_json
                    elif row.question_type == 'five_choice':
                        choices_data = row.choices_json
                    
                    items.append(KesgItem(
                        id=row.id,
                        item_name=row.item_name,
                        question_type=row.question_type,
                        choices=choices_data,
                        category="자가진단"
                    ))
                
                logger.info(f"✅ kesg 테이블에서 {len(items)}개 항목 조회 성공")
                return items
                
        except SQLAlchemyError as e:
            logger.error(f"❌ kesg 테이블 조회 중 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ kesg 테이블 조회 중 예상치 못한 오류: {e}")
            raise
    
    def get_kesg_item_by_id(self, item_id: int) -> Optional[KesgItem]:
        """특정 ID의 kesg 항목 조회"""
        try:
            with self.engine.connect() as conn:
                query = text("SELECT id, item_name, question_type, levels_json, choices_json FROM kesg WHERE id = :item_id")
                result = conn.execute(query, {"item_id": item_id})
                row = result.fetchone()
                
                if row:
                    # question_type에 따라 적절한 choices 데이터 설정
                    choices_data = None
                    if row.question_type in ['three_level', 'five_level']:
                        choices_data = row.levels_json
                    elif row.question_type == 'five_choice':
                        choices_data = row.choices_json
                    
                    return KesgItem(
                        id=row.id,
                        item_name=row.item_name,
                        question_type=row.question_type,
                        choices=choices_data,
                        category="자가진단"
                    )
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"❌ kesg 항목 조회 중 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ kesg 항목 조회 중 예상치 못한 오류: {e}")
            raise