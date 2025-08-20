# api/v1/rules.py
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging
from datetime import datetime
import uuid
import json
import redis.asyncio as redis

# Import dari schemas (bukan dari models)
from ...models.event_alarm import (
    AlarmRuleResponse, 
    AlarmRuleCreate, 
    AlarmRuleUpdate
)
from ...models.alarm_schema import *
from ...core.alarm_manager import AlarmManager
from ...databases import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rules", tags=["rules"])

# Konfigurasi Redis untuk cache
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_TTL = 300  # 5 menit

async def get_redis_client():
    """Mendapatkan koneksi Redis client."""
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        await redis_client.ping()
        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None

async def get_alarm_manager(request: Request) -> AlarmManager:
    """
    Dependency untuk mendapatkan instance AlarmManager.
    """
    return request.app.state.alarm_manager

# Perbaikan: Import model AlarmRule dari lokasi yang benar
# Sesuaikan path ini dengan struktur direktori Anda
try:
    # Coba import dari services.event_alarm.models.event_alarm
    #from ...models.event_alarm import AlarmRule
    logger.info("Successfully imported AlarmRule from services.event_alarm.models.event_alarm")
except ImportError:
    try:
        # Coba import dari services.data_processing.models.event_alarm
        from ...models.event_alarm import AlarmRule
        logger.info("Successfully imported AlarmRule from services.data_processing.models.event_alarm")
    except ImportError as e:
        logger.error(f"Failed to import AlarmRule: {e}")
        raise ImportError("Cannot import AlarmRule model. Please check your project structure.")

def serialize_alarm_rule(rule: AlarmRule) -> dict:
    """Serialize SQLAlchemy model to dictionary."""
    return {
        "id": str(rule.id),
        "name": rule.name,
        "description": rule.description,
        "tag_id": rule.tag_id,
        "condition": rule.condition,
        "severity": rule.severity,
        "is_active": rule.is_active,
        "created_at": rule.created_at.isoformat() if rule.created_at else None,
        "updated_at": rule.updated_at.isoformat() if rule.updated_at else None
    }

def serialize_alarm_rule_list(rules: List[AlarmRule]) -> List[dict]:
    """Serialize list of SQLAlchemy models to list of dictionaries."""
    return [serialize_alarm_rule(rule) for rule in rules]

