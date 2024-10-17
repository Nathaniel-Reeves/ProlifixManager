<template>
  <div class="my_component">
    <div>
      <b-sidebar id="sidebar-right" title="Filter Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
        <div class="px-3 py-2">
          <div class="input-group mb-3">
            <input v-model="search_query_buff" type="text" class="form-control" placeholder="Search Lot Numbers..." aria-label="Search Lot Numbers" aria-describedby="button-addon2" v-on:keyup.enter="search()">
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
          <h2 class="card-title flex-grow-1">Lot Numbers</h2>
          <b-button :to="{ name: 'NewSalesOrder'}" v-b-tooltip.hover title="New Order" style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light" type="button">
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
          <LotAndBatchNumberTable :lot-and-batch-numbers="lot_and_batch_numbers" :exclude-col="['actions']"/>
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
import LotAndBatchNumberTable from '@/components/LotAndBatchNumberTable.vue'

export default {
  name: 'LotNumbersHome',
  components: {
    LotAndBatchNumberTable
  },
  data: function () {
    return {
      loaded: false,
      search_query_buff: '',
      search_query: '',
      hide: true,
      isMd: false,
      lot_and_batch_numbers: [],
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
  },
  created: function () {
    this.loaded = true
  }
}
</script>

<style scoped>
.custom_card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
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
