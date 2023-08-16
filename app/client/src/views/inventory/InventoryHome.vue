<template>
  <div class="inventory">
    <div>
      <b-sidebar id="sidebar-right" title="Filter filters" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query" type="text" class="form-control" placeholder="Search Inventory..."
              aria-label="Search Inventory" aria-describedby="button-addon2">
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><i class="bi bi-x"></i></button>
            </div>
          </div>

          <!-- item_type filter selectors -->
          <h5>Product Type Filters</h5>
            <table>
                <tr>
                    <th><b-form-checkbox v-model="selectAll" switch>
                        All
                    </b-form-checkbox></th>
                </tr>
                <tr v-for="filter in filters" v-bind:key="filter.value">
                    <td>
                        <b-form-checkbox v-model="productTypeSelected" :value="filter.value" switch>
                            {{ filter.text }}
                        </b-form-checkbox>
                    </td>
                </tr>
            </table>

        </div>
      </b-sidebar>
    </div>

    <div class="card m-2">
      <div class="card-body">
        <div class="input-group d-flex justify-content-between">
          <h2 class="card-title mr-2">Inventory</h2>
            <b-button v-b-toggle.sidebar-right v-bind:class="['btn', 'my-2', filterActive ? 'btn-info' : 'btn-light']" type="button" id="button-addon2">
              <i class="bi bi-filter"></i>
            </b-button>
        </div>

        <div v-show="!loaded">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>

        <p>{{ productTypeSelected }}</p>

        <InventoryGrid v-bind:inventory="inv_data"></InventoryGrid>

      </div>
    </div>
  </div>
</template>

<style scoped>
.inventory {
    width: 95%;
}
</style>

<script>
import InventoryGrid from './components/InventoryGrid.vue'

export default {
  name: 'InventoryHome',
  data () {
    return {
      inv_data: [],
      filtered_inv_data: [],
      search_query: '',
      productTypeSelected: [
        'products',
        'powders',
        'liquids',
        'containers',
        'pouches',
        'shrink_bands',
        'lids',
        'labels',
        'capsules',
        'misc',
        'scoops',
        'desiccants',
        'boxes',
        'cartons',
        'packaging_materials'
      ],
      filters: [
        { text: 'Products', value: 'products' },
        { text: 'Powders', value: 'powders' },
        { text: 'Liquids', value: 'liquids' },
        { text: 'Containers', value: 'containers' },
        { text: 'Pouches', value: 'pouches' },
        { text: 'Shrink Bands', value: 'shrink_bands' },
        { text: 'Lids', value: 'lids' },
        { text: 'Labels', value: 'labels' },
        { text: 'Capsules', value: 'capsules' },
        { text: 'Misc', value: 'misc' },
        { text: 'Scoops', value: 'scoops' },
        { text: 'Desiccants', value: 'desiccants' },
        { text: 'Boxes', value: 'boxes' },
        { text: 'Cartons', value: 'cartons' },
        { text: 'Packaging Materials', value: 'packaging_materials' }
      ]
    }
  },
  methods: {
    clearSearch () {
      this.search_query = ''
    },
    fetchInventoryData () {
      const fetchRequest = window.origin + '/api/inventory'
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.inv_data = data.data[0]
            console.log(this.inv_data)
            this.loaded = true
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    }
  },
  computed: {
    filterActive: function () {
      return this.search_query.length > 0
    },
    selectAll: {
      get: function () {
        return this.filters ? this.productTypeSelected.length === this.filters.length : false
      },
      set: function (value) {
        const productTypeSelected = []

        if (value) {
          this.filters.forEach(function (filter) {
            productTypeSelected.push(filter.value)
          })
        }

        this.productTypeSelected = productTypeSelected
      }
    }
  },
  components: {
    InventoryGrid
  },
  created: function () {
    this.fetchInventoryData()
  }
}

</script>
