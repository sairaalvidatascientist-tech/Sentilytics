"""
Alert System for Sentilytics
Detects sentiment spikes and triggers notifications
"""
from typing import Dict, List
from datetime import datetime
from .config import config

class AlertSystem:
    def __init__(self):
        self.alert_history = []
        self.negative_threshold = config.NEGATIVE_SENTIMENT_ALERT_THRESHOLD
    
    def check_sentiment_spike(self, sentiment_data: Dict) -> Dict:
        """
        Check if there's a significant sentiment spike
        Returns alert information if spike detected
        """
        total = sentiment_data['total']
        if total == 0:
            return None
        
        negative_percentage = sentiment_data['negative'] / total
        
        if negative_percentage >= self.negative_threshold:
            alert = {
                'type': 'negative_spike',
                'severity': 'high' if negative_percentage >= 0.6 else 'medium',
                'message': f'High negative sentiment detected ({negative_percentage*100:.1f}%)',
                'timestamp': datetime.now().isoformat(),
                'data': sentiment_data
            }
            
            self.alert_history.append(alert)
            return alert
        
        return None
    
    def check_sudden_change(self, previous_data: Dict, current_data: Dict) -> Dict:
        """
        Check for sudden changes in sentiment
        """
        if not previous_data or not current_data:
            return None
        
        prev_total = previous_data['total']
        curr_total = current_data['total']
        
        if prev_total == 0 or curr_total == 0:
            return None
        
        prev_negative_pct = previous_data['negative'] / prev_total
        curr_negative_pct = current_data['negative'] / curr_total
        
        change = curr_negative_pct - prev_negative_pct
        
        # Alert if negative sentiment increased by more than 20%
        if change >= 0.2:
            alert = {
                'type': 'sudden_change',
                'severity': 'high',
                'message': f'Sudden increase in negative sentiment (+{change*100:.1f}%)',
                'timestamp': datetime.now().isoformat(),
                'previous_data': previous_data,
                'current_data': current_data
            }
            
            self.alert_history.append(alert)
            return alert
        
        return None
    
    def get_alert_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent alerts
        """
        return self.alert_history[-limit:]
    
    def clear_history(self):
        """
        Clear alert history
        """
        self.alert_history = []
