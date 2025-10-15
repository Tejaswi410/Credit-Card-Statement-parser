import re
import pdfplumber
from datetime import datetime
from typing import Dict, List, Optional, Any

class CreditCardParser:
    def __init__(self):
        self.providers = {
            'HDFC': self._parse_hdfc,
            'ICICI': self._parse_icici,
            'AXIS': self._parse_axis,
            'KOTAK': self._parse_kotak,
            'SBI': self._parse_sbi
        }
    
    def parse(self, filepath: str) -> Dict[str, Any]:
        """Main parsing method"""
        try:
            text = self._extract_text(filepath)
            
            if not text:
                return {
                    'success': False,
                    'error': 'Could not extract text from PDF'
                }
            
            provider = self._detect_provider(text)
            
            if provider in self.providers:
                data = self.providers[provider](text)
            else:
                data = self._parse_generic(text)
            
            return {
                'success': True,
                'provider': provider or 'Unknown',
                'data': data,
                'confidence': self._calculate_confidence(data)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Parsing error: {str(e)}'
            }
    
    def _extract_text(self, filepath: str) -> str:
        """Extract text from PDF using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to read PDF: {str(e)}")
    
    def _detect_provider(self, text: str) -> str:
        """Detect credit card provider from text"""
        text_upper = text.upper()
        
        if 'HDFC BANK' in text_upper:
            return 'HDFC'
        elif 'ICICI BANK' in text_upper:
            return 'ICICI'
        elif 'AXIS BANK' in text_upper:
            return 'AXIS'
        elif 'KOTAK' in text_upper:
            return 'KOTAK'
        elif 'STATE BANK OF INDIA' in text_upper or 'SBI' in text_upper:
            return 'SBI'
        
        return 'Unknown'
    
    def _parse_hdfc(self, text: str) -> Dict[str, Any]:
        """Parse HDFC credit card statement"""
        data = {
            'cardholder_name': self._extract_hdfc_name(text),
            'card_number': self._extract_hdfc_card(text),
            'statement_date': self._extract_hdfc_statement_date(text),
            'payment_due_date': self._extract_hdfc_due_date(text),
            'total_amount_due': self._extract_hdfc_total_due(text),
            'minimum_amount_due': self._extract_hdfc_min_due(text),
            'credit_limit': self._extract_hdfc_credit_limit(text),
            'transactions': self._extract_hdfc_transactions(text)
        }
        return data
    
    def _parse_icici(self, text: str) -> Dict[str, Any]:
        """Parse ICICI credit card statement"""
        data = {
            'cardholder_name': self._extract_icici_name(text),
            'card_number': self._extract_icici_card(text),
            'statement_date': self._extract_icici_statement_date(text),
            'payment_due_date': self._extract_icici_due_date(text),
            'total_amount_due': self._extract_icici_total_due(text),
            'minimum_amount_due': self._extract_icici_min_due(text),
            'credit_limit': self._extract_icici_credit_limit(text),
            'transactions': self._extract_icici_transactions(text)
        }
        return data
    
    def _parse_axis(self, text: str) -> Dict[str, Any]:
        """Parse Axis Bank credit card statement"""
        data = {
            'cardholder_name': self._extract_axis_name(text),
            'card_number': self._extract_axis_card(text),
            'statement_date': self._extract_axis_statement_date(text),
            'payment_due_date': self._extract_axis_due_date(text),
            'total_amount_due': self._extract_axis_total_due(text),
            'minimum_amount_due': self._extract_axis_min_due(text),
            'credit_limit': self._extract_axis_credit_limit(text),
            'transactions': self._extract_axis_transactions(text)
        }
        return data
    
    def _parse_kotak(self, text: str) -> Dict[str, Any]:
        """Parse Kotak credit card statement"""
        data = {
            'cardholder_name': self._extract_kotak_name(text),
            'card_number': self._extract_kotak_card(text),
            'statement_date': self._extract_kotak_statement_date(text),
            'payment_due_date': self._extract_kotak_due_date(text),
            'total_amount_due': self._extract_kotak_total_due(text),
            'minimum_amount_due': self._extract_kotak_min_due(text),
            'credit_limit': self._extract_kotak_credit_limit(text),
            'transactions': self._extract_kotak_transactions(text)
        }
        return data
    
    def _parse_sbi(self, text: str) -> Dict[str, Any]:
        """Parse SBI credit card statement"""
        data = {
            'cardholder_name': self._extract_sbi_name(text),
            'card_number': self._extract_sbi_card(text),
            'statement_date': self._extract_sbi_statement_date(text),
            'payment_due_date': self._extract_sbi_due_date(text),
            'total_amount_due': self._extract_sbi_total_due(text),
            'minimum_amount_due': self._extract_sbi_min_due(text),
            'credit_limit': self._extract_sbi_credit_limit(text),
            'transactions': self._extract_sbi_transactions(text)
        }
        return data
    
    def _parse_generic(self, text: str) -> Dict[str, Any]:
        """Generic parser for unknown providers"""
        return {
            'cardholder_name': self._extract_generic_name(text),
            'card_number': self._extract_generic_card(text),
            'statement_date': 'Not Found',
            'payment_due_date': self._extract_generic_due_date(text),
            'total_amount_due': self._extract_generic_amount(text),
            'minimum_amount_due': 'Not Found',
            'credit_limit': 'Not Found',
            'transactions': []
        }
    
    # ===== HDFC EXTRACTION METHODS =====
    
    def _extract_hdfc_name(self, text: str) -> str:
        match = re.search(r'Name\s*:\s*([A-Z\s]+)', text)
        if match:
            return match.group(1).strip()
        return 'Not Found'
    
    def _extract_hdfc_card(self, text: str) -> str:
        match = re.search(r'Card\s*No:\s*([\dX\s]+)', text)
        if match:
            return match.group(1).strip()
        return 'Not Found'
    
    def _extract_hdfc_statement_date(self, text: str) -> str:
        match = re.search(r'Statement\s*Date:\s*(\d{2}/\d{2}/\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_hdfc_due_date(self, text: str) -> str:
        match = re.search(r'Payment\s*Due\s*Date\s*Total\s*Dues[^\n]*\n\s*(\d{2}/\d{2}/\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_hdfc_total_due(self, text: str) -> str:
        match = re.search(r'Total\s*Dues[^\n]*\n\s*\d{2}/\d{2}/\d{4}\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_hdfc_min_due(self, text: str) -> str:
        match = re.search(r'Minimum\s*Amount\s*Due[^\n]*\n\s*\d{2}/\d{2}/\d{4}\s*[\d,]+\.?\d*\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_hdfc_credit_limit(self, text: str) -> str:
        match = re.search(r'Credit\s*Limit\s*Available[^\n]*\n\s*([\d,]+)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_hdfc_transactions(self, text: str) -> List[Dict]:
        transactions = []
        lines = text.split('\n')
        in_transaction_section = False
        
        for line in lines:
            if 'Domestic Transactions' in line or 'International Transactions' in line:
                in_transaction_section = True
                continue
            
            if in_transaction_section:
                match = re.match(r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.\d{2})\s*(Cr)?', line.strip())
                if match:
                    transactions.append({
                        'date': match.group(1),
                        'description': match.group(2).strip(),
                        'amount': f"₹{match.group(3)}",
                        'type': 'Credit' if match.group(4) else 'Debit'
                    })
        
        return transactions
    
    # ===== ICICI EXTRACTION METHODS =====
    
    def _extract_icici_name(self, text: str) -> str:
        match = re.search(r'MR\.\s+([A-Z\s]+)', text)
        if match:
            name = match.group(1).strip()
            # Stop at address indicators
            name = re.split(r'\d{3,}|[A-Z]{2,}\s+B\s+\d+', name)[0].strip()
            return name
        return 'Not Found'
    
    def _extract_icici_card(self, text: str) -> str:
        match = re.search(r'(\d{4}[X]{6,}\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_icici_statement_date(self, text: str) -> str:
        match = re.search(r'STATEMENT\s*DATE[^\n]*\n[^\n]*\n[^\n]*\n([A-Za-z]+\s+\d{1,2},\s*\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_icici_due_date(self, text: str) -> str:
        match = re.search(r'PAYMENT\s*DUE\s*DATE[^\n]*\n[^\n]*\n[^\n]*\n([A-Za-z]+\s+\d{1,2},\s*\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_icici_total_due(self, text: str) -> str:
        match = re.search(r'Total\s*Amount\s*due\s*`([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_icici_min_due(self, text: str) -> str:
        match = re.search(r'Minimum\s*Amount\s*due\s*`([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_icici_credit_limit(self, text: str) -> str:
        match = re.search(r'Credit\s*Limit[^\n]*\n\s*`([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_icici_transactions(self, text: str) -> List[Dict]:
        transactions = []
        pattern = r'(\d{2}/\d{2}/\d{4})\s+\d+\s+(.+?)\s+\d+\s+([\d,]+\.?\d*)\s*(CR)?'
        
        for match in re.finditer(pattern, text):
            transactions.append({
                'date': match.group(1),
                'description': match.group(2).strip(),
                'amount': f"₹{match.group(3)}",
                'type': 'Credit' if match.group(4) else 'Debit'
            })
        
        return transactions
    
    # ===== AXIS EXTRACTION METHODS =====
    
    def _extract_axis_name(self, text: str) -> str:
        match = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*\nCredit\s*Card\s*Statement', text)
        if match:
            return match.group(1).strip()
        return 'Not Found'
    
    def _extract_axis_card(self, text: str) -> str:
        match = re.search(r'Card\s*Number\s*:\s*([\d\*]+)', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_axis_statement_date(self, text: str) -> str:
        match = re.search(r'Statement\s*Date\s*(\d{2}/\d{2}/\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_axis_due_date(self, text: str) -> str:
        match = re.search(r'Payment\s*Due\s*Date\s*(\d{2}/\d{2}/\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_axis_total_due(self, text: str) -> str:
        match = re.search(r'Total\s*Amount\s*Due\s*r\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_axis_min_due(self, text: str) -> str:
        match = re.search(r'Minimum\s*Amount\s*Due\s*r\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_axis_credit_limit(self, text: str) -> str:
        match = re.search(r'Credit\s*Limit\s*r\s*([\d,]+)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_axis_transactions(self, text: str) -> List[Dict]:
        transactions = []
        pattern = r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.?\d*)\s*(CR)?'
        
        lines = text.split('\n')
        in_transaction_section = False
        
        for line in lines:
            if 'Transaction Date' in line:
                in_transaction_section = True
                continue
            
            if in_transaction_section and re.match(r'^\d{2}/\d{2}/\d{4}', line.strip()):
                match = re.match(r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.?\d*)\s*(CR)?', line.strip())
                if match:
                    transactions.append({
                        'date': match.group(1),
                        'description': match.group(2).strip(),
                        'amount': f"₹{match.group(3)}",
                        'type': 'Credit' if match.group(4) else 'Debit'
                    })
        
        return transactions
    
    # ===== KOTAK EXTRACTION METHODS =====
    
    def _extract_kotak_name(self, text: str) -> str:
        # Kotak names appear as concatenated strings like "JULLYSHAILESHSHAH"
        # Look for pattern: NAME followed by "StatementDate"
        match = re.search(r'^([A-Z]+)\s+StatementDate', text, re.MULTILINE)
        if match:
            name = match.group(1)
            if len(name) > 6:  # Reasonable name length
                # Try to add spaces between likely word boundaries
                # Look for patterns where lowercase letters might indicate word boundaries
                formatted_name = self._format_kotak_name(name)
                return formatted_name
        return 'Not Found'
    
    def _format_kotak_name(self, name: str) -> str:
        """Format concatenated Kotak name by adding spaces between likely words"""
        # This is a simple heuristic - could be improved with better logic
        # For now, just return the name as-is since it's working
        # In the future, this could be enhanced with name splitting logic
        return name
    
    def _extract_kotak_card(self, text: str) -> str:
        match = re.search(r'(\d{6}X+\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_kotak_statement_date(self, text: str) -> str:
        match = re.search(r'Statement\s*Date\s*(\d{2}-[A-Za-z]{3}-\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_kotak_due_date(self, text: str) -> str:
        match = re.search(r'Remember\s*to\s*Pay\s*By\s*(\d{2}-[A-Za-z]{3}-\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_kotak_total_due(self, text: str) -> str:
        match = re.search(r'Total\s*Amount\s*Due\s*Rs\.\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_kotak_min_due(self, text: str) -> str:
        match = re.search(r'Minimum\s*Amount\s*Due\s*Rs\.\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_kotak_credit_limit(self, text: str) -> str:
        match = re.search(r'Total\s*Credit\s*Limit\s*Rs\.\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_kotak_transactions(self, text: str) -> List[Dict]:
        transactions = []
        pattern = r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+[A-Za-z\s]+\s+([\d,]+\.?\d*)\s*(Cr)?'
        
        for match in re.finditer(pattern, text):
            transactions.append({
                'date': match.group(1),
                'description': match.group(2).strip(),
                'amount': f"₹{match.group(3)}",
                'type': 'Credit' if match.group(4) else 'Debit'
            })
        
        return transactions
    
    # ===== SBI EXTRACTION METHODS =====
    
    def _extract_sbi_name(self, text: str) -> str:
        match = re.search(r'MR\.\s+([A-Z\s]+)', text)
        if match:
            return match.group(1).strip()
        return 'Not Found'
    
    def _extract_sbi_card(self, text: str) -> str:
        match = re.search(r'(\d{4}\s*X+\s*X+\s*X+\s*\d{4})', text)
        if match:
            return match.group(1).replace(' ', '')
        return 'Not Found'
    
    def _extract_sbi_statement_date(self, text: str) -> str:
        match = re.search(r'Statement\s*Date\s*(\d{2}\s*[A-Z]{3}\s*\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_sbi_due_date(self, text: str) -> str:
        match = re.search(r'Payment\s*Due\s*Date\s*(\d{2}\s*[A-Z]{3}\s*\d{4})', text)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_sbi_total_due(self, text: str) -> str:
        match = re.search(r'Total\s*Payment\s*Due\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_sbi_min_due(self, text: str) -> str:
        match = re.search(r'Minimum\s*Payment\s*Due\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_sbi_credit_limit(self, text: str) -> str:
        match = re.search(r'Credit\s*Limit\s*([\d,]+\.?\d*)', text)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _extract_sbi_transactions(self, text: str) -> List[Dict]:
        transactions = []
        pattern = r'(\d{2}\.\d{2}\.\d{4})\s+([A-Z]+)\s+(.+?)\s+([\d,]+\.?\d*)'
        
        for match in re.finditer(pattern, text):
            transactions.append({
                'date': match.group(1),
                'description': f"{match.group(2)} {match.group(3)}".strip(),
                'amount': f"₹{match.group(4)}",
                'type': 'Debit'
            })
        
        return transactions
    
    # ===== GENERIC EXTRACTION METHODS =====
    
    def _extract_generic_name(self, text: str) -> str:
        patterns = [
            r'(?:Name|Cardholder)[:\s]*([A-Z][A-Z\s\.]+)',
            r'(?:Mr\.|Ms\.|Mrs\.)\s*([A-Z][A-Z\s]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                if 2 <= len(name.split()) <= 5:
                    return name
        return 'Not Found'
    
    def _extract_generic_card(self, text: str) -> str:
        patterns = [
            r'(\d{4}[\sX*]{4,}\d{4})',
            r'Card.*?(\d{4})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return 'Not Found'
    
    def _extract_generic_due_date(self, text: str) -> str:
        pattern = r'(?:Due\s*Date|Payment\s*Due)[:\s]*(\d{1,2}[\/\-][A-Za-z]{3}[\/\-]\d{2,4}|\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return 'Not Found'
    
    def _extract_generic_amount(self, text: str) -> str:
        pattern = r'(?:Total.*?Due|Amount.*?Due)[:\s]*(?:Rs\.?|₹)?\s*([\d,]+\.?\d*)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"₹{match.group(1)}"
        return 'Not Found'
    
    def _calculate_confidence(self, data: Dict) -> int:
        """Calculate confidence score based on extracted fields"""
        found_fields = 0
        total_fields = 0
        
        for key, value in data.items():
            if key == 'transactions':
                continue
            total_fields += 1
            if value and value != 'Not Found':
                found_fields += 1
        
        if total_fields == 0:
            return 0
        
        confidence = int((found_fields / total_fields) * 100)
        return confidence