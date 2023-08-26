<template>
  <div class="organizations">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query" type="text" class="form-control" placeholder="Search Organizations..."
              aria-label="Search Organizations" aria-describedby="button-addon2">
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><i class="bi bi-x"></i></button>
            </div>
          </div>
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <input type="checkbox" aria-label="clients_filter" v-model="clients_filter">
              </div>
            </div>
            <label class="form-control" aria-label="clients_filter">Clients</label>
          </div>
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <input type="checkbox" aria-label="suppliers_filter" v-model="suppliers_filter">
              </div>
            </div>
            <label class="form-control" aria-label="suppliers_filter">Suppliers</label>
          </div>
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <input type="checkbox" aria-label="labs_filter" v-model="labs_filter">
              </div>
            </div>
            <label class="form-control" aria-label="labs_filter">Labs</label>
          </div>
        </div>
      </b-sidebar>
    </div>

    <div class="card m-2">
      <div class="card-body">
        <div class="input-group d-flex justify-content-between">
          <h2 class="card-title mr-2">Organizations</h2>
            <b-button v-b-toggle.sidebar-right v-bind:class="['btn', 'my-2', filterActive ? 'btn-info' : 'btn-light']" type="button" id="button-addon2">
              <i class="bi bi-filter"></i>
            </b-button>
        </div>

        <div v-show="!loaded">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>

        <div v-show="loaded" class="accordion overflow-auto border-top border-bottom" id="accordionExample" style="height:100vh;">
          <div class="card" v-for="org in filterOrganizations" :key="org.organization_id">
            <div class="card-header" v-bind:id="'heading' + org.organization_id">
              <h2 class="mb-0">
                <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse"
                  v-bind:data-target="'#collapse' + org.organization_id" aria-expanded="false"
                  v-bind:aria-controls="'collapse' + org.organization_id" v-on:click="populateOrg(org.organization_id)">
                  {{ org.organization_name }}
                </button>
              </h2>
            </div>

            <div v-bind:id="'collapse' + org.organization_id" class="collapse"
              v-bind:aria-labelledby="'heading' + org.organization_id" data-parent="#accordionExample">
              <div class="card-body d-flex flex-wrap">

                <div class="p-2" v-if="org.hasOwnProperty('facilities')" v-show="Object.keys(org.facilities).length !== 0">
                  <h5>Facilities</h5>
                  <FacilitiesGrid v-bind:facilities="org.facilities"></FacilitiesGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('sales_orders')" v-show="Object.keys(org.sales_orders).length !== 0">
                  <h5>Sales Orders</h5>
                  <SalesOrdersGrid v-bind:sales_orders="org.sales_orders"></SalesOrdersGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('purchase_orders')" v-show="Object.keys(org.purchase_orders).length !== 0">
                  <h5>Purchase Orders</h5>
                  <PurchaseOrdersGrid v-bind:purchase_orders="org.purchase_orders"></PurchaseOrdersGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('people')" v-show="Object.keys(org.people).length !== 0">
                  <h5>People</h5>
                  <PeopleGrid v-bind:people="org.people"></PeopleGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('components')" v-show="Object.keys(org.components).length !== 0">
                  <h5>Components</h5>
                  <ComponentsGrid v-bind:components="org.components"></ComponentsGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('products')" v-show="Object.keys(org.products).length !== 0">
                  <h5>Products</h5>
                  <ProductsGrid v-bind:products="org.products"></ProductsGrid>
                </div>

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
import FacilitiesGrid from './components/FacilitiesGrid.vue'
import SalesOrdersGrid from './components/SalesOrdersGrid.vue'
import PurchaseOrdersGrid from './components/PurchaseOrdersGrid.vue'
import PeopleGrid from './components/PeopleGrid.vue'
import ComponentsGrid from './components/ComponentsGrid.vue'
import ProductsGrid from './components/ProductsGrid.vue'

export default {
  name: 'OrganizationsHome',
  data: function () {
    return {
      org_data: [],
      search_query: '',
      loaded: false,
      clients_filter: this.clients_filter_prop,
      suppliers_filter: this.suppliers_filter_prop,
      labs_filter: this.labs_filter_prop
    }
  },
  methods: {
    clearSearch: function () {
      this.search_query = ''
    },
    populateOrg: function (orgId) {
      const fetchRequest = window.origin + '/api/organizations?org-id=' + orgId + '&populate=facilities&populate=sales-orders&populate=purchase-orders&populate=people&populate=components&populate=products'
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': [
            'http://localhost:3000',
            'http://127.0.0.1:3000'
          ]
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.org_data[orgId] = Object.values(data.data[0])[0]
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    },
    getOrgData: function () {
      const fetchRequest = window.origin + '/api/organizations'
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': [
            'http://localhost:3000',
            'http://127.0.0.1:3000'
          ]
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.org_data = data.data[0]
            console.log(this.org_data)
            this.loaded = true
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    },
    compare: function (a, b) {
      if (a.organization_name < b.organization_name) {
        return -1
      }
      if (a.organization_name > b.organization_name) {
        return 1
      }
      return 0
    }
  },
  computed: {
    filterActive: function () {
      return this.clients_filter || this.suppliers_filter || this.labs_filter || this.search_query
    },
    searchOrganizations: function () {
      const searched = []
      if (
        this.search_query
      ) {
        const list = Object.values(this.org_data)
        list.forEach(org => {
          if (
            org.organization_name.toLowerCase().includes(this.search_query.toLowerCase()) ||
            org.organization_initial.toLowerCase().includes(this.search_query.toLowerCase())
          ) {
            searched.push(org)
          }
        })
        return searched.sort(this.compare)
      } else {
        return Object.values(this.org_data).sort(this.compare)
      }
    },
    filterOrganizations: function () {
      const filtered = []
      if (
        this.clients_filter ||
        this.suppliers_filter ||
        this.labs_filter
      ) {
        const list = Object.values(this.searchOrganizations)
        list.forEach(org => {
          if (
            (org.supplier & this.suppliers_filter) ||
            (org.client & this.clients_filter) ||
            (org.lab & this.labs_filter)
          ) {
            filtered.push(org)
          }
        })
        return filtered.sort(this.compare)
      } else {
        return Object.values(this.searchOrganizations).sort(this.compare)
      }
    }
  },
  created: function () {
    this.getOrgData()
  },
  props: {
    clients_filter_prop: Boolean,
    suppliers_filter_prop: Boolean,
    labs_filter_prop: Boolean
  },
  components: {
    FacilitiesGrid,
    SalesOrdersGrid,
    PurchaseOrdersGrid,
    PeopleGrid,
    ComponentsGrid,
    ProductsGrid
  }
}
</script>
