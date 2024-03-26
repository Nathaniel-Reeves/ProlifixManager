<template>
  <div class="home">
    <div class="card p-0 mt-2 mb-4 bg-image boarder-0" style="border:0px;">
      <div class="card-img custom-background-image m-0" v-bind:style="{'background-position-y':'bottom', 'background-image': 'url(' + require('../assets/supplements_stock_photo.jpg')+')'}">
        <div class="d-flex justify-content-center align-items-center" style="
          background-color: rgb(255 255 255 / 0.75);
          max-height: 10rem;
          width:100%;
          align-self:center;
          transform: translate(0%, 40%);
          backdrop-filter: blur(1)">
          <img style="max-height: 10rem; align-self:center;" alt="Prolifix Nutrition Logo" src="../assets/Company Images/logos png/Transparent Logo.png">
        </div>
      </div>
    </div>

    <div class="container-fluid p-0">
      <div class="d-flex flex-wrap justify-content-between">

        <div class="card custom-card">
          <div class="imgbox m-0">
              <img class="image-blured m-0" alt="Supplements Manufacturing" src="../assets/supplements_manufacturing.jpg">
            </div>
          <div class="specifies">
            <h2>Production <br>
              <span>Lot# | History | BPRs</span>
            </h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div>
            <label class="mb-0 mt-2">Product Lines</label>
            <ul>
                <li>Powder Fill</li>
                <li>Liquid Fill</li>
                <li>Capsule Fill</li>
            </ul>
            <label class="mb-0 mt-2">Tools</label>
            <ul>
                <li>Lot#</li>
                <li>BPR's'</li>
                <li>MMR's</li>
            </ul>
            <button disabled class="btn btn-light my-2" style="width:100%;">All Production</button>
          </div>
        </div>

        <div class="card custom-card">
          <div class="imgbox m-0">
            <img class="image-blured m-0" alt="Supplements" src="../assets/supplements.jpg">
          </div>
          <div class="specifies">
            <h2>Products <br>
              <span>Formulas | Specs</span>
            </h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div>
            <label class="mb-0 mt-2">Product Lines</label>
            <ul>
              <li>Powder</li>
              <li>Liquid</li>
              <li>Capsule</li>
            </ul>
            <label class="mb-0 mt-2">Tools</label>
            <ul>
              <li>Specs</li>
              <li>Formulas</li>
              <li>Labels</li>
            </ul>
            <button disabled class="btn btn-light my-2" style="width:100%;">All Products</button>
          </div>
        </div>

        <div class="card custom-card">
          <div class="imgbox m-0">
            <img class="image-blured m-0" alt="Warehouse" src="../assets/inventory-warehouse-boxes.jpg">
          </div>
          <div class="specifies">
            <h2>Inventory <br>
              <span>Components | Products</span>
            </h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div>
            <label class="mb-0 mt-2">Product Lines</label>
            <ul>
              <li>Ingredients</li>
              <li>Components</li>
              <li>Catalogue</li>
            </ul>
            <label class="mb-0 mt-2">Tools</label>
            <ul>
              <li>Ordering</li>
              <li>Cycle Counts</li>
              <li>Inventory</li>
            </ul>
            <button disabled class="btn btn-light my-2" style="width:100%;">All Inventory</button>
          </div>
        </div>

        <div class="card custom-card">
          <div class="imgbox m-0">
            <img class="image-blured m-0" alt="Hand Shake" src="../assets/Hand-shake.png">
          </div>
          <div class="specifies">
            <h2>Organizations <br>
              <span>Clients | Suppliers | Labs</span>
            </h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div>
            <label class="mb-0 mt-2">Catagories</label>
            <ul>
              <li>Clients</li>
              <li>Suppliers</li>
              <li>labs</li>
            </ul>
            <label class="mb-0 mt-2">Tools</label>
            <ul>
              <li>People</li>
              <li>Facilities</li>
              <li>Status</li>
            </ul>
            <button disabled class="btn btn-light my-2" style="width:100%;">All Organizations</button>
          </div>
        </div>

        <div class="card custom-card">
          <div class="imgbox m-0">
            <img class="image-blured m-0" alt="Office Worker" src="../assets/orders.jpg">
          </div>
          <div class="specifies">
            <h2>Orders <br>
              <span>POs | SOs</span>
            </h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div>
            <label class="mb-0 mt-2">Product Lines</label>
            <ul>
              <li>Purchase Orders</li>
              <li>Sales Orders</li>
            </ul>
            <label class="mb-0 mt-2">Tools</label>
            <ul>
              <li>Lot#</li>
              <li>PO Summary</li>
              <li>Order List</li>
            </ul>
            <button disabled class="btn btn-light my-2" style="width:100%;">All Orders</button>
          </div>
        </div>

        <div class="card custom-card">
          <div class="imgbox m-0">
                <img class="image-blured m-0" alt="Signing Documents" src="../assets/policy.jpg">
              </div>
          <div class="specifies">
            <h2>Policies <br>
              <span>SOPs | GMPs</span>
            </h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div>
            <label class="mb-0 mt-2">Documents</label>
            <ul>
              <li>SOPs</li>
              <li>GMPs</li>
              <li>Mission Statement</li>
            </ul>
            <label class="mb-0 mt-2">Tools</label>
            <ul>
              <li>Policy</li>
              <li>Mission Statement'</li>
              <li>Training App</li>
            </ul>
            <button disabled class="btn btn-light my-2" style="width:100%;">All Products</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  width: 90%;
}

