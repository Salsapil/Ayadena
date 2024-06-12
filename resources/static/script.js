$(document).ready(function () {
    // Fetch categories from the backend
    $.get("/category", function (categories) {
      const filterButtonsContainer = $("#filter-buttons .col-12");
      categories.forEach(category => {
        const button = `<button class="btn mb-2 mx-1" data-filter="${category.name}">${category.name}</button>`;
        filterButtonsContainer.append(button);
      });
    });
  
    // Fetch products from the backend
    $.get("/product", function (products) {
      const filterableCardsContainer = $("#filterable-cards");
      products.forEach(product => {
        const card = `
          <div class="card p-0" data-name="${product.category}">
            <img src="images/${product.image}" alt="img" />
            <div class="card-body">
              <h5 class="card-title">${product.price} LE.</h5>
              <p class="card-text">${product.name}<br>${product.description}</p>
              <button class="boo"><a href="#">Add to cart</a><i class='bx bxs-cart-alt'></i></button>
            </div>
          </div>`;
        filterableCardsContainer.append(card);
      });
    });
  
    // Function to filter cards based on filter buttons
    const filterCards = (e) => {
      $("#filter-buttons .active").removeClass("active");
      $(e.target).addClass("active");
  
      $("#filterable-cards .card").each(function () {
        const card = $(this);
        if (card.data("name") === $(e.target).data("filter") || $(e.target).data("filter") === "all") {
          card.removeClass("hide").addClass("show");
        } else {
          card.removeClass("show").addClass("hide");
        }
      });
    }
  
    // Event listener for filter buttons
    $("#filter-buttons").on("click", "button", filterCards);
  });
  