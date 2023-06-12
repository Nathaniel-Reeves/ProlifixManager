<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'SalesOrdersGrid',
  components: {
    Grid
  },
  props: {
    sales_orders: Object
  },
  data () {
    return {
      cols: ['Sales Order', 'Client PO'],
      sales_orders_data: Object.values(this.sales_orders),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.sales_orders_data.forEach(salesOrder => {
      const row = [
        salesOrder.prefix + salesOrder.year + salesOrder.month + salesOrder.sec_number,
        salesOrder.client_po_num
      ]
      this.rows.push(row)
    })
  }
}
</script>
