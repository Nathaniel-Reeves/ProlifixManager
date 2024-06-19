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
            <h2 class="card-title">{{ product_data.product_name }} {{ product_data.organization_name }}</h2>
            <CertBadge :data="product_data"></CertBadge>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#Formulas" @click="scrollIntoView" :disabled="edit_specs">Formulas</b-nav-item>
            <b-nav-item href="#Manufacturing" @click="scrollIntoView" :disabled="edit_formulas || edit_specs">Manufacturing</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView" v-if="product_data.doc.specifications !== undefined" :disabled="edit_formulas">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in product_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView" :disabled="edit_formulas">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <ProductFormula  v-show="!edit_specs" :v-key="formula_key" :product-id="product_data.product_id" v-model:formulas="product_data.formulas" v-model:default-formula-id="product_data.default_formula_id" v-model:num-versions="product_data.num_formula_versions" @edit-formulas="(e) => {edit_formulas = e}"></ProductFormula>
          <hr v-show="!edit_formulas && !edit_specs">
          <ProductManufacturing v-show="!edit_formulas && !edit_specs" :manufacturing="product_data.manufacturing" :edit="edit_manufacturing"></ProductManufacturing>
          <hr v-show="!edit_formulas">
          <SpecificationsComponent v-show="!edit_formulas" :data="product_data.doc" :spectype="'product'" :name="product_data.product_name" @update-spec-buffer="update_spec_buffer" @update-file-buffer="update_file_buffer" @update-remove-file-buffer="update_remove_file_buffer" @save-specs="save_specs" @edit-specs="(e) => {edit_specs = e}"></SpecificationsComponent>
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
import CertBadge from '../../../components/CertBadge.vue'
import ProductFormula from './ProductFormula.vue'
import ProductManufacturing from './ProductManufacturing.vue'
import SpecificationsComponent from '../SpecificationsComponent.vue'

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
      edit_formulas: false,
      edit_specs: false,
      edit_specs_buffer: {},
      upload_files_buffer: {},
      remove_files_buffer: [],
      formula_key: 0
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
      const original = structuredClone(this.product_data.doc.specifications) // Deep Copy
      this.product_data.doc.specifications = structuredClone(this.edit_specs_buffer) // Deep Copy
      this.product_data.doc.files = structuredClone(this.upload_files_buffer) // Deep Copy
      this.putProductData().then(outcome => {
        if (outcome !== true) {
          this.product_data.doc.specifications = original
        }
      })
    },
    putProductData: async function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/products/' + this.id
      // eslint-disable-next-line
      console.log(
        'PUT ' + fetchRequest
      )
      const formData = new FormData()
      formData.append('product_id', this.id)
      formData.append('product_name', this.product_data.product_name)
      formData.append('current_product', this.product_data.current_product)
      formData.append('exp_time_frame', this.product_data.exp_time_frame)
      formData.append('exp_unit', this.product_data.exp_unit)
      formData.append('exp_type', this.product_data.exp_type)
      formData.append('exp_use_oldest_ingredient', this.product_data.exp_use_oldest_ingredient)
      formData.append('default_formula_version', this.product_data.default_formula_version)
      formData.append('num_formula_versions', this.product_data.num_formula_versions)
      formData.append('default_manufacturing_version', this.product_data.default_manufacturing_version)
      formData.append('num_manufacturing_versions', this.product_data.num_manufacturing_versions)
      formData.append('certified_usda_organic', this.product_data.certified_usda_organic)
      formData.append('certified_halal', this.product_data.certified_halal)
      formData.append('certified_kosher', this.product_data.certified_kosher)
      formData.append('certified_gluten_free', this.product_data.certified_gluten_free)
      formData.append('certified_national_sanitation_foundation', this.product_data.certified_national_sanitation_foundation)
      formData.append('certified_us_pharmacopeia', this.product_data.certified_us_pharmacopeia)
      formData.append('certified_non_gmo', this.product_data.certified_non_gmo)
      formData.append('certified_vegan', this.product_data.certified_vegan)
      this.product_data.doc.remove_files = this.remove_files_buffer
      for (const pair of Object.entries(this.product_data.doc.files)) {
        const key = pair[0]
        const value = pair[1]
        const fileObj = structuredClone(value.file)
        delete value.file
        this.product_data.doc.files[key] = value
        formData.append(key, fileObj)
      }
      formData.append('doc', JSON.stringify(this.product_data.doc))
      try {
        this.loaded = false
        const response = await fetch(fetchRequest, {
          method: 'PUT',
          credentials: 'include',
          body: formData
        })
        if (response.status === 201) {
          const data = await response.json()
          this.flash_messages = data.messages.flash
          const createToast = this.$root.createToast
          this.flash_messages.forEach(function (message) {
            createToast(message)
          })
          this.getComponentData()
          this.loaded = true
          return true
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          response.json().then(data => {
            this.flash_messages = data.messages.flash
            const createToast = this.$root.createToast
            this.flash_messages.forEach(function (message) {
              createToast(message)
            })
          })
          this.loaded = true
          return false
        }
      } catch (error) {
        const err = error
        this.loaded = true
        // eslint-disable-next-line
        console.error('There has been a problem with your fetch operation: ', err)
        const errorToast = {
          title: 'Failure to save changes.',
          message: 'Find IT to help fix the issue.',
          variant: 'danger',
          visible: true,
          noCloseButton: false,
          noAutoHide: true,
          autoHideDelay: false,
          appendToast: true,
          solid: true,
          toaster: 'b-toaster-bottom-right'
        }
        const createToast = this.$root.createToast
        createToast(errorToast)
        return false
      }
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
