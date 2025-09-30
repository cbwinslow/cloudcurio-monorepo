"""
CloudCurio Feature Tracking Configuration
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class FeatureTrackingConfig:
    """Configuration for feature tracking"""
    
    # Database settings
    db_path: str = "~/.cloudcurio/feature_tracking.db"
    
    # Tracking settings
    enabled: bool = True
    track_failures_only: bool = False  # Only track failed features
    min_duration_threshold: float = 0.0  # Minimum duration to track (in seconds)
    max_metadata_size: int = 1024 * 10  # 10KB max for metadata
    
    # Privacy settings
    anonymize_user_data: bool = True  # Hash user IDs
    exclude_sensitive_features: list = None  # Features to never track
    
    # Performance settings
    flush_interval: int = 100  # Batch records and flush every N records
    max_batch_size: int = 50  # Max records per batch
    
    def __post_init__(self):
        if self.exclude_sensitive_features is None:
            self.exclude_sensitive_features = []
    
    @classmethod
    def from_env(cls) -> 'FeatureTrackingConfig':
        """Create config from environment variables"""
        return cls(
            db_path=os.getenv('FEATURE_TRACKING_DB_PATH', "~/.cloudcurio/feature_tracking.db"),
            enabled=os.getenv('FEATURE_TRACKING_ENABLED', 'true').lower() == 'true',
            track_failures_only=os.getenv('FEATURE_TRACKING_FAILURES_ONLY', 'false').lower() == 'true',
            min_duration_threshold=float(os.getenv('FEATURE_TRACKING_MIN_DURATION', '0.0')),
            max_metadata_size=int(os.getenv('FEATURE_TRACKING_MAX_METADATA_SIZE', str(1024 * 10))),
            anonymize_user_data=os.getenv('FEATURE_TRACKING_ANONYMIZE', 'true').lower() == 'true',
            exclude_sensitive_features=os.getenv('FEATURE_TRACKING_EXCLUDE', '').split(','),
            flush_interval=int(os.getenv('FEATURE_TRACKING_FLUSH_INTERVAL', '100')),
            max_batch_size=int(os.getenv('FEATURE_TRACKING_MAX_BATCH_SIZE', '50'))
        )


# Global configuration instance
config = FeatureTrackingConfig.from_env()