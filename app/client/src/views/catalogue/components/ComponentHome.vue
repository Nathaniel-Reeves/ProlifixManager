<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query_buff" type="text" class="form-control" placeholder="Search Components..." aria-label="Search Components" aria-describedby="button-addon2" v-on:keyup.enter="search()">
            <div class="input-group-append" v-if="search_query.length > 0">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><b-icon icon="x"></b-icon></button>
            </div>
            <div class="input-group-append" v-else>
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="search()"><b-icon icon="search"></b-icon></button>
            </div>
          </div>

          <!-- <b-form-select v-model="type_filter" :options="type_filter_options"></b-form-select> -->
          <select v-model="type_filter" class="custom-select" id="__BVID__1418">
            <option v-for="option in type_filter_options" :key="option.value" :value="option.value">{{ option.text }}</option>
          </select>

          <!-- <b-form-group class="mt-2" v-show="type_filter === 'powder'">
            <template #label>
              <b>Powder Certification Filter:</b><br>
              <b-form-checkbox v-model="allPowderCertSelected" :indeterminate="powderCertIndeterminate" aria-describedby="powder_cert_options" aria-controls="powder_cert_options" @change="toggleAllCerts">
                {{ allPowderCertSelected ? 'Un-select All' : 'Select All' }}
              </b-form-checkbox>
            </template>

            <template v-slot="{ ariaDescribedby }">
              <b-form-checkbox-group id="powder_cert_filter" v-model="powder_cert_filter" :options="powder_cert_options" name="powder_cert_filter" class="ml-4" aria-label="Individual Certifications" :aria-describedby="ariaDescribedby" stacked></b-form-checkbox-group>
            </template>
          </b-form-group> -->
          <form class="mt-2" v-show="type_filter === 'powder'">
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
          <h2 class="card-title flex-grow-1">Components Catalogue</h2>
          <b-button :to="{ name: 'NewComponent'}" v-b-tooltip.hover title="New Component" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
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
          <b-card no-body class="mb-1" style="box-shadow: 0px 0px;" v-for="component in filteredComponents" :key="component.component_id">
            <b-card-header v-bind:id="'heading' + component.component_id">
              <h2 class="d-flex mb-0">
                <b-button class="text-left" v-b-toggle="'collapse' + component.component_id" @click="populateComponent(component)" variant="light" style="width:100%;">
                  <b-container fluid class="m-0">
                    <b-row align-v="center">
                      <b-col sm="0.5"><b-icon icon="chevron-down"></b-icon></b-col>
                      <b-col sm="1.5"><h4 class="p-2">{{ component.component_type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ') }}</h4></b-col>
                      <b-col sm="4"><h4 class="p-2">{{ component.component_primary_name }}         {{ getBrandName(component) }}</h4></b-col>
                      <b-col><div class="p-2"><CertBadge :data="component"></CertBadge></div></b-col>
                      <b-col sm="0.5"><h3 class="mx-3 my-0"><b-badge class="p-2 align-middle" v-show="!verifySpecs(component)" variant="warning">Incomplete Specs</b-badge></h3></b-col>
                      <b-col  sm="1.5">
                        <router-link :to="{path:`/catalogue/components/${component.component_id}`}"><button type="button" class="btn btn-light ms-auto" style="border-width: 2px; border-color:#999999">View Details</button></router-link>
                      </b-col>
                    </b-row>
                  </b-container>
                </b-button>
              </h2>
            </b-card-header>

            <b-collapse v-bind:id="'collapse' + component.component_id">
              <div v-if="!component.populated">
                <div class="d-flex justify-content-center my-4">
                  <div class="spinner-border text-primary" role="status"></div>
                </div>
              </div>

              <div v-else class="card-body d-flex flex-wrap">

                <!-- Alias Names -->
                <NamesComponent :p-names="component.component_names" naming-type="component" :allow-edit="false"></NamesComponent>
                <hr>

                <!-- Specifications -->
                <div v-if="component.doc.specifications !== undefined">
                  <h3 id="Specifications">Specifications</h3>
                  <div>
                    <p><strong>Spec Issued: </strong>{{ component.doc.specifications.date_issued !== undefined && component.doc.specifications.date_issued !== '' ? new Date(component.doc.specifications.date_issued).toDateString() : "No Spec" }}</p>
                    <p><strong>Spec Revised: </strong>{{ component.doc.specifications.date_revised !== undefined && component.doc.specifications.date_revised !== '' ? new Date(component.doc.specifications.date_revised).toDateString() : "No Spec" }}</p>
                    <p><strong>Revision Number: </strong>{{ component.doc.specifications.revision_number }}</p>
                  </div>
                  <div>
                    <p v-if="component.doc.specifications.description_statement.length > 0"><strong>Component Description</strong><br>{{ component.doc.specifications.description_statement }}</p>
                    <p v-if="component.doc.specifications.origin.length > 0"><strong>Origin</strong><br>{{ component.doc.specifications.origin }}</p>
                    <p v-if="component.doc.specifications.identity_statement.length > 0"><strong>Identity Statement</strong><br>{{ component.doc.specifications.identity_statement }}</p>
                    <p v-if="component.doc.specifications.strength_statement.length > 0"><strong>Strength Statement</strong><br>{{ component.doc.specifications.strength_statement }}</p>
                    <p v-if="component.doc.specifications.purity_statement.length > 0"><strong>Purity Statement</strong><br>{{ component.doc.specifications.purity_statement }}</p>
                    <p v-if="component.doc.specifications.parts_used.length > 0"><strong>Parts Used</strong><br>{{ component.doc.specifications.parts_used }}</p>
                  </div>
                </div>

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
// import FacilitiesGrid from './components/FacilitiesGrid.vue'
import CertBadge from '../../../components/CertBadge.vue'
import NamesComponent from './NamesComponent.vue'

export default {
  name: 'ComponentsHome',
  components: {
    CertBadge,
    NamesComponent
  },
  props: {
    type: {
      default: 'all',
      type: String
    }
  },
  data: function () {
    return {
      components_data: {},
      search_query: '',
      search_query_buff: '',
      loaded: false,
      type_filter: this.type,
      fetched_all_components: this.type === 'all',
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
    verifySpecs: function (component) {
      if (component.component_type !== 'powder') { return true }
      return (
        component.doc.specifications?.revision_number > 0 &&
        component.doc.specifications?.specs.microbiological.revision_number > 0 &&
        component.doc.specifications?.specs.heavy_metals.revision_number > 0 &&
        component.doc.specifications?.specs.organoleptic.revision_number > 0 &&
        component.doc.specifications?.specs.microscopic.revision_number > 0
      )
    },
    clearSearch: function () {
      this.search_query = ''
      this.search_query_buff = ''
    },
    search: function () {
      this.search_query = this.search_query_buff
    },
    getPrimaryName: function (component) {
      if (component.component_names !== undefined && component.component_names.length > 0) {
        for (let i = 0; i < component.component_names.length; i++) {
          if (component.component_names[i].primary_name) {
            return component.component_names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    getBrandName: function (component) {
      if (component.Organization_Names !== undefined && component.Organization_Names.length > 0) {
        for (let i = 0; i < component.Organization_Names.length; i++) {
          if (component.Organization_Names[i].primary_name) {
            return component.Organization_Names[i].organization_name
          }
        }
      }
      return ''
    },
    getComponentData: function () {
      let fetchRequest = this.$root.getOrigin() + '/api/v1/catalogue/components/?doc=true&populate=component_names'
      if (this.type_filter !== 'all') {
        fetchRequest += '&type=' + this.type_filter
      } else {
        this.fetched_all_components = true
      }
      // eslint-disable-next-line
      console.log(
        'GET ' + fetchRequest
      )
      this.loaded = false
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.components_data = data.data
            // eslint-disable-next-line
            console.log(this.components_data)
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
    populateComponent: function (component) {
      if (component.populated) {
        return
      }
      const fetchRequest = this.$root.getOrigin() + '/api/v1/catalogue/components?doc=true&populate=component_names&component-id=' + component.component_id
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
            const t = data.data[0]
            t.populated = true
            console.log(t)
            const index = this.components_data.findIndex((c) => c.component_id === t.component_id)
            this.components_data[index] = t
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
    componentType: function (a, b) {
      if (a.component_type < b.component_type) {
        return -1
      }
      if (a.component_type > b.component_type) {
        return 1
      }
      return 0
    },
    alphabetical: function (a, b) {
      // const aPrime = this.getPrimaryName(a)
      // const bPrime = this.getPrimaryName(b)
      const aPrime = a.component_primary_name
      const bPrime = b.component_primary_name
      if (aPrime < bPrime) {
        return -1
      }
      if (aPrime > bPrime) {
        return 1
      }
      return 0
    },
    toggleAllCerts: function (checked) {
      this.powder_cert_filter = checked ? this.powder_cert_options.map((obj) => obj.value).slice() : []
    },
    searchFilter: function (component) {
      if (component.component_names !== undefined && component.component_names.length > 0) {
        for (let i = 0; i < component.component_names.length; i++) {
          if (component.component_names[i].component_name.toLowerCase().includes(this.search_query.toLowerCase())) {
            return true
          }
        }
      }
      return false
      // return component.component_primary_name.toLowerCase().includes(this.search_query.toLowerCase())
    },
    componentTypeFilter: function (component) {
      if (component.component_type === this.type_filter) {
        return true
      }
      return false
    },
    certFilter: function (component) {
      let flag = false
      for (let i = 0; i < this.powder_cert_options.length; i++) {
        if (component[this.powder_cert_options[i].value] && this.powder_cert_filter.includes(this.powder_cert_options[i].value)) { flag = true }
      }
      return flag
    }
  },
  watch: {
    search_query_buff: function (newValue, oldValue) {
      if (newValue.length === 0) {
        this.search_query = ''
      }
    },
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
    },
    type_filter: function (newValue, oldValue) {
      if (this.fetch_all_components) {
        return
      }
      this.loaded = false
      this.getComponentData()
    },
    type: function (newValue, oldValue) {
      this.type_filter = newValue
    }
  },
  computed: {
    filterActive: function () {
      if (this.type_filter !== 'all' || this.search_query.length > 0) {
        return true
      }
      return false
    },
    filteredComponents: function () {
      let list = Object.values(structuredClone(this.components_data))
      if (this.search_query.length > 0) {
        list = list.filter(this.searchFilter)
      }
      if (this.type_filter === 'powder' && this.powder_cert_filter.length > 0) {
        list = list.filter(this.certFilter)
      } else if (this.type_filter !== 'all') {
        list = list.filter(this.componentTypeFilter)
      }
      list = list.sort(this.alphabetical).sort(this.componentType)
      return list
    }
  },
  created: function () {
    this.getComponentData()
  }
}
</script>
