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
          <b-button v-b-tooltip.hover title="New Order" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
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
          <b-table primary-key="" striped hover :items="orders" v-model="orders" :fields="hide || isMd ? fields_hidden : fields_show" show-empty sticky-header="80vh" small no-border-collapse outlined sort-icon-left sort-null-last :sort-compare="sortCompare">
            <template #cell(actions)="row">
              <div class="d-flex flex-row flex-nowrap">
                <b-button @click="row.toggleDetails();populateSale(row.item.so_id)" size="sm" class="btn-light" style="border-width: 2px; border-color:#999999" v-b-tooltip.hover title="Peek Order Details">
                  <b-icon v-show="row.detailsShowing" icon="chevron-up"></b-icon>
                  <b-icon v-show="!row.detailsShowing" icon="chevron-down"></b-icon>
                </b-button>
                <b-button size="sm ml-2"  class="btn-light" style="border-width: 2px; border-color:#999999" v-b-tooltip.hover title="Go to Order Page">
                  <b-icon icon="box"></b-icon>
                </b-button>
                <b-button size="sm ml-2" @click="info(row.item, row.index, $event.target)" v-b-tooltip.hover title="Quick Edit" class="btn-light" style="border-width: 2px; border-color:#999999">
                  <b-icon icon="pencil-square"></b-icon>
                </b-button>
              </div>
            </template>
            <template #cell(pk)="row">
              {{  formatSONumber(row.item) }}
            </template>
            <template #cell(year)="row">
              {{ row.item?.year ? row.item.year.toString().padStart(2, '0') : '' }}
            </template>
            <template #cell(sec_number)="row">
              {{ row.item?.sec_number ? row.item.sec_number.toString().padStart(3, '0') : '' }}
            </template>
            <template #cell(client_name)="row">
              <router-link class="text-info" v-show="!isMd" :to="'/organizations/'+row.item?.client[0].organization_id" target="_blank">{{ row.item?.client[0].organization_name ? row.item?.client[0].organization_name : '' }}</router-link>
              <router-link class="text-info" v-show="isMd" :to="'/organizations/'+row.item?.client[0].organization_id" target="_blank">{{ row.item?.client[0].organization_initial ? row.item?.client[0].organization_initial : '' }}</router-link>
            </template>
            <template #cell(order_date)="row">
              {{ row.item?.order_date ? new Date(row.item.order_date).toLocaleDateString('en-US') : '' }}
            </template>
            <template #cell(target_completion_date)="row">
              {{ row.item?.target_completion_date ? new Date(row.item.target_completion_date).toLocaleDateString('en-US') : '' }}
            </template>
            <template #cell(completion_date)="row">
              {{ row.item?.completion_date ? new Date(row.item.completion_date).toLocaleDateString('en-US') : '' }}
            </template>
            <template #cell(closed_date)="row">
              {{ row.item?.closed_date ? new Date(row.item.closed_date).toLocaleDateString('en-US') : '' }}
            </template>
            <template #row-details="row">
              <b-card class="no-shaddow">
                <div v-show="row.item.sale_order_detail.length === 0">
                  <div class="d-flex justify-content-center">
                    <div class="spinner-border text-primary" role="status"></div>
                  </div>
                </div>
                <div v-show="row.item.sale_order_detail.length !== 0">
                  <h3>Sale: {{ formatSONumber(row.item) }} Details</h3>
                  <div>
                    <h4>Order Items</h4>
                    <OrderDetailsTable :order-details="row.item.sale_order_detail" />
                  </div>
                  <div>
                    <h4>Order Payments</h4>
                  </div>
                </div>
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
import OrderDetailsTable from './OrderDetailsTable.vue'

