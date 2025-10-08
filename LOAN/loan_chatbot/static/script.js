// 추가 JavaScript 기능들

class LoanCalculator {
    constructor() {
        this.initializeEventListeners();
        this.setupFormValidation();
    }

    initializeEventListeners() {
        // 실시간 DTI 계산
        document.addEventListener('input', (e) => {
            if (['annual_income', 'monthly_debt', 'desired_amount'].includes(e.target.id)) {
                this.calculateRealTimeDTI();
            }
        });

        // 금액 입력 포맷팅
        this.setupNumberFormatting();
        
        // 툴팁 초기화
        this.initializeTooltips();
    }

    setupFormValidation() {
        const form = document.getElementById('loanForm');
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }

    validateField(field) {
        const value = field.value.replace(/,/g, '');
        let isValid = true;
        let errorMessage = '';

        switch(field.id) {
            case 'age':
                if (value < 19 || value > 65) {
                    isValid = false;
                    errorMessage = '나이는 19세 이상 65세 이하여야 합니다.';
                }
                break;
            case 'credit_score':
                if (value < 300 || value > 1000) {
                    isValid = false;
                    errorMessage = '신용점수는 300점 이상 1000점 이하여야 합니다.';
                }
                break;
            case 'annual_income':
                if (value < 10000000) {
                    isValid = false;
                    errorMessage = '연소득은 최소 1,000만원 이상이어야 합니다.';
                }
                break;
            case 'desired_amount':
                if (value < 5000000) {
                    isValid = false;
                    errorMessage = '대출금액은 최소 500만원 이상이어야 합니다.';
                }
                break;
        }

        this.displayFieldValidation(field, isValid, errorMessage);
        return isValid;
    }

    displayFieldValidation(field, isValid, errorMessage) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        if (!isValid) {
            field.classList.add('is-invalid');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error text-danger small mt-1';
            errorDiv.textContent = errorMessage;
            field.parentNode.appendChild(errorDiv);
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    calculateRealTimeDTI() {
        const annualIncome = this.getNumericValue('annual_income');
        const monthlyDebt = this.getNumericValue('monthly_debt');
        const desiredAmount = this.getNumericValue('desired_amount');

        if (annualIncome > 0 && desiredAmount > 0) {
            const monthlyIncome = annualIncome / 12;
            const estimatedRate = 5.0; // 추정 금리
            const termMonths = 60; // 5년
            
            const monthlyRate = estimatedRate / 100 / 12;
            const monthlyPayment = desiredAmount * (monthlyRate * Math.pow(1 + monthlyRate, termMonths)) / 
                                 (Math.pow(1 + monthlyRate, termMonths) - 1);
            
            const totalMonthlyDebt = monthlyDebt + monthlyPayment;
            const dti = (totalMonthlyDebt / monthlyIncome) * 100;

            this.displayRealTimeDTI(dti);
        }
    }

    displayRealTimeDTI(dti) {
        let dtiElement = document.getElementById('realTimeDTI');
        if (!dtiElement) {
            // DTI 표시 요소가 없으면 생성
            const container = document.querySelector('#loanForm');
            const dtiDiv = document.createElement('div');
            dtiDiv.className = 'alert alert-info mt-3';
            dtiDiv.innerHTML = `
                <strong>예상 DTI: </strong>
                <span id="realTimeDTI" class="fw-bold">${dti.toFixed(1)}%</span>
                <small class="d-block">실제 DTI는 대출 조건에 따라 달라질 수 있습니다.</small>
            `;
            container.appendChild(dtiDiv);
        } else {
            dtiElement.textContent = dti.toFixed(1) + '%';
            
            // DTI에 따른 색상 변경
            const alertDiv = dtiElement.closest('.alert');
            alertDiv.className = 'alert mt-3 ';
            if (dti <= 30) {
                alertDiv.className += 'alert-success';
            } else if (dti <= 40) {
                alertDiv.className += 'alert-warning';
            } else {
                alertDiv.className += 'alert-danger';
            }
        }
    }

    getNumericValue(id) {
        const element = document.getElementById(id);
        if (!element) return 0;
        const value = element.value.replace(/,/g, '');
        return parseFloat(value) || 0;
    }

    setupNumberFormatting() {
        const numberFields = ['annual_income', 'desired_amount', 'monthly_debt'];
        
        numberFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', function() {
                    let value = this.value.replace(/[^0-9]/g, '');
                    if (value) {
                        this.value = parseInt(value).toLocaleString();
                    }
                });

