<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-if="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class=" my-2" v-if="loaded">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2" src="../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <h2 class="card-title">{{ product_data.product_name }} {{ product_data.organization_name }}</h2>
            <CertBadge :data="product_data"></CertBadge>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#Formulas" @click="scrollIntoView">Formulas</b-nav-item>
            <b-nav-item href="#Manufacturing" @click="scrollIntoView">Manufacturing</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <h3 id="Formulas">Formulas<b-button v-if="!edit_formulas" v-b-tooltip.hover title="Edit Product Formulas" v-on:click="edit_formulas = !edit_formulas" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <b-tabs content-class="mt-3">
            <b-tab v-for="f in product_data.formulas" :key="'formula-id-' + f.formula_id">
              <template #title>
                <strong>{{ f.formulation_version+'V' }}<b-badge variant="primary" pill class="ml-2" style="font-size:0.8em;" v-show="f.formulation_version === product_data.default_formula_version">PF</b-badge></strong>
              </template>
              <ProductFormula :formula="f" :edit="edit_formulas" :primary="f.formulation_version === product_data.default_formula_version"></ProductFormula>
            </b-tab>
          </b-tabs>
          <hr>
          <h3 id="Manufacturing">Manufacturing<b-button v-if="!edit_specs" v-b-tooltip.hover title="Edit Manufacturing Process" v-on:click="edit_manufacturing = !edit_manufacturing" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <ProductManufacturing :manufacturing="product_data.manufacturing" :edit="edit_manufacturing"></ProductManufacturing>
          <hr>
        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.scrollbox {
  position:relative;
  height:85vh;
  overflow-y:scroll;
}
.customize-table {
  --easy-table-body-item-padding:10px 10px 10px 10px;
}
@media print {
  .scrollbox {
    height: 100%;
    overflow-y:auto;
  }
  @page {
    margin: 30mm 30mm 10mm 10mm;
  }
  body {
    margin: 0px;
  }
}
.bold {
    font-weight: bold;
}
.my_component {
    width: 95%;
}
@media (max-width: 1024px) {
    .my_component {
        width: 98%;
    }
}
@media (max-width: 400px) {
    .my_component {
        width: 100%;
    }
}
</style>

<script>
import CertBadge from '../../components/CertBadge.vue'
import ProductFormula from './ProductFormula.vue'
import ProductManufacturing from './ProductManufacturing.vue'

export default {
  name: 'ProductsDetail',
  components: {
    CertBadge,
    ProductFormula,
    ProductManufacturing
  },
  data: function () {
    return {
      loaded: false,
      edit_specs: false,
      id: this.$route.params.id,
      product_data: {},
      edit_formulas: false,
      edit_manufacturing: false
    }
  },
  methods: {
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    getProductData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/products?product-id=' + this.id + '&doc=true&populate=formulas&populate=manufacturing'
      // eslint-disable-next-line
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.product_data = data.data[0]
            // eslint-disable-next-line
            console.log(this.product_data)
            this.loaded = true
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else if (response.status === 404) {
          this.$router.push({
            name: 'NotFound'
          })
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    }
  },
  created: function () {
    this.getProductData()
  }
}
</script>
