<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query_buff" type="text" class="form-control" placeholder="Search Products..." aria-label="Search Components" aria-describedby="button-addon2" v-on:keyup.enter="search()">
            <div class="input-group-append" v-if="search_query.length > 0">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><b-icon icon="x"></b-icon></button>
            </div>
            <div class="input-group-append" v-else>
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="search()"><b-icon icon="search"></b-icon></button>
            </div>
          </div>

          <form class="mt-2">
            <b>Powder Certification Filter:</b><br>
            <div class="custom-control custom-checkbox" v-for="cert in powder_cert_options" :key="cert.value">
              <input class="custom-control-input" type="checkbox" :id="cert.value" :value="cert.value" v-model="powder_cert_filter">
              <label class="custom-control-label" :for="cert.value">
                <span>{{ cert.text }}</span>
              </label>
            </div>
          </form>
        </div>
      </b-sidebar>
    </div>

    <div class="card my-2">
      <div class="card-body">
        <div class="input-group d-flex">
          <h2 class="card-title flex-grow-1">Products Catalogue</h2>
          <b-button :to="{ name: 'NewProduct'}" v-b-tooltip.hover title="New Product" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
            <b-icon icon="plus"></b-icon>
          </b-button>
          <b-button v-b-tooltip.hover title="Filter" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', filterActive ? 'btn-info' : 'btn-light']" type="button" id="button-addon2">
            <b-icon icon="filter"></b-icon>
          </b-button>
        </div>

        <div v-show="!loaded">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>

        <div v-show="loaded" class="accordion overflow-auto border-top border-bottom" role="tablist" style="height:100vh;">
          <b-card no-body class="mb-1" style="box-shadow: 0px 0px;" v-for="product in filteredProducts" :key="product.product_id">
            <b-card-header v-bind:id="'heading' + product.product_id">
              <h2 class="d-flex mb-0">
                <b-button class="text-left" v-b-toggle="'collapse' + product.product_id" variant="light" style="width:100%;">
                  <b-container fluid class="m-0">
                    <b-row align-v="center">
                      <b-col sm="0.5"><b-icon icon="chevron-down"></b-icon></b-col>
                      <b-col sm="4"><h4 class="p-2">{{ product.product_name }}</h4></b-col>
                      <b-col sm="4"><h4 class="p-2">{{ product.organization_name }}</h4></b-col>
                      <b-col><div class="p-2"><CertBadge :data="product"></CertBadge></div></b-col>
                      <b-col sm="0.5"><h3 class="mx-3 my-0"><b-badge v-show="!product.current_product" class="p-2 align-middle" variant="danger">Discontinued</b-badge></h3></b-col>
                      <b-col sm="1.5">
                        <router-link :to="{path:`/catalogue/products/${product.product_id}`}"><button type="button" class="btn btn-light ms-auto" style="border-width: 2px; border-color:#999999">View Details</button></router-link>
                      </b-col>
                    </b-row>
                  </b-container>
                </b-button>
              </h2>
            </b-card-header>

            <b-collapse v-bind:id="'collapse' + product.product_id">
              <div class="card-body d-flex flex-wrap">

              </div>
            </b-collapse>
          </b-card>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my_component {
    width: 80%;
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

export default {
  name: 'ProductHome',
  components: {
    CertBadge
  },
  data: function () {
    return {
      loaded: false,
      search_query: '',
      search_query_buff: '',
      products_data: [],
      powder_cert_options: [
        { value: 'certified_usda_organic', text: 'Certified USDA Organic', active: false },
        { value: 'certified_halal', text: 'Certified Halal', active: false },
        { value: 'certified_kosher', text: 'Certified Kosher', active: false },
        { value: 'certified_national_sanitation_foundation', text: 'Certified NSF', active: false },
        { value: 'certified_us_pharmacopeia', text: 'Certified US Pharma', active: false },
        { value: 'certified_non_gmo', text: 'Certified Non-GMO', active: false },
        { value: 'certified_vegan', text: 'Certified Vegan', active: false }
      ],
      powder_cert_filter: [],
      allPowderCertSelected: false,
      powderCertIndeterminate: false
    }
  },
  methods: {
    certFilter: function (product) {
      let flag = false
      for (let i = 0; i < this.powder_cert_options.length; i++) {
        if (product[this.powder_cert_options[i].value] && this.powder_cert_filter.includes(this.powder_cert_options[i].value)) { flag = true }
      }
      return flag
    },
    toggleAllCerts: function (checked) {
      this.powder_cert_filter = checked ? this.powder_cert_options.map((obj) => obj.value).slice() : []
    },
    clearSearch: function () {
      this.search_query = ''
      this.search_query_buff = ''
    },
    search: function () {
      this.search_query = this.search_query_buff
    },
    getProductData: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/catalogue/products/'
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
            this.products_data = data.data
            // eslint-disable-next-line
            console.log(this.products_data)
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
    },
    alphabetical: function (a, b) {
      const aPrime = a.product_name
      const bPrime = b.product_name
      if (aPrime < bPrime) {
        return -1
      }
      if (aPrime > bPrime) {
        return 1
      }
      return 0
    },
    productBrand: function (a, b) {
      const aPrime = a.organization_name
      const bPrime = b.organization_name
      if (aPrime < bPrime) {
        return -1
      }
      if (aPrime > bPrime) {
        return 1
      }
      return 0
    },
    searchFilter: function (product) {
      return product.product_name.toLowerCase().includes(this.search_query.toLowerCase())
    }
  },
  watch: {
    search_query_buff: function (newValue, oldValue) {
      if (newValue.length === 0) {
        this.search_query = ''
      }
    }
  },
  computed: {
    filteredProducts: function () {
      let list = Object.values(structuredClone(this.products_data))
      if (this.search_query.length > 3) {
        list = list.filter(this.searchFilter)
      }
      if (this.powder_cert_filter.length > 0) {
        list = list.filter(this.certFilter)
      }
      list = list.sort(this.alphabetical).sort(this.productBrand)
      return list
    },
    filterActive: function () {
      if (this.search_query.length > 3 || this.powder_cert_filter.length > 0) {
        return true
      }
      return false
    }
  },
  created: function () {
    this.getProductData()
  }
}
</script>
