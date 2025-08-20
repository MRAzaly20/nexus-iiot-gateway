# core/analytics_engine.py
import logging
import numpy as np
from scipy import fft
from typing import List, Dict, Any
from datetime import datetime
import uuid

# Import dari schemas
from ..models.analytics import (
    AnalyticsJobResponse, 
    AnalyticsType, 
    AnalyticsResultResponse
)
from ..models.data_processing import DataPointResponse

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """
    Melakukan analisis sederhana di edge.
    """
    def __init__(self):
        pass

    def run_job(self, job: Dict, data_points: List[Dict]) -> Dict:
        """
        Menjalankan sebuah job analytics pada data points.
        
        Args:
            job: Dictionary representasi AnalyticsJob
            data_points: List of dictionary representasi DataPoint
            
        Returns:
            Dictionary representasi AnalyticsResult
        """
        try:
            # Validasi input dengan Pydantic models
            job_model = AnalyticsJobResponse(**job)
            data_point_models = [DataPointResponse(**dp) for dp in data_points]
        except Exception as e:
            logger.error(f"Invalid input data for analytics job: {e}")
            raise ValueError(f"Invalid input data: {e}")

        logger.info(f"Running analytics job: {job_model.name} (Type: {job_model.type})")
        
        try:
            # Ekstrak values dan timestamps
            values = np.array([dp.value for dp in data_point_models])
            timestamps = [dp.timestamp for dp in data_point_models]

            result_data = {}
            execution_start = datetime.now()

            if job_model.type == AnalyticsType.STATISTICS:
                result_data = self._calculate_statistics(values)
            elif job_model.type == AnalyticsType.FFT:
                result_data = self._perform_fft(values, job_model.parameters or {})
            elif job_model.type == AnalyticsType.ANOMALY_DETECTION:
                result_data = self._detect_anomalies(values)
            else:
                logger.warning(f"Unsupported analytics type: {job_model.type}")
                result_data = {"error": f"Unsupported type: {job_model.type}"}

            execution_end = datetime.now()
            execution_time_ms = int((execution_end - execution_start).total_seconds() * 1000)

            # Buat result dictionary
            result_dict = {
                "id": str(uuid.uuid4()),
                "job_id": job_model.id,
                "timestamp": datetime.now(),
                "result_data": result_data,
                "execution_time_ms": execution_time_ms,
                "status": "success" if "error" not in result_data else "failed",
                "created_at": datetime.now()
            }

            logger.info(f"Analytics job {job_model.name} completed in {execution_time_ms}ms")
            return result_dict

        except Exception as e:
            logger.error(f"Error running analytics job {job_model.name}: {e}", exc_info=True)
            
            # Return error result
            error_result = {
                "id": str(uuid.uuid4()),
                "job_id": job_model.id,
                "timestamp": datetime.now(),
                "result_data": {"error": str(e)},
                "execution_time_ms": 0,
                "status": "failed",
                "error_message": str(e),
                "created_at": datetime.now()
            }
            return error_result

    def _calculate_statistics(self, values: np.ndarray) -> Dict[str, float]:
        """Menghitung statistik dasar."""
        if len(values) == 0:
            return {"error": "No data points provided"}
            
        try:
            return {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "median": float(np.median(values)),
                "count": int(len(values)),
                "sum": float(np.sum(values))
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {"error": f"Failed to calculate statistics: {str(e)}"}

    def _perform_fft(self, values: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
        """Melakukan FFT sederhana."""
        if len(values) == 0:
            return {"error": "No data points provided"}
            
        try:
            # Parameter dengan default values
            sampling_rate = params.get("sampling_rate", 1.0)
            max_frequency = params.get("max_frequency", None)
            
            # Validasi sampling rate
            if sampling_rate <= 0:
                return {"error": "Sampling rate must be positive"}
                
            # Perform FFT
            yf = fft.fft(values)
            xf = fft.fftfreq(len(values), 1 / sampling_rate)
            
            # Ambil hanya komponen positif
            half_len = len(values) // 2
            xf_positive = xf[:half_len]
            yf_positive = yf[:half_len]
            
            # Filter berdasarkan max_frequency jika diberikan
            if max_frequency is not None and max_frequency > 0:
                freq_mask = xf_positive <= max_frequency
                xf_positive = xf_positive[freq_mask]
                yf_positive = yf_positive[freq_mask]
            
            return {
                "frequencies": xf_positive.tolist(),
                "magnitudes": np.abs(yf_positive).tolist(),
                "phase": np.angle(yf_positive).tolist(),
                "sampling_rate": sampling_rate,
                "total_points": len(values)
            }
        except Exception as e:
            logger.error(f"Error performing FFT: {e}")
            return {"error": f"Failed to perform FFT: {str(e)}"}

    def _detect_anomalies(self, values: np.ndarray) -> Dict[str, Any]:
        """Deteksi anomaly sederhana menggunakan Z-score."""
        if len(values) == 0:
            return {"error": "No data points provided"}
            
        try:
            mean = np.mean(values)
            std = np.std(values)
            
            if std == 0:
                # Semua nilai sama, tidak ada anomaly
                return {
                    "anomalies": [], 
                    "z_scores": [0.0] * len(values),
                    "mean": float(mean),
                    "std": 0.0,
                    "threshold": 2.0
                }
            
            z_scores = np.abs((values - mean) / std)
            threshold = 2.0  # Z-score threshold untuk anomaly
            anomaly_indices = np.where(z_scores > threshold)[0]
            
            anomalies = []
            for i in anomaly_indices:
                anomalies.append({
                    "index": int(i),
                    "value": float(values[i]),
                    "z_score": float(z_scores[i]),
                    "mean": float(mean),
                    "std": float(std)
                })
            
            return {
                "anomalies": anomalies,
                "z_scores": z_scores.tolist(),
                "mean": float(mean),
                "std": float(std),
                "threshold": threshold,
                "anomaly_count": len(anomalies),
                "total_points": len(values)
            }
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return {"error": f"Failed to detect anomalies: {str(e)}"}

    def validate_job_parameters(self, job_type: str, parameters: Dict[str, Any]) -> bool:
        """Validasi parameter untuk job analytics."""
        try:
            if job_type == AnalyticsType.FFT:
                sampling_rate = parameters.get("sampling_rate", 1.0)
                if not isinstance(sampling_rate, (int, float)) or sampling_rate <= 0:
                    return False
                max_frequency = parameters.get("max_frequency")
                if max_frequency is not None and (not isinstance(max_frequency, (int, float)) or max_frequency <= 0):
                    return False
            elif job_type == AnalyticsType.STATISTICS:
                # Statistics tidak memerlukan parameter khusus
                pass
            elif job_type == AnalyticsType.ANOMALY_DETECTION:
                # Anomaly detection tidak memerlukan parameter khusus
                pass
            return True
        except Exception:
            return False