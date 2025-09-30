#!/usr/bin/env python3
"""
CloudCurio Feature Tracking CLI

Command-line interface for the feature tracking system.
"""

import argparse
import sys
from datetime import datetime
from typing import List

from feature_tracking.feature_tracker import FeatureTracker, FeatureCategory, FeatureStatus
from feature_tracking.config import config


def list_features(tracker: FeatureTracker, args):
    """List top features by usage"""
    features = tracker.get_top_features(args.limit)
    print(f"Top {args.limit} features by usage:")
    print("-" * 80)
    print(f"{'Feature Name':<30} {'Category':<20} {'Calls':<10} {'Avg Duration':<12} {'Efficiency':<10} {'Success%':<8}")
    print("-" * 80)
    
    for feature in features:
        print(f"{feature['feature_name']:<30} {feature['category']:<20} {feature['usage_count']:<10} "
              f"{feature['avg_duration']:<12.3f} {feature['avg_efficiency']:<10.3f} {feature['success_rate']:<8.1f}")


def get_feature_stats(tracker: FeatureTracker, args):
    """Get statistics for a specific feature"""
    try:
        category = FeatureCategory(args.category) if args.category else None
    except ValueError:
        print(f"Invalid category: {args.category}")
        return
    
    stats = tracker.get_feature_stats(args.feature_name, category)
    
    print(f"Statistics for feature: {args.feature_name}")
    print("-" * 40)
    print(f"Total calls: {stats['total_calls']}")
    print(f"Average duration: {stats['avg_duration']:.3f}s")
    print(f"Success count: {stats['success_count']}")
    print(f"Failure count: {stats['failure_count']}")
    print(f"Average efficiency: {stats['avg_efficiency']:.3f}")
    print(f"Success rate: {stats['success_rate']:.1f}%")


def list_records(tracker: FeatureTracker, args):
    """List feature usage records"""
    try:
        category = FeatureCategory(args.category) if args.category else None
    except ValueError:
        print(f"Invalid category: {args.category}")
        return
    
    records = tracker.get_all_records(
        feature_name=args.feature if hasattr(args, 'feature') and args.feature else None,
        category=category,
        user_id=args.user if hasattr(args, 'user') and args.user else None,
        limit=args.limit
    )
    
    print(f"Feature usage records (limit: {args.limit}):")
    print("-" * 120)
    print(f"{'Feature':<20} {'Status':<10} {'Duration':<10} {'Start Time':<20} {'Efficiency':<10} {'User ID':<15}")
    print("-" * 120)
    
    for record in records:
        start_time = record.start_time.strftime('%Y-%m-%d %H:%M:%S')
        duration = f"{record.duration:.3f}s"
        efficiency = f"{record.efficiency_score:.3f}" if record.efficiency_score is not None else "N/A"
        user_id = record.user_id if record.user_id else "Anonymous"
        
        print(f"{record.feature_name:<20} {record.status.value:<10} {duration:<10} "
              f"{start_time:<20} {efficiency:<10} {user_id:<15}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="CloudCurio Feature Tracking CLI")
    
    # Global options
    parser.add_argument(
        "--db-path",
        help="Path to the feature tracking database",
        default=config.db_path
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List features command
    list_features_parser = subparsers.add_parser("list-features", help="List top features by usage")
    list_features_parser.add_argument("--limit", type=int, default=10, help="Number of features to show")
    
    # Feature stats command
    stats_parser = subparsers.add_parser("feature-stats", help="Get statistics for a feature")
    stats_parser.add_argument("feature_name", help="Name of the feature to get stats for")
    stats_parser.add_argument("--category", help="Category of the feature")
    
    # List records command
    records_parser = subparsers.add_parser("list-records", help="List feature usage records")
    records_parser.add_argument("--feature", help="Filter by feature name")
    records_parser.add_argument("--category", help="Filter by category")
    records_parser.add_argument("--user", help="Filter by user ID")
    records_parser.add_argument("--limit", type=int, default=20, help="Number of records to show")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize the tracker
    tracker = FeatureTracker(db_path=args.db_path)
    
    if args.command == "list-features":
        list_features(tracker, args)
    elif args.command == "feature-stats":
        get_feature_stats(tracker, args)
    elif args.command == "list-records":
        list_records(tracker, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()