# core/transformer.py
import logging
from typing import List, Dict, Any
from datetime import datetime
import copy

# Import dari schemas, bukan models
from ..models.data_processing import (
    DataPointResponse, 
    TransformFunctionResponse, 
    TransformType
)

logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Menangani fungsi transformasi data low-code.
    """

    def __init__(self):
        # Bisa diinisialisasi dengan fungsi transformasi kustom jika diperlukan
        pass

    def apply_transformations(self, data_points: List[Dict], transforms: List[Dict]) -> List[Dict]:
        """
        Menerapkan daftar transformasi secara berurutan pada batch data point.
        
        Args:
            data_points: List of data point dictionaries
            transforms: List of transform function dictionaries
            
        Returns:
            List of transformed data point dictionaries
        """
        logger.info(f"Applying {len(transforms)} transformations to {len(data_points)} data points.")
        transformed_points = copy.deepcopy(data_points)

        for transform_dict in transforms:
            try:
                # Konversi ke Pydantic model untuk validasi dan akses yang lebih muda
                transform = TransformFunctionResponse(**transform_dict)
                
                if transform.type == TransformType.SCALE:
                    transformed_points = self._scale(transformed_points, transform.parameters)
                elif transform.type == TransformType.NORMALIZE:
                    transformed_points = self._normalize(transformed_points, transform.parameters)
                elif transform.type == TransformType.UNIT_CONVERT:
                    transformed_points = self._unit_convert(transformed_points, transform.parameters)
                elif transform.type == TransformType.FILTER:
                    transformed_points = self._filter(transformed_points, transform.parameters)
                elif transform.type == TransformType.AGGREGATE:
                    transformed_points = self._aggregate(transformed_points, transform.parameters)
                else:
                    logger.warning(f"Unknown transform type: {transform.type}")
            except Exception as e:
                logger.error(f"Error applying transform {transform_dict.get('name', 'Unknown')}: {e}")
                # Untuk sekarang, kita lewati transformasi yang error
                continue
                
        return transformed_points

    def _scale(self, data_points: List[Dict], params: Dict[str, Any]) -> List[Dict]:
        """
        Melakukan scaling linier: y = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        """
        in_min = params.get('input_min')
        in_max = params.get('input_max')
        out_min = params.get('output_min')
        out_max = params.get('output_max')

        if None in [in_min, in_max, out_min, out_max]:
            logger.error("Missing parameters for scaling.")
            return data_points  # Return as is if params are missing

        if in_max == in_min:
            logger.warning("input_max equals input_min, scaling not possible.")
            return data_points

        scale_factor = (out_max - out_min) / (in_max - in_min)
        scaled_points = []
        
        for point_dict in data_points:
            try:
                # Konversi ke Pydantic model untuk validasi
                point = DataPointResponse(**point_dict)
                new_value = (point.value - in_min) * scale_factor + out_min
                
                # Update point dengan nilai baru
                new_point_dict = point_dict.copy()
                new_point_dict['value'] = new_value
                new_point_dict['id'] = f"{point.id}_scaled" if point.id else None
                
                scaled_points.append(new_point_dict)
            except Exception as e:
                logger.warning(f"Error scaling point: {e}")
                scaled_points.append(point_dict)  # Keep original if error
                
        logger.debug(f"Scaled {len(scaled_points)} points using parameters {params}.")
        return scaled_points

    def _normalize(self, data_points: List[Dict], params: Dict[str, Any]) -> List[Dict]:
        """
        Melakukan normalisasi data (min-max normalization ke range 0-1).
        """
        if not data_points:
            return data_points
            
        try:
            # Ekstrak nilai untuk menghitung min/max
            values = [point.get('value', 0) for point in data_points]
            if not values:
                return data_points
                
            min_val = min(values)
            max_val = max(values)
            
            if max_val == min_val:
                logger.warning("All values are the same, normalization not possible.")
                return data_points
            
            normalized_points = []
            for point_dict in data_points:
                try:
                    value = point_dict.get('value', 0)
                    normalized_value = (value - min_val) / (max_val - min_val)
                    
                    new_point_dict = point_dict.copy()
                    new_point_dict['value'] = normalized_value
                    new_point_dict['id'] = f"{point_dict.get('id', 'point')}_normalized"
                    
                    normalized_points.append(new_point_dict)
                except Exception as e:
                    logger.warning(f"Error normalizing point: {e}")
                    normalized_points.append(point_dict)
                    
            logger.debug(f"Normalized {len(normalized_points)} points.")
            return normalized_points
            
        except Exception as e:
            logger.error(f"Error in normalization: {e}")
            return data_points

    def _unit_convert(self, data_points: List[Dict], params: Dict[str, Any]) -> List[Dict]:
        """
        Melakukan konversi unit sederhana (contoh: Celsius ke Fahrenheit).
        """
        conversion_type = params.get('conversion_type', 'celsius_to_fahrenheit')
        
        converted_points = []
        for point_dict in data_points:
            try:
                value = point_dict.get('value', 0)
                new_value = value
                
                if conversion_type == 'celsius_to_fahrenheit':
                    new_value = (value * 9/5) + 32
                elif conversion_type == 'fahrenheit_to_celsius':
                    new_value = (value - 32) * 5/9
                # Tambahkan konversi lainnya sesuai kebutuhan
                
                new_point_dict = point_dict.copy()
                new_point_dict['value'] = new_value
                new_point_dict['id'] = f"{point_dict.get('id', 'point')}_converted"
                
                converted_points.append(new_point_dict)
                
            except Exception as e:
                logger.warning(f"Error converting unit for point: {e}")
                converted_points.append(point_dict)
                
        logger.debug(f"Converted {len(converted_points)} points using {conversion_type}.")
        return converted_points

    def _filter(self, data_points: List[Dict], params: Dict[str, Any]) -> List[Dict]:
        """
        Melakukan filtering sederhana (contoh: moving average).
        """
        filter_type = params.get('filter_type', 'moving_average')
        window_size = params.get('window_size', 3)
        
        if filter_type == 'moving_average':
            return self._moving_average(data_points, window_size)
        else:
            logger.warning(f"Unknown filter type: {filter_type}")
            return data_points

    def _moving_average(self, data_points: List[Dict], window_size: int) -> List[Dict]:
        """
        Melakukan moving average filter.
        """
        if len(data_points) < window_size:
            logger.warning("Not enough data points for moving average.")
            return data_points
            
        filtered_points = []
        values = [point.get('value', 0) for point in data_points]
        
        for i in range(len(values)):
            if i < window_size - 1:
                # Untuk titik pertama, gunakan nilai asli
                filtered_points.append(data_points[i])
            else:
                # Hitung rata-rata dari window
                window_values = values[i - window_size + 1:i + 1]
                avg_value = sum(window_values) / len(window_values)
                
                new_point_dict = data_points[i].copy()
                new_point_dict['value'] = avg_value
                new_point_dict['id'] = f"{data_points[i].get('id', 'point')}_filtered"
                
                filtered_points.append(new_point_dict)
                
        logger.debug(f"Applied moving average filter with window size {window_size}.")
        return filtered_points

    def _aggregate(self, data_points: List[Dict], params: Dict[str, Any]) -> List[Dict]:
        """
        Melakukan agregasi data (contoh: rata-rata per menit).
        """
        aggregation_type = params.get('aggregation_type', 'average')
        time_window = params.get('time_window', '1m')  # 1 menit default
        
        # Untuk implementasi sederhana, kita akan menghitung agregasi dasar
        if not data_points:
            return data_points
            
        try:
            values = [point.get('value', 0) for point in data_points]
            
            if aggregation_type == 'average':
                result_value = sum(values) / len(values) if values else 0
            elif aggregation_type == 'sum':
                result_value = sum(values)
            elif aggregation_type == 'min':
                result_value = min(values) if values else 0
            elif aggregation_type == 'max':
                result_value = max(values) if values else 0
            else:
                logger.warning(f"Unknown aggregation type: {aggregation_type}")
                return data_points
            
            # Buat satu point hasil agregasi
            aggregated_point = {
                'id': f"aggregated_{datetime.now().isoformat()}",
                'timestamp': datetime.now().isoformat(),
                'tag_id': data_points[0].get('tag_id', 'aggregated') if data_points else 'aggregated',
                'value': result_value,
                'data_metadata': {
                    'aggregation_type': aggregation_type,
                    'original_count': len(data_points)
                }
            }
            
            logger.debug(f"Aggregated {len(data_points)} points to single value: {result_value}")
            return [aggregated_point]
            
        except Exception as e:
            logger.error(f"Error in aggregation: {e}")
            return data_points