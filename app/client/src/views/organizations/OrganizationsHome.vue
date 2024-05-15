<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query" type="text" class="form-control" placeholder="Search Organizations..."
              aria-label="Search Organizations" aria-describedby="button-addon2">
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><b-icon icon="x"></b-icon></button>
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
        <div class="input-group d-flex">
          <h2 class="card-title flex-grow-1">Organizations</h2>
          <b-button disabled title="New Organization" style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', 'btn-light']" type="button"
                id="button-addon2">
            <b-icon icon="plus"></b-icon>
          </b-button>
          <b-button v-b-tooltip.hover title="Filter" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', filterActive ? 'btn-info' : 'btn-light']" type="button"
              id="button-addon2">
            <b-icon icon="filter"></b-icon>
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
              <h2 class="d-flex flex-row mb-0">
                <button class="btn btn-block text-left" type="button" data-toggle="collapse"
                  v-bind:data-target="'#collapse' + org.organization_id" aria-expanded="false"
                  v-bind:aria-controls="'collapse' + org.organization_id" v-on:click="populateOrg(org.organization_id)">
                  <b-container fluid class="d-flex justify-content-start flex-wrap">
                      <b-icon icon="chevron-down"></b-icon>
                      <div class="p-2">{{ org.Organization_Names[0].organization_name }}</div>
                    </b-container>
                </button>
                <b-container fluid class="d-flex justify-content-end flex-wrap" style="max-width:10rem;">
                  <button disabled type="button" class="btn btn-light ms-auto" style="border-width: 2px; border-color:#999999">View Details</button>
                </b-container>
              </h2>
            </div>

            <div v-bind:id="'collapse' + org.organization_id" class="collapse"
              v-bind:aria-labelledby="'heading' + org.organization_id" data-parent="#accordionExample">
              <div v-show="!org.populated" class="d-flex justify-content-center">
                <div v-show="!org.populated" class="spinner-border text-primary mt-3" role="status"></div>
              </div>
              <div class="card-body d-flex flex-wrap">

                <div class="p-2" v-if="org.hasOwnProperty('Facilities')" v-show="Object.keys(org.Facilities).length !== 0">
                  <h5>Facilities</h5>
                  <FacilitiesGrid v-bind:Facilities="org.Facilities"></FacilitiesGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('Sales_Orders')" v-show="Object.keys(org.Sales_Orders).length !== 0">
                  <h5>Sales Orders</h5>
                  <SalesOrdersGrid v-bind:Sales_Orders="org.Sales_Orders"></SalesOrdersGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('Purchase_Orders')" v-show="Object.keys(org.Purchase_Orders).length !== 0">
                  <h5>Purchase Orders</h5>
                  <PurchaseOrdersGrid v-bind:Purchase_Orders="org.Purchase_Orders"></PurchaseOrdersGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('People')" v-show="Object.keys(org.People).length !== 0">
                  <h5>People</h5>
                  <PeopleGrid v-bind:People="org.People"></PeopleGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('Components')" v-show="Object.keys(org.Components).length !== 0">
                  <h5>Components</h5>
                  <ComponentsGrid v-bind:Components="org.Components" v-bind:Component_Names="org.Component_Names"></ComponentsGrid>
                </div>
                <div class="p-2" v-if="org.hasOwnProperty('Products')" v-show="Object.keys(org.Products).length !== 0">
                  <h5>Products</h5>
                  <ProductsGrid v-bind:Products="org.Products"></ProductsGrid>
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
import FacilitiesGrid from '../../components/FacilitiesGrid.vue'
import SalesOrdersGrid from '../../components/SalesOrdersGrid.vue'
import PurchaseOrdersGrid from '../../components/PurchaseOrdersGrid.vue'
import PeopleGrid from '../../components/PeopleGrid.vue'
import ComponentsGrid from '../../components/ComponentsGrid.vue'
import ProductsGrid from '../../components/ProductsGrid.vue'

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
      if (this.org_data[orgId].populated) {
        return
      }
      // TODO: Fix Component Names and add them to Populate
      const fetchRequest = window.origin + '/api/v1/organizations/?org-id=' + orgId + '&populate=facilities&populate=sales-orders&populate=purchase-orders&populate=people&populate=products'
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
            this.org_data[orgId] = Object.values(data.data[0])[0]
            this.org_data[orgId].populated = true
          })
        } else if (response.status === 404) {
          this.org_data[orgId].populated = true
          const errorToast = {
            title: `'${this.org_data[orgId].Organization_Names[0].organization_name}' 404 Not Found.`,
            message: 'Looks like there is no additional data to see here.',
            variant: 'info',
            visible: true,
            noCloseButton: true,
            noAutoHide: false,
            autoHideDelay: 1.5,
            appendToast: true,
            solid: true,
            toaster: 'b-toaster-bottom-right'
          }
          const createToast = this.$root.createToast
          createToast(errorToast)
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          this.org_data[orgId].populated = true
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    },
    getOrgData: function () {
      const fetchRequest = window.origin + '/api/v1/organizations'
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
            this.org_data = data.data[0]
            for (let i = 0; i < this.org_data.length; i++) {
              this.org_data[i].populated = false
            }
            // eslint-disable-next-line
            console.log(this.org_data)
            this.loaded = true
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
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
            org.Organization_Names[0].organization_name.toLowerCase().includes(this.search_query.toLowerCase()) ||
            org.Organization_Names[0].organization_initial.toLowerCase().includes(this.search_query.toLowerCase())
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
