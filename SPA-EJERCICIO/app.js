const app = document.getElementById('app');

function renderHome(){
    app.innerHTML='<h1> 🏠 Home</h1><p>Bienvenido a nuestra SPA</p>';

}

function renderServices(){
    app.innerHTML='<h1> 🆓 Services</h1><p>Forntend con JS</p>';
}

function renderContact(){
    app.innerHTML='<h1> 📞 Contact</h1><p>clan@hamilton.dev</p>'
}

function rendernotFound(){
    app.innerHTML='<h1> 404</h1> <p> Pagina no encontrada</p>'
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