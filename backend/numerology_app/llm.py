"""
Simple LLM module for Astrooverz API.
Provides a clean interface for OpenAI API calls.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Global client instance
_client = None

def get_client():
    """Get or create OpenAI client instance."""
    global _client
    if _client is None:
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
            if not api_key:
                raise ValueError("No OpenAI API key found in environment variables")
            _client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except ImportError:
            logger.error("OpenAI library not installed")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    return _client

def ask_one_shot(prompt: str, system: Optional[str] = None) -> Optional[str]:
    """
    Ask a single question to the LLM.
    
    Args:
        prompt: User prompt/question
        system: Optional system prompt (defaults to Astrooverz system prompt)
        
    Returns:
        LLM response text or None if error
    """
    try:
        client = get_client()
        
        # Default system prompt for Astrooverz
        if system is None:
            system = (
                "You are Astrooverz, a knowledgeable Vedic astrology and numerology guide. "
                "Provide helpful, accurate information about astrology, numerology, and life guidance "
                "based on ancient wisdom. Be concise and practical in your responses."
            )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return None

def ask_with_context(prompt: str, context: str, system: Optional[str] = None) -> Optional[str]:
    """
    Ask a question with additional context.
    
    Args:
        prompt: User prompt/question
        context: Additional context to include
        system: Optional system prompt
        
    Returns:
        LLM response text or None if error
    """
    try:
        client = get_client()
        
        if system is None:
            system = (
                "You are Astrooverz, a knowledgeable Vedic astrology and numerology guide. "
                "Use the provided context to give accurate, helpful responses."
            )
        
        full_prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{prompt}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": full_prompt},
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return None