@router.get("/", response_model=List[AlarmRuleResponse])
async def list_alarm_rules(
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """List all alarm/event rules with Redis caching."""
    cache_key = "alarm_rules:all"
    
    try:
        # Coba ambil dari cache dulu
        if redis_client:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                try:
                    rules_data = json.loads(cached_data)
                    logger.debug("Retrieved alarm rules from Redis cache")
                    return [AlarmRuleResponse(**rule) for rule in rules_data]
                except (json.JSONDecodeError, Exception) as e:
                    logger.warning(f"Error parsing cached alarm rules: {e}")

        # Jika tidak ada di cache, ambil dari database
        stmt = select(AlarmRule).order_by(AlarmRule.created_at.desc())
        result = await db.execute(stmt)
        rules = result.scalars().all()
        
        # Serialize rules
        rules_serialized = serialize_alarm_rule_list(rules)
        
        # Simpan ke cache
        if redis_client and rules_serialized:
            try:
                await redis_client.setex(
                    cache_key, 
                    CACHE_TTL, 
                    json.dumps(rules_serialized, default=str)
                )
                logger.debug("Stored alarm rules in Redis cache")
            except Exception as e:
                logger.warning(f"Error caching alarm rules: {e}")
        
        return [AlarmRuleResponse(**rule) for rule in rules_serialized]
        
    except SQLAlchemyError as e:
        logger.error(f"Database error while listing alarm rules: {e}")
        raise HTTPException(status_code=500, detail="Database error while retrieving alarm rules")
    except Exception as e:
        logger.error(f"Failed to list alarm rules: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve alarm rules: {str(e)}")

@router.get("/{rule_id}", response_model=AlarmRuleResponse)
async def get_alarm_rule(
    rule_id: str,
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Get a specific alarm rule by ID with Redis caching."""
    cache_key = f"alarm_rule:{rule_id}"
    
    try:
        # Coba ambil dari cache dulu
        if redis_client:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                try:
                    rule_data = json.loads(cached_data)
                    logger.debug(f"Retrieved alarm rule {rule_id} from Redis cache")
                    return AlarmRuleResponse(**rule_data)
                except (json.JSONDecodeError, Exception) as e:
                    logger.warning(f"Error parsing cached alarm rule {rule_id}: {e}")

        # Jika tidak ada di cache, ambil dari database
        try:
            uuid.UUID(rule_id)  # Validasi UUID
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rule ID format")
            
        stmt = select(AlarmRule).where(AlarmRule.id == rule_id)
        result = await db.execute(stmt)
        rule = result.scalar_one_or_none()
        
        if not rule:
            raise HTTPException(status_code=404, detail="Alarm rule not found")
        
        # Serialize rule
        rule_serialized = serialize_alarm_rule(rule)
        
        # Simpan ke cache
        if redis_client:
            try:
                await redis_client.setex(
                    cache_key, 
                    CACHE_TTL, 
                    json.dumps(rule_serialized, default=str)
                )
                logger.debug(f"Stored alarm rule {rule_id} in Redis cache")
            except Exception as e:
                logger.warning(f"Error caching alarm rule {rule_id}: {e}")
        
        return AlarmRuleResponse(**rule_serialized)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting alarm rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error while retrieving alarm rule")
    except Exception as e:
        logger.error(f"Failed to get alarm rule {rule_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve alarm rule: {str(e)}")

@router.post("/", response_model=AlarmRuleResponse, status_code=201)
async def create_alarm_rule(
    rule: AlarmRuleCreate,
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Create a new alarm rule and invalidate cache."""
    try:
        # Buat alarm rule baru
        new_rule = AlarmRule(
            id=str(uuid.uuid4()),
            name=rule.name,
            description=rule.description,
            tag_id=rule.tag_id,
            condition=rule.condition,
            severity=rule.severity,
            is_active=rule.is_active
        )
        
        db.add(new_rule)
        await db.commit()
        await db.refresh(new_rule)
        
        logger.info(f"Created new alarm rule: {rule.name} (ID: {new_rule.id})")
        
        # Invalidate cache
        if redis_client:
            try:
                await redis_client.delete("alarm_rules:all")
                logger.debug("Invalidated alarm rules cache after creation")
            except Exception as e:
                logger.warning(f"Error invalidating cache after creation: {e}")
        
        # Serialize dan return response
        rule_serialized = serialize_alarm_rule(new_rule)
        return AlarmRuleResponse(**rule_serialized)
        
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while creating alarm rule: {e}")
        raise HTTPException(status_code=500, detail="Database error while creating alarm rule")
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create alarm rule: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create alarm rule: {str(e)}")

@router.put("/{rule_id}", response_model=AlarmRuleResponse)
async def update_alarm_rule(
    rule_id: str,
    rule: AlarmRuleUpdate,
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Update an existing alarm rule and invalidate cache."""
    try:
        try:
            uuid.UUID(rule_id)  # Validasi UUID
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rule ID format")
            
        # Cari rule yang ada
        stmt = select(AlarmRule).where(AlarmRule.id == rule_id)
        result = await db.execute(stmt)
        existing_rule = result.scalar_one_or_none()
        
        if not existing_rule:
            raise HTTPException(status_code=404, detail="Alarm rule not found")

        # Update fields yang disediakan
        update_data = rule.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(existing_rule, field, value)
        
        # Update timestamp
        existing_rule.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(existing_rule)
        
        logger.info(f"Updated alarm rule: {rule_id}")
        
        # Invalidate cache
        if redis_client:
            try:
                await redis_client.delete("alarm_rules:all")
                await redis_client.delete(f"alarm_rule:{rule_id}")
                logger.debug(f"Invalidated alarm rule cache after update: {rule_id}")
            except Exception as e:
                logger.warning(f"Error invalidating cache after update: {e}")
        
        # Serialize dan return response
        rule_serialized = serialize_alarm_rule(existing_rule)
        return AlarmRuleResponse(**rule_serialized)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while updating alarm rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error while updating alarm rule")
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update alarm rule {rule_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update alarm rule: {str(e)}")

@router.delete("/{rule_id}")
async def delete_alarm_rule(
    rule_id: str,
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Delete an alarm rule and invalidate cache."""
    try:
        try:
            uuid.UUID(rule_id)  # Validasi UUID
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rule ID format")
            
        # Cari rule yang ada
        stmt = select(AlarmRule).where(AlarmRule.id == rule_id)
        result = await db.execute(stmt)
        existing_rule = result.scalar_one_or_none()
        
        if not existing_rule:
            raise HTTPException(status_code=404, detail="Alarm rule not found")
        
        # Hapus rule
        await db.delete(existing_rule)
        await db.commit()
        
        logger.info(f"Deleted alarm rule: {rule_id}")
        
        # Invalidate cache
        if redis_client:
            try:
                await redis_client.delete("alarm_rules:all")
                await redis_client.delete(f"alarm_rule:{rule_id}")
                logger.debug(f"Invalidated alarm rule cache after deletion: {rule_id}")
            except Exception as e:
                logger.warning(f"Error invalidating cache after deletion: {e}")
        
        return {
            "message": f"Alarm rule {rule_id} deleted successfully",
            "rule_id": rule_id
        }
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while deleting alarm rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error while deleting alarm rule")
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete alarm rule {rule_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete alarm rule: {str(e)}")

@router.post("/{rule_id}/toggle", response_model=AlarmRuleResponse)
async def toggle_alarm_rule(
    rule_id: str,
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Toggle the active status of an alarm rule and invalidate cache."""
    try:
        try:
            uuid.UUID(rule_id)  # Validasi UUID
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rule ID format")
            
        # Cari rule yang ada
        stmt = select(AlarmRule).where(AlarmRule.id == rule_id)
        result = await db.execute(stmt)
        existing_rule = result.scalar_one_or_none()
        
        if not existing_rule:
            raise HTTPException(status_code=404, detail="Alarm rule not found")

        # Toggle is_active status
        existing_rule.is_active = not existing_rule.is_active
        existing_rule.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(existing_rule)
        
        # Status message
        status = "activated" if existing_rule.is_active else "deactivated"
        logger.info(f"Alarm rule {rule_id} {status}")
        
        # Invalidate cache
        if redis_client:
            try:
                await redis_client.delete("alarm_rules:all")
                await redis_client.delete(f"alarm_rule:{rule_id}")
                logger.debug(f"Invalidated alarm rule cache after toggle: {rule_id}")
            except Exception as e:
                logger.warning(f"Error invalidating cache after toggle: {e}")
        
        # Serialize dan return response
        rule_serialized = serialize_alarm_rule(existing_rule)
        return AlarmRuleResponse(**rule_serialized)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while toggling alarm rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error while toggling alarm rule")
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to toggle alarm rule {rule_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to toggle alarm rule: {str(e)}")