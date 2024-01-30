<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'ProductsGrid',
  components: {
    Grid
  },
  props: {
    Products: Array
  },
  data () {
    return {
      cols: ['Product Name', 'Type'],
      product_data: this.Products,
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    if (this.product_data !== undefined) {
      this.product_data.forEach(product => {
        const row = [
          product.product_name,
          product.type
        ]
        this.rows.push(row)
      })
    }
  }
}
</script>
