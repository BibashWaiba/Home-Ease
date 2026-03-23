const nav = document.getElementById('navbar');

/* NAVBAR SCROLL EFFECT */
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 20);
});

/* MOBILE MENU */
const ham = document.getElementById('hamburger');
const mob = document.getElementById('mobileMenu');

ham.onclick = () => mob.classList.toggle('open');

mob.querySelectorAll('a').forEach(a =>
  a.onclick = () => mob.classList.remove('open')
);

/* FADE-IN ANIMATION */
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
});

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));