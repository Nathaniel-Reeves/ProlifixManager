<template>
  <div>
    <b-table striped hover :items="orderDetails" :fields="fieldsComputed" show-empty small no-border-collapse outlined sort-icon-left sort-null-last>
      <template #cell(actions)="row">
        <div class="d-flex flex-row flex-nowrap">
          <b-button @click="row.toggleDetails()" size="sm" class="btn-light" style="border-width: 2px; border-color:#999999" v-b-tooltip.hover title="Peek Order Details">
            <b-icon v-show="row.detailsShowing" icon="chevron-up"></b-icon>
            <b-icon v-show="!row.detailsShowing" icon="chevron-down"></b-icon>
          </b-button>
        </div>
      </template>
      <template #cell(product_name)="row">
        <div>
          <router-link class="text-info" v-show="!isMd" :to="'/catalogue/products/'+row.item.product_id" target="_blank">{{ row.item.product[0].product_name }} V{{ row.item.formula[0].formulation_version }} {{ row.item.variant[0].variant_title }}</router-link>
        </div>
      </template>
      <template #cell(certs)="row">
        <CertBadge :data="row.item.product[0]" size="3em"></CertBadge>
      </template>
      <template #cell(unit_order_qty)="row">
        <div>{{ row.item.unit_order_qty.toLocaleString() }} units</div>
      </template>
      <template #cell(bid_price_per_unit)="row">
        <div>{{ row.item.bid_price_per_unit.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) }}</div>
      </template>
      <template #cell(lot_num_assigned)="row">
        <h4 class="d-flex justify-content-center"><b-badge v-if="!row.value" variant="warning" class="p-2" v-b-tooltip.hover title="Batch & Lot Number Assignment Incomplete">
          <b-icon icon="exclamation-triangle-fill"></b-icon>
        </b-badge></h4>
      </template>
      <template #cell(bulk)="row">
        <div v-if="row.item.variant[0].variant_type === 'powder'">
          {{ (Math.ceil((row.item.variant[0].total_grams_per_unit * row.item.unit_order_qty) / 1000) + (Math.ceil((row.item.variant[0].total_grams_per_unit * row.item.unit_order_qty) / 1000) * (row.item.percent_overage / 100))).toLocaleString() }} kg
        </div>
        <div v-else-if="row.item.variant[0].variant_type === 'capsule'">
          {{ (Math.ceil((row.item.variant[0].total_mg_per_capsule * row.item.variant[0].total_capsules_per_unit * row.item.unit_order_qty) / 1000000) + (Math.ceil((row.item.variant[0].total_mg_per_capsule * row.item.variant[0].total_capsules_per_unit * row.item.unit_order_qty) / 1000000) * (row.item.percent_overage / 100))).toLocaleString() }} kg
        </div>
        <div v-else-if="row.item.variant[0].variant_type === 'liquid'">
          {{ (Math.ceil((row.item.variant[0].total_milliliters_per_unit * row.item.unit_order_qty) / 1000) + (Math.ceil((row.item.variant[0].total_milliliters_per_unit * row.item.unit_order_qty) / 1000) * (row.item.percent_overage / 100))).toLocaleString() }} L
        </div>
      </template>
      <template #row-details="row">
        <div v-show="row.item.lot_and_batch_numbers.length === 0">
          <div class="d-flex justify-content-center">
            <b>Lot and Batch Assignment is Incomplete!</b>
          </div>
        </div>
        <div v-show="row.item.lot_and_batch_numbers.length !== 0">
          <LotAndBatchNumberTable :lot-and-batch-numbers="row.item.lot_and_batch_numbers" />
        </div>
      </template>
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
import LotAndBatchNumberTable from '@/components/LotAndBatchNumberTable.vue'

export default {
  name: 'OrderDetailsTable',
  components: {
    CertBadge,
    LotAndBatchNumberTable
  },
  props: {
    orderDetails: {
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
        { key: 'lot_num_assigned', label: '' },
        { key: 'product_name', label: 'Product' },
        { key: 'certs', label: 'Certs' },
        { key: 'unit_order_qty', label: 'Qty' },
        { key: 'bid_price_per_unit', label: '$ per Unit' },
        { key: 'special_instructions', label: 'Special Instructions' },
        { key: 'bulk', label: 'Bulk Qty' },
        { key: 'actions', label: 'Actions' }
      ]
    }
  },
  computed: {
    fieldsComputed: function () {
      return this.fields.filter(field => !this.excludeCol.includes(field.key))
    }
  }
}
</script>
