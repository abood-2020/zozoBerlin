document.addEventListener('DOMContentLoaded', function () {
    const depositOption = document.getElementById('depositOption');
    const fullPaymentOption = document.getElementById('fullPaymentOption');
    const amountToPay = document.getElementById('amountToPay');

    const totalAmount = 1000; // المبلغ الإجمالي المطلوب دفعه (تحديث هذا الرقم حسب الحاجة)

    // تحديث المبلغ عند تغيير خيار الدفع
    function updateAmount() {
        if (depositOption.checked) {
            amountToPay.value = (totalAmount * 0.3).toFixed(2); // 30% من المبلغ
        } else if (fullPaymentOption.checked) {
            amountToPay.value = totalAmount.toFixed(2); // المبلغ الكامل
        }
    }

    // إضافة مستمع للأحداث لتغيير خيار الدفع
    depositOption.addEventListener('change', updateAmount);
    fullPaymentOption.addEventListener('change', updateAmount);

    // تحديث المبلغ عند تحميل الصفحة بناءً على الخيار المحدد
    updateAmount();
});
