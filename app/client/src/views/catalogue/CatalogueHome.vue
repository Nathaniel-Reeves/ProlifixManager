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
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <input type="checkbox" aria-label="powder_filter" v-model="powder_filter">
              </div>
            </div>
            <label class="form-control" aria-label="powder_filter">Powders</label>
          </div>
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <input type="checkbox" aria-label="liquid_filter" v-model="liquid_filter">
              </div>
            </div>
            <label class="form-control" aria-label="liquid_filter">Liquids</label>
          </div>
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <input type="checkbox" aria-label="container_filter" v-model="container_filter">
              </div>
            </div>
            <label class="form-control" aria-label="container_filter">Containers</label>
          </div>
        </div>
      </b-sidebar>
    </div>

    <div class="card m-2">
      <div class="card-body">
        <div class="input-group d-flex justify-content-between">
          <h2 class="card-title mr-2">Components</h2>
            <b-button v-b-toggle.sidebar-right v-bind:class="['btn', 'my-2', filterActive ? 'btn-info' : 'btn-light']" type="button"
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
                <h2 class="mb-0">
                  <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse"
                    v-bind:data-target="'#collapse' + component.component_id" aria-expanded="false"
                    v-bind:aria-controls="'collapse' + component.component_id" v-on:click="populateOrg(org.organization_id)">
                    {{ component.component_id }}
                  </button>
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
.organizations {
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
      powder_filter: this.powder_filter_prop,
      liquid_filter: this.liquid_filter_prop,
      container_filter: this.container_filter_prop
    }
  },
  methods: {
    clearSearch: function () {
      this.search_query = ''
    },
    populateComponent: function (componentId) {
      const fetchRequest = window.origin + '/api/v1/catalogue/components/?component-id=' + componentId
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
      const fetchRequest = window.origin + '/api/v1/catalogue/components'
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
      if (a.Component_Names[0].component_name < b.Component_Names[0].component_name) {
        return -1
      }
      if (a.Component_Names[0].component_name > b.Component_Names[0].component_name) {
        return 1
      }
      return 0
    }
  },
  computed: {
    filterActive: function () {
      return this.powder_filter || this.liquid_filter || this.container_filter || this.search_query
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
        this.powder_filter ||
        this.liquid_filter ||
        this.container_filter
      ) {
        const list = Object.values(this.searchComponents)
        list.forEach(component => {
          if (
            component.component_type === 'powder'
          ) {
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
    container_filter_prop: Boolean
  }
  // components: {
  //     FacilitiesGrid,
  // }
}
</script>
