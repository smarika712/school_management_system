document.addEventListener('DOMContentLoaded', function() {
    // Back to Top
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            backToTopBtn.classList.toggle('visible', window.scrollY > 300);
        });
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Auto-dismiss alerts
    document.querySelectorAll('.alert-standalone').forEach(function(alert) {
        setTimeout(function() {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        }, 5000);
    });

    // Confirm before delete
    document.querySelectorAll('[data-confirm]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) e.preventDefault();
        });
    });

    // Active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-nav .nav-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) link.classList.add('active');
    });
});