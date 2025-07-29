document.addEventListener('DOMContentLoaded', function() {
    // Filtrage des projets
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Active le bouton cliqué
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const filterValue = button.getAttribute('data-filter');
            
            // Filtre les projets
            projectCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Animation au scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.skill-card, .project-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Initial state for animation
    document.querySelectorAll('.skill-card, .project-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Trigger once on load
});

// Gestion de l'expansion des cartes projets
document.querySelectorAll('.view-details').forEach(button => {
    button.addEventListener('click', (e) => {
        e.stopPropagation();
        const projectCard = e.target.closest('.project-card');
        projectCard.classList.add('expanded');
    });
});

document.querySelectorAll('.btn-close-details').forEach(button => {
    button.addEventListener('click', (e) => {
        e.stopPropagation();
        const projectCard = e.target.closest('.project-card');
        projectCard.classList.remove('expanded');
    });
});

// Fermer en cliquant à l'extérieur
document.addEventListener('click', (e) => {
    if (!e.target.closest('.project-card.expanded')) {
        document.querySelectorAll('.project-card.expanded').forEach(card => {
            card.classList.remove('expanded');
        });
    }
});

// Fermer avec la touche Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.project-card.expanded').forEach(card => {
            card.classList.remove('expanded');
        });
    }
});


// Gestion du menu burger
const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('.mobile-menu');
const mobileOverlay = document.querySelector('.mobile-overlay');

menuToggle.addEventListener('click', () => {
    document.body.classList.toggle('menu-open');
});

mobileOverlay.addEventListener('click', () => {
    document.body.classList.remove('menu-open');
});

// Fermer le menu quand on clique sur un lien
document.querySelectorAll('.mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
        document.body.classList.remove('menu-open');
    });
});