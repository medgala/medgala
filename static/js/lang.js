const translations = {
  en: {
    nav: { home: "Home", contact: "Contact" },
    hero: {
      subtitle: "A gala for medical students from the universities of Milan",
      tagline: "Where Medicine Meets Fashion",
      cta: "Tickets Coming Soon",
    },
    about: {
      label: "About the Event",
      heading1: "The First",
      heading3: "Milano",
      text: "MED GALA Milano is the first inter-university gala bringing together medical students from Milan in an elegant and exclusive night.",
    },
    universities: {
      label: "Participating",
      heading: "Universities",
    },
    highlights: {
      label: "What Awaits You",
      heading: "Event Highlights",
      items: ["Networking", "Red Carpet", "Professional Photos", "Elegant Evening"],
    },
    eventInfo: {
      label: "Details",
      heading: "Event Information",
      details: [
        { label: "Location", value: "Milan" },
        { label: "Date", value: "June 2026" },
        { label: "Dress Code", value: "Black Tie" },
      ],
    },
    cta: {
      heading2: "MED GALA",
      subtext: "Be part of an unforgettable night of elegance, connection, and celebration.",
      btn: "Get Updates",
      join: "Join the First",
    },
    contact: {
      label: "Get in Touch",
      heading: "Contact & Partnerships",
      intro: "For sponsorships, partnerships, and business inquiries, please contact us.",
      sections: [
        { title: "Sponsors", desc: "Partner with the premier medical student gala in Milan." },
        { title: "Collaborations", desc: "Join forces for an unforgettable event experience." },
        { title: "Business & Media", desc: "Press inquiries, media coverage, and business proposals." },
      ],
      formTitle: "Send Us a Message",
      name: "Name",
      email: "Email",
      message: "Message",
      namePlaceholder: "Your name",
      emailPlaceholder: "your@email.com",
      messagePlaceholder: "Tell us about your inquiry...",
      send: "Send Message",
      sending: "Sending...",
      successMsg: "Message sent! We'll get back to you soon.",
      errorMsg: "Please fill in all fields.",
    },
    footer: { rights: "All rights reserved." },
  },
  it: {
    nav: { home: "Home", contact: "Contatti" },
    hero: {
      subtitle: "Un gala per gli studenti di medicina delle università di Milano",
      tagline: "Dove la Medicina Incontra la Moda",
      cta: "Biglietti in Arrivo",
    },
    about: {
      label: "L'Evento",
      heading1: "Il Primo",
      heading3: "Milano",
      text: "MED GALA Milano è il primo gala inter-universitario che riunisce gli studenti di medicina di Milano in una serata elegante ed esclusiva.",
    },
    universities: {
      label: "Partecipanti",
      heading: "Università",
    },
    highlights: {
      label: "Cosa Ti Aspetta",
      heading: "Highlights dell'Evento",
      items: ["Networking", "Red Carpet", "Foto Professionali", "Serata Elegante"],
    },
    eventInfo: {
      label: "Dettagli",
      heading: "Informazioni sull'Evento",
      details: [
        { label: "Luogo", value: "Milano" },
        { label: "Data", value: "Giugno 2026" },
        { label: "Dress Code", value: "Black Tie" },
      ],
    },
    cta: {
      heading2: "MED GALA",
      subtext: "Fai parte di una notte indimenticabile all'insegna dell'eleganza, della connessione e della celebrazione.",
      btn: "Ricevi Aggiornamenti",
      join: "Partecipa al Primo",
    },
    contact: {
      label: "Contattaci",
      heading: "Contatti & Partnership",
      intro: "Per sponsorizzazioni, partnership e richieste commerciali, contattaci.",
      sections: [
        { title: "Sponsor", desc: "Diventa partner del principale gala per studenti di medicina di Milano." },
        { title: "Collaborazioni", desc: "Unisci le forze per un'esperienza evento indimenticabile." },
        { title: "Business & Media", desc: "Richieste stampa, copertura media e proposte commerciali." },
      ],
      formTitle: "Inviaci un Messaggio",
      name: "Nome",
      email: "Email",
      message: "Messaggio",
      namePlaceholder: "Il tuo nome",
      emailPlaceholder: "tua@email.com",
      messagePlaceholder: "Raccontaci della tua richiesta...",
      send: "Invia Messaggio",
      sending: "Invio in corso...",
      successMsg: "Messaggio inviato! Ti risponderemo presto.",
      errorMsg: "Compila tutti i campi.",
    },
    footer: { rights: "Tutti i diritti riservati." },
  },
};

let currentLanguage = localStorage.getItem("medgala_lang") || "it";

function setLanguage(l){
  currentLanguage = l;
  localStorage.setItem("medgala_lang", l);
  applyLanguage();
  updateButtons();
}

