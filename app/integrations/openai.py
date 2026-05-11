"""
OpenAI API Client
Handles LLM completions for data extraction
"""
import openai
import json
from typing import Optional
from app.config import settings


class OpenAIClient:
    """Client for OpenAI API - LLM completions"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        openai.api_key = self.api_key
    
    async def completion(
        self,
        prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        response_format: Optional[dict] = None
    ) -> str:
        """
        Get a completion from OpenAI's chat models.
        
        Args:
            prompt: The user prompt/query
            model: Model to use (default: gpt-4o-mini - cost-effective and fast)
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens in response (None = model default)
            response_format: Force specific format (e.g., {"type": "json_object"} for JSON)
            
        Returns:
            String response from the model
            
        Example:
            # Regular completion
            response = await openai_client.completion(
                prompt="Extract contact info from: ...",
                model="gpt-4o-mini",
                temperature=0.1
            )
            
            # Force JSON response (guaranteed valid JSON)
            response = await openai_client.completion(
                prompt="Convert this to JSON: ...",
                model="gpt-4o-mini",
                response_format={"type": "json_object"}
            )
        """
        try:
            # Update system message based on response format
            system_content = "You are a data structuring assistant."
            if response_format and response_format.get("type") == "json_object":
                system_content = "You are a data structuring assistant. Return only valid JSON without any markdown formatting or additional text."
            else:
                system_content = "You are a data extraction assistant. Extract structured information from website content and return valid JSON only. Do not include markdown code blocks or any text outside the JSON."
            
            messages = [
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            
            if response_format:
                kwargs["response_format"] = response_format
            
            # Use the new OpenAI client (v1.0+)
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(**kwargs)
            
            content = response.choices[0].message.content
            
            # Clean up response (remove markdown code blocks if present)
            # Only needed if NOT using response_format=json_object
            if not response_format or response_format.get("type") != "json_object":
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                elif content.startswith("```"):
                    content = content.replace("```", "").strip()
            
            return content
            
        except openai.AuthenticationError:
            raise Exception("OpenAI API authentication failed. Check your API key.")
        except openai.RateLimitError:
            raise Exception("OpenAI API rate limit exceeded.")
        except Exception as e:
            raise Exception(f"OpenAI completion error: {str(e)}")
    
    async def parse_json_response(
        self, 
        prompt: str, 
        model: str = "gpt-4o-mini",
        use_json_mode: bool = True
    ) -> dict:
        """
        Get a completion and parse it as JSON.
        
        Args:
            prompt: The user prompt requesting JSON output
            model: Model to use
            use_json_mode: Use response_format=json_object for guaranteed valid JSON
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            ValueError: If response is not valid JSON
            
        Example:
            data = await openai_client.parse_json_response(
                prompt="Convert this to JSON: ...",
                model="gpt-4o-mini",
                use_json_mode=True  # Guarantees valid JSON
            )
        """
        response_format = {"type": "json_object"} if use_json_mode else None
        response = await self.completion(
            prompt, 
            model=model, 
            temperature=0.1,
            response_format=response_format
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response (fallback)
            # Sometimes the model includes extra text
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    return json.loads(response[start:end])
                except:
                    pass
            
            raise ValueError(f"Failed to parse JSON from OpenAI response: {str(e)}\nResponse: {response[:500]}")


# Create global client instance
openai_client = OpenAIClient()
