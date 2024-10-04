<template>
  <div>
    <b-table striped hover :items="orderDetails" :fields="fields" show-empty small no-border-collapse outlined sort-icon-left sort-null-last>
      <template #cell(product_name)="row">
        {{ row.item.product[0].product_name }}
      </template>
      <template #cell(certs)="row">
        <CertBadge :data="row.item.product[0]"></CertBadge>
      </template>
    </b-table>
  </div>
</template>

<script>
import CertBadge from '@/components/CertBadge.vue'

export default {
  name: 'OrderDetailsTable',
  components: {
    CertBadge
  },
  props: {
    orderDetails: {
      type: Array,
      required: true
    }
  },
  data: function () {
    return {
      fields: [
        { key: 'product_name', label: 'Product', sortable: true },
        { key: 'certs', label: 'Certs' }
      ]
    }
  }
}
</script>
