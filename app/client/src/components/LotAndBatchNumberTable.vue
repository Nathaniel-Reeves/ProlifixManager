<template>
  <div>
    <b-table :striped="false" :hover="false" :items="lotAndBatchNumbers" :fields="fieldsComputed" show-empty small no-border-collapse outlined sort-icon-left sort-null-last>
      <!-- <template #cell(actions)="row">
        <div class="d-flex flex-row flex-nowrap">
          <b-button @click="row.toggleDetails();populateSale(row.item.so_id)" size="sm" class="btn-light" style="border-width: 2px; border-color:#999999" v-b-tooltip.hover title="Peek Order Details">
            <b-icon v-show="row.detailsShowing" icon="chevron-up"></b-icon>
            <b-icon v-show="!row.detailsShowing" icon="chevron-down"></b-icon>
          </b-button>
        </div>
      </template> -->
      <template #cell(lot)="row">
        <div>{{ formatLotNumber(row.item) }}</div>
      </template>
      <template #cell(product_name)="row">
        <router-link class="text-info" v-show="!isMd" :to="'/catalogue/products/'+row.item.product.product_id" target="_blank">{{ formatProductName(row.item) }}</router-link>
      </template>
      <template #cell(certs)="row">
        <CertBadge :data="row.item.product" size="3em"></CertBadge>
      </template>
      <template #cell(target_unit_yield)="row">
        <div>{{ row.item.target_unit_yield.toLocaleString() }} units</div>
      </template>
      <!-- <template #cell(bulk)="row">
        <div v-if="row.item.variant[0].variant_type === 'powder'">
          {{ (Math.ceil((row.item.variant[0].total_grams_per_unit * row.item.unit_order_qty) / 1000) + (Math.ceil((row.item.variant[0].total_grams_per_unit * row.item.unit_order_qty) / 1000) * (row.item.percent_overage / 100))).toLocaleString() }} kg
        </div>
        <div v-else-if="row.item.variant[0].variant_type === 'capsule'">
          {{ (Math.ceil((row.item.variant[0].total_mg_per_capsule * row.item.variant[0].total_capsules_per_unit * row.item.unit_order_qty) / 1000000) + (Math.ceil((row.item.variant[0].total_mg_per_capsule * row.item.variant[0].total_capsules_per_unit * row.item.unit_order_qty) / 1000000) * (row.item.percent_overage / 100))).toLocaleString() }} kg
        </div>
        <div v-else-if="row.item.variant[0].variant_type === 'liquid'">
          {{ (Math.ceil((row.item.variant[0].total_milliliters_per_unit * row.item.unit_order_qty) / 1000) + (Math.ceil((row.item.variant[0].total_milliliters_per_unit * row.item.unit_order_qty) / 1000) * (row.item.percent_overage / 100))).toLocaleString() }} L
        </div>
      </template> -->
    </b-table>
  </div>
</template>

<style scoped>
.table th, .table td {
  vertical-align: middle;
}
</style>

<script>
import CertBadge from '@/components/CertBadge.vue'

export default {
  name: 'LotAndBatchNumberTable',
  components: {
    CertBadge
  },
  props: {
    lotAndBatchNumbers: {
      type: Array,
      required: true
    },
    excludeCol: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  data: function () {
    return {
      isMd: false,
      fields: [
        { key: 'lot', label: 'Lot #' },
        { key: 'product_name', label: 'Product' },
        { key: 'certs', label: 'Certs' },
        { key: 'target_unit_yield', label: 'Target Yield' },
        { key: 'actions', label: 'Actions' }
      ]
    }
  },
  methods: {
    formatLotNumber: function (item) {
      return `${item.prefix} ${item.year.toString().padStart(2, '0')}${item.month.toString().padStart(2, '0')}${item.sec_number.toString().padStart(3, '0')} ${item.suffix}`
    },
    formatProductName: function (item) {
      return `${item.product.product_name} V${item.formula.formulation_version} ${item.variant.variant_title}`
    }
  },
  computed: {
    fieldsComputed: function () {
      return this.fields.filter(field => !this.excludeCol.includes(field.key))
    }
  }
}
</script>
