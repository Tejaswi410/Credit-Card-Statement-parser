import re
import pdfplumber
from datetime import datetime

class CreditCardParser:
    def __init__(self):
        self.providers = {
            'HDFC': self._parse_hdfc,
            'ICICI': self._parse_icici,
            'SBI': self._parse_sbi,
            'AXIS': self._parse_axis,
            'KOTAK': self._parse_kotak
        }
    
    def parse(self, filepath):
        """Main parsing method"""
        try:
            # Extracting text from PDF
            text = self._extract_text(filepath)
            
            if not text:
                return {
                    'success': False,
                    'error': 'Could not extract text from PDF'
                }
            
            # Detecting provider
            provider = self._detect_provider(text)
            
            # Parsing based on provider
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
    
    def _extract_text(self, filepath):
        """Extracting text from PDF using pdfplumber"""
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
    
    def _detect_provider(self, text):
        """Detecting credit card provider from text"""
        text_upper = text.upper()
        
        if 'HDFC BANK' in text_upper or 'HDFC' in text_upper:
            return 'HDFC'
        elif 'ICICI BANK' in text_upper or 'ICICI' in text_upper:
            return 'ICICI'
        elif 'STATE BANK' in text_upper or 'SBI CARD' in text_upper:
            return 'SBI'
        elif 'AXIS BANK' in text_upper or 'AXIS' in text_upper:
            return 'AXIS'
        elif 'KOTAK' in text_upper:
            return 'KOTAK'
        
        return 'Generic'
    
    def _parse_hdfc(self, text):
        """Parsing HDFC credit card statement"""
        return {
            'cardholder_name': self._extract_cardholder_name(text),
            'card_last_4': self._extract_card_last_4(text),
            'billing_period': self._extract_billing_period(text),
            'total_amount_due': self._extract_amount_due(text),
            'payment_due_date': self._extract_due_date(text)
        }
    
    def _parse_icici(self, text):
        """Parsing ICICI credit card statement"""
        return {
            'cardholder_name': self._extract_cardholder_name(text),
            'card_last_4': self._extract_card_last_4(text),
            'billing_period': self._extract_billing_period(text),
            'total_amount_due': self._extract_amount_due(text),
            'payment_due_date': self._extract_due_date(text)
        }
    
    def _parse_sbi(self, text):
        """Parsing SBI credit card statement"""
        return {
            'cardholder_name': self._extract_cardholder_name(text),
            'card_last_4': self._extract_card_last_4(text),
            'billing_period': self._extract_billing_period(text),
            'total_amount_due': self._extract_amount_due(text),
            'payment_due_date': self._extract_due_date(text)
        }
    
    def _parse_axis(self, text):
        """Parsing Axis credit card statement"""
        return {
            'cardholder_name': self._extract_cardholder_name(text),
            'card_last_4': self._extract_card_last_4(text),
            'billing_period': self._extract_billing_period(text),
            'total_amount_due': self._extract_amount_due(text),
            'payment_due_date': self._extract_due_date(text)
        }
    
    def _parse_kotak(self, text):
        """Parsing Kotak credit card statement"""
        return {
            'cardholder_name': self._extract_cardholder_name(text),
            'card_last_4': self._extract_card_last_4(text),
            'billing_period': self._extract_billing_period(text),
            'total_amount_due': self._extract_amount_due(text),
            'payment_due_date': self._extract_due_date(text)
        }
    
    def _parse_generic(self, text):
        """providing generic parser for unknown providers"""
        return {
            'cardholder_name': self._extract_cardholder_name(text),
            'card_last_4': self._extract_card_last_4(text),
            'billing_period': self._extract_billing_period(text),
            'total_amount_due': self._extract_amount_due(text),
            'payment_due_date': self._extract_due_date(text)
        }
    
    # ===== THESE ARE FIELD EXTRACTION METHODS =====
    
    def _extract_cardholder_name(self, text):
        """Extracting cardholder name"""
        def _clean_candidate_name(raw: str) -> str:
            name = raw.strip()
            # Removing text after commas or slashes that often start addresses or clauses
            name = re.split(r'[,/\n]', name)[0]
            # Removing specific nuisance phrases
            name = re.sub(r'\b(Name\s*of\s*Nominee.*?)$', '', name, flags=re.IGNORECASE).strip()
            name = re.sub(r'\b(of\s+nominee|nominee|for\s+lost\s+or\s+stolen\s+card|customer\s*care|helpline)\b.*$', '', name, flags=re.IGNORECASE).strip()
            # Collapse spaces
            name = re.sub(r'\s+', ' ', name)
            # Keeping only alphabet, dot and space
            name = re.sub(r'[^A-Za-z\.\s]', '', name).strip()
            # Filtering out lines that still contain generic words
            if re.search(r'\b(ACCOUNT|STATEMENT|SUMMARY|AMOUNT|DUE|DATE|BILL|PERIOD|CYCLE|ADDRESS|NOMINEE)\b', name, flags=re.IGNORECASE):
                return ''
            # Prefer 2-5 words
            tokens = [t for t in name.split(' ') if t]
            if len(tokens) < 2 or len(tokens) > 5:
                return ''
            # Title case tokens with dots preserved (e.g., A. B. NAME)
            def tc(tok: str) -> str:
                if '.' in tok and len(tok) <= 3:
                    return tok.upper()
                return tok.capitalize()
            name = ' '.join(tc(t) for t in tokens)
            return name if 3 < len(name) < 50 else ''

        # 1) Line-by-line scan for strong labels, excluding nominee lines
        labels = [
            r'Cardmember\s*Name', r'Card\s*Member\s*Name', r'Customer\s*Name',
            r'Cardholder', r'Card\s*Holder', r'Name\s*:\s*'
        ]
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in lines:
            if re.search(r'Nominee', ln, re.IGNORECASE):
                continue
            for lb in labels:
                m = re.search(rf'(?:{lb})[:\s]*([A-Z][A-Z\s\.-]{{3,}})$', ln, re.IGNORECASE)
                if m:
                    candidate = _clean_candidate_name(m.group(1))
                    if candidate:
                        return candidate

        # 2) "Dear NAME," style greetings
        m = re.search(r'Dear\s+(?:Mr\.?|Ms\.?|Mrs\.?|Mx\.?)?\s*([A-Z][A-Z\s\.-]+?)(?:,|\n)', text, re.IGNORECASE)
        if m:
            candidate = _clean_candidate_name(m.group(1))
            if candidate:
                return candidate

        # 3) Fallback regex patterns from the entire text
        patterns = [
            r'(?:Cardmember\s*Name|Card\s*Member\s*Name|Customer\s*Name|Cardholder|Card\s*Holder|Name)[:\s]+([A-Z][A-Z\s\.]+)',
            r'(?:Mr\.?|Ms\.?|Mrs\.?|Mx\.?)\s*([A-Z][A-Z\s]+)',
            r'(?:Attention|Attn\.|To)[:\s]+([A-Z][A-Z\s\.]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                candidate = _clean_candidate_name(match.group(1))
                if candidate:
                    return candidate

        return 'Not Found'
    
    def _extract_card_last_4(self, text):
        """Extracting last 4 digits of card number"""
        # Include common mask symbols used in PDFs and OCR (e.g bullets)
        masked = r'(?:X|x|\*|•|●|■|◼︎)'
        sep = r'[\s\-]+'
        patterns = [
            # Labelled masked number
            rf'(?:Card\s*Number|Card\s*No\.?|Account\s*Number)[:\s]*{masked}{{4,}}(?:{sep}?{masked}{{4,}}){{2,3}}{sep}?(\d{{4}})',
            # Generic masked groups like XXXX-XXXX-XXXX-1234 or **** **** **** 1234
            rf'{masked}{{4}}(?:{sep}?{masked}{{4}}){{2,3}}{sep}?(\d{{4}})',
            # Unmasked grouped 16-digit numbers
            r'(?:\b\d{4}[\s\-]?){3}(\d{4})\b',
            # Phrases like 'ending 1234' or 'ends with 1234'
            r'(?:ending|ending\s*in|ends\s*with)[:\s]*(\d{4})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Trying to find any 16-digit number (credit card format)
        match = re.search(r'(?:\b\d{4}\s+){3}(\d{4})\b', text)
        if match:
            return match.group(1)
        
        return 'Not Found'
    
    def _extract_billing_period(self, text):
        """Extracting billing period or statement cycle"""
        patterns = [
            # Month name formats: Jan 1, 2023 to Jan 31, 2023
            r'(?:Statement\s*Period|Billing\s*Period|Statement\s*Cycle|Cycle|Period)[:\s]*([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4})\s*(?:to|-|through)\s*([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4})',
            # Numeric with slashes or dashes: 01/01/2023 - 31/01/2023
            r'(?:From|Period|Cycle)[:\s]*(\d{1,2}[\/-]\d{1,2}[\/-]\d{2,4})\s*(?:to|To|-|through)\s*(\d{1,2}[\/-]\d{1,2}[\/-]\d{2,4})',
            # Using dots: 01.01.2023 to 31.01.2023
            r'(\d{1,2}[\.\s][A-Za-z]{3,9}[\.\s]?\s*\d{2,4})\s*(?:to|-|through)\s*(\d{1,2}[\.\s][A-Za-z]{3,9}[\.\s]?\s*\d{2,4})',
            # Day Month Year words: 1 Jan 2023 - 31 Jan 2023
            r'(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})\s*(?:to|-|through)\s*(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start_date = match.group(1)
                end_date = match.group(2)
                return f"{start_date} - {end_date}"
        
        return 'Not Found'
    
    def _extract_amount_due(self, text):
        """Extracting total amount due"""
        # Capture money with optional currency symbol or text and possible '/-'
        currency = r'(?:Rs\.?|INR|₹|Rupees)?'
        amount_core = r'([\d]{1,3}(?:,[\d]{2,3})*(?:\.\d{1,2})?|[\d]+(?:\.\d{1,2})?)'
        tail = r'(?:\s*/-)?'
        money = rf'(?:{currency}\s*)?{amount_core}{tail}'
        # Labels often used across providers
        labels_total_due = r'(?:Total\s*Amount\s*Due|Total\s*Amt\.?\s*Due|Total\s*Due|Total\s*Dues|Amount\s*Payable\s*(?:by\s*Due\s*Date)?|Amount\s*Payable|Amount\s*to\s*be\s*Paid|Net\s*Amount\s*Payable)'
        labels_balance = r'(?:Current\s*Balance|Outstanding\s*Amount|Total\s*Outstanding|Closing\s*Balance)'
        labels_min_due = r'(?:Minimum\s*Amount\s*Due|Min\.?\s*Due|Minimum\s*Due)'
        patterns = [
            rf'{labels_total_due}[:\s]*{money}',
            rf'{labels_balance}[:\s]*{money}',
            rf'{labels_min_due}[:\s]*{money}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Find the first captured amount group by scanning groups backwards (to skip label match groups)
                amount = None
                for g in match.groups()[::-1]:
                    if g and re.match(r'^\d', g):
                        amount = g
                        break
                if amount:
                    # Normalize thousand separators like 1,23,456.78 as-is
                    return f"₹{amount}"
        
        return 'Not Found'
    
    def _extract_due_date(self, text):
        """Extracting payment due date"""
        # Allow ordinal suffixes and various separators
        day = r'\d{1,2}(?:st|nd|rd|th)?'
        month_name = r'[A-Za-z]{3,9}'
        year = r'\d{2,4}|XX|xx'  # Include XX/xx for sample statements
        date_wordy = rf'{day}\s+{month_name}\s+{year}'
        date_wordy_monthfirst = rf'{month_name}\s+{day},?\s+{year}'
        date_numeric = r'\d{1,2}[\/-]\d{1,2}[\/-](?:\d{2,4}|XX|xx)'  # Include XX/xx
        date_dot = r'\d{1,2}\.\d{1,2}\.(?:\d{2,4}|XX|xx)'  # Include XX/xx

        labels = r'(?:Payment\s*Due\s*Date|Payment\s*Due|Due\s*Date|Due\s*Dt\.?|Pay\s*by|Pay\s*on|Due\s*on|Due\s*by|Last\s*date\s*of\s*payment|On\s*or\s*before)'

        patterns = [
            rf'{labels}[:\s]*({date_wordy_monthfirst})',
            rf'{labels}[:\s]*({date_wordy})',
            rf'{labels}[:\s]*({date_numeric})',
            rf'{labels}[:\s]*({date_dot})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return 'Not Found'
    
    def _calculate_confidence(self, data):
        """Calculating confidence score based on extracted fields"""
        found_fields = sum(1 for value in data.values() if value != 'Not Found')
        total_fields = len(data)
        confidence = int((found_fields / total_fields) * 100)
        return confidence