"""
Agent module for Country Information AI Agent.
Implements the three-step agent workflow: intent identification, tool invocation, and answer synthesis.
"""

from typing import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools import CountryAPITool
from config import Config


class IntentIdentification(BaseModel):
    """Structured output model for intent identification."""
    country: str = Field(description="The name of the country mentioned in the query")
    fields: list[str] = Field(
        description="List of specific fields requested, or ['all'] if asking for general information. "
        "Common fields: population, capital, currency, currencies, region, languages, area, borders, timezones"
    )


class AgentState(TypedDict):
    """State structure for the agent."""
    user_query: str
    identified_country: str
    identified_fields: list[str]
    country_data: dict
    extracted_data: dict
    final_answer: str
    error: str


class CountryInformationAgent:
    """Agent for answering country information questions."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.DEFAULT_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=0
        )
        self.structured_llm = self.llm.with_structured_output(IntentIdentification)
        self.tool = CountryAPITool()
        self.graph = self._build_graph()
    
    def _identify_intent(self, state: AgentState) -> AgentState:
        """
        Step 1: Identify the country name and fields of interest from user query.
        Uses structured output for reliable parsing.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with identified_country and identified_fields
        """
        user_query = state["user_query"]
        
        system_prompt = """You are an intent identification system for country information queries.
Your task is to extract:
1. The country name from the user's query
2. The specific fields/information the user is asking about

Common fields include: population, capital, currency/currencies, region, languages, area, borders, timezones.
If the user asks for general information or doesn't specify fields, use ['all'].

Examples:
- "What is the population of Germany?" -> country: "Germany", fields: ["population"]
- "What is the capital and population of Brazil?" -> country: "Brazil", fields: ["capital", "population"]
- "Tell me about Japan" -> country: "Japan", fields: ["all"]
- "What currency does Japan use?" -> country: "Japan", fields: ["currency"]"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User query: {user_query}")
        ]
        
        try:
            result = self.structured_llm.invoke(messages)
            
            if not result.country:
                state["error"] = "Could not identify country name from query."
                return state
            
            state["identified_country"] = result.country
            state["identified_fields"] = result.fields if result.fields else ["all"]
            state["error"] = ""
            
        except Exception as e:
            state["error"] = f"Error in intent identification: {str(e)}"
        
        return state
    
    def _invoke_tool(self, state: AgentState) -> AgentState:
        """
        Step 2: Invoke the REST Countries API tool to fetch country data.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with country_data
        """
        if state.get("error"):
            return state
        
        country_name = state["identified_country"]
        
        try:
            country_data = self.tool.fetch_country_data(country_name)
            
            if not country_data:
                state["error"] = f"Country '{country_name}' not found in the database."
                return state
            
            state["country_data"] = country_data
            state["error"] = ""
            
        except Exception as e:
            state["error"] = f"Error fetching country data: {str(e)}"
        
        return state
    
    def _extract_data(self, state: AgentState) -> AgentState:
        """
        Extract specific fields from country data based on identified fields.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with extracted_data
        """
        if state.get("error") or not state.get("country_data"):
            return state
        
        country_data = state["country_data"]
        identified_fields = state["identified_fields"]
        extracted_data = {}
        
        if "all" in identified_fields:
            extracted_data = {
                "name": country_data.get("name", {}).get("common"),
                "official_name": country_data.get("name", {}).get("official"),
                "population": country_data.get("population"),
                "capital": country_data.get("capital", [None])[0] if country_data.get("capital") else None,
                "currencies": list(country_data.get("currencies", {}).keys()) if country_data.get("currencies") else None,
                "region": country_data.get("region"),
                "subregion": country_data.get("subregion"),
                "languages": list(country_data.get("languages", {}).values()) if country_data.get("languages") else None,
                "area": country_data.get("area"),
            }
        else:
            for field in identified_fields:
                try:
                    value = self.tool.extract_field(country_data, field)
                    if value is not None:
                        extracted_data[field] = value
                except Exception:
                    pass
        
        state["extracted_data"] = extracted_data
        return state
    
    def _synthesize_answer(self, state: AgentState) -> AgentState:
        """
        Step 3: Synthesize a natural language answer from extracted data.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with final_answer
        """
        if state.get("error"):
            state["final_answer"] = f"I'm sorry, I encountered an error: {state['error']}"
            return state
        
        user_query = state["user_query"]
        extracted_data = state.get("extracted_data", {})
        country_name = state.get("identified_country", "the country")
        
        if not extracted_data:
            state["final_answer"] = f"I couldn't find the requested information for {country_name}."
            return state
        
        system_prompt = """You are a helpful assistant that provides information about countries.
Based on the extracted data, provide a clear, concise, and natural answer to the user's question.
Be factual and accurate. If a specific field is not available, mention that it's not available.
Keep your answer focused on what was asked."""
        
        data_str = "\n".join([f"{k}: {v}" for k, v in extracted_data.items()])
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User question: {user_query}\n\nExtracted data:\n{data_str}\n\nProvide a natural answer:")
        ]
        
        try:
            response = self.llm.invoke(messages)
            state["final_answer"] = response.content.strip()
        except Exception as e:
            state["final_answer"] = f"I encountered an error while generating the answer: {str(e)}"
        
        return state
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow graph."""
        workflow = StateGraph(AgentState)
        
        workflow.add_node("identify_intent", self._identify_intent)
        workflow.add_node("invoke_tool", self._invoke_tool)
        workflow.add_node("extract_data", self._extract_data)
        workflow.add_node("synthesize_answer", self._synthesize_answer)
        
        workflow.set_entry_point("identify_intent")
        workflow.add_edge("identify_intent", "invoke_tool")
        workflow.add_edge("invoke_tool", "extract_data")
        workflow.add_edge("extract_data", "synthesize_answer")
        workflow.add_edge("synthesize_answer", END)
        
        return workflow.compile()
    
    def query(self, user_query: str) -> str:
        """
        Process a user query through the agent workflow.
        
        Args:
            user_query: The user's question about a country
            
        Returns:
            The agent's answer
        """
        initial_state: AgentState = {
            "user_query": user_query,
            "identified_country": "",
            "identified_fields": [],
            "country_data": {},
            "extracted_data": {},
            "final_answer": "",
            "error": ""
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state.get("final_answer", "I'm sorry, I couldn't process your query.")

