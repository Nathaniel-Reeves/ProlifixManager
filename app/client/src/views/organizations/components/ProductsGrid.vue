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
    products: Object
  },
  data () {
    return {
      cols: ['Product Name', 'Type'],
      product_data: Object.values(this.products),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.product_data.forEach(product => {
      const row = [
        product.product_name,
        product.type
      ]
      this.rows.push(row)
    })
  }
}
</script>
