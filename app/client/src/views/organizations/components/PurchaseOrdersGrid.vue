<template>
  <Grid :cols="cols" :rows="rows" :pagination="{ 'limit': 5 }" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'PurchaseOrdersGrid',
  components: {
    Grid
  },
  props: {
    purchase_orders: Object
  },
  data () {
    return {
      cols: ['Purchase Order', 'Client SO'],
      purchase_orders_data: Object.values(this.purchase_orders),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.purchase_orders_data.forEach(purchaseOrder => {
      const row = [
        purchaseOrder.prefix + purchaseOrder.year + purchaseOrder.month + purchaseOrder.sec_number,
        purchaseOrder.client_so_num
      ]
      this.rows.push(row)
    })
  }
}
</script>
