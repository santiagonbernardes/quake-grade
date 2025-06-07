"""
LLM Service for earthquake data analysis and insights generation.
Integrates with OpenAI API for generating insights, risk assessments, and data quality analysis.
"""

from typing import Optional

import pandas as pd
from openai import OpenAI

from .llm_prompts import (
    INSIGHTS_SYSTEM_PROMPT,
    QUALITY_SYSTEM_PROMPT,
    RISK_SYSTEM_PROMPT,
    create_insights_prompt,
    create_quality_prompt,
    create_risk_prompt,
)


class LLMService:
    """Service for LLM-powered earthquake data analysis."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize LLM service with OpenAI client."""
        self._client = None
        self._error_message = None
        if api_key:
            self._initialize_client(api_key)

    def _initialize_client(self, api_key: str) -> None:
        """Initialize OpenAI client with API key."""
        try:
            self._client = OpenAI(api_key=api_key)
        except Exception as e:
            self._error_message = f"Erro ao inicializar serviço de IA: {str(e)}"

    def is_available(self) -> bool:
        """Check if LLM service is available."""
        return self._client is not None

    def get_error_message(self) -> Optional[str]:
        """Get the last error message if service is not available."""
        return self._error_message

    def generate_prediction_insights(
        self, predictions_df: pd.DataFrame
    ) -> Optional[str]:
        """Generate insights from earthquake prediction results."""
        if not self.is_available():
            return None

        data_summary = self._prepare_data_summary(predictions_df)
        prompt = create_insights_prompt(data_summary)

        return self._call_openai_api(
            system_prompt=INSIGHTS_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=1000,
            temperature=0.3,
            error_message="Erro ao gerar insights",
        )

    def generate_risk_assessment(
        self, predictions_df: pd.DataFrame
    ) -> Optional[str]:
        """Generate risk assessment narrative from predictions."""
        if not self.is_available():
            return None

        risk_summary = self._prepare_risk_summary(predictions_df)
        prompt = create_risk_prompt(risk_summary)

        return self._call_openai_api(
            system_prompt=RISK_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=800,
            temperature=0.2,
            error_message="Erro ao gerar avaliação de risco",
        )

    def analyze_data_quality(self, df: pd.DataFrame) -> Optional[str]:
        """Analyze data quality and provide recommendations."""
        if not self.is_available():
            return None

        quality_summary = self._prepare_quality_summary(df)
        prompt = create_quality_prompt(quality_summary)

        return self._call_openai_api(
            system_prompt=QUALITY_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=600,
            temperature=0.3,
            error_message="Erro ao analisar qualidade dos dados",
        )

    def _call_openai_api(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
        error_message: str,
    ) -> Optional[str]:
        """Make API call to OpenAI with error handling."""
        try:
            response = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            self._error_message = f"{error_message}: {str(e)}"
            return None

    def _prepare_data_summary(self, df: pd.DataFrame) -> dict:
        """Prepare data summary for LLM analysis using only available columns."""
        try:
            summary = {
                "total_events": len(df),
                "magnitude_stats": {},
                "depth_stats": {},
                "latitude_range": {},
                "longitude_range": {},
                "severity_distribution": {}
            }

            if "Magnitud" in df.columns:
                summary["magnitude_stats"] = self._get_numeric_stats(df["Magnitud"])

            if "Profundidad" in df.columns:
                summary["depth_stats"] = self._get_numeric_stats(df["Profundidad"])

            if "Latitud" in df.columns:
                summary["latitude_range"] = self._get_range_stats(df["Latitud"])

            if "Longitud" in df.columns:
                summary["longitude_range"] = self._get_range_stats(df["Longitud"])

            if "Gravedad" in df.columns:
                summary["severity_distribution"] = (
                    df["Gravedad"].value_counts().to_dict()
                )

            return summary
        except Exception:
            return {"total_events": len(df), "error": "Erro ao processar dados"}

    def _get_numeric_stats(self, series: pd.Series) -> dict:
        """Get numeric statistics for a pandas series."""
        return {
            "min": float(series.min()),
            "max": float(series.max()),
            "mean": float(series.mean()),
            "std": float(series.std())
        }

    def _get_range_stats(self, series: pd.Series) -> dict:
        """Get range statistics for a pandas series."""
        return {
            "min": float(series.min()),
            "max": float(series.max())
        }

    def _prepare_risk_summary(self, df: pd.DataFrame) -> dict:
        """Prepare risk summary for assessment using only available columns."""
        try:
            summary = {
                "total_events": len(df),
                "high_risk_count": 0,
                "medium_risk_count": 0,
                "low_risk_count": 0,
                "avg_magnitude_high_risk": 0
            }

            if "Gravedad" in df.columns:
                high_risk = df[df["Gravedad"] == "Muy Alta"]
                medium_risk = df[df["Gravedad"] == "Alta"]
                low_risk = df[df["Gravedad"].isin(["Media", "Baja"])]

                summary["high_risk_count"] = len(high_risk)
                summary["medium_risk_count"] = len(medium_risk)
                summary["low_risk_count"] = len(low_risk)

                if len(high_risk) > 0 and "Magnitud" in high_risk.columns:
                    summary["avg_magnitude_high_risk"] = float(
                        high_risk["Magnitud"].mean()
                    )

            return summary
        except Exception:
            return {
                "total_events": len(df),
                "error": "Erro ao processar dados de risco",
            }

    def _prepare_quality_summary(self, df: pd.DataFrame) -> dict:
        """Prepare data quality summary."""
        try:
            summary = {
                "total_rows": len(df),
                "columns": list(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "duplicate_rows": df.duplicated().sum(),
                "data_types": df.dtypes.astype(str).to_dict()
            }
            return summary
        except Exception:
            return {"total_rows": len(df), "error": "Erro ao analisar qualidade"}



# Factory function to create LLM service instance
def create_llm_service(api_key: Optional[str] = None) -> LLMService:
    """Create and return an LLM service instance."""
    return LLMService(api_key=api_key)