.custom-background-image {
  height: 400px;
  width: auto;
  margin-top: 58px;
  background-repeat: no-repeat;
  background-size: cover;
}

.image-blured {
  filter: blur(0px);
  transition: 0.5s;
  transform: scale(3) translate(0%, 30%);
}

.custom-card:hover .image-blured {
  filter: blur(1px);
  transition: 0.5s;
}

.tilted {
  top: 50%;
  left: 50%;
  max-width: 100%;
  max-height: 100%;
  transform: translate(-50%, -70%) rotate(9deg) scale(1.8);
  position: absolute;
}

.custom-card {
  width: 300px;
  height: 400px;
  box-shadow: 0 20px 40px rgba(0,0,0,.2);
  border-radius: 5px;
  border: 0;
  margin-bottom: 24px;
  background:white;
  overflow: hidden
}

.custom-card .imgbox {
  height: 100%;
  box-sizing: border-box;
  width: 18rem;
  height: 300px;
}

.custom-card .imgbox img {
  display: block;
  width: 80%;
  margin: 10px auto 0;
}

.specifies {
  position: absolute;
  width: 100%;
  bottom: -175px;
  background: #67803a;
  color: white;
  padding:10px;
  box-sizing: border-box;
  transition: .5s
}

.custom-card:hover .specifies {
  bottom: 0
}

.specifies h2 {
  margin: 0;
  padding: 0;
  font-size: 20px;
  width: 100%
}

.specifies h2 span {
  font-size: 15px;
  color: #ccc;
  font-weight: normal
}

.specifies .price {
  position: absolute;
  top: 12px;
  right: 25px;
  font-weight: bold;
  color: white;
  font-size: 30px
}

label {
  display: block;
  margin-top: 5px;
  font-weight: bold;
  font-size: 15px
}

ul {
  display: flex;
  margin: 0;
  padding: 0
}

ul li {
  list-style: none;
  margin: 5px 5px 0;
  font-size: 15px;
  font-style: normal;
  color: #ccc
}

@media (max-width: 700px) {
  .custom-card {
    width: 100%;
    margin-right: 0px;
  }

  .custom-card .imgbox img {
    display: block;
    width: 110%;
    margin: 10px auto 0;
  }
}
</style>
