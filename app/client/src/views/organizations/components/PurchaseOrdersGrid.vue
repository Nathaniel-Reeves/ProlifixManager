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
    Purchase_Orders: Array
  },
  data () {
    return {
      cols: ['Purchase Order', 'Client SO'],
      purchase_order_data: this.Purchase_Orders,
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    if (this.purchase_order_data !== undefined) {
      this.purchase_order_data.forEach(purchaseOrder => {
        const row = [
          purchaseOrder.prefix + purchaseOrder.year + purchaseOrder.month + purchaseOrder.sec_number,
          purchaseOrder.client_so_num
        ]
        this.rows.push(row)
      })
    }
  }
}
</script>
