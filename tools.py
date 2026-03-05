"""
Tools module for Country Information AI Agent.
Contains the REST Countries API integration tool.
"""

import requests
from typing import Dict, Any, Optional
from config import Config


class CountryAPITool:
    """Tool for fetching country information from REST Countries API."""
    
    def __init__(self):
        self.base_url = Config.REST_COUNTRIES_API_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
    
    def fetch_country_data(self, country_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch country data from REST Countries API.
        
        Args:
            country_name: Name of the country to fetch data for
            
        Returns:
            Dictionary containing country data, or None if not found
        """
        try:
            url = f"{self.base_url}/name/{country_name}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            elif isinstance(data, dict):
                return data
            else:
                return None
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch country data: {str(e)}")
    
    def extract_field(self, country_data: Dict[str, Any], field: str) -> Any:
        """
        Extract a specific field from country data.
        
        Args:
            country_data: Country data dictionary
            field: Field name to extract (e.g., 'population', 'capital', 'currencies')
            
        Returns:
            Extracted field value, or None if not found
        """
        field_mapping = {
            "population": lambda d: d.get("population"),
            "capital": lambda d: d.get("capital", [None])[0] if d.get("capital") else None,
            "currencies": lambda d: list(d.get("currencies", {}).keys()) if d.get("currencies") else None,
            "currency": lambda d: list(d.get("currencies", {}).keys())[0] if d.get("currencies") else None,
            "region": lambda d: d.get("region"),
            "subregion": lambda d: d.get("subregion"),
            "languages": lambda d: list(d.get("languages", {}).values()) if d.get("languages") else None,
            "area": lambda d: d.get("area"),
            "borders": lambda d: d.get("borders", []),
            "timezones": lambda d: d.get("timezones", []),
            "name": lambda d: d.get("name", {}).get("common"),
            "official_name": lambda d: d.get("name", {}).get("official"),
        }
        
        extractor = field_mapping.get(field.lower())
        if extractor:
            return extractor(country_data)
        
        return country_data.get(field)

