const app = document.getElementById('app');

function renderHome(){
    app.innerHTML='<h1>Home</h1><p>Bienvenido a nuestra SPA</p>';

}

function renderServices(){
    app.innerHTML='<h1>Services</h1><p>Forntend con JS</p>';
}

function renderContact(){
    app.innerHTML='<h1>Contact</h1><p>clan@hamilton.dev</p>'
}

function rendernotFound(){
    app.innerHTML='<h1>404</h1> <p> Pagina no encontrada</p>'
}

let counter = 0;
function renderCounter(){
    app.innerHTML= `
     <h1>Contador </h1>
     <p>${counter}</p>
     <button id='rest'>-</button>
     <button id="add">+</button>
        `;
      
    document.getElementById('rest').onclick = () => {
        counter--;
        renderCounter();
    }
    document.getElementById('add').onclick = () => {
        counter++;
        renderCounter();
    }
    
    
}

function Navbar(){
    return
    <nav>
        <a href="#home">Home</a>
        <a href="#services">Services</a>
        <a href="#contact">Contacto</a>
    </nav>
}

function Home() {
  return '<h1>🏠 Home</h1><p>Bienvenido</p>';
}

function Services() {
  return '<h1>🛠️ Servicios</h1>';
}

function Contact() {
  return '<h1>📩 Contacto</h1>';
}

const app = document.getElementById('app');

function render(view) {
  app.innerHTML = `
    ${Navbar()}
    <main>
      ${view}
    </main>
  `;
}

function router(){
    const route = location.hash;

    switch (route){
        case '#home':
            renderHome();
            break;
        case'#services':
            renderServices();
            break;
        case'#contact':
            renderContact();
            break;
        case'#/counter':
            renderCounter();
            break;
        default:
            renderHome();
    }
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router)


/*document.getElementById('home').addEventListener('click',renderHome);
document.getElementById('services').addEventListener('click',renderServices);
document.getElementById('contact').addEventListener('click',renderContact)

renderHome();*/