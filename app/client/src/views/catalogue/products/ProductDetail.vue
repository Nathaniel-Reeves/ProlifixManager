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
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2" src="../../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <div>
              <div class="card-title d-flex align-items-center">
                <h1>{{ product_data.product_name }}</h1>
                <CertBadge :data="product_data"></CertBadge>
              </div>
              <router-link :to="'/organizations/'+product_data.organization_id" target="_blank"><h4 class="card-subtitle text-muted mb-2">{{ product_data.organization_name }} {{ product_data.organizaiton_initial ? '(' + product_data.organizaiton_initial + ')' : '' }}</h4></router-link>
            </div>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#Labels" @click="scrollIntoView" :disabled="edit_manufacturing || edit_specs || edit_formulas">Labels</b-nav-item>
            <b-nav-item href="#Formulas" @click="scrollIntoView" :disabled="edit_manufacturing || edit_specs || edit_labels">Formulas</b-nav-item>
            <b-nav-item href="#Manufacturing" @click="scrollIntoView" :disabled="edit_formulas || edit_specs || edit_labels">Manufacturing</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView" v-if="product_data.doc.specifications !== undefined" :disabled="edit_manufacturing || edit_formulas || edit_labels">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in product_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView" :disabled="edit_manufacturing || edit_formulas || edit_labels">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <ProductLabel
            v-show="!edit_manufacturing && !edit_specs && !edit_formulas"
            :id="product_data.product_id"
            :doc="product_data.doc"
            :name="product_data.product_name"
            v-on:edit-labels="(e) => {edit_labels = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductLabel>
          <hr v-show="!edit_manufacturing && !edit_specs && !edit_formulas">
          <ProductFormula
            v-show="!edit_manufacturing && !edit_specs && !edit_labels"
            :v-key="formula_key"
            :product-id="product_data.product_id"
            :formulas="product_data.formulas"
            :num-versions="product_data.num_formula_versions"
            :default-formula-id="product_data.default_formula_version"
            v-on:edit-formulas="(e) => {edit_formulas = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductFormula>
          <hr v-show="!edit_manufacturing && !edit_specs && !edit_labels">
          <ProductManufacturing
            v-show="!edit_formulas && !edit_specs && !edit_labels"
            :product-id="product_data.product_id"
            :manufacturing="product_data.manufacturing"
            :edit="edit_manufacturing"
            v-on:edit-manufacturing="(e) => {edit_manufacturing = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductManufacturing>
          <hr v-show="!edit_formulas && !edit_specs && !edit_labels">
          <SpecificationsComponent
            v-show="!edit_formulas && !edit_manufacturing && !edit_labels"
            :doc="product_data.doc"
            :spectype="'product'"
            :name="product_data.product_name"
            :id="product_data.product_id"
            v-on:edit-specs="(e) => edit_specs = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></SpecificationsComponent>
          <hr v-show="!edit_formulas && !edit_manufacturing && !edit_labels">
        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import CertBadge from '../../../components/CertBadge.vue'
import ProductFormula from './ProductFormula.vue'
import ProductLabel from './ProductLabel.vue'
import ProductManufacturing from './ProductManufacturing.vue'
import SpecificationsComponent from '../SpecificationsComponent.vue'

export default {
  name: 'ProductsDetail',
  components: {
    CertBadge,
    ProductFormula,
    ProductManufacturing,
    SpecificationsComponent,
    ProductLabel
  },
  data: function () {
    return {
      loaded: false,
      id: this.$route.params.id,
      product_data: {},
      edit_manufacturing: false,
      edit_formulas: false,
      edit_specs: false,
      edit_labels: false,
      formula_key: 0
    }
  },
  methods: {
    toggleLoaded: function (val) {
      this.loaded = val
    },
    refreshParent: function (val) {
      this.getProductData()
    },
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
            this.edit_specs = false
            this.edit_manufacturing = false
            this.edit_formulas = false
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
  watch: {
    product_data: function () {
      // refresh product formula if the formula data has changed in the parent.
      this.formula_key += 1
      this.edit_formulas = false
    }
  },
  created: function () {
    this.getProductData()
  }
}
</script>

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
