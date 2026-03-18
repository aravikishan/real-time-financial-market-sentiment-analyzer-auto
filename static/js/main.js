document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Form validation
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const input = form.querySelector('input[name="stock_symbol"]');
        if (!input.value.trim()) {
            event.preventDefault();
            alert('Please enter a stock symbol.');
        }
    });

    // Dynamic content loading
    async function loadSentiment(stockSymbol) {
        try {
            const response = await fetch(`/api/sentiment/${stockSymbol}`);
            if (!response.ok) throw new Error('Stock symbol not found');
            const data = await response.json();
            console.log(data);
            // Render data in the UI
        } catch (error) {
            console.error(error);
            alert('Error loading sentiment data.');
        }
    }

    // Example usage
    // loadSentiment('AAPL');
});