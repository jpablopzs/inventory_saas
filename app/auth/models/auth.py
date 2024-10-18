from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Integer
from datetime import datetime
from app.core.database import Base

# User

class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        UniqueConstraint('email', name='uq_email'),
        UniqueConstraint('username', name='uq_username'),
        {'schema': 'auth'}
        
    )
    id = Column((Integer), primary_key=True)
    name = Column(String(150), nullable=False)
    username = Column(String(50), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(100), index=True, nullable=False)
    password = Column(String(300), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    update_at = Column(DateTime, nullable=False, default=datetime.now)
    create_at = Column(DateTime, nullable=False, default=datetime.now)


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = (
        UniqueConstraint('name','company_id', name='uq_role_company'),
        {'schema': 'auth'}
    )
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

# Permissions

class Permission(Base):
    __tablename__ = 'permission'
    __table_args__ = (
        UniqueConstraint('name', name='uq_name_permission'),
        UniqueConstraint('permission_key', name='uq_key_permission'),
        {'schema': 'auth'}
    )
    id = Column((Integer), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    permission_key = Column(String(100), nullable=False)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

# User Roles
class UserRole(Base):
    __tablename__ = 'user_role'
    __table_args__ = (
        UniqueConstraint('id_user','id_role', 'company_id', name='uq_user_role'),
        {'schema': 'auth'}
    )
    id = Column((Integer), primary_key=True) 
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    id_user = Column((Integer), ForeignKey("auth.user.id", name='fk_user_id'), nullable=False)
    id_role = Column((Integer), ForeignKey("auth.role.id", name='fk_role_id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

# Permissions Role

class PermissionRole(Base):
    __tablename__ = 'permissions_role'
    __table_args__ = (
        UniqueConstraint('id_role','id_permission', 'company_id', name='uq_permission_role'),
        {'schema': 'auth'}
    )

    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    id_role = Column((Integer), ForeignKey("auth.role.id", name='fk_role_id'), nullable=False, index=True)
    id_permission = Column((Integer), ForeignKey("auth.permission.id", name='fk_permision_id'), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)
