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
          <b-button v-show="hide" :disabled="isMd" v-b-tooltip.hover title="Show All Columns" @click="hide = false" style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', 'btn-light']" type="button" id="button-addon2">
            <b-icon icon="eye-fill"></b-icon>
          </b-button>
          <b-button v-show="!hide" :disabled="isMd" v-b-tooltip.hover title="Hide PO Columns" @click="hide = true" style="border-width: 2px; border-color:#999999" v-bind:class="['btn', 'my-2', 'mx-1', 'btn-light']" type="button" id="button-addon2">
            <b-icon icon="eye-slash-fill"></b-icon>
          </b-button>
        </div>

        <div v-show="!loaded">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>

        <div v-show="loaded">
          <div
            v-b-visible="handleVisible"
            class="position-fixed d-block d-lg-none"
            style="z-index: 20000; height: 1px;"
          ></div>
          <b-table primary-key="" striped hover :items="orders" v-model="orders" :fields="hide || isMd ? fields_hidden : fields_show" show-empty responsive stacked="md" small no-border-collapse sticky-header outlined>
            <template #cell(actions)="row">
              <b-button size="sm" @click="row.toggleDetails" class="btn-light" style="border-width: 2px; border-color:#999999" v-b-tooltip.hover title="Peek Order Details">
                <b-icon v-show="row.detailsShowing" icon="chevron-up"></b-icon>
                <b-icon v-show="!row.detailsShowing" icon="chevron-down"></b-icon>
              </b-button>
              <b-button size="sm ml-2"  class="btn-light" style="border-width: 2px; border-color:#999999" v-b-tooltip.hover title="Go to Order Page">
                <b-icon icon="box"></b-icon>
              </b-button>
              <b-button size="sm ml-2" @click="info(row.item, row.index, $event.target)" v-b-tooltip.hover title="Quick Edit" class="btn-light" style="border-width: 2px; border-color:#999999">
                <b-icon icon="pencil-square"></b-icon>
              </b-button>
            </template>
            <template #row-details="row">
              <b-card class="no-shaddow">
                <ul>
                  <li v-for="(value, key) in row.item" :key="key">{{ key }}: {{ value }}</li>
                </ul>
              </b-card>
            </template>
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
          <!-- Info modal -->
          <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
            <pre>{{ infoModal.content }}</pre>
          </b-modal>
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
      hide: true,
      isMd: false,
      orders: [
      ],
      fields_hidden: [
        { key: 'pk', label: 'SO#', sortable: true },
        { key: 'client_po_num', label: 'Client PO', sortable: true },
        { key: 'organization_primary_name', label: 'Client', sortable: true },
        { key: 'organization_primary_initial', label: 'CI', sortable: true },
        { key: 'order_date', label: 'Date Ordered', sortable: true },
        { key: 'target_completion_date', label: 'ETA', sortable: true },
        { key: 'completion_date', label: 'Finished', sortable: true },
        { key: 'closed_date', label: 'Closed on', sortable: true },
        { key: 'actions', label: 'Actions' }
      ],
      fields_show: [
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
      ],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: ''
      }
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
    info: function (item, index, button) {
      this.infoModal.title = `Row index: ${index}`
      this.infoModal.content = JSON.stringify(item, null, 2)
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    resetInfoModal: function () {
      this.infoModal.title = ''
      this.infoModal.content = ''
    },
    clearSearch: function () {
      this.search_query = ''
      this.search_query_buff = ''
    },
    search: function () {
      this.search_query = this.search_query_buff
    },
    handleVisible: function (isVisible) {
      this.isMd = isVisible
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
