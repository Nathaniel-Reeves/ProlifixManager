<template>
  <div class="home">
    <div class="card p-0 mt-2 mb-4 bg-image boarder-0">
      <div class="card-img custom-background-image m-0" v-bind:style="{'background-position-y':'bottom', 'background-image': 'url(' + require('../assets/supplements_stock_photo.jpg')+')'}">
        <div class="d-flex justify-content-center align-items-center" style="
          background-color: rgb(255 255 255 / 0.6);
          max-height: 10rem;
          width:100%;
          align-self:center;
          transform: translate(0%, 40%);
          backdrop-filter: blur(1)">
          <img style="max-height: 10rem; align-self:center;" alt="Prolifix Nutrition Logo" src="../assets/Company Images/logos jpg/Prolifix Logo Cropped.jpg">
        </div>
      </div>
    </div>

    <div class="container-fluid p-0">
      <div class="card-deck">

        <div class="custom-card card border-0">
          <div class="imgbox m-0">
                <img class="image-blured m-0" alt="Prolifix Nutrition Logo" src="../assets/Production Flow Charts - New Manufacturing Flow Chart (POSTER).png">
              </div>
          <div class="specifies">
            <h2>Production <br> <span>Tools</span></h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div> <label>Tables</label>
            <ul>
                <li>10MM</li>
                <li>20MM</li>
                <li>30MM</li>
                <li>40MM</li>
                <li>50MM</li>
            </ul> <label>Charts</label>
            <ul class="colors">
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
            </ul> <button class="btn btn-light" style="width:100%;">Production Page</button>
          </div>
        </div>

        <div class="custom-card card ml-0 border-0">
          <div class="imgbox m-0">
                <img class="image-blured m-0" alt="Prolifix Nutrition Logo" src="../assets/Production Flow Charts - New Manufacturing Flow Chart (POSTER).png">
              </div>
          <div class="specifies">
            <h2>Production <br> <span>Tools</span></h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div> <label>Tables</label>
            <ul>
                <li>10MM</li>
                <li>20MM</li>
                <li>30MM</li>
                <li>40MM</li>
                <li>50MM</li>
            </ul> <label>Charts</label>
            <ul class="colors">
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
            </ul> <button class="btn btn-light" style="width:100%;">Production Page</button>
          </div>
        </div>

        <div class="custom-card card ml-0 border-0">
          <div class="imgbox m-0">
                <img class="image-blured m-0" alt="Prolifix Nutrition Logo" src="../assets/Production Flow Charts - New Manufacturing Flow Chart (POSTER).png">
              </div>
          <div class="specifies">
            <h2>Production <br> <span>Tools</span></h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div> <label>Tables</label>
            <ul>
                <li>10MM</li>
                <li>20MM</li>
                <li>30MM</li>
                <li>40MM</li>
                <li>50MM</li>
            </ul> <label>Charts</label>
            <ul class="colors">
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
            </ul> <button class="btn btn-light" style="width:100%;">Production Page</button>
          </div>
        </div>

        <div class="custom-card card ml-0 border-0">
          <div class="imgbox m-0">
                <img class="image-blured m-0" alt="Prolifix Nutrition Logo" src="../assets/Production Flow Charts - New Manufacturing Flow Chart (POSTER).png">
              </div>
          <div class="specifies">
            <h2>Production <br> <span>Tools</span></h2>
            <div class="price"><i class="bi bi-arrow-down"></i></div> <label>Tables</label>
            <ul>
                <li>10MM</li>
                <li>20MM</li>
                <li>30MM</li>
                <li>40MM</li>
                <li>50MM</li>
            </ul> <label>Charts</label>
            <ul class="colors">
                <li></li>
                <li></li>
                <li></li>
                <li></li>
                <li></li>
            </ul> <button class="btn btn-light" style="width:100%;">Production Page</button>
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
  max-width: 100%;
  max-height: 100%;
  transform: translate(-50%, -70%) rotate(9deg) scale(1.8);
  filter: blur(1px);
  position: absolute;
  top: 50%;
  left: 50%;
}

.custom-card {
  width: 300px;
  height: 400px;
  box-shadow: 0 20px 40px rgba(0,0,0,.2);
  border-radius: 5px;
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
  bottom: -145px;
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
</style>
