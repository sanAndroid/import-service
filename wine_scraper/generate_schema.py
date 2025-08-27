#!/usr/bin/env python3
"""
Generate JSON Schema from Wine model for Java DTO generation.

This script generates a JSON Schema from the Pydantic Wine model
which can be used to automatically generate Java DTO classes.
"""

import json
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from pipelines.models import Wine

def generate_json_schema():
    """Generate JSON Schema from the Wine model."""
    try:
        # Generate schema using Pydantic's built-in method
        schema = Wine.model_json_schema()
        
        # Add metadata
        schema['$schema'] = "http://json-schema.org/draft-07/schema#"
        schema['title'] = "Wine"
        schema['description'] = "Wine data model for cross-language DTO generation"
        
        # Write schema to file
        schema_file = Path(__file__).parent / "wine-schema.json"
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON Schema generated: {schema_file}")
        print(f"📄 Schema includes {len(schema.get('properties', {}))} properties")
        
        # Also print to console for quick reference
        print("\n📋 JSON Schema preview:")
        print(json.dumps(schema, indent=2)[:500] + "...")
        
        return schema_file
        
    except Exception as e:
        print(f"❌ Error generating schema: {e}")
        return None

if __name__ == "__main__":
    generate_json_schema()