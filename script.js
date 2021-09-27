// Selecionar todas as opcoes do menu
const menuItems = document.querySelectorAll('.menu a');

// Para cada item do menu, adicionar o evento de clique e ao clicar chamar a funcao do scroll
menuItems.forEach(item => {
  item.addEventListener('click', scrollParaId);
})

// Pegar a distancia em pixels do topo ate a id do menu que foi cliclada
function distanciaScrollTopo(element) {
  const id = element.getAttribute('href'); // Pegar a ID e guardar na constante
  return document.querySelector(id).offsetTop;
}

// Fazer o scroll ao clicar no item do menu
function scrollParaId(event) {
  event.preventDefault(); // Tirar o comportamento padrao do site
  const to = distanciaScrollTopo(event.target) - 110;
  smoothScroll(to);
}

// Fazer o scroll suave
function smoothScroll(to) {
  window.scroll({
    top: to,
    behavior: "smooth",
  });
}
