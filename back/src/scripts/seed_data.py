from src.models.database import SessionLocal, engine
from src.models.user import User
from src.models.database import Base

def create_tables():
    """Cria todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_data():
    """Cria usuários de exemplo"""
    db = SessionLocal()
    
    try:
        # Criar usuários de exemplo
        users = [
            User(id=1, email="comprador@feira.com", full_name="João Comprador", is_vendor=False),
            User(id=2, email="feirante@feira.com", full_name="Maria Feirante", is_vendor=True),
        ]
        
        for user in users:
            db.merge(user)
        
        db.commit()
        print("✅ Tabelas e dados iniciais criados!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_data()