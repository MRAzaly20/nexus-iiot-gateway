# core/rule_engine.py
import logging
from typing import List
from ..models import DataPoint, AlarmRule, Alarm

logger = logging.getLogger(__name__)

class RuleEngine:
    """
    Mengevaluasi aturan alarm berdasarkan data yang masuk.
    """
    def __init__(self):
        # Daftar aturan aktif, bisa dimuat dari database
        self.active_rules: List[AlarmRule] = []

    def load_rules(self, rules: List[AlarmRule]):
        """Memuat atau memperbarui daftar aturan."""
        self.active_rules = [rule for rule in rules if rule.is_active]
        logger.info(f"Loaded {len(self.active_rules)} active alarm rules.")

    def evaluate(self, data_point: DataPoint) -> List[Alarm]:
        """
        Mengevaluasi sebuah data point terhadap semua aturan aktif.
        Mengembalikan daftar alarm yang terpicu.
        """
        triggered_alarms = []
        for rule in self.active_rules:
            if rule.tag_id == data_point.tag_id:
                # Evaluasi kondisi yang sangat sederhana
                # Di produksi, gunakan library evaluasi ekspresi yang aman
                try:
                    # WARNING: eval() bisa berbahaya. Gunakan library seperti `simpleeval` untuk produksi.
                    # condition = f"{data_point.value} {rule.condition}" # e.g., "85 > 80"
                    # if eval(condition):
                    
                    # Contoh evaluasi manual sederhana untuk 'value > X'
                    if rule.condition.startswith("value > "):
                        threshold = float(rule.condition.split(">")[1].strip())
                        if data_point.value > threshold:
                            alarm = self._create_alarm(rule, data_point)
                            triggered_alarms.append(alarm)
                    # Tambahkan kondisi lain seperti <, ==, range, dll.
                    
                except Exception as e:
                    logger.error(f"Error evaluating rule {rule.id} for data point {data_point.tag_id}: {e}")
        return triggered_alarms

    def _create_alarm(self, rule: AlarmRule, data_point: DataPoint) -> Alarm:
        """Membuat objek alarm berdasarkan rule dan data point."""
        return Alarm(
            rule_id=rule.id,
            name=rule.name,
            description=rule.description,
            tag_id=rule.tag_id,
            severity=rule.severity,
            timestamp_triggered=data_point.timestamp, # Gunakan timestamp data point
            value_at_trigger=data_point.value
        )
