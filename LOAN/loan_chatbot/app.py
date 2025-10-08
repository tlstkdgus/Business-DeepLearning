from flask import Flask, render_template, request, jsonify
import json
import os
import yaml
import google.generativeai as genai
from typing import Dict, List, Any
import re

app = Flask(__name__)

# 설정 파일 로드
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"설정 파일 로드 오류: {e}")
        return {}

config = load_config()

# Gemini AI 설정
try:
    api_key = config.get('gemini', {}).get('api_key', '')
    model_name = config.get('gemini', {}).get('model', 'gemini-pro')
    
    if api_key and api_key != "your-api-key-here":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        print(f"Gemini AI 모델 '{model_name}' 설정 완료")
    else:
        model = None
        print("데모 모드로 실행 중 (API 키 없음)")
except Exception as e:
    print(f"Gemini AI 설정 오류: {e}")
    model = None

class LoanRAGSystem:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.knowledge_base = self.load_knowledge_base()
    
    def load_knowledge_base(self) -> Dict[str, Any]:
        """모든 JSON 파일을 로드하여 지식베이스 구축"""
        knowledge = {}
        
        files = [
            'loan_regulations.json',
            'loan_products.json', 
            'credit_scoring.json',
            'interest_rates.json',
            'risk_factors.json'
        ]
        
        for file in files:
            file_path = os.path.join(self.data_path, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        key = file.replace('.json', '')
                        knowledge[key] = data
                        print(f"✅ {file} 로드 완료 - {len(data.get(list(data.keys())[0], []))}개 항목")
                except Exception as e:
                    print(f"❌ {file} 로드 실패: {e}")
            else:
                print(f"❌ {file} 파일이 존재하지 않습니다: {file_path}")
        
        print(f"📊 총 {len(knowledge)}개 지식베이스 로드 완료")
        return knowledge
    
    def calculate_dti(self, annual_income: int, monthly_debt: int = 0, loan_amount: int = 0, 
                     loan_term_months: int = 60, interest_rate: float = 5.0) -> float:
        """DTI(총부채원리금상환비율) 계산"""
        if annual_income <= 0:
            return 0
        
        monthly_income = annual_income / 12
        
        # 신규 대출의 월 상환금 계산 (원리금균등상환)
        if loan_amount > 0:
            monthly_rate = interest_rate / 100 / 12
            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** loan_term_months) / \
                                ((1 + monthly_rate) ** loan_term_months - 1)
            else:
                monthly_payment = loan_amount / loan_term_months
        else:
            monthly_payment = 0
        
        total_monthly_debt = monthly_debt + monthly_payment
        dti = (total_monthly_debt / monthly_income) * 100
        
        return round(dti, 2)
    
    def search_relevant_content(self, user_input: str, user_info: Dict) -> Dict[str, List]:
        """사용자 입력과 정보를 바탕으로 관련 콘텐츠 검색"""
        relevant_content = {
            'regulations': [],
            'products': [],
            'scoring': [],
            'rates': [],
            'risks': []
        }
        
        # 키워드 추출
        keywords = self.extract_keywords(user_input, user_info)
        
        # 각 지식베이스에서 관련 콘텐츠 검색
        for category, data in self.knowledge_base.items():
            if category == 'loan_regulations':
                relevant_content['regulations'] = self.search_regulations(keywords, user_info)
            elif category == 'loan_products':
                relevant_content['products'] = self.search_products(keywords, user_info)
            elif category == 'credit_scoring':
                relevant_content['scoring'] = self.search_scoring(keywords, user_info)
            elif category == 'interest_rates':
                relevant_content['rates'] = self.search_rates(keywords, user_info)
            elif category == 'risk_factors':
                relevant_content['risks'] = self.search_risks(keywords, user_info)
        
        return relevant_content
    
    def extract_keywords(self, user_input: str, user_info: Dict) -> List[str]:
        """사용자 입력과 정보에서 키워드 추출"""
        keywords = []
        
        # 사용자 입력에서 키워드 추출
        input_keywords = re.findall(r'\\b[가-힣]{2,}\\b', user_input)
        keywords.extend(input_keywords)
        
        # 사용자 정보 기반 키워드 추가
        age = user_info.get('age', 0)
        if age < 35:
            keywords.append('청년')
        elif age >= 55:
            keywords.append('시니어')
        
        credit_score = user_info.get('credit_score', 0)
        if credit_score >= 800:
            keywords.extend(['프리미엄', '우대'])
        elif credit_score < 600:
            keywords.extend(['위험', '보증'])
        
        return keywords
    
    def search_regulations(self, keywords: List[str], user_info: Dict) -> List[Dict]:
        """규정 검색"""
        regulations = self.knowledge_base.get('loan_regulations', {}).get('regulations', [])
        relevant = []
        
        for reg in regulations:
            # DTI, LTV, DSR 관련 규정 우선 선택
            if any(keyword in reg.get('content', '') for keyword in ['DTI', 'LTV', 'DSR']):
                relevant.append(reg)
            # 연령, 소득 관련 규정
            elif any(keyword in reg.get('content', '') for keyword in ['연령', '소득', '신용점수']):
                relevant.append(reg)
        
        return relevant[:5]  # 상위 5개만 반환
    
    def search_products(self, keywords: List[str], user_info: Dict) -> List[Dict]:
        """상품 검색 - 더 유연한 매칭 로직"""
        products = self.knowledge_base.get('loan_products', {}).get('products', [])
        suitable_products = []
        
        age = user_info.get('age', 0)
        income = user_info.get('annual_income', 0)
        credit_score = user_info.get('credit_score', 0)
        loan_amount = user_info.get('desired_amount', 0)
        
        for product in products:
            score = 0  # 매칭 점수
            reasons = []
            
            # 신용점수 조건 확인
            min_credit = product.get('min_credit_score', 0)
            if credit_score >= min_credit:
                score += 30
                if credit_score >= 800 and '프리미엄' in product.get('name', ''):
                    score += 20
                    reasons.append('프리미엄 고객 대상')
            elif credit_score >= min_credit - 50:  # 50점 정도 부족해도 고려
                score += 15
                reasons.append('신용점수 개선 시 가능')
            
            # 소득 조건 확인
            min_income = product.get('min_income', 0)
            if income >= min_income:
                score += 25
            elif income >= min_income * 0.8:  # 80% 이상이면 고려
                score += 15
                reasons.append('소득 조건 근접')
            
            # 대출금액 조건 확인
            min_amount = product.get('min_amount', 0)
            max_amount = product.get('max_amount', float('inf'))
            if min_amount <= loan_amount <= max_amount:
                score += 25
            elif loan_amount > max_amount:
                # 요청 금액이 한도를 초과하는 경우
                score += 10
                reasons.append(f'최대 {max_amount:,}원까지 가능')
            elif loan_amount < min_amount:
                # 요청 금액이 최소 금액보다 적은 경우
                score += 15
                reasons.append(f'최소 {min_amount:,}원부터 가능')
            
            # 연령 특별 조건
            if age < 35 and '청년' in product.get('name', ''):
                score += 20
                reasons.append('청년 우대 상품')
            elif age >= 55 and '시니어' in product.get('name', ''):
                score += 20
                reasons.append('시니어 전용 상품')
            
            # 직업별 특별 상품 (기본적으로 모든 직업에 적용 가능하다고 가정)
            if any(job in product.get('name', '') for job in ['직장인', '공무원', '교사']):
                score += 10
            
            # 점수가 40점 이상인 상품만 추천
            if score >= 40:
                match_reason = reasons[0] if reasons else '기본 자격 조건 충족'
                suitable_products.append({
                    **product, 
                    'match_score': score,
                    'match_reason': match_reason,
                    'all_reasons': reasons
                })
        
        # 점수 순으로 정렬하여 상위 5개 반환
        suitable_products.sort(key=lambda x: x['match_score'], reverse=True)
        return suitable_products[:5]
    
    def search_scoring(self, keywords: List[str], user_info: Dict) -> List[Dict]:
        """신용평가 기준 검색"""
        scoring = self.knowledge_base.get('credit_scoring', {}).get('scoring_criteria', [])
        relevant = []
        
        for criteria in scoring:
            category = criteria.get('category', '')
            if any(keyword in category for keyword in ['신용점수', '소득', '연령', '고용']):
                relevant.append(criteria)
        
        return relevant[:3]  # 상위 3개만 반환
    
    def search_rates(self, keywords: List[str], user_info: Dict) -> List[Dict]:
        """금리 정보 검색"""
        rates = self.knowledge_base.get('interest_rates', {}).get('interest_rates', [])
        relevant = []
        
        credit_score = user_info.get('credit_score', 0)
        age = user_info.get('age', 0)
        
        for rate in rates:
            category = rate.get('category', '')
            # 신용점수에 따른 금리 정보
            if credit_score >= 800 and '우대' in category:
                relevant.append(rate)
            elif age < 35 and '청년' in category:
                relevant.append(rate)
            elif category in ['기준금리', '변동금리', '고정금리']:
                relevant.append(rate)
        
        return relevant[:3]  # 상위 3개만 반환
    
    def search_risks(self, keywords: List[str], user_info: Dict) -> List[Dict]:
        """리스크 요인 검색"""
        risks = self.knowledge_base.get('risk_factors', {}).get('risk_factors', [])
        relevant = []
        
        credit_score = user_info.get('credit_score', 0)
        age = user_info.get('age', 0)
        income = user_info.get('annual_income', 0)
        
        for risk in risks:
            category = risk.get('category', '')
            # 사용자 상황에 맞는 리스크 요인 선택
            if credit_score < 700 and '신용' in category:
                relevant.append(risk)
            elif income < 30000000 and '소득' in category:
                relevant.append(risk)
            elif age >= 55 and '고용' in category:
                relevant.append(risk)
            elif category in ['시장 리스크', '경제 리스크']:
                relevant.append(risk)
        
        return relevant[:3]  # 상위 3개만 반환
    
    def generate_ai_response(self, user_info: Dict, relevant_content: Dict, dti: float) -> Dict:
        """Gemini AI를 사용하여 대출 승인 가능성 및 추천 생성"""
        
        # 프롬프트 구성
        prompt = f"""
        당신은 전문적인 대출 심사 AI입니다. 다음 고객 정보와 관련 규정을 바탕으로 대출 승인 가능성을 분석하고 조언해주세요.

        ## 고객 정보
        - 나이: {user_info.get('age', 0)}세
        - 연소득: {user_info.get('annual_income', 0):,}원
        - 신용점수: {user_info.get('credit_score', 0)}점
        - 희망 대출금액: {user_info.get('desired_amount', 0):,}원
        - 계산된 DTI: {dti}%

        ## 관련 규정 정보
        {self.format_content_for_prompt(relevant_content)}

        다음 마크다운 형식으로 응답해주세요:
        
        ## 대출 심사 결과 분석
        **승인 가능성: XX%**
        
        (승인 가능성 분석 내용을 ✅🟡⚠️❌ 이모지와 함께 작성)
        
        ## DTI(총부채원리금상환비율) 분석
        **계산된 DTI: {dti}%**
        
        (DTI 분석 내용)
        
        ## 신용점수 분석
        **현재 신용점수: {user_info.get('credit_score', 0)}점**
        
        (신용점수 분석 내용)
        
        ## 맞춤형 조언
        - 🎯 (조언 1)
        - 💰 (조언 2)
        - 📊 (조언 3)
        
        ## 다음 단계
        1. (단계 1)
        2. (단계 2)
        3. (단계 3)
        
        응답은 친근하면서도 전문적인 톤으로 작성하고, 적절한 이모지를 사용해주세요.
        """
        
        try:
            # 실제 API 키가 있는 경우에만 AI 호출
            if model is not None:
                response = model.generate_content(prompt)
                ai_analysis = response.text
            else:
                # 백업 모드 - 기본 응답 생성
                ai_analysis = self.generate_demo_response(user_info, dti)
            
            # 승인 가능성 퍼센테지 추출
            approval_percentage = self.extract_approval_percentage(ai_analysis, user_info, dti)
            
            return {
                'approval_percentage': approval_percentage,
                'dti': dti,
                'ai_explanation': ai_analysis,
                'recommended_products': relevant_content.get('products', [])[:3]
            }
        
        except Exception as e:
            print(f"AI 생성 오류: {e}")
            # AI 응답 실패 시 기본 분석 제공
            return self.generate_fallback_response(user_info, dti, relevant_content)
    
    def extract_approval_percentage(self, ai_text: str, user_info: Dict, dti: float) -> int:
        """AI 응답에서 승인 가능성 퍼센테지 추출 또는 계산"""
        # AI 응답에서 퍼센테지 패턴 찾기
        percentage_match = re.search(r'(\\d+)%', ai_text)
        if percentage_match:
            return int(percentage_match.group(1))
        
        # 기본 계산 로직
        base_score = 50
        
        # 신용점수 점수
        credit_score = user_info.get('credit_score', 0)
        if credit_score >= 800:
            base_score += 30
        elif credit_score >= 700:
            base_score += 20
        elif credit_score >= 600:
            base_score += 10
        else:
            base_score -= 20
        
        # DTI 점수
        if dti <= 30:
            base_score += 15
        elif dti <= 40:
            base_score += 5
        elif dti <= 50:
            base_score -= 5
        else:
            base_score -= 20
        
        # 소득 점수
        income = user_info.get('annual_income', 0)
        if income >= 50000000:
            base_score += 10
        elif income >= 30000000:
            base_score += 5
        elif income < 20000000:
            base_score -= 10
        
        return max(0, min(100, base_score))
    
    def generate_demo_response(self, user_info: Dict, dti: float) -> str:
        """데모 모드용 AI 응답 생성"""
        approval = self.extract_approval_percentage("", user_info, dti)
        credit_score = user_info.get('credit_score', 0)
        income = user_info.get('annual_income', 0)
        age = user_info.get('age', 0)
        amount = user_info.get('desired_amount', 0)
        
        analysis_parts = []
        
        # 승인 가능성 분석
        analysis_parts.append(f"## 대출 심사 결과 분석\n\n**승인 가능성: {approval}%**\n")
        
        if approval >= 80:
            analysis_parts.append("✅ **승인 가능성이 매우 높습니다!**\n")
            analysis_parts.append("고객님의 신용상태와 소득조건이 우수하여 대출 승인이 원활할 것으로 예상됩니다.\n")
        elif approval >= 60:
            analysis_parts.append("🟡 **승인 가능성이 양호합니다.**\n")
            analysis_parts.append("전반적인 조건이 적절하나, 일부 개선사항이 있을 수 있습니다.\n")
        elif approval >= 40:
            analysis_parts.append("⚠️ **승인 가능성이 보통입니다.**\n")
            analysis_parts.append("추가 서류나 조건 개선이 필요할 수 있습니다.\n")
        else:
            analysis_parts.append("❌ **승인이 어려울 수 있습니다.**\n")
            analysis_parts.append("신용점수나 소득조건 개선 후 재신청을 권장합니다.\n")
        
        # DTI 분석
        analysis_parts.append(f"\n## DTI(총부채원리금상환비율) 분석\n\n**계산된 DTI: {dti}%**\n")
        
        if dti <= 30:
            analysis_parts.append("✅ **DTI가 매우 양호합니다.** 추가 대출 여력이 충분합니다.\n")
        elif dti <= 40:
            analysis_parts.append("🟡 **DTI가 적정 범위입니다.** 안정적인 상환이 가능할 것으로 보입니다.\n")
        elif dti <= 50:
            analysis_parts.append("⚠️ **DTI가 다소 높습니다.** 상환 부담을 신중히 고려해주세요.\n")
        else:
            analysis_parts.append("❌ **DTI가 위험 수준입니다.** 대출금액 조정이나 기존 부채 정리를 권장합니다.\n")
        
        # 신용점수 분석
        analysis_parts.append(f"\n## 신용점수 분석\n\n**현재 신용점수: {credit_score}점**\n")
        
        if credit_score >= 800:
            analysis_parts.append("✨ **최우수 신용등급**으로 최저금리 혜택을 받을 수 있습니다.\n")
        elif credit_score >= 700:
            analysis_parts.append("✅ **우수한 신용등급**으로 우대금리 적용이 가능합니다.\n")
        elif credit_score >= 600:
            analysis_parts.append("🟡 **보통 신용등급**으로 일반 조건으로 대출이 가능합니다.\n")
        else:
            analysis_parts.append("⚠️ **신용점수 개선이 필요합니다.** 신용관리 후 재신청을 권장합니다.\n")
        
        # 맞춤형 조언
        analysis_parts.append("\n## 맞춤형 조언\n")
        
        if age < 35:
            analysis_parts.append("- 🎯 **청년 우대 상품**을 적극 활용하세요.\n")
        
        if income >= 50000000:
            analysis_parts.append("- 💰 **고소득자 전용 상품**을 고려해보세요.\n")
        
        if dti > 40:
            analysis_parts.append("- 📊 **DTI 개선**을 위해 기존 부채 정리를 우선 고려하세요.\n")
        
        if credit_score < 700:
            analysis_parts.append("- 📈 **신용점수 향상**을 위해 연체 방지와 신용카드 사용률을 줄이세요.\n")
        
        analysis_parts.append("\n## 다음 단계\n")
        analysis_parts.append("1. 관심 상품의 상세 조건을 확인하세요.\n")
        analysis_parts.append("2. 필요 서류를 미리 준비하세요.\n")
        analysis_parts.append("3. 영업점 방문 또는 온라인으로 정식 신청하세요.\n")
        analysis_parts.append("\n⚠️ **주의**: 이 결과는 AI 기반 예상 분석이며, 실제 심사 결과와 다를 수 있습니다.")
        
        return "\n".join(analysis_parts)
    
    def format_content_for_prompt(self, content: Dict) -> str:
        """프롬프트용 콘텐츠 포매팅"""
        formatted = []
        
        for category, items in content.items():
            if items:
                formatted.append(f"### {category.upper()}")
                for item in items[:3]:  # 각 카테고리당 최대 3개
                    if isinstance(item, dict):
                        title = item.get('title', item.get('name', ''))
                        description = item.get('description', item.get('content', ''))
                        formatted.append(f"- {title}: {description}")
        
        return "\\n".join(formatted)
    
    def generate_fallback_response(self, user_info: Dict, dti: float, relevant_content: Dict) -> Dict:
        """AI 응답 실패 시 기본 응답 생성"""
        approval = self.extract_approval_percentage("", user_info, dti)
        
        explanation = f"""
        ## 대출 심사 결과

        **승인 가능성: {approval}%**

        ### DTI 분석
        계산된 DTI는 {dti}%입니다.
        {'적정 수준입니다.' if dti <= 40 else 'DTI가 높아 대출 승인에 불리할 수 있습니다.'}

        ### 권장사항
        - 신용점수: {user_info.get('credit_score', 0)}점
        - {'우수한 신용등급입니다.' if user_info.get('credit_score', 0) >= 700 else '신용점수 개선이 필요합니다.'}
        - 정기적인 소득 증빙이 중요합니다.

        더 자세한 상담은 영업점에 문의하시기 바랍니다.
        """
        
        return {
            'approval_percentage': approval,
            'dti': dti,
            'ai_explanation': explanation,
            'recommended_products': relevant_content.get('products', [])[:3]
        }

