<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query_buff" type="text" class="form-control" placeholder="Search Purchase Orders..." aria-label="Search Purchase Orders" aria-describedby="button-addon2" v-on:keyup.enter="search()">
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
          <h2 class="card-title flex-grow-1">Purchases</h2>
          <b-button disabled :to="{ name: 'NewPurchaseOrder'}" v-b-tooltip.hover title="New Order" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
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
        <TipTap v-model="contents" :edit="true"></TipTap>
        <TipTap v-model="contents" :edit="true"></TipTap>
        <TipTap v-model="contents" :edit="true"></TipTap>
        <!-- <div v-html="contents"></div> -->
      </div>
    </div>
  </div>
</template>

<script>
import TipTap from '../../../components/TipTap.vue'

export default {
  name: 'PurchaseOrdersHome',
  components: {
    TipTap
  },
  data: function () {
    return {
      loaded: true,
      contents: '<h3>Text</h3><p><u>Here</u><s> is</s> <em>some</em> <strong>text</strong>!</p><ul><li><p>item 1</p></li><li><p>thing 2</p></li><li><p>object 3</p><ul><li><p>sub object</p></li></ul></li></ul><p style="text-align: center"><span style="font-family: monospace">Center TEXT</span></p><p style="text-align: center"><span style="font-family: monospace">asdf </span></p><p></p><table><thead><tr><th>Header 1</th><th>Header 2</th></tr></thead><tbody><tr><td>data 1</td><td>data 2</td></tr><tr><td>data 3</td><td>data 4</td></tr></tbody></table><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p>',
      search_query_buff: '',
      search_query: '',
      hide: true,
      isMd: false,
      orders: [
        {
          pk: 'PO21010001A',
          prefix: 'PO',
          year: '21',
          month: '01',
          sec_number: '0001',
          suffix: 'A',
          supplier_so_num: '12345',
          organization_primary_name: 'Supplier 1',
          organization_primary_initial: 'S1',
          order_date: '2021-01-01',
          eta_date: '2021-01-15',
          status: 'Open',
          actions: 'View'
        },
        {
          pk: 'PO21010002A',
          prefix: 'PO',
          year: '21',
          month: '01',
          sec_number: '0002',
          suffix: 'A',
          supplier_so_num: '12346',
          organization_primary_name: 'Supplier 2',
          organization_primary_initial: 'S2',
          order_date: '2021-01-02',
          eta_date: '2021-01-16',
          status: 'Open',
          actions: 'View'
        },
        {
          pk: 'PO21010003A',
          prefix: 'PO',
          year: '21',
          month: '01',
          sec_number: '0003',
          suffix: 'A',
          supplier_so_num: '12347',
          organization_primary_name: 'Supplier 3',
          organization_primary_initial: 'S3',
          order_date: '2021-01-03',
          eta_date: '2021-01-17',
          status: 'Open',
          actions: 'View'
        }
      ],
      fields_hidden: [
        { key: 'pk', label: 'PO#', sortable: true },
        { key: 'supplier_so_num', label: 'Supplier SO', sortable: true },
        { key: 'organization_primary_name', label: 'Supplier', sortable: true },
        { key: 'organization_primary_initial', label: 'SI', sortable: true },
        { key: 'order_date', label: 'Date Ordered', sortable: true },
        { key: 'eta_date', label: 'ETA', sortable: true },
        { key: 'status', label: 'Status', sortable: true },
        { key: 'actions', label: 'Actions' }
      ],
      fields_show: [
        { key: 'prefix', label: 'Pre', sortable: true },
        { key: 'year', label: 'Y', sortable: true },
        { key: 'month', label: 'M', sortable: true },
        { key: 'sec_number', label: 'Sec #', sortable: true },
        { key: 'suffix', label: 'Suf', sortable: true },
        { key: 'supplier_so_num', label: 'Supplier SO', sortable: true },
        { key: 'organization_primary_name', label: 'Supplier', sortable: true },
        { key: 'organization_primary_initial', label: 'SI', sortable: true },
        { key: 'order_date', label: 'Date Ordered', sortable: true },
        { key: 'eta_date', label: 'ETA', sortable: true },
        { key: 'status', label: 'Status', sortable: true },
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
