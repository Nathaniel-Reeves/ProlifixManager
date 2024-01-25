<template>
  <div class="components">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query" type="text" class="form-control" placeholder="Search Components..."
              aria-label="Search Components" aria-describedby="button-addon2">
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><i
                class="bi bi-x"></i></button>
            </div>
          </div>

          <div v-for="filter in all_filters" :key="filter.f_name">
            <div class="input-group mb-3">
              <div class="input-group-prepend">
                <div class="input-group-text">
                  <input type="checkbox" :aria-label="filter.f_name" v-model="filter.filter_state">
                </div>
              </div>
              <label class="form-control" :aria-label="filter.f_name">{{ filter.display_name }}</label>
            </div>
          </div>

        </div>
      </b-sidebar>
    </div>

    <div class="card m-2">
      <div class="card-body">
        <div class="input-group d-flex">
          <h2 class="card-title flex-grow-1">Components Catalogue</h2>
          <b-button v-b-tooltip.hover title="New Component" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', filterActive ? 'btn-info' : 'btn-light']" type="button"
                id="button-addon2">
            <i class="bi bi-plus-lg"></i>
          </b-button>
          <b-button v-b-tooltip.hover title="Filter" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', filterActive ? 'btn-info' : 'btn-light']" type="button"
              id="button-addon2">
            <i class="bi bi-filter"></i>
          </b-button>
        </div>

          <div v-show="!loaded">
            <div class="d-flex justify-content-center">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
          </div>

          <div v-show="loaded" class="accordion overflow-auto border-top border-bottom" id="accordionExample" style="height:100vh;">
            <div class="card" v-for="component in filterComponents" :key="component.component_id">
              <div class="card-header" v-bind:id="'heading' + component.component_id">
                <h2 class="d-flex flex-row mb-0">
                  <button class="btn btn-block text-left" type="button" data-toggle="collapse"
                    v-bind:data-target="'#collapse' + component.component_id" aria-expanded="false"
                    v-bind:aria-controls="'collapse' + component.component_id" v-on:click="populateComponent(component.component_id)">
                    <b-container fluid class="d-flex justify-content-start flex-wrap">
                      <i class="bi bi-chevron-down p-2"></i>
                      <div class="p-2">{{ component.component_type.replace("_", " ").toLowerCase()
                        .split(' ')
                        .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
                        .join(' ') }}</div>
                      <div class="p-2">{{ get_comopnent_primary_name(component) }}</div>
                      <div class="p-2" v-show="component.certified_usda_organic">Certified Organic</div>
                      <div class="p-2">{{ get_component_brand_name(component) }}</div>
                    </b-container>
                  </button>
                  <b-container fluid class="d-flex justify-content-end flex-wrap" style="max-width:10rem;">
                    <button type="button" class="btn btn-light ms-auto" style="border-width: 2px; border-color:#999999">View Details</button>
                  </b-container>
                </h2>
              </div>

              <div v-bind:id="'collapse' + component.component_id" class="collapse" v-bind:aria-labelledby="'heading' + component.component_id"
                data-parent="#accordionExample">
                <div class="card-body d-flex flex-wrap">

                  <!-- <div class="p-2" v-if="component.hasOwnProperty('Facilities')" v-show="Object.keys(component.Facilities).length !== 0">
                    <h5>Facilities</h5>
                    <FacilitiesGrid v-bind:Facilities="component.Facilities"></FacilitiesGrid>
                  </div> -->

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.components {
  width: 95%;
}
</style>

<script>
// import FacilitiesGrid from './components/FacilitiesGrid.vue'

export default {
  name: 'ComponentsHome',
  data: function () {
    return {
      components_data: {},
      search_query: '',
      loaded: false,
      all_filters: [
        {
          f_name: 'powder_filter',
          name: 'powder',
          display_name: 'Powders',
          filter_state: this.powder_filter_prop
        },
        {
          f_name: 'liquid_filter',
          name: 'liquid',
          display_name: 'Liquids',
          filter_state: this.liquid_filter_prop
        },
        {
          f_name: 'container_filter',
          name: 'container',
          display_name: 'Containers',
          filter_state: this.container_filter_prop
        },
        {
          f_name: 'pouch_filter',
          name: 'pouch',
          display_name: 'Pouches',
          filter_state: this.pouch_filter_prop
        },
        {
          f_name: 'shrink_band_filter',
          name: 'shrink_band',
          display_name: 'Shrink Bands',
          filter_state: this.shrink_filter_prop
        },
        {
          f_name: 'lid_filter',
          name: 'lid',
          display_name: 'Lids',
          filter_state: this.lid_filter_prop
        },
        {
          f_name: 'label_filter',
          name: 'label',
          display_name: 'Labels',
          filter_state: this.label_filter_prop
        },
        {
          f_name: 'capsule_filter',
          name: 'capsule',
          display_name: 'Capsules',
          filter_state: this.capsule_filter_prop
        },
        {
          f_name: 'misc_filter',
          name: 'misc',
          display_name: 'Miscellaneous',
          filter_state: this.misc_filter_prop
        },
        {
          f_name: 'scoop_filter',
          name: 'scoop',
          display_name: 'Scoops',
          filter_state: this.scoop_filter_prop
        },
        {
          f_name: 'desiccant_filter',
          name: 'desiccant',
          display_name: 'Desiccants',
          filter_state: this.desiccant_filter_prop
        },
        {
          f_name: 'box_filter',
          name: 'box',
          display_name: 'Boxes',
          filter_state: this.box_filter_prop
        },
        {
          f_name: 'carton_filter',
          name: 'carton',
          display_name: 'Cartons',
          filter_state: this.carton_filter_prop
        },
        {
          f_name: 'packaging_material_filter',
          name: 'packaging_material',
          display_name: 'Packaging Materials',
          filter_state: this.packaging_material_filter_prop
        }
      ]
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
    }
  },
  computed: {
    filterActive: function () {
      let state = false
      for (let i = 0; i < this.all_filters.length; i++) {
        if (this.all_filters[i].filter_state) {
          state = true
        }
      }
      return state
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
    filterComponents: function () {
      const filtered = []
      if (
        this.filterActive
      ) {
        const list = Object.values(this.searchComponents)
        const filteredTypes = []
        for (let i = 0; i < this.all_filters.length; i++) {
          if (this.all_filters[i].filter_state) {
            filteredTypes.push(this.all_filters[i].name)
          }
        }

        console.log(filteredTypes)

        list.forEach(component => {
          if (filteredTypes.includes(component.component_type)) {
            filtered.push(component)
          }
        })
        return filtered.sort(this.compare)
      } else {
        return Object.values(this.searchComponents).sort(this.compare)
      }
    }
  },
  created: function () {
    this.getComponentData()
  },
  props: {
    powder_filter_prop: Boolean,
    liquid_filter_prop: Boolean,
    container_filter_prop: Boolean,
    pouch_filter_prop: Boolean,
    shrink_band_filter_prop: Boolean,
    lid_filter_prop: Boolean,
    label_filter_prop: Boolean,
    capsule_filter_prop: Boolean,
    misc_filter_prop: Boolean,
    scoop_filter_prop: Boolean,
    desiccant_filter_prop: Boolean,
    box_filter_prop: Boolean,
    carton_filter_prop: Boolean,
    packaging_material_filter_prop: Boolean
  }
  // components: {
  //     FacilitiesGrid,
  // }
}
</script>