# RAG 시스템 초기화
rag_system = LoanRAGSystem()

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/loan-check', methods=['POST'])
def loan_check():
    """대출 심사 API"""
    try:
        data = request.get_json()
        
        # 사용자 정보 추출
        user_info = {
            'age': int(data.get('age', 0)),
            'annual_income': int(data.get('annual_income', 0)),
            'credit_score': int(data.get('credit_score', 0)),
            'desired_amount': int(data.get('desired_amount', 0)),
            'monthly_debt': int(data.get('monthly_debt', 0)),
            'loan_purpose': data.get('loan_purpose', '생활자금')
        }
        
        # DTI 계산
        dti = rag_system.calculate_dti(
            annual_income=user_info['annual_income'],
            monthly_debt=user_info['monthly_debt'],
            loan_amount=user_info['desired_amount']
        )
        
        # 관련 콘텐츠 검색
        user_input = f"나이 {user_info['age']}세, 연소득 {user_info['annual_income']:,}원, 신용점수 {user_info['credit_score']}점으로 {user_info['desired_amount']:,}원 대출을 받고 싶습니다."
        relevant_content = rag_system.search_relevant_content(user_input, user_info)
        
        # AI 분석 생성
        result = rag_system.generate_ai_response(user_info, relevant_content, dti)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)