"""Non-audio curriculum and PostgreSQL staging safety regressions.
Uses isolated test fixtures only.
"""
import pytest
from test_integration import SessionLocal
from app.deep_language_audit import audit
from app.seed import LANGS

def test_ten_language_mechanical_script_and_quiz_audit():
    with SessionLocal() as db: result=audit(db)
    assert result['issue_count']==0,result['issues'][:5]
    assert set(result['languages'])==set(LANGS)
    assert sum(v['vocabulary'] for v in result['languages'].values())==606
    assert sum(v['questions'] for v in result['languages'].values())==778


def test_staging_verifier_refuses_non_postgresql_database():
    from scripts.staging_postgres_qa import safety_check
    with pytest.raises(RuntimeError,match='actual PostgreSQL'):
        safety_check()