                field.addEventListener('focus', function() {
                    this.value = this.value.replace(/,/g, '');
                });

                field.addEventListener('blur', function() {
                    if (this.value) {
                        this.value = parseInt(this.value.replace(/,/g, '')).toLocaleString();
                    }
                });
            }
        });
    }

    initializeTooltips() {
        // Bootstrap 툴팁 초기화
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    animateResults(data) {
        // 결과 애니메이션
        const percentage = data.approval_percentage;
        const progressBar = document.getElementById('approvalProgress');
        const percentageElement = document.getElementById('approvalPercentage');
        
        // 카운터 애니메이션
        this.animateCounter(percentageElement, 0, percentage, 2000);
        
        // 프로그레스 바 애니메이션
        setTimeout(() => {
            progressBar.style.transition = 'width 2s ease-in-out';
            progressBar.style.width = percentage + '%';
        }, 500);

        // DTI 애니메이션
        const dtiElement = document.getElementById('dtiDisplay');
        this.animateCounter(dtiElement, 0, data.dti, 1500, '%');

        // 카드 fade-in 효과
        const resultCards = document.querySelectorAll('#results .card');
        resultCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 200);
        });
    }

    animateCounter(element, start, end, duration, suffix = '%') {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.round(current) + suffix;
        }, 16);
    }

    generateDetailedAnalysis(data) {
        // 상세 분석 생성
        const analysis = {
            creditAnalysis: this.analyzeCreditScore(data.credit_score),
            incomeAnalysis: this.analyzeIncome(data.annual_income),
            dtiAnalysis: this.analyzeDTI(data.dti),
            recommendations: this.generateRecommendations(data)
        };

        return analysis;
    }

    analyzeCreditScore(score) {
        if (score >= 900) return { grade: 'S', desc: '최우수 신용등급', color: 'success' };
        if (score >= 800) return { grade: 'A', desc: '우수 신용등급', color: 'success' };
        if (score >= 700) return { grade: 'B', desc: '양호 신용등급', color: 'info' };
        if (score >= 600) return { grade: 'C', desc: '보통 신용등급', color: 'warning' };
        return { grade: 'D', desc: '신용개선 필요', color: 'danger' };
    }

    analyzeIncome(income) {
        if (income >= 100000000) return { level: '고소득', desc: '대출 조건 우수', color: 'success' };
        if (income >= 50000000) return { level: '중상위소득', desc: '안정적 상환능력', color: 'info' };
        if (income >= 30000000) return { level: '중간소득', desc: '적정 상환능력', color: 'primary' };
        return { level: '중하위소득', desc: '신중한 대출 계획 필요', color: 'warning' };
    }

    analyzeDTI(dti) {
        if (dti <= 30) return { level: '우수', desc: '여유로운 상환능력', color: 'success' };
        if (dti <= 40) return { level: '적정', desc: '안정적 상환능력', color: 'info' };
        if (dti <= 50) return { level: '주의', desc: '상환부담 증가', color: 'warning' };
        return { level: '위험', desc: '상환능력 부족', color: 'danger' };
    }

    generateRecommendations(data) {
        const recommendations = [];
        
        if (data.credit_score < 700) {
            recommendations.push({
                type: '신용점수 개선',
                desc: '신용카드 사용 줄이기, 연체 방지',
                priority: 'high'
            });
        }

        if (data.dti > 40) {
            recommendations.push({
                type: 'DTI 개선',
                desc: '기존 부채 정리 또는 대출금액 조정',
                priority: 'high'
            });
        }

        if (data.annual_income < 30000000) {
            recommendations.push({
                type: '소득 증대',
                desc: '부업 또는 소득증명 방법 다양화',
                priority: 'medium'
            });
        }

        return recommendations;
    }

    exportResults(data) {
        // 결과를 PDF로 내보내기 (window.print 사용)
        const printWindow = window.open('', '_blank');
        const printContent = this.generatePrintContent(data);
        
        printWindow.document.write(printContent);
        printWindow.document.close();
        printWindow.print();
    }

    generatePrintContent(data) {
        return `
            <html>
            <head>
                <title>대출 심사 결과</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .header { text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; }
                    .result-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
                    .highlight { background: #f8f9fa; padding: 10px; border-left: 4px solid #007bff; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>AI 대출 심사 결과</h1>
                    <p>생성일: ${new Date().toLocaleDateString()}</p>
                </div>
                
                <div class="result-section">
                    <h2>심사 결과</h2>
                    <div class="highlight">
                        <p><strong>승인 가능성:</strong> ${data.approval_percentage}%</p>
                        <p><strong>DTI 비율:</strong> ${data.dti}%</p>
                    </div>
                </div>
                
                <div class="result-section">
                    <h2>AI 분석 의견</h2>
                    <p>${data.ai_explanation.replace(/\n/g, '<br>')}</p>
                </div>
                
                <div class="result-section">
                    <h2>추천 상품</h2>
                    ${data.recommended_products.map(product => `
                        <div style="margin-bottom: 15px; padding: 10px; border: 1px solid #eee;">
                            <h3>${product.name}</h3>
                            <p>${product.description}</p>
                            <p><strong>금리:</strong> ${product.interest_rate_min}% ~ ${product.interest_rate_max}%</p>
                        </div>
                    `).join('')}
                </div>
            </body>
            </html>
        `;
    }
}

