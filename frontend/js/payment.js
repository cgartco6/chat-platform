// Update pricing based on country
function updatePricing() {
    const country = countrySelect.value;
    let currencySymbol = '$';
    let exchangeRate = 1;
    
    if (country === 'ZA') {
        currencySymbol = 'R';
        exchangeRate = 18.5; // ZAR to USD
    } else if (country === 'AU') {
        currencySymbol = 'A$';
        exchangeRate = 1.5; // AUD to USD
    } else if (country === 'GB') {
        currencySymbol = '£';
        exchangeRate = 0.8; // GBP to USD
    } else if (country === 'DE') {
        currencySymbol = '€';
        exchangeRate = 0.9; // EUR to USD
    }
    
    creditPackages.forEach(pkg => {
        const amount = pkg.dataset.amount;
        const usdPrice = parseFloat(pkg.dataset.price);
        const localPrice = (usdPrice * exchangeRate).toFixed(2);
        
        pkg.querySelector('h3').textContent = `${amount} Credits`;
        pkg.querySelector('div:last-child').textContent = `${currencySymbol}${localPrice}`;
    });
}

// Event listeners
attachButton.addEventListener('click', () => {
    // Show payment modal when trying to attach files
    paymentModal.style.display = 'flex';
});

closeModal.addEventListener('click', () => {
    paymentModal.style.display = 'none';
});

creditPackages.forEach(pkg => {
    pkg.addEventListener('click', () => {
        creditPackages.forEach(p => p.classList.remove('selected'));
        pkg.classList.add('selected');
    });
});

paymentButton.addEventListener('click', () => {
    const selectedPackage = document.querySelector('.credit-package.selected');
    const amount = selectedPackage.dataset.amount;
    const country = countrySelect.value;
    
    alert(`Payment processed successfully! ${amount} credits added to your account. Country: ${country}`);
    paymentModal.style.display = 'none';
});

countrySelect.addEventListener('change', updatePricing);

// Initialize pricing
updatePricing();
