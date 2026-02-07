"""
Custom JSON utilities for handling NaN values in API responses.
Provides JSON-safe encoding that converts NaN/Inf to null.
"""

import json
import math
from typing import Any
from fastapi.responses import JSONResponse


class NaNSafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that converts NaN and Inf values to null."""
    
    def default(self, obj):
        # Let the base encoder handle the object
        return super().default(obj)
    
    def encode(self, obj):
        # Process the object to replace NaN/Inf before encoding
        return super().encode(self._sanitize(obj))
    
    def iterencode(self, obj, _one_shot=False):
        # Process the object to replace NaN/Inf before encoding
        return super().iterencode(self._sanitize(obj), _one_shot)
    
    def _sanitize(self, obj):
        """Recursively sanitize NaN and Inf values."""
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj
        elif isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._sanitize(item) for item in obj]
        else:
            return obj


class NaNSafeJSONResponse(JSONResponse):
    """Custom JSONResponse that handles NaN/Inf values gracefully."""
    
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=NaNSafeJSONEncoder,
        ).encode("utf-8")