function updateButtons(){
  document.querySelectorAll(".lang-btn").forEach(btn => {
    if(btn.dataset.lang === currentLanguage){
      btn.classList.add("lang-active");
    } else {
      btn.classList.remove("lang-active");
    }
  });
}

function applyCommon(){
  const tr = translations[currentLanguage];
  document.querySelectorAll('[data-i18n="nav.home"]').forEach(el => el.textContent = tr.nav.home);
  document.querySelectorAll('[data-i18n="nav.contact"]').forEach(el => el.textContent = tr.nav.contact);
  const footerRights = document.getElementById("footerRights");
  if(footerRights) footerRights.textContent = tr.footer.rights;
}

function applyHome(){
  const tr = translations[currentLanguage];
  const ids = {
    heroSubtitle: tr.hero.subtitle,
    heroTagline: tr.hero.tagline,
    heroCta: tr.hero.cta,
    aboutLabel: tr.about.label,
    aboutHeading1: tr.about.heading1,
    aboutHeading3: tr.about.heading3,
    aboutText: tr.about.text,
    uniLabel: tr.universities.label,
    uniHeading: tr.universities.heading,
    highlightsLabel: tr.highlights.label,
    highlightsHeading: tr.highlights.heading,
    highlight0: tr.highlights.items[0],
    highlight1: tr.highlights.items[1],
    highlight2: tr.highlights.items[2],
    highlight3: tr.highlights.items[3],
    eventLabel: tr.eventInfo.label,
    eventHeading: tr.eventInfo.heading,
    eventDetailLabel0: tr.eventInfo.details[0].label,
    eventDetailLabel1: tr.eventInfo.details[1].label,
    eventDetailLabel2: tr.eventInfo.details[2].label,
    eventDetailValue0: tr.eventInfo.details[0].value,
    eventDetailValue1: tr.eventInfo.details[1].value,
    eventDetailValue2: tr.eventInfo.details[2].value,
    ctaJoin: tr.cta.join,
    ctaHeading2: tr.cta.heading2,
    ctaSubtext: tr.cta.subtext,
    ctaButtonText: tr.cta.btn
  };

  Object.keys(ids).forEach(key => {
    const el = document.getElementById(key);
    if(el) el.textContent = ids[key];
  });
}

function applyContact(){
  const tr = translations[currentLanguage].contact;

  const ids = {
    contactLabel: tr.label,
    contactHeading: tr.heading,
    contactIntro: tr.intro,
    contactFormTitle: tr.formTitle,
    nameLabel: tr.name,
    emailLabel: tr.email,
    messageLabel: tr.message,
    sendButton: tr.send
  };

  Object.keys(ids).forEach(key => {
    const el = document.getElementById(key);
    if(el) el.textContent = ids[key];
  });

  const nameField = document.getElementById("nameField");
  const emailField = document.getElementById("emailField");
  const messageField = document.getElementById("messageField");

  if(nameField) nameField.placeholder = tr.namePlaceholder;
  if(emailField) emailField.placeholder = tr.emailPlaceholder;
  if(messageField) messageField.placeholder = tr.messagePlaceholder;

  const wrap = document.getElementById("contactSectionsWrap");
  if(wrap){
    wrap.innerHTML = "";
    tr.sections.forEach(section => {
      const item = document.createElement("div");
      item.className = "contact-card";
      item.innerHTML = `<h3>${section.title}</h3><p>${section.desc}</p>`;
      wrap.appendChild(item);
    });
  }
}

function showToast(message, success=true){
  const box = document.getElementById("toastBox");
  if(!box) return;
  box.innerHTML = `<div class="toast ${success ? "toast-success" : "toast-error"}">${message}</div>`;
  setTimeout(() => {
    box.innerHTML = "";
  }, 2600);
}

function setupContactForm(){
  const form = document.getElementById("contactForm");
  if(!form) return;

  form.addEventListener("submit", function(e){
    e.preventDefault();
    const tr = translations[currentLanguage].contact;
    const name = document.getElementById("nameField").value.trim();
    const email = document.getElementById("emailField").value.trim();
    const message = document.getElementById("messageField").value.trim();

    if(!name || !email || !message){
      showToast(tr.errorMsg, false);
      return;
    }

    showToast(tr.successMsg, true);
    form.reset();
  });
}

function setupMenu(){
  const toggle = document.getElementById("menuToggle");
  const menu = document.getElementById("mobileMenu");
  if(toggle && menu){
    toggle.addEventListener("click", function(){
      menu.classList.toggle("menu-open");
    });
  }
}

function applyLanguage(){
  applyCommon();
  if(document.body.dataset.page === "home") applyHome();
  if(document.body.dataset.page === "contact") applyContact();
}

document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.addEventListener("click", function(){
      setLanguage(btn.dataset.lang);
    });
  });

  updateButtons();
  applyLanguage();
  setupContactForm();
  setupMenu();
});
