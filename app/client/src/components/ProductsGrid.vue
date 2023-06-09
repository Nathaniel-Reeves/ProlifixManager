<template>
    <Grid :cols="cols" :rows="rows"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'ProductsGrid',
  components: {
    Grid
  },
  props: {
    products: Object
  },
  data () {
    return {
      cols: ['Product Name', 'Type', 'Date Entered'],
      product_data: Object.values(this.products),
      rows: []
    }
  },
  created: function () {
    this.product_data.forEach(product => {
      var row = [
        product.product_name,
        product.type,
        product.date_entered
      ]
      this.rows.push(row)
    })
  }
}
</script>