export default {
  name: 'SalesOrdersHome',
  components: {
    OrderDetailsTable
  },
  data: function () {
    return {
      loaded: false,
      search_query_buff: '',
      search_query: '',
      hide: true,
      isMd: false,
      orders: [
      ],
      fields_hidden: [
        { key: 'pk', label: 'SO#', sortable: true },
        { key: 'client_po_num', label: 'Client PO', sortable: true },
        { key: 'client_name', label: 'Client', sortable: true },
        { key: 'order_date', label: 'Date Ordered', sortable: true },
        { key: 'target_completion_date', label: 'ETA', sortable: true },
        { key: 'completion_date', label: 'Finished', sortable: true },
        { key: 'closed_date', label: 'Closed on', sortable: true },
        { key: 'actions', label: 'Actions' }
      ],
      fields_show: [
        { key: 'prefix', label: 'Pre', sortable: true },
        { key: 'year', label: 'Y', sortable: true },
        { key: 'sec_number', label: 'Sec #', sortable: true },
        { key: 'suffix', label: 'Suf', sortable: true },
        { key: 'client_po_num', label: 'Client PO', sortable: true },
        { key: 'client_name', label: 'Client', sortable: true },
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
    formatSONumber: function (item) {
      let soNumber = ''
      if (item.prefix) {
        soNumber += item.prefix + ' '
      }
      if (item.year) {
        soNumber += item.year.toString().padStart(2, '0')
      }
      // if (item.month) {
      //   soNumber += item.month.toString().padStart(2, '0')
      // }
      if (item.sec_number) {
        soNumber += '-' + item.sec_number.toString().padStart(3, '0')
      }
      if (item.suffix) {
        soNumber += ' ' + item.suffix
      }
      return soNumber
    },
    sortCompare: function (aRow, bRow, key, sortDesc, formatter, compareOptions, compareLocale) {
      const a = aRow[key] // or use Lodash `_.get()`
      const b = bRow[key]

      // Custom Sorting
      if (key === 'order_date' || key === 'target_completion_date' || key === 'completion_date' || key === 'closed_date') {
        return this.sortDate(a, b)
      }
      if (key === 'client_name') {
        return this.sortClient(aRow, bRow)
      }
      if (key === 'pk') {
        return this.sortSONum(aRow, bRow)
      }

      // Default Boostrap Sorting
      if (
        (typeof a === 'number' && typeof b === 'number') ||
        (a instanceof Date && b instanceof Date)
      ) {
        // If both compared fields are native numbers or both are native dates
        return a < b ? -1 : a > b ? 1 : 0
      } else {
        // Otherwise stringify the field data and use String.prototype.localeCompare
        return this.toString(a).localeCompare(this.toString(b), compareLocale, compareOptions)
      }
    },
    sortSONum: function (a, b) {
      const aSONum = this.formatSONumber(a)
      const bSONum = this.formatSONumber(b)
      return aSONum.localeCompare(bSONum)
    },
    sortClient: function (a, b) {
      const aName = a.client[0].organization_name
      const bName = b.client[0].organization_name
      return aName.localeCompare(bName)
    },
    sortDate: function (a, b) {
      return new Date(a) - new Date(b)
    },
    toString: function (value) {
      if (value === null || typeof value === 'undefined') {
        return ''
      } else if (value instanceof Object) {
        return Object.keys(value)
          .sort()
          .map(key => toString(value[key]))
          .join(' ')
      } else {
        return String(value)
      }
    },
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
    },
    populateSale: function (id) {
      console.log('populateSale:', id)
      const index = this.orders.findIndex(order => order.so_id === id)
      if (this.orders[index].sale_order_detail.length > 0) {
        return
      }

      const fetchRequest = this.$root.getOrigin() + '/api/v1/orders/sales?populate=sale_order_detail&so_id=' + id
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
            this.orders[index].sale_order_detail = data.data[0].sale_order_detail
            // eslint-disable-next-line
            console.log(data.data[0].sale_order_detail)
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
    getSales: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/orders/sales?populate=client'
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
            this.orders = data.data
            // eslint-disable-next-line
            console.log(this.orders)
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
    }
  },
  created: function () {
    this.getSales()
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
