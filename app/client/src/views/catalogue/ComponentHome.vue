<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query" type="text" class="form-control" placeholder="Search Components..." aria-label="Search Components" aria-describedby="button-addon2">
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><i class="bi bi-x"></i></button>
            </div>
          </div>

          <b-form-select v-model="type_filter" :options="type_filter_options"></b-form-select>

          <b-form-group class="mt-2" v-show="type_filter === 'powder'">
            <template #label>
              <b>Powder Certification Filter:</b><br>
              <b-form-checkbox v-model="allPowderCertSelected" :indeterminate="powderCertIndeterminate" aria-describedby="powder_cert_options" aria-controls="powder_cert_options" @change="toggleAllCerts">
                {{ allPowderCertSelected ? 'Un-select All' : 'Select All' }}
              </b-form-checkbox>
            </template>

            <template v-slot="{ ariaDescribedby }">
              <b-form-checkbox-group id="powder_cert_filter" v-model="powder_cert_filter" :options="powder_cert_options" name="powder_cert_filter" class="ml-4" aria-label="Individual Certifications" :aria-describedby="ariaDescribedby" stacked></b-form-checkbox-group>
            </template>
          </b-form-group>

        </div>
      </b-sidebar>
    </div>

    <div class="card my-2">
      <div class="card-body">
        <div class="input-group d-flex">
          <h2 class="card-title flex-grow-1">Components Catalogue</h2>
          <b-button :to="{ name: 'NewComponent'}" v-b-tooltip.hover title="New Component" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
            <i class="bi bi-plus-lg"></i>
          </b-button>
          <b-button v-b-tooltip.hover title="Filter" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', filterActive ? 'btn-info' : 'btn-light']" type="button" id="button-addon2">
            <i class="bi bi-filter"></i>
          </b-button>
        </div>

        <div v-show="!loaded">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>

        <div v-show="loaded" class="accordion overflow-auto border-top border-bottom" id="accordionExample" style="height:100vh;">
          <div class="card" v-for="component in filterPowderCerts" :key="component.component_id">
            <div class="card-header" v-bind:id="'heading' + component.component_id">
              <h2 class="d-flex mb-0">
                <button class="btn btn-block text-left" type="button" data-toggle="collapse" v-bind:data-target="'#collapse' + component.component_id" aria-expanded="false" v-bind:aria-controls="'collapse' + component.component_id" v-on:click="populateComponent(component.component_id)">
                  <b-container>
                    <b-row align-v="baseline">
                      <b-col sm style="max-width:1em;"><i class="bi bi-chevron-down p-2"></i></b-col>
                      <b-col sm><div class="p-2">{{ component.component_type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ') }}</div></b-col>
                      <b-col sm><div class="p-2">{{ get_comopnent_primary_name(component) }}</div></b-col>
                      <b-col sm="2"><div class="p-2"><CertBadge :data="component"></CertBadge></div></b-col>
                      <b-col sm><div class="p-2">{{ get_component_brand_name(component) }}</div></b-col>
                    </b-row>
                  </b-container>
                </button>
              </h2>
            </div>

            <div v-bind:id="'collapse' + component.component_id" class="collapse" v-bind:aria-labelledby="'heading' + component.component_id" data-parent="#accordionExample">
              <div class="card-body d-flex flex-wrap">

                <b-container fluid class="d-flex justify-content-end flex-wrap" style="max-width:10rem;">
                  <router-link :to="{path:`/catalogue/components/${component.component_id}`}"><button type="button" class="btn btn-light ms-auto" style="border-width: 2px; border-color:#999999">View Details</button></router-link>
                </b-container>

              </div>
            </div>
          </div>
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
// import FacilitiesGrid from './components/FacilitiesGrid.vue'
import CertBadge from '../../components/CertBadge.vue'

export default {
  name: 'ComponentsHome',
  components: {
    CertBadge
  },
  data: function () {
    return {
      components_data: {},
      search_query: '',
      loaded: false,
      type_filter: 'all',
      type_filter_options: [
        { value: 'all', text: 'All Components' },
        { value: 'powder', text: 'Powders' },
        { value: 'liquid', text: 'Liquids' },
        { value: 'container', text: 'Containers' },
        { value: 'pouch', text: 'Pouches' },
        { value: 'shrink_band', text: 'Shrink Bands' },
        { value: 'lid', text: 'Lids' },
        { value: 'label', text: 'Labels' },
        { value: 'capsule', text: 'Capsules' },
        { value: 'misc', text: 'Miscellaneous' },
        { value: 'scoop', text: 'Scoops' },
        { value: 'desiccant', text: 'Desiccants' },
        { value: 'box', text: 'Boxes' },
        { value: 'carton', text: 'Cartons' },
        { value: 'packaging_material', text: 'Packaging Materials' }
      ],
      powder_cert_options: [
        { value: 'certified_usda_organic', text: 'Certified USDA Organic' },
        { value: 'certified_halal', text: 'Certified Halal' },
        { value: 'certified_kosher', text: 'Certified Kosher' },
        { value: 'certified_national_sanitation_foundation', text: 'Certified NSF' },
        { value: 'certified_us_pharmacopeia', text: 'Certified US Pharma' },
        { value: 'certified_non_gmo', text: 'Certified Non-GMO' },
        { value: 'certified_vegan', text: 'Certified Vegan' }
      ],
      powder_cert_filter: [],
      allPowderCertSelected: false,
      powderCertIndeterminate: false
    }
  },
  methods: {
    clearSearch: function () {
      this.search_query = ''
    },
    get_comopnent_primary_name: function (component) {
      if (component.Component_Names !== undefined && component.Component_Names.length > 0) {
        for (let i = 0; i < component.Component_Names.length; i++) {
          if (component.Component_Names[i].primary_name) {
            return component.Component_Names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    get_component_brand_name: function (component) {
      if (component.Organization_Names !== undefined && component.Organization_Names.length > 0) {
        for (let i = 0; i < component.Organization_Names.length; i++) {
          if (component.Organization_Names[i].primary_name) {
            return component.Organization_Names[i].organization_name
          }
        }
      }
      return ''
    },
    populateComponent: function (componentId) {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?component-id=' + componentId + '&populate=product_materials&populate=purchase_order_detail&populate=label_formula_master&populate=ingredient_formula_master&populate=item_id&populate=inventory&populate=brand&doc=true'
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
            this.components_data[componentId] = Object.values(data.data[0])[0]
            console.log(this.components_data[componentId])
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    },
    getComponentData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components/?populate=brand'
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
            this.components_data = data.data[0]
            console.log(this.components_data)
            this.loaded = true
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    },
    compare: function (a, b) {
      if (a.component_type < b.component_type) {
        return -1
      }
      if (a.component_type > b.component_type) {
        return 1
      }
      return 0
    },
    toggleAllCerts: function (checked) {
      this.powder_cert_filter = checked ? this.powder_cert_options.map((obj) => obj.value).slice() : []
    }
  },
  watch: {
    powder_cert_filter: function (newValue, oldValue) {
      // Handle changes in individual flavour checkboxes
      if (newValue.length === 0) {
        this.powderCertIndeterminate = false
        this.allPowderCertSelected = false
      } else if (newValue.length === this.powder_cert_options.length) {
        this.powderCertIndeterminate = false
        this.allPowderCertSelected = true
      } else {
        this.powderCertIndeterminate = true
        this.allPowderCertSelected = false
      }
    }
  },
  computed: {
    filterActive: function () {
      if (this.type_filter !== 'all') {
        return true
      }
      return false
    },
    searchComponents: function () {
      const searched = []
      if (this.search_query) {
        const list = Object.values(this.components_data)
        list.forEach(component => {
          if (component.Component_Names[0].component_name.toLowerCase().includes(this.search_query.toLowerCase())) {
            searched.push(component)
          }
        })
        return searched.sort(this.compare)
      } else {
        return Object.values(this.components_data).sort(this.compare)
      }
    },
    filterComponentTypes: function () {
      const filtered = []

      if (this.type_filter === 'all') {
        return Object.values(this.searchComponents).sort(this.compare)
      }

      this.searchComponents.forEach(component => {
        if (component.component_type === this.type_filter) {
          filtered.push(component)
        }
      })
      return filtered.sort(this.compare)
    },
    filterPowderCerts: function () {
      const filtered = []

      if (this.type_filter === 'all' || this.powder_cert_filter.length === 0) {
        return Object.values(this.filterComponentTypes).sort(this.compare)
      }

      this.filterComponentTypes.forEach(component => {
        this.powder_cert_options.forEach(cert => {
          if (this.powder_cert_filter.includes(cert.value) && component[cert.value]) {
            filtered.push(component)
          }
        })
      })
      return filtered.sort(this.compare)
    }
  },
  created: function () {
    this.getComponentData()
  }
}
</script>