// DOM 로드 완료 후 초기화
document.addEventListener('DOMContentLoaded', function() {
    const calculator = new LoanCalculator();
    
    // 전역 함수로 접근 가능하도록 설정
    window.loanCalculator = calculator;
    
    // 폼 제출 이벤트 수정
    const originalSubmitHandler = document.getElementById('loanForm').onsubmit;
    document.getElementById('loanForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // 폼 유효성 검사
        const form = e.target;
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!calculator.validateField(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            alert('입력 정보를 확인해주세요.');
            return;
        }
        
        // 기존 제출 로직 실행
        // ... (기존 코드와 동일)
        
        // 로딩 화면 표시
        document.getElementById('welcome').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('loading').style.display = 'block';
        
        // 폼 데이터 수집
        const formData = {
            age: parseInt(document.getElementById('age').value),
            annual_income: parseInt(document.getElementById('annual_income').value.replace(/,/g, '')),
            credit_score: parseInt(document.getElementById('credit_score').value),
            desired_amount: parseInt(document.getElementById('desired_amount').value.replace(/,/g, '')),
            monthly_debt: parseInt(document.getElementById('monthly_debt').value.replace(/,/g, '')) || 0,
            loan_purpose: document.getElementById('loan_purpose').value
        };
        
        try {
            const response = await fetch('/api/loan-check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // 결과 표시 (애니메이션 포함)
                displayResults(result.data);
                calculator.animateResults(result.data);
            } else {
                alert('오류가 발생했습니다: ' + result.error);
            }
        } catch (error) {
            alert('서버 통신 오류가 발생했습니다.');
            console.error('Error:', error);
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    });
});

// 유틸리티 함수들
function formatCurrency(amount) {
    return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW'
    }).format(amount);
}

function formatPercentage(value, decimals = 1) {
    return (value).toFixed(decimals) + '%';
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}