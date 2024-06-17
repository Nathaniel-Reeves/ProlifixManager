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
            <b-nav-item href="#Specifications" @click="scrollIntoView"
              v-if="product_data.doc.specifications !== undefined">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in product_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <ProductFormula :formulas="product_data.formulas" :primary="product_data.default_formula_id" :num-versions="product_data.num_formula_versions"></ProductFormula>
          <hr>
          <ProductManufacturing :manufacturing="product_data.manufacturing" :edit="edit_manufacturing"></ProductManufacturing>
          <hr>
          <SpecificationsComponent :data="product_data.doc" :spectype="'product'" :name="product_data.product_name" @update-spec-buffer="update_spec_buffer" @update-file-buffer="update_file_buffer" @update-remove-file-buffer="update_remove_file_buffer" @save-specs="save_specs"></SpecificationsComponent>
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
import SpecificationsComponent from './SpecificationsComponent.vue'

export default {
  name: 'ProductsDetail',
  components: {
    CertBadge,
    ProductFormula,
    ProductManufacturing,
    SpecificationsComponent
  },
  data: function () {
    return {
      loaded: false,
      id: this.$route.params.id,
      product_data: {},
      edit_manufacturing: false,
      edit_specs_buffer: {},
      upload_files_buffer: {},
      remove_files_buffer: []
    }
  },
  methods: {
    update_spec_buffer: function (data) {
      this.edit_specs_buffer = data
    },
    update_file_buffer: function (data) {
      this.upload_files_buffer = data
    },
    update_remove_file_buffer: function (data) {
      this.remove_files_buffer = data
    },
    save_specs: function () {
      const original = structuredClone(this.component_data.doc.specifications) // Deep Copy
      this.component_data.doc.specifications = structuredClone(this.edit_specs_buffer) // Deep Copy
      this.component_data.doc.files = structuredClone(this.upload_files_buffer) // Deep Copy
      this.putComponent().then(outcome => {
        if (outcome !== true) {
          this.component_data.doc.specifications = original
        }
      })
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
