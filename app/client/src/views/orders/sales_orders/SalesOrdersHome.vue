<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query_buff" type="text" class="form-control" placeholder="Search Sale Orders..." aria-label="Search Sale Orders" aria-describedby="button-addon2" v-on:keyup.enter="search()">
            <div class="input-group-append" v-if="search_query.length > 0">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="clearSearch()"><b-icon icon="x"></b-icon></button>
            </div>
            <div class="input-group-append" v-else>
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="search()"><b-icon icon="search"></b-icon></button>
            </div>
          </div>

        </div>
      </b-sidebar>
    </div>

    <div class="card my-2">
      <div class="card-body">
        <div class="input-group d-flex">
          <h2 class="card-title flex-grow-1">Sales</h2>
          <b-button disabled :to="{ name: 'NewSaleOrder'}" v-b-tooltip.hover title="New Order" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
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

        <div v-show="loaded">
          <b-table striped hover :items="orders" :fields="fields" show-empty responsive stacked="md" sticky-header outlined>
            <template #empty>
              <div class="d-flex justify-content-center">
                <h4>No orders yet!  Add some by clicking the '+' button above.</h4>
              </div>
            </template>
            <template #emptyfiltered>
              <div class="d-flex justify-content-center">
                <h4>No orders match your filters.</h4>
              </div>
            </template>
          </b-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SalesOrdersHome',
  data: function () {
    return {
      loaded: true,
      search_query_buff: '',
      search_query: '',
      orders: [
      ],
      fields: [
        { key: 'prefix', label: 'Pre', sortable: true },
        { key: 'year', label: 'Y', sortable: true },
        { key: 'month', label: 'M', sortable: true },
        { key: 'sec_number', label: 'Sec #', sortable: true },
        { key: 'suffix', label: 'Suf', sortable: true },
        { key: 'client_po_num', label: 'Client PO', sortable: true },
        { key: 'organization_primary_name', label: 'Client', sortable: true },
        { key: 'organization_primary_initial', label: 'CI', sortable: true },
        { key: 'order_date', label: 'Date Ordered', sortable: true },
        { key: 'target_completion_date', label: 'Due Date', sortable: true },
        { key: 'completion_date', label: 'Finished', sortable: true },
        { key: 'closed_date', label: 'Closed on', sortable: true },
        { key: 'actions', label: 'Actions' }
      ]
    }
  },
  computed: {
    filterActive: function () {
      if (this.search_query.length > 0) {
        return true
      }
      return false
    }
  },
  methods: {
    clearSearch: function () {
      this.search_query = ''
      this.search_query_buff = ''
    },
    search: function () {
      this.search_query = this.search_query_buff
    }
  }
}
</script>

<style scoped>
.my_component {
    width: 90%;
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
